# Checksum Verification

This directory contains tools for verifying checksums and ensuring data integrity in the post-quantum secure key generation system.

## Tools

- **verify_binary_representation.py** - Binary representation verification with SHA256/SHA512 checksum validation
- **verify_large_seeds.py** - Large seed checksum verification for seeds exceeding 1056 bits

## Features

- SHA256 and SHA512 checksum calculation
- Binary representation verification
- 8-fold Heartbeat operation validation
- ZPE Overflow extraction verification
- Data integrity verification during transmission or storage
- NIST PQC compatible verification methods
- Large seed file verification (1056+ bits)
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

### Large Seed Verification

```bash
# Verify all large seeds (1056+ bits) in formats/ directory
python checksum/verify_large_seeds.py

# Verify with manifested data calculation
python checksum/verify_large_seeds.py --manifested

# Verify specific seed files
python checksum/verify_large_seeds.py formats/golden_seed_132.bin formats/golden_seed_256.bin

# Output in JSON format
python checksum/verify_large_seeds.py --json

# Use custom checksums file
python checksum/verify_large_seeds.py --checksums path/to/checksums.json
```

## Large Seed Files

The repository includes test seed files with 1056+ bit sizes for verification:

- **golden_seed_132.bin** - 132 bytes (1056 bits) - Minimum size requirement
- **golden_seed_256.bin** - 256 bytes (2048 bits) - Medium size seed
- **golden_seed_512.bin** - 512 bytes (4096 bits) - Large size seed

Expected checksums are stored in `formats/test_checksums.json` for automated validation.

## Automated Verification

The GitHub Actions workflow `.github/workflows/checksum-verification.yml` automatically verifies:

1. Existence of input files with 1056+ bit sizes
2. SHA-256 and SHA-512 checksums for all large seeds
3. Manifested binary data integrity
4. Generates verification logs stored as artifacts

The workflow triggers on `push` and `pull_request` events to the `main` branch.
