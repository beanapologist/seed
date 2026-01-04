# NIST Post-Quantum Cryptography (PQC) Integration Guide

This guide demonstrates how to integrate the deterministic key generation system with NIST-approved Post-Quantum Cryptography algorithms.

## Overview

The Binary Fusion Tap key generation system is designed to work seamlessly with NIST PQC standards, providing quantum-resistant security for long-term data protection. The generated keys can serve as seed material for PQC implementations.

## Supported NIST PQC Algorithms

### CRYSTALS-Kyber (Key Encapsulation Mechanism)
- **Purpose**: Secure key exchange resistant to quantum attacks
- **Security Levels**: Kyber512, Kyber768, Kyber1024
- **Use Case**: Establishing shared secrets in communication protocols

### CRYSTALS-Dilithium (Digital Signature Algorithm)
- **Purpose**: Post-quantum secure digital signatures
- **Security Levels**: Dilithium2, Dilithium3, Dilithium5
- **Use Case**: Authentication, message signing, certificate authorities

### FrodoKEM (Conservative Lattice-based KEM)
- **Purpose**: Alternative KEM with conservative security assumptions
- **Security Levels**: FrodoKEM-640, FrodoKEM-976, FrodoKEM-1344
- **Use Case**: Long-term secure key exchange

## Integration Patterns

### Pattern 1: Seed Material for PQC Key Generation

Use the deterministic key generator to create reproducible seed material for PQC algorithm key generation:

```python
from gq import UniversalQKD

# Generate deterministic seed for PQC key generation
generator = UniversalQKD()
seed_material = next(generator)  # 128-bit deterministic key

# Use with NIST PQC library (pseudocode):
# kyber_keypair = kyber.generate_keypair(seed=seed_material)
# dilithium_keypair = dilithium.generate_keypair(seed=seed_material)
```

### Pattern 2: Hybrid Classical/Post-Quantum Systems

Combine classical deterministic keys with PQC algorithms for defense-in-depth:

```python
from gq import UniversalQKD

generator = UniversalQKD()

# Generate deterministic component
deterministic_key = next(generator)

# Combine with PQC key encapsulation (pseudocode):
# pqc_shared_secret = kyber_kem.encapsulate(public_key)
# hybrid_key = kdf(deterministic_key || pqc_shared_secret)
```

### Pattern 3: PQC Signature with Deterministic Tie-Breaking

Use deterministic keys for consensus while securing signatures with PQC:

```python
from gq import UniversalQKD

generator = UniversalQKD()

# Generate deterministic tie-breaking value
tie_breaker = next(generator)

# Sign with Dilithium (pseudocode):
# signature = dilithium.sign(private_key, message || tie_breaker)
# This ensures deterministic consensus with quantum-resistant signatures
```

### Pattern 4: Key Derivation for PQC Systems

Use as a deterministic key derivation function in PQC-secured systems:

```python
from gq import UniversalQKD
import hashlib

generator = UniversalQKD()

def derive_pqc_compatible_key(context: bytes, length: int = 32) -> bytes:
    """Derive a PQC-compatible key with context binding."""
    base_key = next(generator)
    
    # Combine with context for domain separation
    derived = hashlib.sha256(base_key + context).digest()
    
    # Extend if needed for specific PQC algorithm requirements
    while len(derived) < length:
        derived += hashlib.sha256(derived).digest()
    
    return derived[:length]

# Generate keys for different PQC contexts
kyber_seed = derive_pqc_compatible_key(b"KYBER_KEYGEN")
dilithium_seed = derive_pqc_compatible_key(b"DILITHIUM_KEYGEN")
```

## Security Considerations

### Quantum Resistance
- The deterministic key generation itself uses classical cryptography (SHA-256)
- SHA-256 provides 128-bit quantum security (Grover's algorithm)
- When combined with NIST PQC algorithms, provides full quantum resistance

### Key Sizes
- **128-bit keys**: Suitable for Kyber512, Dilithium2 seed material
- **256-bit keys**: Recommended for Kyber768, Kyber1024, Dilithium3, Dilithium5
- **512-bit keys**: For FrodoKEM and conservative applications

### Hybrid Security Model
The recommended approach is **hybrid cryptography**:
1. Use deterministic key generation for reproducibility and consensus
2. Layer PQC algorithms for quantum resistance
3. Combine both for defense-in-depth against classical and quantum threats

## Implementation Example (Conceptual)

```python
# Conceptual integration with hypothetical PQC library
from gq import UniversalQKD

class PQCSecureChannel:
    """Hybrid post-quantum secure communication channel."""
    
    def __init__(self, deterministic_seed: bool = True):
        self.generator = UniversalQKD() if deterministic_seed else None
        
    def establish_session(self, peer_public_key):
        """Establish quantum-resistant session key."""
        # Step 1: Generate deterministic component (if enabled)
        if self.generator:
            deterministic_component = next(self.generator)
        else:
            deterministic_component = b'\x00' * 16
            
        # Step 2: PQC Key Encapsulation (pseudocode)
        # kyber_ciphertext, kyber_shared_secret = kyber.kem_encap(peer_public_key)
        
        # Step 3: Combine for hybrid security
        # session_key = kdf(deterministic_component || kyber_shared_secret)
        
        return {
            'session_key': b'...',  # Hybrid session key
            'ciphertext': b'...',   # Send to peer
            'algorithm': 'HYBRID-KYBER768-GQ'
        }
    
    def sign_message(self, message: bytes, private_key):
        """Sign message with PQC algorithm."""
        # Add deterministic nonce for reproducibility
        if self.generator:
            nonce = next(self.generator)
        else:
            nonce = secrets.token_bytes(16)
            
        # Sign with Dilithium (pseudocode)
        # signature = dilithium.sign(private_key, message, nonce=nonce)
        
        return {
            'message': message,
            'signature': b'...',
            'algorithm': 'DILITHIUM3-GQ'
        }
```

## Reference Implementations

For actual PQC implementations, refer to:
- **liboqs**: Open Quantum Safe library (C)
- **PQClean**: Clean implementations of NIST PQC algorithms
- **pqcrypto**: Rust PQC library
- **pyca/cryptography**: Python cryptography library (future PQC support)

## Standards References

- **NIST FIPS 203**: Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM/Kyber)
- **NIST FIPS 204**: Module-Lattice-Based Digital Signature Algorithm (ML-DSA/Dilithium)
- **NIST FIPS 205**: Stateless Hash-Based Digital Signature Algorithm (SLH-DSA/SPHINCS+)
- **NIST SP 800-208**: Recommendation for Stateful Hash-Based Signature Schemes

## Conclusion

This deterministic key generation system provides a solid foundation for building quantum-resistant systems when combined with NIST PQC algorithms. The reproducible nature of the keys makes it ideal for distributed consensus, while integration with PQC algorithms ensures protection against quantum computer attacks.

For production deployments, always use certified PQC implementations and follow NIST guidelines for key management and cryptographic operations.
