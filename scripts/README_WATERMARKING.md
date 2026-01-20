# Watermarking Scripts

This directory contains scripts for creating and verifying watermarked binary files for commercial licensing compliance.

## Overview

The watermarking system embeds traceable licensing data into binary outputs while preserving deterministic properties and ensuring cryptographic integrity.

## Scripts

### create_watermarked_binary.py

Creates watermarked binary files for licensed commercial distribution.

**Usage:**
```bash
python scripts/create_watermarked_binary.py \
    --input <input_binary> \
    --output <output_binary> \
    --license-id <license_id> \
    --user-info <user_info> \
    --secret <secret_key>
```

**Example:**
```bash
export WATERMARK_SECRET="your-secret-key"
python scripts/create_watermarked_binary.py \
    --input formats/golden_seed_256.bin \
    --output output/licensed_seed.bin \
    --license-id "LICENSE-2026-001" \
    --user-info "Acme Corporation"
```

### verify_watermark.py

Verifies watermarked binaries and extracts licensing information.

**Usage:**
```bash
python scripts/verify_watermark.py \
    --input <watermarked_binary> \
    --secret <secret_key>
```

**Example:**
```bash
export WATERMARK_SECRET="your-secret-key"
python scripts/verify_watermark.py \
    --input output/licensed_seed.bin
```

**JSON Output:**
```bash
python scripts/verify_watermark.py \
    --input output/licensed_seed.bin \
    --secret "your-secret-key" \
    --json
```

## Workflow for Licensed Users

### 1. Obtain License

Contact the repository owner to obtain:
- Unique License ID (e.g., `LICENSE-2026-001`)
- Secret key for watermark signing
- Authorization for commercial distribution

### 2. Generate Watermarked Binaries

Create your binary outputs with embedded watermarks:

```bash
# Set secret key (recommended: use environment variable)
export WATERMARK_SECRET="your-provided-secret-key"

# Create watermarked binary
python scripts/create_watermarked_binary.py \
    --input your_input.bin \
    --output your_licensed_output.bin \
    --license-id "YOUR-LICENSE-ID" \
    --user-info "Your Organization Name"
```

### 3. Distribute Licensed Binaries

Distribute the watermarked binaries according to your license terms. The watermark:
- Identifies your license
- Traces distribution
- Proves authenticity
- Ensures compliance

### 4. Verify Binaries

Recipients can verify licensing information (if they have the secret):

```bash
python scripts/verify_watermark.py \
    --input received_binary.bin \
    --secret "verification-secret"
```

## Security Best Practices

### Secret Key Management

- **Never commit secrets to version control**
- **Use environment variables** instead of command-line arguments
- **Rotate keys** if compromised
- **Limit access** to authorized personnel only

### Setting Environment Variables

**Linux/macOS:**
```bash
export WATERMARK_SECRET="your-secret-key"
```

**Windows (Command Prompt):**
```cmd
set WATERMARK_SECRET=your-secret-key
```

**Windows (PowerShell):**
```powershell
$env:WATERMARK_SECRET="your-secret-key"
```

### Secure Storage

Store secrets securely using:
- Environment variables
- Secret management services (e.g., AWS Secrets Manager, HashiCorp Vault)
- Encrypted configuration files with restricted permissions

## Compliance

All watermarked binaries are subject to the terms in `COMMERCIAL_LICENSE.md`:

- **Authorization Required**: Only authorized licensees may create watermarked binaries
- **No Tampering**: Watermarks must not be removed or modified
- **No Secret Sharing**: Secret keys must not be shared with unauthorized parties
- **Traceability**: Each watermark uniquely identifies the licensee
- **Verification**: Licensing status can be verified cryptographically

## Troubleshooting

### "ERROR: Secret key is required"

Ensure you've set the secret key via `--secret` flag or `WATERMARK_SECRET` environment variable.

### "ERROR: Input file not found"

Verify the input file path is correct and the file exists.

### "Signature verification failed"

This indicates:
- Wrong secret key used for verification
- Watermark has been tampered with
- File corruption

### "No watermark found in binary file"

The binary file does not contain a watermark. Ensure you're verifying a watermarked binary.

## Advanced Usage

### Batch Processing

Create a script to watermark multiple files:

```bash
#!/bin/bash
export WATERMARK_SECRET="your-secret-key"

for file in input/*.bin; do
    basename=$(basename "$file")
    python scripts/create_watermarked_binary.py \
        --input "$file" \
        --output "output/licensed_${basename}" \
        --license-id "LICENSE-2026-001" \
        --user-info "Your Organization"
done
```

### Automated Verification

Verify multiple files and collect results:

```bash
#!/bin/bash
export WATERMARK_SECRET="your-secret-key"

for file in *.bin; do
    echo "Verifying: $file"
    python scripts/verify_watermark.py \
        --input "$file" \
        --json >> verification_results.json
done
```

## Documentation

For complete documentation, see:
- `docs/WATERMARK_DOCUMENTATION.md` - Comprehensive watermarking guide
- `COMMERCIAL_LICENSE.md` - Commercial licensing terms
- `test_watermark.py` - Test suite with usage examples

## Support

For licensing inquiries or technical support, refer to the main repository documentation.
