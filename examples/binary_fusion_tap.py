#!/usr/bin/env python3
"""
Binary Tap Operation - Python Implementation
Deterministic key generation using bit-shifting and XOR operations

This demonstrates basic binary manipulation operations:
- Bit-shifting (multiplication by powers of 2)
- Addition (introducing offset bits)
- XOR (extracting difference bits)
"""

def binary_fusion_tap(k: int) -> dict:
    """
    Generate binary tap operation with bit-shifting and XOR extraction.

    This performs a simple mathematical transformation:
    1. Create seed from digit sequence (1,2,3,...,k)
    2. Shift bits left by 3 positions (multiply by 8)
    3. Add offset parameter k
    4. Use XOR to extract the bits contributed by k

    Args:
        k: Offset parameter (recommended: 11 for this application)

    Returns:
        Dictionary with transformation data
    """
    # 1. Generate seed from concatenated digit sequence
    seed_val = int("".join(map(str, range(1, k + 1))))

    # 2. Apply bit-shift left by 3 (equivalent to multiplying by 8)
    shifted_val = seed_val << 3

    # 3. Add offset to shifted value
    result = shifted_val + k

    # 4. Extract difference bits using XOR
    # For k < 10, no extraction is needed
    # For k >= 10, XOR reveals the bits added by the offset
    if k < 10:
        diff_bits = 0
    else:
        diff_bits = result ^ (seed_val * 8)

    return {
        "k": k,
        "seed_value": seed_val,
        "binary_seed": bin(seed_val),
        "tap_state": bin(result),
        "zpe_overflow": bin(diff_bits),  # Kept for backward compatibility
        "zpe_overflow_decimal": diff_bits  # Kept for backward compatibility
    }


# Example usage
if __name__ == "__main__":
    result = binary_fusion_tap(11)
    print(f"Offset Parameter: {result['k']}")
    print(f"Seed Value: {result['seed_value']}")
    print(f"Result State: {result['tap_state']}")
    print(f"Difference Bits: {result['zpe_overflow']}")
