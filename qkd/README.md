# Post-Quantum Secure Key Generation

This directory contains the core post-quantum secure key generation implementation with deterministic key generation aligned with NIST Post-Quantum Cryptography (PQC) standards.

## Structure

- **algorithms/** - Core PQC-compatible algorithms and key generation implementations
  - `universal_qkd.py` - Universal Key Generator (GCP-1)
  - `gqs1.py` - Golden Standard Test Vectors (GQS-1)
  - `quantum_key_generator.py` - Key Generator Service

- **utils/** - Utility functions for key generation operations

## Features

- Deterministic key generation with verified checksums
- **NIST PQC Alignment**: Compatible with Kyber, Dilithium, and FrodoKEM
- Cross-implementation consistency
- Zero-dependency architecture for maximum security
- Cryptographic forward secrecy via state ratcheting
- Quantum-resistant design for post-quantum security

## NIST PQC Integration

This system provides key generation capabilities that integrate with NIST-approved Post-Quantum Cryptography algorithms:
- **CRYSTALS-Kyber** (Key Encapsulation)
- **CRYSTALS-Dilithium** (Digital Signatures)
- **FrodoKEM** (Conservative Lattice-based KEM)

## Usage

See the main README.md for detailed usage instructions and examples.
