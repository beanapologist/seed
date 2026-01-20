#!/usr/bin/env python3
"""
Generate Binary Random Data for NIST STS Testing

This script generates binary random data from the deterministic stream generators
in this repository for use with the NIST Statistical Test Suite (STS).

⚠️ NOT FOR CRYPTOGRAPHY: This generates deterministic pseudo-random streams
for testing purposes only.

The binary file format is optimized for NIST STS processing.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import gq module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from gq import generate_universal_keys, generate_gqs1_vectors
except ImportError:
    print("ERROR: Unable to import gq module. Please install the package first:")
    print("  pip install -e .")
    sys.exit(1)


def generate_binary_sequence(num_sequences: int, sequence_type: str = "universal") -> bytes:
    """
    Generate binary sequence from deterministic stream generator.
    
    Args:
        num_sequences: Number of stream sequences to generate
        sequence_type: Type of generator ("universal", "gqs1")
    
    Returns:
        Binary data suitable for NIST STS testing
    """
    binary_data = bytearray()
    
    if sequence_type == "universal":
        # Generate Universal deterministic streams
        keys = generate_universal_keys(num_sequences)
        for key_hex in keys:
            binary_data.extend(bytes.fromhex(key_hex))
            
    elif sequence_type == "gqs1":
        # Generate GQS-1 test vectors
        vectors = generate_gqs1_vectors(num_sequences)
        for vector_hex in vectors:
            binary_data.extend(bytes.fromhex(vector_hex))
    else:
        raise ValueError(f"Unknown sequence type: {sequence_type}")
    
    return bytes(binary_data)


def convert_to_ascii_binary(data: bytes) -> str:
    """
    Convert binary data to ASCII '0' and '1' characters for NIST STS.
    
    NIST STS expects input as ASCII text file with '0' and '1' characters.
    
    Args:
        data: Binary data to convert
    
    Returns:
        String of '0' and '1' characters
    """
    binary_string = ''.join(format(byte, '08b') for byte in data)
    return binary_string


def main():
    parser = argparse.ArgumentParser(
        description="Generate binary random data for NIST STS testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1 million bits from Universal stream generator (default)
  python scripts/generate_nist_binary.py -n 1000000 -o data/random.txt
  
  # Generate 10 million bits from GQS-1
  python scripts/generate_nist_binary.py -n 10000000 -t gqs1 -o data/gqs1_random.txt
  
Sequence Types:
  universal   - Universal deterministic stream generator [16 bytes per stream]
  gqs1       - GQS-1 test vectors [16 bytes per vector]
        """
    )
    
    parser.add_argument(
        '-n', '--num-bits',
        type=int,
        default=1000000,
        help='Number of bits to generate (default: 1000000 = 1M bits)'
    )
    
    parser.add_argument(
        '-t', '--type',
        choices=['universal', 'gqs1'],
        default='universal',
        help='Type of generator to use (default: universal)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='data/random.txt',
        help='Output file path (default: data/random.txt)'
    )
    
    parser.add_argument(
        '--binary-format',
        action='store_true',
        help='Output as binary file instead of ASCII 0/1 text (not recommended for NIST STS)'
    )
    
    args = parser.parse_args()
    
    # Calculate number of sequences needed
    bytes_per_sequence = {
        'universal': 16,
        'gqs1': 16
    }
    
    bits_per_sequence = bytes_per_sequence[args.type] * 8
    num_sequences = (args.num_bits + bits_per_sequence - 1) // bits_per_sequence
    
    print(f"Generating {args.num_bits:,} bits using {args.type} generator...")
    print(f"  Sequences needed: {num_sequences}")
    print(f"  Bits per sequence: {bits_per_sequence}")
    
    # Generate binary data
    binary_data = generate_binary_sequence(num_sequences, args.type)
    
    # Trim to exact number of bits requested
    total_bits = len(binary_data) * 8
    if total_bits > args.num_bits:
        # Convert to bits, trim, and convert back
        bit_string = convert_to_ascii_binary(binary_data)
        bit_string = bit_string[:args.num_bits]
        print(f"  Trimmed from {total_bits:,} to {len(bit_string):,} bits")
    else:
        bit_string = convert_to_ascii_binary(binary_data)
    
    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    if args.binary_format:
        # Write as binary file
        with open(output_path, 'wb') as f:
            # Convert bit string back to bytes
            byte_data = bytearray()
            for i in range(0, len(bit_string), 8):
                byte_chunk = bit_string[i:i+8]
                if len(byte_chunk) == 8:
                    byte_data.append(int(byte_chunk, 2))
            f.write(bytes(byte_data))
        print(f"\n✓ Binary file written: {output_path}")
    else:
        # Write as ASCII text file with '0' and '1' characters
        with open(output_path, 'w') as f:
            f.write(bit_string)
        print(f"\n✓ ASCII binary file written: {output_path}")
    
    print(f"  Total bits: {len(bit_string):,}")
    print(f"  File size: {output_path.stat().st_size:,} bytes")
    
    # Basic statistics
    ones = bit_string.count('1')
    zeros = bit_string.count('0')
    balance = abs(ones - zeros) / len(bit_string)
    
    print(f"\nBasic Statistics:")
    print(f"  Ones:  {ones:,} ({ones/len(bit_string)*100:.2f}%)")
    print(f"  Zeros: {zeros:,} ({zeros/len(bit_string)*100:.2f}%)")
    print(f"  Balance: {balance:.6f} (lower is better, should be < 0.05)")
    
    if balance > 0.05:
        print(f"\n⚠️  WARNING: Balance is high, may fail NIST monobit test")
    else:
        print(f"\n✓ Balance looks good for NIST testing")


if __name__ == '__main__':
    main()
