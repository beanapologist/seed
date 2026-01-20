# NIST Post-Quantum Cryptography (PQC) Integration Guide

This guide demonstrates how to use the **production-ready hybrid key generation** system with NIST-approved Post-Quantum Cryptography algorithms.

## Overview

The system provides **hybrid key generation** combining:
- **Deterministic keys** from GCP-1 protocol (16 bytes)
- **PQC-compatible seeds** derived for NIST algorithms (32-64 bytes)

This provides **defense-in-depth security** where security holds as long as either component remains secure.

## Supported NIST PQC Algorithms

### CRYSTALS-Kyber (ML-KEM) - NIST FIPS 203
Key Encapsulation Mechanism for secure key exchange:
- **Kyber-512** (Security Level 1) - Equivalent to AES-128
- **Kyber-768** (Security Level 3) - Equivalent to AES-192
- **Kyber-1024** (Security Level 5) - Equivalent to AES-256

### CRYSTALS-Dilithium (ML-DSA) - NIST FIPS 204
Digital signature algorithm for authentication:
- **Dilithium2** (Security Level 2) - Equivalent to SHA-256/SHA3-256
- **Dilithium3** (Security Level 3) - Equivalent to AES-192
- **Dilithium5** (Security Level 5) - Equivalent to AES-256

### SPHINCS+ (SLH-DSA) - NIST FIPS 205
Stateless hash-based signature scheme:
- **SPHINCS+-128f** (Security Level 1) - Fast variant
- **SPHINCS+-192f** (Security Level 3) - Medium security
- **SPHINCS+-256f** (Security Level 5) - High security

## Quick Start

### Basic Hybrid Key Generation

```python
from gq import generate_kyber_seed, generate_dilithium_seed, generate_sphincs_seed

# Generate Kyber-768 hybrid key (recommended for most applications)
det_key, pqc_seed = generate_kyber_seed(level=768, context=b"KEYGEN")
print(f"Deterministic key (16 bytes): {det_key.hex()}")
print(f"PQC seed (32 bytes): {pqc_seed.hex()}")

# Generate Dilithium3 hybrid key for signatures
det_key, pqc_seed = generate_dilithium_seed(level=3, context=b"SIGN")

# Generate SPHINCS+-128f hybrid key for hash-based signatures
det_key, pqc_seed = generate_sphincs_seed(level=128, context=b"HASH_SIGN")
```

### Advanced Usage

```python
from gq import (
    PQCAlgorithm,
    generate_hybrid_key,
    generate_hybrid_key_stream,
    validate_pqc_seed_entropy,
    get_algorithm_info
)

# Generate hybrid key for specific algorithm
det_key, pqc_seed = generate_hybrid_key(
    PQCAlgorithm.KYBER768,
    context=b"SESSION_KEY"
)

# Generate multiple hybrid keys for batch operations
keys = generate_hybrid_key_stream(
    PQCAlgorithm.DILITHIUM3,
    count=10,
    context=b"BATCH_SIGN"
)
for i, (det_key, pqc_seed) in enumerate(keys):
    print(f"Key {i}: det={det_key.hex()[:16]}... pqc={pqc_seed.hex()[:16]}...")

# Validate entropy quality of generated seeds
metrics = validate_pqc_seed_entropy(pqc_seed)
print(f"Shannon entropy: {metrics['shannon_entropy']:.2f} bits/byte")
print(f"Byte diversity: {metrics['byte_diversity']:.2f}")
print(f"Passes basic checks: {metrics['passes_basic_checks']}")

# Get algorithm information
info = get_algorithm_info(PQCAlgorithm.KYBER768)
print(f"Algorithm: {info['name']}")
print(f"Type: {info['type']}")
print(f"Security level: {info['security_level']}")
print(f"Required seed length: {info['seed_length']} bytes")
```

## Integration Patterns

### Pattern 1: Direct PQC Seed Material

Use hybrid keys directly as seed material for PQC libraries:

```python
from gq import generate_kyber_seed

# Generate seed for Kyber key pair generation
det_key, kyber_seed = generate_kyber_seed(level=768, context=b"KEYGEN")

# Use with actual PQC library (pseudocode):
# from pqcrypto.kem.kyber768 import generate_keypair
# public_key, secret_key = generate_keypair(seed=kyber_seed)
```

### Pattern 2: Hybrid Classical/Post-Quantum Systems

Combine both components for maximum security:

```python
from gq import generate_hybrid_key, PQCAlgorithm
import hashlib

def create_hybrid_session_key(peer_public_key):
    """Create hybrid session key combining classical and PQC."""
    # Generate hybrid components
    classical_key, pqc_seed = generate_hybrid_key(
        PQCAlgorithm.KYBER768,
        context=b"SESSION"
    )
    
    # Use PQC seed for key encapsulation (pseudocode)
    # pqc_ciphertext, pqc_shared_secret = kyber_kem.encapsulate(
    #     peer_public_key,
    #     seed=pqc_seed
    # )
    
    # Combine both for hybrid key
    # hybrid_key = hashlib.sha256(classical_key + pqc_shared_secret).digest()
    
    return {
        'classical_component': classical_key,
        'pqc_seed': pqc_seed,
        # 'pqc_ciphertext': pqc_ciphertext,
        # 'hybrid_key': hybrid_key
    }
```

### Pattern 3: Deterministic PQC Signatures

Use deterministic keys for reproducibility with PQC signatures:

```python
from gq import generate_dilithium_seed

def sign_with_deterministic_nonce(message: bytes, context: bytes):
    """Sign message with deterministic nonce from hybrid key."""
    # Generate deterministic components
    nonce, dilithium_seed = generate_dilithium_seed(
        level=3,
        context=context
    )
    
    # Use with Dilithium (pseudocode)
    # signature = dilithium.sign(
    #     secret_key,
    #     message,
    #     nonce=nonce  # Deterministic nonce for reproducibility
    # )
    
    return {
        'nonce': nonce,
        'dilithium_seed': dilithium_seed,
        # 'signature': signature
    }

# Sign with deterministic context for consensus
signature_data = sign_with_deterministic_nonce(
    message=b"consensus_proposal",
    context=b"CONSENSUS_ROUND_42"
)
```

### Pattern 4: Key Derivation for PQC Systems

Derive multiple PQC-compatible keys from single hybrid source:

```python
from gq import generate_hybrid_key_stream, PQCAlgorithm

def derive_multiple_pqc_keys(base_context: bytes, count: int):
    """Derive multiple PQC keys with context binding."""
    keys = generate_hybrid_key_stream(
        PQCAlgorithm.KYBER768,
        count=count,
        context=base_context
    )
    
    derived_keys = []
    for i, (det_key, pqc_seed) in enumerate(keys):
        derived_keys.append({
            'index': i,
            'deterministic_key': det_key,
            'pqc_seed': pqc_seed,
            'use_case': f"KEY_{i}_{base_context.decode()}"
        })
    
    return derived_keys

# Derive keys for different purposes
keys = derive_multiple_pqc_keys(b"APPLICATION", count=5)
for key_info in keys:
    print(f"Key {key_info['index']}: {key_info['use_case']}")
```

### Pattern 5: Multi-Algorithm Security

Use different algorithms for different security requirements:

```python
from gq import (
    generate_kyber_seed,
    generate_dilithium_seed,
    generate_sphincs_seed
)

class HybridPQCKeyManager:
    """Manage hybrid keys for multiple PQC algorithms."""
    
    def __init__(self):
        self.keys = {}
    
    def generate_kem_key(self, security_level: int = 3):
        """Generate key for Key Encapsulation Mechanism."""
        det_key, pqc_seed = generate_kyber_seed(
            level=768 if security_level == 3 else 1024,
            context=b"KEM"
        )
        self.keys['kem'] = (det_key, pqc_seed)
        return det_key, pqc_seed
    
    def generate_signature_key(self, security_level: int = 3):
        """Generate key for digital signatures."""
        det_key, pqc_seed = generate_dilithium_seed(
            level=security_level,
            context=b"SIGN"
        )
        self.keys['signature'] = (det_key, pqc_seed)
        return det_key, pqc_seed
    
    def generate_hash_signature_key(self, security_level: int = 128):
        """Generate key for hash-based signatures (long-term security)."""
        det_key, pqc_seed = generate_sphincs_seed(
            level=security_level,
            context=b"HASH_SIGN"
        )
        self.keys['hash_signature'] = (det_key, pqc_seed)
        return det_key, pqc_seed

# Use the manager
manager = HybridPQCKeyManager()
kem_key = manager.generate_kem_key(security_level=3)
sig_key = manager.generate_signature_key(security_level=3)
hash_sig_key = manager.generate_hash_signature_key(security_level=128)
```

## Security Considerations

### Quantum Resistance
- **Classical Component**: SHA-256 provides 128-bit quantum security (Grover's algorithm)
- **PQC Component**: Full quantum resistance against Shor's and Grover's algorithms
- **Hybrid Security**: Secure as long as **either** component remains unbroken

### Key Sizes and Security Levels

| Algorithm | Seed Length | Security Level | Classical Equivalent |
|-----------|-------------|----------------|---------------------|
| Kyber-512 | 32 bytes | Level 1 | AES-128 |
| Kyber-768 | 32 bytes | Level 3 | AES-192 |
| Kyber-1024 | 32 bytes | Level 5 | AES-256 |
| Dilithium2 | 32 bytes | Level 2 | SHA-256 |
| Dilithium3 | 32 bytes | Level 3 | AES-192 |
| Dilithium5 | 32 bytes | Level 5 | AES-256 |
| SPHINCS+-128f | 48 bytes | Level 1 | AES-128 |
| SPHINCS+-192f | 64 bytes | Level 3 | AES-192 |
| SPHINCS+-256f | 64 bytes | Level 5 | AES-256 |

### Entropy Quality Validation

All generated PQC seeds undergo entropy quality validation:
- **Shannon Entropy**: Minimum 4.0 bits per byte for 32-byte seeds
- **Byte Diversity**: Minimum 10% unique bytes
- **Cryptographic Quality**: Derived from SHA-256 output

```python
from gq import generate_hybrid_key, PQCAlgorithm, validate_pqc_seed_entropy

# Generate and validate
_, pqc_seed = generate_hybrid_key(PQCAlgorithm.KYBER768)
metrics = validate_pqc_seed_entropy(pqc_seed)

assert metrics['passes_basic_checks'], "Seed quality check failed"
print(f"✓ Seed quality validated")
```

## Reference Implementations

For actual PQC algorithm implementations, refer to:

- **liboqs** - Open Quantum Safe library (C/C++)
  - https://github.com/open-quantum-safe/liboqs
  
- **PQClean** - Clean implementations of NIST PQC algorithms
  - https://github.com/PQClean/PQClean
  
- **pqcrypto** - Rust PQC library
  - https://github.com/rustpq/pqcrypto
  
- **pyca/cryptography** - Python cryptography library (PQC support in development)
  - https://github.com/pyca/cryptography

## NIST Standards References

- **NIST FIPS 203**: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM/Kyber)
  - https://csrc.nist.gov/pubs/fips/203/final
  
- **NIST FIPS 204**: Module-Lattice-Based Digital Signature Standard (ML-DSA/Dilithium)
  - https://csrc.nist.gov/pubs/fips/204/final
  
- **NIST FIPS 205**: Stateless Hash-Based Digital Signature Standard (SLH-DSA/SPHINCS+)
  - https://csrc.nist.gov/pubs/fips/205/final
  
- **NIST SP 800-208**: Recommendation for Stateful Hash-Based Signature Schemes
  - https://csrc.nist.gov/pubs/sp/800/208/final

## Testing and Validation

Run comprehensive NIST PQC compliance tests:

```bash
# Run all NIST PQC tests
python -m unittest test_nist_pqc -v

# Run test vector compliance tests
python -m unittest test_nist_pqc_vectors -v

# Run CI compliance workflow locally (requires act)
act -j nist-pqc-validation
```

## Conclusion

This hybrid key generation system provides a **production-ready foundation** for building quantum-resistant systems. The combination of:
- **Deterministic reproducibility** from GCP-1
- **Quantum resistance** from NIST PQC algorithms
- **Defense-in-depth** security model

Makes it ideal for:
- Distributed consensus systems
- Secure communication protocols
- Long-term data protection
- Post-quantum cryptography research

For production deployments:
1. ✅ Use certified PQC implementations (liboqs, PQClean)
2. ✅ Follow NIST guidelines for key management
3. ✅ Validate entropy quality of generated seeds
4. ✅ Implement proper key rotation and forward secrecy
5. ✅ Test against NIST test vectors regularly
