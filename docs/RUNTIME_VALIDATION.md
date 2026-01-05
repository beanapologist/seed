# Runtime Validation for Cryptographic Operations

This document provides comprehensive documentation for the runtime validation system that monitors and validates cryptographic operations during live deployments.

## Overview

The runtime validation system provides real-time monitoring and logging of cryptographic operations including:

- **Random Number Generation (RNG)**: Monitors the generation of random numbers from the Universal QKD generator
- **Cryptographic Key Exchanges**: Monitors hybrid key generation for NIST PQC algorithms
- **Entropy Quality Metrics**: Real-time entropy analysis and validation
- **Security Compliance**: Zero-bias checks and cryptographic integrity validation

## Architecture

```
┌─────────────────────────────────────┐
│   Cryptographic Operations          │
│   (Universal QKD, NIST PQC)         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Runtime Monitor                   │
│   - Operation Logging               │
│   - Entropy Analysis                │
│   - Bias Detection                  │
│   - Checksum Validation             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Output & Reporting                │
│   - JSON Log Files                  │
│   - Console Output                  │
│   - CI/CD Integration               │
└─────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Golden Quantum package installed (`pip install -e .`)

### Setup

The runtime validation script is located at `scripts/runtime_validation.py` and is ready to use after package installation:

```bash
# Install the package
cd /path/to/seed
pip install -e .

# Make script executable (on Unix-like systems)
chmod +x scripts/runtime_validation.py
```

## Usage

### Basic Usage

Run a single validation cycle with default parameters:

```bash
python scripts/runtime_validation.py
```

This will:
- Monitor 10 random number generations
- Monitor 5 key exchange operations
- Save results to `runtime_validation_log.json`

### Monitor for Specific Duration

Monitor operations for a specific time period:

```bash
# Monitor for 60 seconds
python scripts/runtime_validation.py --monitor-duration 60

# Monitor for 5 minutes
python scripts/runtime_validation.py --monitor-duration 300
```

### Continuous Monitoring

Run in continuous monitoring mode (useful for production deployments):

```bash
python scripts/runtime_validation.py --continuous
```

Press `Ctrl+C` to stop monitoring. All logs will be saved before exit.

### Custom Parameters

Customize the number of operations monitored:

```bash
python scripts/runtime_validation.py \
  --rng-count 50 \
  --kex-count 20 \
  --output custom_validation.json
```

### Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--monitor-duration <seconds>` | None | Duration in seconds to monitor operations |
| `--output <file>` | `runtime_validation_log.json` | Output file for validation logs |
| `--continuous` | False | Run in continuous monitoring mode |
| `--rng-count <n>` | 10 | Number of RNG operations to monitor per cycle |
| `--kex-count <n>` | 5 | Number of key exchange operations to monitor per cycle |

## Output Format

### Console Output

The script provides real-time console output:

```
============================================================
Cryptographic Runtime Validation Monitor
============================================================
Start Time: 2026-01-05T02:30:00.000000Z
Output File: runtime_validation_log.json
============================================================

============================================================
Monitoring Random Number Generation (10 operations)
============================================================

[2026-01-05T02:30:01.234567Z] random_number_generation: {
  "operation_id": 1,
  "key_hex": "3c732e0d04dac163a5cc2b15c7caf42c",
  "key_length_bytes": 16,
  "entropy_bits_per_byte": 4.8125,
  "has_bias": false,
  "sha256_checksum": "abc123...",
  "duration_seconds": 0.001234
}
...
```

### JSON Log File

Results are saved in structured JSON format:

```json
{
  "start_time": "2026-01-05T02:30:00.000000Z",
  "end_time": "2026-01-05T02:31:00.000000Z",
  "total_operations": 15,
  "operations": [
    {
      "timestamp": "2026-01-05T02:30:01.234567Z",
      "type": "random_number_generation",
      "details": {
        "operation_id": 1,
        "key_hex": "3c732e0d04dac163a5cc2b15c7caf42c",
        "key_length_bytes": 16,
        "entropy_bits_per_byte": 4.8125,
        "has_bias": false,
        "sha256_checksum": "...",
        "duration_seconds": 0.001234
      }
    },
    {
      "timestamp": "2026-01-05T02:30:02.345678Z",
      "type": "key_exchange",
      "details": {
        "operation_id": 1,
        "algorithm": "Kyber-768",
        "deterministic_key": {
          "hex": "...",
          "length_bytes": 16,
          "entropy_bits_per_byte": 4.5,
          "has_bias": false,
          "sha256": "..."
        },
        "pqc_seed": {
          "length_bytes": 32,
          "entropy_bits_per_byte": 5.2,
          "has_bias": false,
          "sha256": "..."
        },
        "duration_seconds": 0.002345
      }
    }
  ]
}
```

## Monitored Metrics

### Random Number Generation

For each RNG operation, the following metrics are captured:

- **Operation ID**: Sequential identifier
- **Key Value**: Hex representation of generated key
- **Key Length**: Size in bytes
- **Entropy**: Shannon entropy in bits per byte
- **Bias Check**: Detection of zero-bias patterns
- **Checksum**: SHA-256 integrity hash
- **Duration**: Operation execution time

### Key Exchange Operations

For each key exchange, both components are monitored:

#### Deterministic Key Component
- Key value (hex)
- Length in bytes
- Entropy score
- Bias detection
- SHA-256 checksum

#### PQC Seed Component
- Length in bytes (algorithm-specific)
- Entropy score
- Bias detection
- SHA-256 checksum

### Aggregate Statistics

Summary statistics are computed:

- **Total Operations**: Count of monitored operations
- **Average Entropy**: Mean entropy across all operations
- **Min/Max Entropy**: Range of entropy values
- **Bias Status**: Whether all operations are bias-free

## Integration with CI/CD

### GitHub Actions Integration

The runtime validation is integrated into the CI/CD pipeline via the `.github/workflows/runtime-validation.yml` workflow.

The workflow automatically:
1. Runs validation tests on every push
2. Monitors 20 RNG operations and 10 key exchanges
3. Saves results as artifacts
4. Fails if validation detects issues

### Manual Workflow Trigger

You can manually trigger the workflow:

1. Go to the "Actions" tab on GitHub
2. Select "Runtime Validation and Entropy Testing"
3. Click "Run workflow"

### Viewing Results

Test artifacts are available for 30 days:

1. Go to the workflow run
2. Scroll to "Artifacts" section
3. Download `runtime-validation-results`

## Interpreting Results

### Success Criteria

A successful validation should show:

- ✅ **Entropy > 3.0 bits/byte**: Indicates good randomness for deterministic keys
- ✅ **Entropy > 7.0 bits/byte**: Excellent randomness for aggregate data
- ✅ **No Bias Detected**: All zero-bias checks pass
- ✅ **Consistent Performance**: Operation durations are stable

### Warning Signs

Watch for these indicators:

- ⚠️ **Low Entropy**: Values below 3.0 bits/byte
- ⚠️ **Bias Detected**: Zero-bias checks fail
- ⚠️ **High Variance**: Inconsistent entropy across operations
- ⚠️ **Slow Operations**: Significantly increased duration

### Failure Conditions

Validation fails if:

- ❌ Entropy drops below threshold
- ❌ Systematic bias is detected
- ❌ Checksum validation fails
- ❌ Operations time out or crash

## Local Testing

### Quick Validation

Perform a quick validation check:

```bash
python scripts/runtime_validation.py --rng-count 5 --kex-count 3
```

### Extended Testing

Run extended testing for thorough validation:

```bash
python scripts/runtime_validation.py \
  --rng-count 100 \
  --kex-count 50 \
  --output extended_validation.json
```

### Production Monitoring

Deploy continuous monitoring in production:

```bash
# Run in background with logging
nohup python scripts/runtime_validation.py --continuous \
  --output /var/log/crypto_validation.json > /var/log/crypto_monitor.log 2>&1 &
```

## Troubleshooting

### Issue: Import Errors

**Problem**: Cannot import `gq` modules

**Solution**: Ensure the package is installed:
```bash
pip install -e .
```

### Issue: Low Entropy Warnings

**Problem**: Entropy scores below expected thresholds

**Solution**: 
- Individual deterministic keys may have lower entropy (3-5 bits/byte is acceptable)
- Aggregate entropy should be high (>7 bits/byte)
- Check that sufficient operations are being monitored

### Issue: Performance Degradation

**Problem**: Operations take longer than expected

**Solution**:
- Check system resources
- Reduce operation count for testing
- Verify no other processes interfere with timing

## Security Considerations

### Data Sensitivity

- Generated keys are logged in hex format
- Production deployments should secure log files
- Consider implementing log rotation and encryption

### Access Control

- Restrict access to validation logs
- Use appropriate file permissions (e.g., 600 for logs)
- Implement audit trails for log access

### Compliance

The runtime validation system helps ensure:

- **NIST SP 800-22 Compliance**: Statistical randomness tests
- **Zero-Bias Requirements**: Detection of systematic biases
- **Entropy Thresholds**: Meeting cryptographic standards
- **Auditability**: Complete operation logs for review

## API Reference

### CryptoOperationMonitor Class

```python
from scripts.runtime_validation import CryptoOperationMonitor

# Initialize monitor
monitor = CryptoOperationMonitor(output_file='my_log.json')

# Monitor RNG operations
rng_stats = monitor.monitor_random_generation(count=10)

# Monitor key exchanges
kex_stats = monitor.monitor_key_exchange(count=5)

# Save results
monitor.save_log()
```

### Methods

#### `monitor_random_generation(count: int) -> Dict[str, Any]`

Monitor random number generation operations.

**Parameters:**
- `count`: Number of operations to monitor

**Returns:**
- Dictionary with statistics (total_operations, average_entropy, etc.)

#### `monitor_key_exchange(count: int) -> Dict[str, Any]`

Monitor cryptographic key exchange operations.

**Parameters:**
- `count`: Number of exchanges to monitor

**Returns:**
- Dictionary with exchange statistics

#### `save_log()`

Save the complete operation log to the output file.

## Best Practices

### Development

- Run validation after code changes
- Monitor at least 10 operations for meaningful statistics
- Review logs for unexpected patterns

### Testing

- Use runtime validation in pre-production testing
- Compare results across different environments
- Validate against baseline metrics

### Production

- Enable continuous monitoring
- Set up alerting for validation failures
- Regularly review aggregate statistics
- Implement log rotation and retention policies

## Related Documentation

- [Entropy Testing Guide](ENTROPY_TESTING.md)
- [Dieharder Integration](DIEHARDER_TESTING.md)
- [NIST PQC Integration](../examples/nist_pqc_integration.md)
- [Security Policy](../SECURITY.md)

## Support

For issues or questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Review [existing issues](https://github.com/beanapologist/seed/issues)
3. Open a new issue with validation logs attached

## License

This validation system is part of the Golden Quantum project and is licensed under GPL-3.0-or-later.
