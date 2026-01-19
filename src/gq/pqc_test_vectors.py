"""
NIST PQC-Compatible Test Vector Generation

⚠️ NOT FOR CRYPTOGRAPHIC USE ⚠️

This module generates deterministic test vectors that are COMPATIBLE with NIST
Post-Quantum Cryptography seed formats, but does NOT provide cryptographic security.

USE CASES (VALID):
- Testing PQC algorithm implementations with deterministic seeds
- Generating reproducible test vectors for PQC compliance testing
- Creating deterministic fixtures for PQC library unit tests

MISUSE (INVALID):
- DO NOT use for actual cryptographic key generation
- DO NOT use for security-critical applications
- DO NOT use for password/key derivation
- DO NOT claim this provides quantum resistance

Supported NIST PQC Seed Formats:
- CRYSTALS-Kyber (ML-KEM): 32-byte seeds
- CRYSTALS-Dilithium (ML-DSA): 32-byte seeds
- SPHINCS+: 48-64 byte seeds

The generated seeds are deterministic and suitable for:
- Reproducible testing of PQC implementations
- Cross-platform validation of PQC algorithms
- Test vector generation for compliance verification

Reference Standards (for FORMAT compatibility only):
- NIST FIPS 203: ML-KEM (Kyber)
- NIST FIPS 204: ML-DSA (Dilithium)
- NIST FIPS 205: SLH-DSA (SPHINCS+)
"""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Dict, Tuple
from .stream_generator import golden_stream_generator


class PQCAlgorithm(Enum):
    """NIST PQC algorithm seed formats (for testing only)."""
    KYBER512 = "Kyber-512"
    KYBER768 = "Kyber-768"
    KYBER1024 = "Kyber-1024"
    DILITHIUM2 = "Dilithium2"
    DILITHIUM3 = "Dilithium3"
    DILITHIUM5 = "Dilithium5"
    SPHINCS_PLUS_128F = "SPHINCS+-128f"
    SPHINCS_PLUS_192F = "SPHINCS+-192f"
    SPHINCS_PLUS_256F = "SPHINCS+-256f"


class PQCSecurityLevel(Enum):
    """NIST PQC security levels (reference only - NOT provided by this module)."""
    LEVEL_1 = 1  # Comparable to AES-128
    LEVEL_2 = 2  # Comparable to SHA-256/SHA3-256
    LEVEL_3 = 3  # Comparable to AES-192
    LEVEL_4 = 4  # Comparable to SHA-384/SHA3-384
    LEVEL_5 = 5  # Comparable to AES-256


# Algorithm security level mapping (for reference only)
ALGORITHM_SECURITY_LEVELS: Dict[PQCAlgorithm, PQCSecurityLevel] = {
    PQCAlgorithm.KYBER512: PQCSecurityLevel.LEVEL_1,
    PQCAlgorithm.KYBER768: PQCSecurityLevel.LEVEL_3,
    PQCAlgorithm.KYBER1024: PQCSecurityLevel.LEVEL_5,
    PQCAlgorithm.DILITHIUM2: PQCSecurityLevel.LEVEL_2,
    PQCAlgorithm.DILITHIUM3: PQCSecurityLevel.LEVEL_3,
    PQCAlgorithm.DILITHIUM5: PQCSecurityLevel.LEVEL_5,
    PQCAlgorithm.SPHINCS_PLUS_128F: PQCSecurityLevel.LEVEL_1,
    PQCAlgorithm.SPHINCS_PLUS_192F: PQCSecurityLevel.LEVEL_3,
    PQCAlgorithm.SPHINCS_PLUS_256F: PQCSecurityLevel.LEVEL_5,
}

# Required seed lengths for each algorithm format (in bytes)
ALGORITHM_SEED_LENGTHS: Dict[PQCAlgorithm, int] = {
    PQCAlgorithm.KYBER512: 32,
    PQCAlgorithm.KYBER768: 32,
    PQCAlgorithm.KYBER1024: 32,
    PQCAlgorithm.DILITHIUM2: 32,
    PQCAlgorithm.DILITHIUM3: 32,
    PQCAlgorithm.DILITHIUM5: 32,
    PQCAlgorithm.SPHINCS_PLUS_128F: 48,
    PQCAlgorithm.SPHINCS_PLUS_192F: 64,
    PQCAlgorithm.SPHINCS_PLUS_256F: 64,
}


def derive_test_seed(
    deterministic_stream: bytes,
    algorithm: PQCAlgorithm,
    context: bytes = b""
) -> bytes:
    """
    Derive a PQC-format test seed from deterministic stream.

    ⚠️ FOR TESTING ONLY - NOT CRYPTOGRAPHICALLY SECURE

    Generates deterministic test vectors in PQC-compatible format for
    algorithm testing and validation purposes.

    Args:
        deterministic_stream: Base stream from golden stream generator (16 bytes)
        algorithm: Target PQC algorithm format
        context: Optional context for domain separation in tests

    Returns:
        Test seed of appropriate length for the algorithm format
    """
    required_length = ALGORITHM_SEED_LENGTHS[algorithm]
    algorithm_id = algorithm.value.encode('utf-8')

    # Combine deterministic stream with algorithm identifier and context
    material = deterministic_stream + algorithm_id + context

    # Use SHA-256 for derivation
    derived = hashlib.sha256(material).digest()

    # Extend to required length using iterative hashing if needed
    while len(derived) < required_length:
        derived += hashlib.sha256(derived + material).digest()

    return derived[:required_length]


def generate_test_vector(
    algorithm: PQCAlgorithm,
    context: bytes = b""
) -> Tuple[bytes, bytes]:
    """
    Generate deterministic test vector in PQC-compatible format.

    ⚠️ FOR TESTING ONLY - NOT CRYPTOGRAPHICALLY SECURE

    Produces two components:
    1. Deterministic stream from golden ratio generator
    2. PQC-format test seed derived from stream

    Use for:
    - Testing PQC algorithm implementations
    - Generating reproducible test vectors
    - Cross-platform validation

    DO NOT use for:
    - Actual cryptographic key generation
    - Security-critical applications
    - Production systems

    Args:
        algorithm: Target NIST PQC algorithm format
        context: Optional context for test case separation (e.g., b"TEST1", b"CASE2")

    Returns:
        Tuple of (deterministic_stream, pqc_format_seed)

    Example:
        >>> from gq.pqc_test_vectors import generate_test_vector, PQCAlgorithm
        >>> stream, test_seed = generate_test_vector(
        ...     PQCAlgorithm.KYBER768,
        ...     context=b"TEST_CASE_1"
        ... )
        >>> len(stream)  # Base stream
        16
        >>> len(test_seed)  # Kyber-768 format seed
        32
    """
    # Generate deterministic stream
    generator = golden_stream_generator()
    deterministic_stream = next(generator)

    # Derive PQC-format test seed
    test_seed = derive_test_seed(deterministic_stream, algorithm, context)

    return deterministic_stream, test_seed


def generate_test_vector_stream(
    algorithm: PQCAlgorithm,
    count: int = 1,
    context: bytes = b""
) -> list[Tuple[bytes, bytes]]:
    """
    Generate a stream of test vectors in PQC-compatible format.

    ⚠️ FOR TESTING ONLY - NOT CRYPTOGRAPHICALLY SECURE

    Args:
        algorithm: Target NIST PQC algorithm format
        count: Number of test vectors to generate
        context: Optional context for test case separation

    Returns:
        List of (deterministic_stream, pqc_format_seed) tuples

    Example:
        >>> from gq.pqc_test_vectors import generate_test_vector_stream, PQCAlgorithm
        >>> vectors = generate_test_vector_stream(PQCAlgorithm.DILITHIUM3, count=5)
        >>> len(vectors)
        5
        >>> all(len(stream) == 16 and len(seed) == 32 for stream, seed in vectors)
        True
    """
    generator = golden_stream_generator()
    result = []

    for i in range(count):
        deterministic_stream = next(generator)
        # Add iteration number to context for unique test cases
        iteration_context = context + str(i).encode('utf-8')
        test_seed = derive_test_seed(deterministic_stream, algorithm, iteration_context)
        result.append((deterministic_stream, test_seed))

    return result


def validate_seed_format(seed: bytes) -> Dict[str, float]:
    """
    Validate format quality of test seed material.

    Performs basic statistical analysis to ensure test seed material has
    reasonable distribution for testing purposes (NOT for cryptographic validation).

    Args:
        seed: Test seed material to validate

    Returns:
        Dictionary with statistical metrics:
        - shannon_entropy: Shannon entropy in bits per byte
        - byte_diversity: Ratio of unique bytes to total bytes
        - passes_basic_checks: Boolean indicating if seed has reasonable distribution
    """
    if len(seed) == 0:
        return {
            'shannon_entropy': 0.0,
            'byte_diversity': 0.0,
            'passes_basic_checks': False
        }

    # Calculate Shannon entropy
    import math

    byte_counts = [0] * 256
    for byte in seed:
        byte_counts[byte] += 1

    shannon_entropy = 0.0
    for count in byte_counts:
        if count > 0:
            probability = count / len(seed)
            shannon_entropy -= probability * math.log2(probability)

    # Calculate byte diversity
    unique_bytes = len([c for c in byte_counts if c > 0])
    byte_diversity = unique_bytes / 256

    # Basic distribution checks for test purposes
    # For test seeds, we expect reasonable distribution
    if len(seed) < 32:
        min_entropy = 3.0
        min_diversity = 0.1
    elif len(seed) < 64:
        min_entropy = 4.0
        min_diversity = 0.1
    else:
        min_entropy = 5.0
        min_diversity = 0.15

    passes_checks = (
        shannon_entropy >= min_entropy and
        byte_diversity >= min_diversity
    )

    return {
        'shannon_entropy': shannon_entropy,
        'byte_diversity': byte_diversity,
        'passes_basic_checks': passes_checks
    }


def get_algorithm_format_info(algorithm: PQCAlgorithm) -> Dict[str, any]:
    """
    Get information about a specific NIST PQC algorithm format.

    Args:
        algorithm: NIST PQC algorithm format

    Returns:
        Dictionary with algorithm format information:
        - name: Algorithm name
        - reference_security_level: NIST security level reference (1-5)
        - seed_length: Required seed length in bytes
        - type: Algorithm type (KEM, signature)
    """
    algorithm_types = {
        PQCAlgorithm.KYBER512: "KEM",
        PQCAlgorithm.KYBER768: "KEM",
        PQCAlgorithm.KYBER1024: "KEM",
        PQCAlgorithm.DILITHIUM2: "Signature",
        PQCAlgorithm.DILITHIUM3: "Signature",
        PQCAlgorithm.DILITHIUM5: "Signature",
        PQCAlgorithm.SPHINCS_PLUS_128F: "Signature",
        PQCAlgorithm.SPHINCS_PLUS_192F: "Signature",
        PQCAlgorithm.SPHINCS_PLUS_256F: "Signature",
    }

    return {
        'name': algorithm.value,
        'reference_security_level': ALGORITHM_SECURITY_LEVELS[algorithm].value,
        'seed_length': ALGORITHM_SEED_LENGTHS[algorithm],
        'type': algorithm_types[algorithm]
    }


# Convenience functions for specific algorithm formats
def generate_kyber_test_seed(level: int = 768, context: bytes = b"") -> Tuple[bytes, bytes]:
    """Generate test vector for CRYSTALS-Kyber format (TESTING ONLY)."""
    algorithm_map = {
        512: PQCAlgorithm.KYBER512,
        768: PQCAlgorithm.KYBER768,
        1024: PQCAlgorithm.KYBER1024
    }
    algorithm = algorithm_map.get(level, PQCAlgorithm.KYBER768)
    return generate_test_vector(algorithm, context)


def generate_dilithium_test_seed(level: int = 3, context: bytes = b"") -> Tuple[bytes, bytes]:
    """Generate test vector for CRYSTALS-Dilithium format (TESTING ONLY)."""
    algorithm_map = {
        2: PQCAlgorithm.DILITHIUM2,
        3: PQCAlgorithm.DILITHIUM3,
        5: PQCAlgorithm.DILITHIUM5
    }
    algorithm = algorithm_map.get(level, PQCAlgorithm.DILITHIUM3)
    return generate_test_vector(algorithm, context)


def generate_sphincs_test_seed(level: int = 128, context: bytes = b"") -> Tuple[bytes, bytes]:
    """Generate test vector for SPHINCS+ format (TESTING ONLY)."""
    algorithm_map = {
        128: PQCAlgorithm.SPHINCS_PLUS_128F,
        192: PQCAlgorithm.SPHINCS_PLUS_192F,
        256: PQCAlgorithm.SPHINCS_PLUS_256F
    }
    algorithm = algorithm_map.get(level, PQCAlgorithm.SPHINCS_PLUS_128F)
    return generate_test_vector(algorithm, context)
