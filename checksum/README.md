# Checksum Verification

This directory contains tools for verifying checksums and ensuring data integrity in the post-quantum secure key generation system.

## Tools

- **verify_binary_representation.py** - Binary representation verification with SHA256/SHA512 checksum validation

## Features

- SHA256 and SHA512 checksum calculation
- Binary representation verification
- 8-fold Heartbeat operation validation
- ZPE Overflow extraction verification
- Data integrity verification during transmission or storage
- NIST PQC compatible verification methods

## Usage

```bash
# Run verification for k=11 with seed_11=1234567891011
python checksum/verify_binary_representation.py
```

The tool demonstrates the relationship between seed values and their manifested binary forms using the formula:
```
manifested = (seed * 8) + k
```
