# Checksum Verification

This directory contains tools for verifying checksums and ensuring data integrity in the post-quantum secure key generation system.

## Tools

- **verify_binary_representation.py** - Binary representation verification with SHA256/SHA512 checksum validation
- **verify_large_seeds.py** - Seed file checksum verification for any bit strength

## Features

- SHA256 and SHA512 checksum calculation for any bit strength
- Binary representation verification
- 8-fold Heartbeat operation validation
- ZPE Overflow extraction verification
- Data integrity verification during transmission or storage
- NIST PQC compatible verification methods
- Support for arbitrary input sizes (from small seeds to multi-kilobit files)
- Batch verification support
- Manifested data integrity validation

## Usage

### Binary Representation Verification

```bash
# Run verification for k=11 with seed_11=1234567891011
python checksum/verify_binary_representation.py
```

The tool demonstrates the relationship between seed values and their manifested binary forms using the formula:
```
manifested = (seed * 8) + k
```

### Seed File Verification

```bash
# Verify seed files in formats/ directory
python checksum/verify_large_seeds.py

# Verify with manifested data calculation
python checksum/verify_large_seeds.py --manifested

# Verify specific seed files (any bit size)
python checksum/verify_large_seeds.py formats/golden_seed_16.bin formats/golden_seed_132.bin

# Output in JSON format
python checksum/verify_large_seeds.py --json

# Use custom checksums file
python checksum/verify_large_seeds.py --checksums path/to/checksums.json

# Set custom minimum bit size (default: 0, accepts any size)
python checksum/verify_large_seeds.py --min-bits 1056
```

## Test Seed Files

The repository includes test seed files with various bit sizes for verification:

- **golden_seed_16.bin** - 16 bytes (128 bits) - Small seed example
- **golden_seed_32.bin** - 32 bytes (256 bits) - Standard seed example
- **golden_seed_132.bin** - 132 bytes (1056 bits) - Large seed example
- **golden_seed_256.bin** - 256 bytes (2048 bits) - Extra large seed example
- **golden_seed_512.bin** - 512 bytes (4096 bits) - Multi-kilobit seed example

These files demonstrate the tool's ability to handle arbitrary bit strengths. Expected checksums are stored in `formats/test_checksums.json` for automated validation.

## Automated Verification

The checksum verification tools support:

1. Arbitrary input file sizes (from bytes to megabytes)
2. SHA-256 and SHA-512 checksums for any bit strength
3. Manifested binary data integrity validation
4. Flexible batch verification with configurable size requirements

The tools are designed to work with cryptographic seeds of any size, making them suitable for various post-quantum cryptography applications.
