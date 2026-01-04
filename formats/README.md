# Golden Seed Formats

This directory contains the golden seed values in various binary and hex formats for cross-language compatibility.

## Files

### Standard Golden Seeds
- **golden_seed.hex** - Hex representation of the golden seed (iφ)
- **golden_seed_16.bin** - 16-byte binary seed (iφ)
- **golden_seed_32.bin** - 32-byte binary seed (iφ + 2×φ for consensus)

### Test Seed Files (Various Bit Strengths)
- **golden_seed_132.bin** - 132-byte binary seed (1056 bits) - Large seed example
- **golden_seed_256.bin** - 256-byte binary seed (2048 bits) - Extra large seed example
- **golden_seed_512.bin** - 512-byte binary seed (4096 bits) - Multi-kilobit seed example
- **test_checksums.json** - Expected SHA-256/SHA-512 checksums for test seed files

The test files demonstrate checksum verification for various bit strengths and are not size requirements. The checksum tools support arbitrary bit sizes for cryptographic applications.

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

The test seed files demonstrate checksum verification for various bit strengths and are used for testing and validating checksum verification workflows. These files contain deterministic data based on the golden ratio pattern and demonstrate data integrity validation for binary seeds of different sizes used in cryptographic applications.

The checksum tools in this repository support arbitrary bit sizes, from small seeds (128 bits) to multi-megabit seeds, making them suitable for any post-quantum cryptographic application.

### Verification

To verify the integrity of seed files:

```bash
# Verify seed files with checksums (any bit size)
python checksum/verify_large_seeds.py

# Verify with manifested data
python checksum/verify_large_seeds.py --manifested
```

The expected checksums are stored in `test_checksums.json` for automated validation. The verification tools support arbitrary bit sizes.
