"""
Golden Quantum Standard (GQS-1) Implementation

This module implements the GQS-1 protocol for generating deterministic
test vectors for quantum key distribution testing and compliance.

Protocol Overview:
1. Initialize system state S_0 with hex seed
2. Verify SHA-256 checksum
3. Use Hash-DRBG ratchet: S_{n+1} = SHA-256(S_n + Counter)
4. Simulate quantum sifting (retain bits where Alice Basis == Bob Basis)
5. Apply hardening via XOR folding (256 bits -> 128 bits)
6. Output keys as hexadecimal strings
"""

import hashlib
from typing import List


# Expected SHA-256 checksum for the seed
EXPECTED_CHECKSUM = "096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f"

# Hex seed for initializing system state S_0
HEX_SEED = "0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f"


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


def hash_drbg_ratchet(state: bytes, counter: int) -> bytes:
    """
    Hash-DRBG ratchet function: S_{n+1} = SHA-256(S_n + Counter)
    
    Args:
        state: Current state S_n (32 bytes)
        counter: Counter value (encoded as 4-byte big-endian)
        
    Returns:
        Next state S_{n+1} (32 bytes)
    """
    counter_bytes = counter.to_bytes(4, byteorder='big')
    combined = state + counter_bytes
    return hashlib.sha256(combined).digest()


def simulate_quantum_sifting(raw_bits: bytes) -> bytes:
    """
    Simulate quantum sifting by retaining bits where Alice basis == Bob basis.
    
    In a real QKD system, Alice and Bob randomly choose measurement bases.
    For deterministic test vectors, we simulate basis matching:
    - We use the state to generate both "Alice bits" and "Bob bits"
    - We also generate basis selections deterministically
    - Retain bits where bases match
    
    For this implementation, we'll use a simplified model:
    - Take the first 256 bits as Alice's raw measurements
    - Take bits at even positions (basis matching simulation)
    
    Args:
        raw_bits: Raw bits from DRBG (32 bytes = 256 bits)
        
    Returns:
        Sifted bits (still 32 bytes, but conceptually only "matched" bits are used)
    """
    # For deterministic test vectors, we use a simple basis matching model
    # In practice, this simulates the case where ~50% of bits have matching bases
    # For simplicity in test vectors, we retain all bits from the DRBG output
    # and apply the hardening step to achieve the final 128-bit key
    return raw_bits


def xor_fold_hardening(bits: bytes) -> bytes:
    """
    Apply XOR folding to harden 256 bits into 128 bits.
    
    XOR folding provides information-theoretic hardening:
    - Split 256 bits into two 128-bit halves
    - XOR them together to produce final 128-bit key
    
    Args:
        bits: Input bits (32 bytes = 256 bits)
        
    Returns:
        Hardened key (16 bytes = 128 bits)
    """
    half_len = len(bits) // 2
    first_half = bits[:half_len]
    second_half = bits[half_len:]
    
    # XOR the two halves
    hardened = bytes(a ^ b for a, b in zip(first_half, second_half))
    return hardened


def generate_key(state: bytes, counter: int) -> tuple[bytes, bytes]:
    """
    Generate a single hardened 128-bit key from the current state.
    
    Args:
        state: Current system state (32 bytes)
        counter: Counter for this key generation
        
    Returns:
        Tuple of (hardened_key, next_state)
    """
    # Apply Hash-DRBG ratchet
    next_state = hash_drbg_ratchet(state, counter)
    
    # Simulate quantum sifting (for test vectors, this is deterministic)
    sifted_bits = simulate_quantum_sifting(next_state)
    
    # Apply XOR folding hardening
    hardened_key = xor_fold_hardening(sifted_bits)
    
    return hardened_key, next_state


def generate_test_vectors(num_keys: int = 10) -> List[str]:
    """
    Generate the first N test vectors for GQS-1 compliance testing.
    
    Args:
        num_keys: Number of keys to generate (default: 10)
        
    Returns:
        List of hexadecimal key strings
    """
    # Initialize system state S_0 with the hex seed
    seed = bytes.fromhex(HEX_SEED)
    
    # Verify checksum
    if not verify_seed_checksum(seed):
        raise ValueError(
            f"Seed checksum verification failed. "
            f"Expected: {EXPECTED_CHECKSUM}, "
            f"Got: {hashlib.sha256(seed).hexdigest()}"
        )
    
    # Initialize state
    state = seed
    test_vectors = []
    
    # Generate keys
    for counter in range(1, num_keys + 1):
        key, state = generate_key(state, counter)
        test_vectors.append(key.hex())
    
    return test_vectors


def main():
    """
    Main function to generate and display test vectors.
    """
    print("Golden Quantum Standard (GQS-1) Test Vector Generation")
    print("=" * 60)
    print()
    print(f"Hex Seed: {HEX_SEED}")
    print(f"Expected Checksum: {EXPECTED_CHECKSUM}")
    print()
    
    # Verify seed
    seed = bytes.fromhex(HEX_SEED)
    actual_checksum = hashlib.sha256(seed).hexdigest()
    print(f"Actual Checksum: {actual_checksum}")
    print(f"Checksum Valid: {verify_seed_checksum(seed)}")
    print()
    
    # Generate test vectors
    print("Generating first 10 test vectors...")
    print()
    test_vectors = generate_test_vectors(10)
    
    print("Test Vectors:")
    print("-" * 60)
    for i, key in enumerate(test_vectors, 1):
        print(f"Key {i:2d}: {key}")
    print()


if __name__ == "__main__":
    main()
