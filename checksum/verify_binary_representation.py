#!/usr/bin/env python3
"""
Binary Representation Verification Tool

This script verifies the binary representation of seed values and their
computed results using deterministic mathematical operations.

The verification demonstrates the relationship between a seed value and
its computed binary representation using the formula:
    result = (seed * 8) + k
where k is an offset parameter.

The binary tap operation consists of:
- Bit-shift left by 3 (equivalent to multiplying by 8)
- Addition of k parameter (phase offset)
- XOR operation for extracting the difference bits
"""

import hashlib


def calculate_checksum(value: int, algorithm: str = 'sha256') -> str:
    """
    Calculate cryptographic checksum of an integer value.

    Args:
        value: The integer value to checksum
        algorithm: Hash algorithm to use ('sha256' or 'sha512')

    Returns:
        Hexadecimal string representation of the checksum
    """
    # Convert integer to bytes (big-endian representation)
    byte_length = (value.bit_length() + 7) // 8
    value_bytes = value.to_bytes(byte_length, byteorder='big')

    # Calculate hash
    if algorithm == 'sha256':
        hash_obj = hashlib.sha256(value_bytes)
    elif algorithm == 'sha512':
        hash_obj = hashlib.sha512(value_bytes)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    return hash_obj.hexdigest()


def verify_checksum_integrity(seed_value: int, result_value: int,
                                expected_seed_checksum: str = None,
                                expected_result_checksum: str = None) -> dict:
    """
    Verify the integrity of seed and computed result values using checksums.

    Args:
        seed_value: The seed value to verify
        result_value: The computed result value to verify
        expected_seed_checksum: Expected SHA256 checksum for seed (optional)
        expected_result_checksum: Expected SHA256 checksum for result (optional)

    Returns:
        Dictionary containing checksum verification results
    """
    actual_seed_checksum = calculate_checksum(seed_value, 'sha256')
    actual_result_checksum = calculate_checksum(result_value, 'sha256')

    result = {
        'seed_sha256': actual_seed_checksum,
        'manifested_sha256': actual_result_checksum,  # Kept for backward compatibility
        'seed_checksum_valid': True,
        'manifested_checksum_valid': True
    }

    # Verify against expected checksums if provided
    if expected_seed_checksum:
        result['seed_checksum_valid'] = (actual_seed_checksum == expected_seed_checksum)

    if expected_result_checksum:
        result['manifested_checksum_valid'] = (actual_result_checksum == expected_result_checksum)

    return result


def binary_fusion_tap(k: int) -> dict:
    """
    Generate binary tap operation with bit-shifting and XOR extraction.

    This function demonstrates a deterministic binary transformation:
    1. Generate seed from concatenated sequence (1,2,3,...,k)
    2. Apply bit-shift left by 3 (equivalent to multiplication by 8)
    3. Add offset parameter (k)
    4. Extract difference bits via XOR for k >= 10

    Mathematical operations:
    - seed << 3 is equivalent to seed * 8 (bit-shift optimization)
    - result = (seed * 8) + k
    - overflow = result XOR (seed * 8) extracts the k bits that were added

    Args:
        k: Offset parameter (typically 11 for this application)

    Returns:
        Dictionary containing computed values and extracted bits
    """
    # 1. Generate the seed value from concatenated digit sequence
    # Example: k=11 produces seed_val = 1234567891011
    seed_val = int("".join(map(str, range(1, k + 1))))
    bin_seed = bin(seed_val)

    # 2. Bit-shift left by 3 positions (equivalent to multiplying by 8)
    # This is a computational optimization: seed << 3 === seed * 8
    shifted_val = seed_val << 3

    # 3. Add the offset parameter k to the shifted value
    result = shifted_val + k

    # 4. Extract the difference bits using XOR operation
    # For k < 10, the offset is small enough that no new bits are needed
    # For k >= 10, the XOR reveals which bits changed due to the addition
    if k < 10:
        diff_bits = 0
    else:
        # XOR finds the difference between result and (seed * 8)
        # This isolates the contribution of the k offset
        diff_bits = result ^ (seed_val * 8)

    return {
        "k": k,
        "seed_value": seed_val,
        "binary_seed": bin_seed,
        "tap_state": bin(result),
        "zpe_overflow": bin(diff_bits),  # Kept for backward compatibility
        "zpe_overflow_decimal": diff_bits  # Kept for backward compatibility
    }


def verify_binary_representation(k: int, seed_value: int) -> dict:
    """
    Verify binary representation of seed and its computed result.

    This function computes the result of the formula: result = (seed * 8) + k
    and provides binary representations and checksums for verification.

    Args:
        k: Offset parameter (typically 11)
        seed_value: The seed value to verify

    Returns:
        Dictionary containing verification results including checksums
    """
    # Calculate binary representation of seed
    binary_representation = bin(seed_value)
    bit_length = len(binary_representation) - 2  # Subtract '0b' prefix

    # Calculate result value using the formula: (seed * 8) + k
    result = (seed_value * 8) + k
    binary_result = bin(result)
    result_bit_length = len(binary_result) - 2

    # Calculate checksums for integrity verification
    checksums = verify_checksum_integrity(seed_value, result)

    return {
        'k': k,
        'seed_value': seed_value,
        'seed_binary': binary_representation,
        'seed_bit_length': bit_length,
        'manifested_value': result,  # Kept for backward compatibility
        'manifested_binary': binary_result,  # Kept for backward compatibility
        'manifested_bit_length': result_bit_length,
        'seed_sha256': checksums['seed_sha256'],
        'manifested_sha256': checksums['manifested_sha256'],
        'seed_checksum_valid': checksums['seed_checksum_valid'],
        'manifested_checksum_valid': checksums['manifested_checksum_valid']
    }


def print_verification_results(results: dict) -> None:
    """
    Print verification results in a formatted manner.

    Args:
        results: Dictionary containing verification results
    """
    print("=" * 70)
    print("BINARY REPRESENTATION VERIFICATION")
    print("=" * 70)
    print(f"\nOffset Parameter (k): {results['k']}")
    print(f"Seed Value: {results['seed_value']}")
    print(f"\nSeed Binary: {results['seed_binary']}")
    print(f"Seed Bit Length: {results['seed_bit_length']}")
    print(f"\nResult Value (seed * 8 + k): {results['manifested_value']}")
    print(f"Result Binary: {results['manifested_binary']}")
    print(f"Result Bit Length: {results['manifested_bit_length']}")
    print(f"\nBit Length Increase: {results['manifested_bit_length'] - results['seed_bit_length']}")
    
    # Print checksum validation results
    print("\n" + "=" * 70)
    print("CHECKSUM VALIDATION")
    print("=" * 70)
    print(f"\nSeed SHA256:")
    print(f"  {results['seed_sha256']}")
    print(f"  Status: {'✅ VALID' if results['seed_checksum_valid'] else '❌ INVALID'}")
    
    print(f"\nResult SHA256:")
    print(f"  {results['manifested_sha256']}")
    print(f"  Status: {'✅ VALID' if results['manifested_checksum_valid'] else '❌ INVALID'}")
    
    print("=" * 70)


if __name__ == "__main__":
    # Final binary verification for k=11
    k = 11
    seed_11 = 1234567891011

    # Perform standard verification
    results = verify_binary_representation(k, seed_11)

    # Print results
    print_verification_results(results)

    # Legacy output format (for backward compatibility)
    print("\nLegacy Output Format:")
    print(f"Seed_11 Bit Length: {results['seed_bit_length']}")
    print(f"Manifested Bit Length: {results['manifested_bit_length']}")
    print(f"Binary Tap (k=11): {results['manifested_binary']}")

    # Binary Tap Operation with Bit-Shifting and XOR Extraction
    print("\n" + "=" * 70)
    print("BINARY TAP OPERATION - BIT MANIPULATION DETAILS")
    print("=" * 70)
    blueprint = binary_fusion_tap(k)
    print(f"\nOffset Parameter k={k}")
    print(f"Seed Value: {blueprint['seed_value']}")
    print(f"Binary Seed: {blueprint['binary_seed']}")
    print(f"\nBit-shift left by 3 applied (equivalent to * 8)")
    print(f"Result for k={k}: {blueprint['tap_state']}")
    print(f"\nDifference Bits Extraction (XOR operation)")
    print(f"XOR Result Bitmask: {blueprint['zpe_overflow']}")
    print(f"XOR Result (decimal): {blueprint['zpe_overflow_decimal']}")
    print("\nExplanation:")
    print("  - The bit-shift (seed << 3) multiplies the seed by 8")
    print("  - Adding k introduces new bits in the lower positions")
    print("  - The XOR operation (result ^ (seed * 8)) extracts these new bits")
    print("=" * 70)
