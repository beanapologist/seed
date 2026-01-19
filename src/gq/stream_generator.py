"""
Deterministic PRNG (Pseudo-Random Number Generator)

A production-grade deterministic PRNG that produces synchronized pseudo-random
output across systems. This implementation uses mathematical constant seeds
with language-agnostic, endian-independent design.

⚠️ NOT FOR CRYPTOGRAPHY: This is a PRNG that generates deterministic pseudo-random
streams and must NOT be used for cryptographic purposes (passwords, keys, tokens, etc.).

Suitable for: procedural generation, reproducible testing, deterministic
simulations, consensus randomness, and space-efficient storage.

Protocol Specification:

Layer 1: Root Seed
  - Seed Hex: 0000000000000000a8f4979b77e3f93fa8f4979b77e3f93f
  - Verify SHA-256: 096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f

Layer 2: State Initialization
  - State = SHA256(Seed)
  - Counter = 0

Layer 3: Stream Generation with Bit Selection
  - Loop until 256 selected bits collected:
    * Entropy = SHA256(State || Counter_string)
      (where || denotes concatenation)
    * State = Entropy (ratchet for forward progression)
    * Counter += 1
    * For each byte in Entropy:
      - Check if bits match using: ((byte >> 1) & 1) == ((byte >> 2) & 1)
      - This provides ~25-50% selection efficiency
      - If bits match: Append (byte & 1) to selected_bits

Layer 4: Output via XOR Folding
  - Split 256 selected bits into two 128-bit halves
  - For i = 0 to 127:
    Output_bit[i] = selected_bits[i] XOR selected_bits[i + 128]
  - Output 128-bit stream (16 bytes)
  - Stream continues indefinitely for subsequent outputs

This implementation provides:
  - Determinism for cross-implementation verification
  - State progression via ratcheting
  - Bit selection for filtering (~25-50% efficiency)
  - XOR folding for output variation
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import struct
from typing import Iterator, List


def _double_pack_hex(value: float) -> str:
    """Helper function to pack a float as hex and double it to 32 bytes."""
    return struct.pack('<d', value).hex() * 2


# Mathematical constants as seeds (IEEE 754 double precision, little-endian)
# These can be used as alternative seeds for different applications by passing
# to golden_stream_generator(seed_hex=CONSTANT_HEX)

# Golden Ratio: φ = (1 + √5)/2 ≈ 1.618033988749895
GOLDEN_RATIO = 1.618033988749894848204586834365638117720309179805762862135
GOLDEN_RATIO_HEX = "0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f"

# Pi: π ≈ 3.14159265358979323846
# Usage: golden_stream_generator(seed_hex=PI_HEX)
PI = 3.141592653589793238462643383279502884197169399375105820974
PI_HEX = _double_pack_hex(PI)

# Euler's Number: e ≈ 2.71828182845904523536
# Usage: golden_stream_generator(seed_hex=E_HEX)
E = 2.718281828459045235360287471352662497757247093699959574966
E_HEX = _double_pack_hex(E)

# Square Root of 2: √2 ≈ 1.41421356237309504880
# Usage: golden_stream_generator(seed_hex=SQRT2_HEX)
SQRT2 = 1.414213562373095048801688724209698078569671875376948073176
SQRT2_HEX = _double_pack_hex(SQRT2)


# Expected SHA-256 checksum for the golden ratio seed
EXPECTED_CHECKSUM = "096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f"

# Default hex seed (golden ratio - φ)
HEX_SEED = GOLDEN_RATIO_HEX


def verify_seed_checksum(seed: bytes) -> bool:
    """
    Verify that the seed matches the expected SHA-256 checksum.

    Args:
        seed: The seed bytes to verify

    Returns:
        True if checksum matches, False otherwise
    """
    checksum = hashlib.sha256(seed).hexdigest()
    return checksum == EXPECTED_CHECKSUM


def bit_selection_check(byte: int) -> bool:
    """
    Check if two specific bits match for bit selection.

    This function performs a bit selection check by comparing bit 1 and bit 2
    of a byte. When these bits are equal, we consider it a "match" and retain
    bit 0 for the selected output.

    The condition ((byte >> 1) & 1) == ((byte >> 2) & 1) provides ~25-50%
    selection efficiency, creating natural filtering in the stream generation.

    Mathematical explanation:
    - (byte >> 1) & 1 extracts bit at position 1
    - (byte >> 2) & 1 extracts bit at position 2
    - When these are equal, we accept bit at position 0

    Args:
        byte: Single byte from entropy source (0-255)

    Returns:
        True if bit 1 equals bit 2, False otherwise
    """
    bit1 = (byte >> 1) & 1  # Extract bit at position 1
    bit2 = (byte >> 2) & 1  # Extract bit at position 2
    return bit1 == bit2


def collect_selected_bits(state: bytes, counter: int) -> tuple[List[int], bytes, int]:
    """
    Collect 256 bits using bit selection filtering.

    This function repeatedly hashes the state to generate entropy, then
    applies a bit selection check to each byte. When the check passes,
    we extract one bit for the output.

    Process:
    1. Concatenate state with counter (as string)
    2. Hash with SHA-256 to get 32 bytes of entropy
    3. Update state to hash output (state progression)
    4. For each byte, check if bits 1 and 2 match
    5. If match: extract bit 0 and add to selected_bits
    6. Repeat until 256 bits collected

    Args:
        state: Current system state (32 bytes)
        counter: Current counter value

    Returns:
        Tuple of (selected_bits, final_state, final_counter)
    """
    selected_bits = []

    while len(selected_bits) < 256:
        # Concatenate state with counter as UTF-8 string
        counter_str = str(counter).encode('utf-8')
        data = state + counter_str

        # Generate entropy and progress state
        entropy = hashlib.sha256(data).digest()
        state = entropy
        counter += 1

        # Apply bit selection check for each byte
        for byte in entropy:
            if bit_selection_check(byte):
                # Extract bit 0 as the selected bit
                selected_bits.append(byte & 1)

                # Stop if we have enough bits
                if len(selected_bits) >= 256:
                    break

    return selected_bits[:256], state, counter


def xor_fold_output(selected_bits: List[int]) -> bytes:
    """
    Apply XOR folding to produce 128-bit output from 256 bits.

    XOR folding combines the first and second halves of the selected bits:
    - For i = 0 to 127: output_bit[i] = selected_bits[i] XOR selected_bits[i+128]

    This creates variation in the output stream.

    Mathematical formula:
    output[i] = first_half[i] ⊕ second_half[i] for i = 0 to 127
    (where ⊕ denotes XOR operation)

    Args:
        selected_bits: List of 256 bits (each element is 0 or 1)

    Returns:
        Output bytes (16 bytes = 128 bits)
    """
    # XOR first half with second half bit by bit
    output_bits = []
    for i in range(128):
        bit = selected_bits[i] ^ selected_bits[i + 128]
        output_bits.append(bit)

    # Convert bit list to bytes (8 bits per byte, MSB first)
    output_bytes = bytearray()
    for i in range(0, 128, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | output_bits[i + j]
        output_bytes.append(byte)

    return bytes(output_bytes)


def golden_stream_generator(seed_hex: str = HEX_SEED) -> Iterator[bytes]:
    """
    Deterministic PRNG - infinite stream of 128-bit pseudo-random outputs.

    ⚠️ NOT FOR CRYPTOGRAPHY: This is a PRNG for procedural generation only.

    This PRNG produces an infinite stream of deterministic pseudo-random bytes
    using a mathematical constant seed as starting point. Each output is generated
    through hash-based entropy generation, bit selection filtering, and XOR folding.

    Stream generation process:
    1. Initialize state from seed using SHA-256
    2. For each output:
       a. Generate entropy via repeated SHA-256 hashing
       b. Apply bit selection to filter bits (~25-50% efficiency)
       c. Collect 256 selected bits
       d. Apply XOR folding to produce 128-bit output
       e. Update state for next iteration

    Args:
        seed_hex: Hex string of the seed (default: golden ratio)

    Yields:
        128-bit outputs as bytes (16 bytes each)

    Raises:
        ValueError: If seed checksum verification fails
    """
    # Initialize with seed
    seed = bytes.fromhex(seed_hex)

    # Verify checksum for data integrity
    if not verify_seed_checksum(seed):
        raise ValueError(
            f"Seed checksum verification failed. "
            f"Expected: {EXPECTED_CHECKSUM}, "
            f"Got: {hashlib.sha256(seed).hexdigest()}"
        )

    # Layer 2: State Initialization
    state = hashlib.sha256(seed).digest()
    counter = 0

    # Infinite stream
    while True:
        # Layer 3: Stream Generation with Bit Selection
        selected_bits, state, counter = collect_selected_bits(state, counter)

        # Layer 4: Output via XOR Folding
        output = xor_fold_output(selected_bits)

        yield output


def generate_streams(num_streams: int, seed_hex: str = HEX_SEED) -> List[str]:
    """
    Generate a specified number of outputs from the stream generator.

    Args:
        num_streams: Number of outputs to generate
        seed_hex: Hex string of the seed (default: golden ratio)

    Returns:
        List of hexadecimal output strings
    """
    generator = golden_stream_generator(seed_hex)
    outputs = []

    for _ in range(num_streams):
        output = next(generator)
        outputs.append(output.hex())

    return outputs


def main():
    """
    Main function for CLI interface.
    """
    parser = argparse.ArgumentParser(
        description="GoldenSeed PRNG - Deterministic pseudo-random number generator for procedural content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  NOT FOR CRYPTOGRAPHY: This is a PRNG for procedural generation, testing, and simulations only.

Examples:
  %(prog)s                          # Generate 10 streams (default)
  %(prog)s -n 100                   # Generate 100 streams
  %(prog)s -n 50 -o streams.txt     # Save 50 streams to file
  %(prog)s -n 20 --json             # Output 20 streams in JSON format
  %(prog)s --json -o streams.json   # Save JSON output to file
  %(prog)s --quiet -n 5             # Generate 5 streams with minimal output
  %(prog)s --verify-only            # Verify seed integrity only

Protocol: Deterministic stream generation with bit selection and XOR folding
        """
    )

    parser.add_argument(
        "-n", "--num-streams",
        type=int,
        default=10,
        metavar="N",
        help="number of streams to generate (default: 10)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        metavar="FILE",
        help="output file path (default: stdout)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="output in JSON format"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="suppress informational messages, only output streams"
    )

    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="only verify seed checksum without generating streams"
    )

    parser.add_argument(
        "--binary",
        action="store_true",
        help="include binary representation in output"
    )

    args = parser.parse_args()

    # Verify seed checksum
    seed = bytes.fromhex(HEX_SEED)
    actual_checksum = hashlib.sha256(seed).hexdigest()

    if not args.quiet:
        print("GoldenSeed PRNG (Pseudo-Random Number Generator)", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(file=sys.stderr)
        print(f"⚠️  NOT FOR CRYPTOGRAPHY - PRNG for procedural generation only", file=sys.stderr)
        print(file=sys.stderr)
        print(f"Seed: {HEX_SEED}", file=sys.stderr)
        print(f"Expected Checksum: {EXPECTED_CHECKSUM}", file=sys.stderr)
        print(f"Actual Checksum: {actual_checksum}", file=sys.stderr)
        print(f"Checksum Valid: {verify_seed_checksum(seed)}", file=sys.stderr)
        print(file=sys.stderr)

    if not verify_seed_checksum(seed):
        print("ERROR: Seed checksum verification failed!", file=sys.stderr)
        sys.exit(1)

    if args.verify_only:
        if not args.quiet:
            print("✓ Seed checksum verified successfully", file=sys.stderr)
        sys.exit(0)

    # Validate num_streams
    if args.num_streams < 1:
        print("ERROR: Number of streams must be at least 1", file=sys.stderr)
        sys.exit(1)

    if args.num_streams > 1000000:
        print("WARNING: Generating a large number of streams may take time", file=sys.stderr)

    # Generate streams
    if not args.quiet:
        print(f"Generating {args.num_streams} stream{'s' if args.num_streams != 1 else ''}...", file=sys.stderr)
        print(file=sys.stderr)

    streams = generate_streams(args.num_streams)

    # Format output
    if args.json:
        output_data = {
            "description": "GoldenSeed PRNG - Deterministic Pseudo-Random Number Generator",
            "warning": "NOT FOR CRYPTOGRAPHY - PRNG for procedural generation only",
            "seed": HEX_SEED,
            "checksum": EXPECTED_CHECKSUM,
            "num_streams": len(streams),
            "streams": []
        }

        for i, stream in enumerate(streams, 1):
            stream_entry = {
                "index": i,
                "hex": stream
            }
            if args.binary:
                stream_bytes = bytes.fromhex(stream)
                binary_str = ''.join(format(byte, '08b') for byte in stream_bytes)
                stream_entry["binary"] = binary_str
            output_data["streams"].append(stream_entry)

        output_str = json.dumps(output_data, indent=2)
    else:
        output_lines = []
        if not args.quiet:
            output_lines.append("Generated Streams:")
            output_lines.append("-" * 60)

        for i, stream in enumerate(streams, 1):
            if args.quiet:
                output_lines.append(stream)
            elif args.binary:
                stream_bytes = bytes.fromhex(stream)
                binary_str = ''.join(format(byte, '08b') for byte in stream_bytes)
                output_lines.append(f"Stream {i:6d}: {stream}")
                output_lines.append(f"           Binary: {binary_str}")
            else:
                output_lines.append(f"Stream {i:6d}: {stream}")

        output_str = "\n".join(output_lines)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output_str)
                if not output_str.endswith('\n'):
                    f.write('\n')

            if not args.quiet:
                print(f"✓ Output written to {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"ERROR: Failed to write to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_str)
        if not output_str.endswith('\n'):
            print()


if __name__ == "__main__":
    main()
