# Dieharder Entropy Testing Integration

This document provides comprehensive documentation for the Dieharder statistical testing integration used to validate the cryptographic quality of random number generators in the Golden Quantum project.

## Overview

Dieharder is a comprehensive random number testing suite developed by Robert G. Brown at Duke University. It includes tests from:

- **DIEHARD**: Original test battery by George Marsaglia
- **NIST STS**: Statistical Test Suite from NIST SP 800-22
- **Additional Tests**: Extended tests for modern RNG validation

Our integration pipes random data from cryptographic generators directly into Dieharder for rigorous statistical validation.

## What is Dieharder?

Dieharder is the gold standard for testing random number generators. It performs extensive statistical tests to detect:

- **Non-randomness**: Patterns or structure in supposedly random data
- **Bias**: Systematic preference for certain values
- **Correlation**: Dependencies between sequential values
- **Distribution Issues**: Deviation from expected uniform distribution

### Why Dieharder?

- ✅ **Industry Standard**: Widely recognized in cryptography and statistics
- ✅ **Comprehensive**: Over 30 different statistical tests
- ✅ **Rigorous**: Detects subtle weaknesses missed by simpler tests
- ✅ **Published**: Based on peer-reviewed statistical methodology
- ✅ **Active**: Maintained and updated regularly

## Installation

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install dieharder
```

### Fedora/RHEL/CentOS

```bash
sudo dnf install dieharder
# or
sudo yum install dieharder
```

### macOS

```bash
brew install dieharder
```

### Verify Installation

```bash
dieharder -h
```

You should see the Dieharder help message.

## Quick Start

### Test Universal QKD Generator

```bash
python scripts/dieharder_test.py \
  --generator universal_qkd \
  --tests sts_monobit \
  --size 5MB \
  --output results.txt
```

### Test NIST PQC Generator

```bash
python scripts/dieharder_test.py \
  --generator nist_pqc \
  --algorithm kyber768 \
  --tests all \
  --size 10MB \
  --output kyber_results.txt
```

### Run Full Test Suite

```bash
python scripts/dieharder_test.py \
  --generator universal_qkd \
  --tests all \
  --size 50MB \
  --output comprehensive_results.txt
```

### Test Data Generation Only (No Dieharder Required)

```bash
# Useful for development/testing without Dieharder installed
python scripts/dieharder_test.py \
  --generate-only \
  --size 5MB
```


## Usage Guide

### Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--generator` | `universal_qkd` | Generator to test: `universal_qkd` or `nist_pqc` |
| `--algorithm` | `kyber768` | PQC algorithm (for nist_pqc generator) |
| `--tests` | `all` | Test suite to run (see Available Tests) |
| `--size` | `10MB` | Amount of data to generate (e.g., 5MB, 100MB, 1GB) |
| `--output` | `dieharder_results.txt` | Output file for test results |
| `--quiet` | False | Suppress verbose output |
| `--generate-only` | False | Only generate and validate data without running Dieharder (useful for testing) |

### Available Generators

#### universal_qkd
Tests the Universal QKD (GCP-1) deterministic key generator.

```bash
python scripts/dieharder_test.py --generator universal_qkd
```

#### nist_pqc
Tests NIST PQC hybrid key generators with available algorithms:

- `kyber512`: CRYSTALS-Kyber-512 (Security Level 1)
- `kyber768`: CRYSTALS-Kyber-768 (Security Level 3)
- `kyber1024`: CRYSTALS-Kyber-1024 (Security Level 5)
- `dilithium2`: CRYSTALS-Dilithium2 (Security Level 2)
- `dilithium3`: CRYSTALS-Dilithium3 (Security Level 3)
- `dilithium5`: CRYSTALS-Dilithium5 (Security Level 5)
- `sphincs_plus_128f`: SPHINCS+-128f (Security Level 1)

```bash
python scripts/dieharder_test.py \
  --generator nist_pqc \
  --algorithm dilithium3
```

### Available Tests

#### Full Test Suite

```bash
--tests all  # Runs all available tests (comprehensive, time-consuming)
```

#### Individual Tests

| Test Name | ID | Description |
|-----------|----|----|
| `birthdays` | 0 | Birthday spacing test |
| `operm5` | 1 | Overlapping permutations test |
| `rank_32x32` | 2 | Binary rank test for 32x32 matrices |
| `rank_6x8` | 3 | Binary rank test for 6x8 matrices |
| `bitstream` | 4 | Bitstream test |
| `opso` | 5 | Overlapping-pairs-sparse-occupancy test |
| `oqso` | 6 | Overlapping-quadruples-sparse-occupancy test |
| `dna` | 7 | DNA test |
| `count_1s_stream` | 8 | Count the 1s in a stream of bytes |
| `count_1s_byte` | 9 | Count the 1s in specific bytes |
| `parking_lot` | 10 | Parking lot test |
| `minimum_distance` | 11 | Minimum distance test |
| `random_spheres` | 12 | Random spheres test |
| `squeeze` | 13 | Squeeze test |
| `sums` | 14 | Sums test |
| `runs` | 15 | Runs test |
| `craps` | 16 | Craps test |
| `sts_monobit` | 100 | NIST STS monobit test |
| `sts_runs` | 101 | NIST STS runs test |
| `sts_serial` | 102 | NIST STS serial test |

#### Recommended Quick Tests

For quick validation (5-10 minutes):

```bash
python scripts/dieharder_test.py \
  --tests sts_monobit \
  --size 5MB
```

For thorough validation (30-60 minutes):

```bash
python scripts/dieharder_test.py \
  --tests all \
  --size 50MB
```

### Data Size Guidelines

| Purpose | Recommended Size | Duration |
|---------|------------------|----------|
| Quick check | 5-10 MB | 5-10 min |
| Standard test | 10-50 MB | 15-30 min |
| Comprehensive | 50-100 MB | 30-60 min |
| Rigorous | 100MB-1GB | 1-4 hours |

**Note**: Larger data sizes provide more statistical power but take longer to generate and test.

### Testing Without Dieharder (Generate-Only Mode)

For development and testing environments where Dieharder is not installed, you can use the `--generate-only` flag to test data generation without running statistical tests:

```bash
# Test Universal QKD data generation
python scripts/dieharder_test.py --generate-only --size 1MB

# Test NIST PQC data generation
python scripts/dieharder_test.py \
  --generate-only \
  --generator nist_pqc \
  --algorithm kyber768 \
  --size 2MB
```

This mode:
- ✅ Validates that data generation works correctly
- ✅ Verifies the correct amount of data is generated
- ✅ Does not require Dieharder installation
- ✅ Useful for CI/CD testing and development
- ✅ Fast feedback on generator functionality

## Understanding Results

### Result Categories

Dieharder reports results in three categories:

#### ✅ PASSED
The generator passed the test with good p-values. This indicates the data appears random with high confidence.

#### ⚠️ WEAK
The test showed borderline results. This doesn't necessarily indicate a failure but warrants investigation. A few weak results in a large test suite are acceptable.

#### ❌ FAILED
The test detected significant non-randomness. This is a serious issue that requires investigation.

### P-Values

Dieharder reports p-values for most tests:

- **p-value near 0.5**: Ideal, indicates perfect randomness
- **0.01 < p < 0.99**: Acceptable range
- **p < 0.01 or p > 0.99**: Suspicious, may indicate issues
- **p near 0 or 1**: Strong evidence of non-randomness

### Example Output

```
#=============================================================================#
#            dieharder version 3.31.1 Copyright 2003 Robert G. Brown          #
#=============================================================================#
   rng_name    |           filename             |rands/second|
        mt19937|                       stdin_input_raw|  1.00e+08  |
#=============================================================================#
        test_name   |ntup| tsamples |psamples|  p-value |Assessment
#=============================================================================#
   diehard_birthdays|   0|       100|     100|0.52634781|  PASSED
      diehard_operm5|   0|   1000000|     100|0.91681180|  PASSED
  diehard_rank_32x32|   0|     40000|     100|0.48265103|  PASSED
    diehard_rank_6x8|   0|    100000|     100|0.93458321|  PASSED
      diehard_opso|   0|   2097152|     100|0.01234567|  WEAK
      diehard_oqso|   0|   2097152|     100|0.78901234|  PASSED
```

### Interpreting Summary

After tests complete, a summary is displayed:

```
============================================================
Test Summary
============================================================
Total Tests: 15
Passed: 13
Weak: 2
Failed: 0
============================================================
```

**Guidelines:**
- **All Passed**: Excellent! Generator meets statistical standards
- **Few Weak (1-3)**: Acceptable for most purposes
- **Many Weak (>3)**: Investigate further or increase data size
- **Any Failed**: Serious concern, requires immediate investigation

## CI/CD Integration

### GitHub Actions Workflow

The Dieharder tests are integrated into our CI/CD pipeline at `.github/workflows/runtime-validation.yml`.

#### Automated Testing

On every push and pull request:
1. **Quick Tests**: Run NIST STS monobit test on multiple generators
2. **Matrix Testing**: Test Universal QKD, Kyber-768, and Dilithium3
3. **Result Storage**: Save results as artifacts (30-day retention)

#### Scheduled Comprehensive Testing

Daily at 2 AM UTC on main branch:
1. **Full Test Suite**: Run all Dieharder tests
2. **Large Data Set**: 50MB of random data
3. **Extended Storage**: Results kept for 90 days

### Manual Trigger

To run tests manually:

1. Go to GitHub Actions tab
2. Select "Runtime Validation and Entropy Testing"
3. Click "Run workflow"
4. Select branch and confirm

### Viewing CI Results

1. Navigate to the workflow run
2. Check job status for each generator
3. Download artifacts for detailed results
4. Review summary in job logs

## Local Testing Examples

### Example 1: Quick Validation

Test basic randomness quickly:

```bash
python scripts/dieharder_test.py \
  --generator universal_qkd \
  --tests sts_monobit \
  --size 5MB
```

Expected time: ~5 minutes

### Example 2: Algorithm Comparison

Test different PQC algorithms:

```bash
# Test Kyber-768
python scripts/dieharder_test.py \
  --generator nist_pqc \
  --algorithm kyber768 \
  --tests runs \
  --size 10MB \
  --output kyber768_runs.txt

# Test Dilithium3
python scripts/dieharder_test.py \
  --generator nist_pqc \
  --algorithm dilithium3 \
  --tests runs \
  --size 10MB \
  --output dilithium3_runs.txt
```

### Example 3: Comprehensive Testing

Run full test suite for thorough validation:

```bash
python scripts/dieharder_test.py \
  --generator universal_qkd \
  --tests all \
  --size 100MB \
  --output comprehensive_results.txt
```

Expected time: ~2 hours

### Example 4: Batch Testing

Test multiple algorithms in sequence:

```bash
for algo in kyber512 kyber768 kyber1024 dilithium2 dilithium3; do
  echo "Testing $algo..."
  python scripts/dieharder_test.py \
    --generator nist_pqc \
    --algorithm $algo \
    --tests sts_monobit \
    --size 10MB \
    --output results_${algo}.txt
done
```

## Troubleshooting

### Issue: Dieharder Not Found

**Problem:**
```
ERROR: Dieharder is not installed.
```

**Solution:**
Install Dieharder using your package manager (see [Installation](#installation)).

### Issue: Tests Take Too Long

**Problem:** Tests running for hours without completing

**Solution:**
- Reduce data size: `--size 10MB` instead of `--size 100MB`
- Run specific tests instead of `all`
- Use faster tests like `sts_monobit` for quick checks

### Issue: All Tests Show WEAK or FAILED

**Problem:** Most or all tests fail

**Solution:**
1. Verify package installation: `pip install -e .`
2. Check data generation is working: Test with small size first
3. Increase data size for more statistical power
4. Review generator implementation for bugs

### Issue: Inconsistent Results

**Problem:** Results differ between runs

**Solution:**
- This is normal for small data sizes
- Use larger data sets (50MB+) for consistent results
- Statistical tests have inherent variance
- Focus on patterns across multiple runs

### Issue: Memory Issues

**Problem:** Script crashes or system runs out of memory

**Solution:**
- Reduce data size
- Close other applications
- Use systems with at least 4GB RAM for large tests
- Consider running tests in chunks

## Best Practices

### Development Workflow

1. **Quick Test**: Run `sts_monobit` with 5MB after code changes
2. **Pre-Commit**: Run standard tests with 10MB before committing
3. **Pre-Release**: Run comprehensive test suite with 100MB

### Data Size Selection

- **Development**: 5-10 MB for quick feedback
- **CI/CD**: 10-50 MB for balance of speed and rigor
- **Release Validation**: 100MB+ for maximum confidence
- **Academic/Research**: 1GB+ for publication-quality results

### Test Selection

**Quick Validation:**
- `sts_monobit`
- `sts_runs`
- `runs`

**Standard Validation:**
- `birthdays`
- `operm5`
- `rank_32x32`
- `bitstream`
- All STS tests

**Comprehensive Validation:**
- `all` (entire test suite)

### Result Interpretation

1. **Don't Panic**: 1-2 weak results in a large suite are acceptable
2. **Context Matters**: Small data sets are less reliable
3. **Patterns Count**: Consistent failures across tests are concerning
4. **Reproduce**: Run tests multiple times to verify issues
5. **Document**: Save results for comparison over time

## Advanced Usage

### Custom Test Sequences

Create scripts to run specific test combinations:

```bash
#!/bin/bash
# custom_test_suite.sh

tests="sts_monobit sts_runs birthdays rank_32x32"

for test in $tests; do
  echo "Running $test..."
  python scripts/dieharder_test.py \
    --generator universal_qkd \
    --tests $test \
    --size 20MB \
    --output results_${test}.txt
done
```

### Integration with Analysis Tools

Parse results programmatically:

```python
import re

def parse_dieharder_results(filename):
    """Extract test results from Dieharder output."""
    results = {'passed': 0, 'weak': 0, 'failed': 0}
    
    with open(filename, 'r') as f:
        for line in f:
            if 'PASSED' in line:
                results['passed'] += 1
            elif 'WEAK' in line:
                results['weak'] += 1
            elif 'FAILED' in line:
                results['failed'] += 1
    
    return results

# Use it
results = parse_dieharder_results('dieharder_results.txt')
print(f"Passed: {results['passed']}, Weak: {results['weak']}, Failed: {results['failed']}")
```

## Performance Considerations

### Generation Speed

Typical data generation rates:

- Universal QKD: ~1-2 MB/s
- NIST PQC: ~0.5-1 MB/s

### Test Duration

Approximate times for full test suite:

| Data Size | Universal QKD | NIST PQC |
|-----------|---------------|----------|
| 10 MB | ~20 min | ~30 min |
| 50 MB | ~60 min | ~90 min |
| 100 MB | ~2 hours | ~3 hours |

### Resource Usage

- **CPU**: High during testing (single-threaded)
- **Memory**: ~100-500 MB depending on test
- **Disk**: Temporary files created and deleted
- **Network**: None required

## Security Implications

### What Dieharder Tests

✅ **Tests for:**
- Statistical randomness
- Pattern detection
- Distribution uniformity
- Bit independence
- Correlation issues

❌ **Does NOT test for:**
- Cryptographic security directly
- Predictability resistance
- Side-channel attacks
- Implementation vulnerabilities

### Complementary Testing

Dieharder should be used alongside:

- **NIST SP 800-22**: Specialized cryptographic tests (included in our entropy_testing.py)
- **TestU01**: Alternative comprehensive test suite
- **Runtime Validation**: Operational monitoring
- **Code Review**: Security audit of implementation

## References

### Official Documentation

- [Dieharder Documentation](https://webhome.phy.duke.edu/~rgb/General/dieharder.php)
- [NIST SP 800-22](https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final)

### Academic Papers

- Marsaglia, G. (1995). "DIEHARD: A Battery of Tests of Randomness"
- Brown, R.G. (2004). "Dieharder: A Random Number Test Suite"
- Rukhin, A., et al. (2010). "A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications" (NIST SP 800-22)

### Related Documentation

- [Runtime Validation Guide](RUNTIME_VALIDATION.md)
- [Entropy Testing Guide](ENTROPY_TESTING.md)
- [NIST PQC Integration](../examples/nist_pqc_integration.md)

## Support

For issues or questions:

1. Review [troubleshooting section](#troubleshooting)
2. Check [GitHub Issues](https://github.com/beanapologist/seed/issues)
3. Consult [Dieharder documentation](https://webhome.phy.duke.edu/~rgb/General/dieharder.php)
4. Open a new issue with test results attached

## License

This integration is part of the Golden Quantum project and is licensed under GPL-3.0-or-later.
