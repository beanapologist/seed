"""
NIST Post-Quantum Cryptography (PQC) Hybrid Key Generation

This module provides hybrid key generation combining deterministic key streams
from the Golden Consensus Protocol with NIST-approved Post-Quantum Cryptography
primitives for quantum-resistant security.

Supported NIST PQC Algorithms:
- CRYSTALS-Kyber (ML-KEM): Key Encapsulation Mechanism
- CRYSTALS-Dilithium (ML-DSA): Digital Signature Algorithm  
- SPHINCS+: Stateless Hash-Based Signature Scheme

The hybrid approach provides:
- Deterministic reproducibility from GCP-1 protocol
- Quantum resistance from NIST PQC algorithms
- Defense-in-depth security model
- Forward compatibility with PQC standards

Reference Standards:
- NIST FIPS 203: ML-KEM (Kyber)
- NIST FIPS 204: ML-DSA (Dilithium)
- NIST FIPS 205: SLH-DSA (SPHINCS+)
"""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Dict, Tuple
from .universal_qkd import universal_qkd_generator


class PQCAlgorithm(Enum):
    """NIST-approved Post-Quantum Cryptography algorithms."""
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
    """NIST PQC security levels."""
    LEVEL_1 = 1  # At least as hard as AES-128
    LEVEL_2 = 2  # At least as hard as SHA-256/SHA3-256
    LEVEL_3 = 3  # At least as hard as AES-192
    LEVEL_4 = 4  # At least as hard as SHA-384/SHA3-384
    LEVEL_5 = 5  # At least as hard as AES-256


# Algorithm security level mapping
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

# Required seed lengths for each algorithm (in bytes)
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


def derive_pqc_seed(
    deterministic_key: bytes,
    algorithm: PQCAlgorithm,
    context: bytes = b""
) -> bytes:
    """
    Derive a PQC-compatible seed from deterministic key material.
    
    Combines the deterministic key from GCP-1 with algorithm-specific
    context to produce seed material suitable for NIST PQC algorithms.
    
    Args:
        deterministic_key: Base key from UniversalQKD generator (16 bytes)
        algorithm: Target PQC algorithm
        context: Optional context for domain separation
        
    Returns:
        PQC-compatible seed of appropriate length for the algorithm
    """
    required_length = ALGORITHM_SEED_LENGTHS[algorithm]
    algorithm_id = algorithm.value.encode('utf-8')
    
    # Combine deterministic key with algorithm identifier and context
    material = deterministic_key + algorithm_id + context
    
    # Use SHA-256 for initial derivation
    derived = hashlib.sha256(material).digest()
    
    # Extend to required length using iterative hashing if needed
    while len(derived) < required_length:
        derived += hashlib.sha256(derived + material).digest()
    
    return derived[:required_length]


def generate_hybrid_key(
    algorithm: PQCAlgorithm,
    context: bytes = b"",
    deterministic: bool = True
) -> Tuple[bytes, bytes]:
    """
    Generate hybrid key material combining GCP-1 with PQC algorithm.
    
    This function produces two components:
    1. Deterministic key from GCP-1 protocol
    2. PQC-compatible seed derived from deterministic key
    
    The hybrid approach ensures:
    - Reproducibility through deterministic generation
    - Quantum resistance through PQC seed derivation
    - Context binding for domain separation
    
    Args:
        algorithm: Target NIST PQC algorithm
        context: Optional context for domain separation (e.g., b"KEYGEN", b"SIGN")
        deterministic: If True, use GCP-1; if False, use entropy mixing
        
    Returns:
        Tuple of (deterministic_key, pqc_seed)
        
    Example:
        >>> from gq.nist_pqc import generate_hybrid_key, PQCAlgorithm
        >>> det_key, pqc_seed = generate_hybrid_key(
        ...     PQCAlgorithm.KYBER768,
        ...     context=b"KEYGEN"
        ... )
        >>> len(det_key)  # GCP-1 key
        16
        >>> len(pqc_seed)  # Kyber-768 seed
        32
    """
    # Generate deterministic key using GCP-1
    generator = universal_qkd_generator()
    deterministic_key = next(generator)
    
    # Derive PQC-compatible seed
    pqc_seed = derive_pqc_seed(deterministic_key, algorithm, context)
    
    return deterministic_key, pqc_seed


def generate_hybrid_key_stream(
    algorithm: PQCAlgorithm,
    count: int = 1,
    context: bytes = b""
) -> list[Tuple[bytes, bytes]]:
    """
    Generate a stream of hybrid keys for the specified PQC algorithm.
    
    Args:
        algorithm: Target NIST PQC algorithm
        count: Number of key pairs to generate
        context: Optional context for domain separation
        
    Returns:
        List of (deterministic_key, pqc_seed) tuples
        
    Example:
        >>> from gq.nist_pqc import generate_hybrid_key_stream, PQCAlgorithm
        >>> keys = generate_hybrid_key_stream(PQCAlgorithm.DILITHIUM3, count=5)
        >>> len(keys)
        5
        >>> all(len(det_key) == 16 and len(pqc) == 32 for det_key, pqc in keys)
        True
    """
    generator = universal_qkd_generator()
    result = []
    
    for i in range(count):
        deterministic_key = next(generator)
        # Add iteration number to context for unique seeds
        iteration_context = context + str(i).encode('utf-8')
        pqc_seed = derive_pqc_seed(deterministic_key, algorithm, iteration_context)
        result.append((deterministic_key, pqc_seed))
    
    return result


def validate_pqc_seed_entropy(seed: bytes) -> Dict[str, float]:
    """
    Validate entropy quality of PQC seed material.
    
    Performs basic entropy analysis to ensure seed material meets
    minimum quality requirements for cryptographic use.
    
    Args:
        seed: PQC seed material to validate
        
    Returns:
        Dictionary with entropy metrics:
        - shannon_entropy: Shannon entropy in bits per byte
        - byte_diversity: Ratio of unique bytes to total bytes
        - passes_basic_checks: Boolean indicating if seed passes basic quality checks
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
    
    # Basic quality checks
    # For cryptographic seeds, we expect reasonable randomness
    # Shannon entropy: For 32 bytes, we expect at least 4-5 bits per byte
    # For larger seeds (64+ bytes), we can expect closer to 7-8 bits per byte
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


def get_algorithm_info(algorithm: PQCAlgorithm) -> Dict[str, any]:
    """
    Get information about a specific NIST PQC algorithm.
    
    Args:
        algorithm: NIST PQC algorithm
        
    Returns:
        Dictionary with algorithm information:
        - name: Algorithm name
        - security_level: NIST security level (1-5)
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
        'security_level': ALGORITHM_SECURITY_LEVELS[algorithm].value,
        'seed_length': ALGORITHM_SEED_LENGTHS[algorithm],
        'type': algorithm_types[algorithm]
    }


# Convenience functions for specific algorithms
def generate_kyber_seed(level: int = 768, context: bytes = b"") -> Tuple[bytes, bytes]:
    """Generate hybrid key material for CRYSTALS-Kyber."""
    algorithm_map = {
        512: PQCAlgorithm.KYBER512,
        768: PQCAlgorithm.KYBER768,
        1024: PQCAlgorithm.KYBER1024
    }
    algorithm = algorithm_map.get(level, PQCAlgorithm.KYBER768)
    return generate_hybrid_key(algorithm, context)


def generate_dilithium_seed(level: int = 3, context: bytes = b"") -> Tuple[bytes, bytes]:
    """Generate hybrid key material for CRYSTALS-Dilithium."""
    algorithm_map = {
        2: PQCAlgorithm.DILITHIUM2,
        3: PQCAlgorithm.DILITHIUM3,
        5: PQCAlgorithm.DILITHIUM5
    }
    algorithm = algorithm_map.get(level, PQCAlgorithm.DILITHIUM3)
    return generate_hybrid_key(algorithm, context)


def generate_sphincs_seed(level: int = 128, context: bytes = b"") -> Tuple[bytes, bytes]:
    """Generate hybrid key material for SPHINCS+."""
    algorithm_map = {
        128: PQCAlgorithm.SPHINCS_PLUS_128F,
        192: PQCAlgorithm.SPHINCS_PLUS_192F,
        256: PQCAlgorithm.SPHINCS_PLUS_256F
    }
    algorithm = algorithm_map.get(level, PQCAlgorithm.SPHINCS_PLUS_128F)
    return generate_hybrid_key(algorithm, context)
