# Quantum Key Distribution (QKD)

This directory contains the core Quantum Key Distribution implementation with deterministic key generation and quantum-level security.

## Structure

- **algorithms/** - Core QKD algorithms and key generation implementations
  - `universal_qkd.py` - Universal QKD Key Generator (GCP-1)
  - `gqs1.py` - Golden Quantum Standard Test Vectors (GQS-1)
  - `quantum_key_generator.py` - Quantum Key Generator Service (QKGS)

- **utils/** - Utility functions for QKD operations

## Features

- Deterministic key generation with verified checksums
- Quantum-level security using Binary Fusion Tap
- Cross-implementation consistency
- Zero-dependency architecture for maximum security
- Cryptographic forward secrecy via state ratcheting

## Usage

See the main README.md for detailed usage instructions and examples.
