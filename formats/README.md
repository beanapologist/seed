# Golden Seed Formats

This directory contains the golden seed values in various binary and hex formats for cross-language compatibility.

## Files

### Standard Golden Seeds
- **golden_seed.hex** - Hex representation of the golden seed (iφ)
- **golden_seed_16.bin** - 16-byte binary seed (iφ)
- **golden_seed_32.bin** - 32-byte binary seed (iφ + 2×φ for consensus)

### Large Seed Test Files (1056+ bits)
- **golden_seed_132.bin** - 132-byte binary seed (1056 bits)
- **golden_seed_256.bin** - 256-byte binary seed (2048 bits)
- **golden_seed_512.bin** - 512-byte binary seed (4096 bits)
- **test_checksums.json** - Expected SHA-256/SHA-512 checksums for large seed files

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

## Large Seed Files

The large seed files (1056+ bits) are used for testing and validating checksum verification workflows. These files contain deterministic data based on the golden ratio pattern and are used to ensure data integrity for larger binary seeds used in cryptographic applications.

### Verification

To verify the integrity of all seed files:

```bash
# Verify large seeds with checksums
python checksum/verify_large_seeds.py

# Verify with manifested data
python checksum/verify_large_seeds.py --manifested
```

The expected checksums are stored in `test_checksums.json` for automated validation.
