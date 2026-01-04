# Golden Seed Formats

This directory contains the golden seed values in various binary and hex formats for cross-language compatibility.

## Files

- **golden_seed.hex** - Hex representation of the golden seed (iφ)
- **golden_seed_16.bin** - 16-byte binary seed (iφ)
- **golden_seed_32.bin** - 32-byte binary seed (iφ + 2×φ for consensus)

## Seed Values

### 16-byte seed (iφ):
```
0000000000000000A8F4979B77E3F93F
```

### 32-byte seed (iφ + 2×φ for consensus):
```
0000000000000000A8F4979B77E3F93FA8F4979B77E3F93FA8F4979B77E3F93F
```

## Mathematical Basis

**iφ = 0 + i × φ** where **φ = (1 + √5)/2 ≈ 1.618033988749895**

## Usage

These binary files can be read in any programming language to obtain the universal golden seed for deterministic key generation with post-quantum security properties.

### Interpretation

- Bytes 0-7: Real part = 0.0
- Bytes 8-15: Imaginary part = φ ≈ 1.618033988749895
- Format: IEEE 754 double-precision (little-endian complex)

These seeds are used for deterministic tie-breaking in distributed systems and post-quantum secure key generation, compatible with NIST PQC algorithms.
