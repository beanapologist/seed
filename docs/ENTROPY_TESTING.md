# Entropy Testing Documentation

## Overview

This directory contains comprehensive entropy testing infrastructure for validating the cryptographic quality of all random number and key generation mechanisms in the project.

## Components

### 1. Core Module: `src/gq/entropy_testing.py`

The entropy testing module provides statistical analysis tools implementing tests from NIST SP 800-22 and other cryptographic standards.

**Key Classes:**
- `EntropyAnalyzer`: Performs comprehensive statistical analysis on binary data

**Key Functions:**
- `analyze_key_stream()`: Analyzes entropy across multiple keys
- `validate_zero_bias()`: Detects systematic biases in key material

### 2. Test Suite: `test_entropy.py`

Comprehensive test suite with 34+ tests covering:
- Statistical test validation
- Universal QKD entropy testing
- NIST PQC hybrid key generation entropy
- Zero-bias validation
- Integration tests across all algorithms

### 3. Analysis Script: `scripts/generate_entropy_report.py`

Automated script that generates detailed entropy analysis reports for all cryptographic mechanisms.

### 4. Documentation: `docs/ENTROPY_ANALYSIS.md`

Comprehensive entropy analysis report with:
- Detailed test results for all algorithms
- Statistical test outcomes
- Recommendations and compliance status

## Statistical Tests Implemented

### 1. Shannon Entropy Analysis
Measures information content per byte (0-8 bits/byte)
- **Target**: > 7.0 for large samples, > 4.0 for small deterministic keys

### 2. Monobit Frequency Test (NIST SP 800-22)
Tests proportion of 0s and 1s
- **Pass Criteria**: Balance < 0.05

### 3. Runs Test
Tests independence of consecutive bits
- **Pass Criteria**: Runs ratio between 0.9 and 1.1

### 4. Serial Correlation Test
Tests for patterns between consecutive bytes
- **Pass Criteria**: |correlation| < 0.1

### 5. Chi-Square Test
Tests uniformity of byte distribution
- **Pass Criteria**: Chi-square statistic < critical value

### 6. Zero-Bias Validation
Detects systematic biases:
- Leading/trailing zeros
- Repeated patterns
- Low byte diversity

## Usage

### Running All Entropy Tests

```bash
# Run comprehensive entropy test suite
python -m unittest test_entropy

# Run specific test class
python -m unittest test_entropy.TestEntropyAnalyzer
python -m unittest test_entropy.TestUniversalQKDEntropy
python -m unittest test_entropy.TestNISTPQCEntropy
```

### Generating Entropy Report

```bash
# Generate comprehensive entropy analysis report
python scripts/generate_entropy_report.py

# Report saved to docs/ENTROPY_ANALYSIS.md
```

### Using Entropy Testing in Code

```python
from gq.entropy_testing import EntropyAnalyzer, validate_zero_bias

# Analyze single key or seed
key = b'\x3c\x73\x2e\x0d...'  # Your key material
analyzer = EntropyAnalyzer(key)

# Get comprehensive analysis
results = analyzer.comprehensive_analysis()
print(f"Shannon Entropy: {results['shannon_entropy']:.2f} bits/byte")
print(f"Overall Quality: {results['overall_quality']}")
print(f"Passes All Tests: {results['passes_all_tests']}")

# Check for bias
bias_result = validate_zero_bias(key)
if bias_result['has_bias']:
    print(f"Warning: Bias detected - {bias_result['bias_types']}")
```

### Analyzing Key Streams

```python
from gq.entropy_testing import analyze_key_stream
from gq.universal_qkd import universal_qkd_generator

# Generate multiple keys
generator = universal_qkd_generator()
keys = [next(generator) for _ in range(100)]

# Analyze the stream
results = analyze_key_stream(keys)
print(f"Aggregate Shannon Entropy: {results['aggregate_analysis']['shannon_entropy']:.2f}")
print(f"Average Per-Key Entropy: {results['per_key_statistics']['average_entropy']:.2f}")
```

## Integration with Existing Tests

Entropy validation has been integrated into existing test suites:

### Universal QKD Tests (`test_universal_qkd.py`)
- Added `test_key_entropy_and_bias()` method
- Validates entropy and bias on generated keys
- Runs automatically with test suite

### NIST PQC Tests (`test_nist_pqc.py`)
- Enhanced existing tests with bias validation
- All hybrid key generation tests now check for zero-bias
- Validates both deterministic keys and PQC seeds

## Continuous Monitoring

Entropy tests run automatically as part of the CI/CD pipeline:

```bash
# All tests including entropy checks
python -m unittest discover

# Entropy tests pass/fail based on NIST thresholds
# Any degradation triggers build failure
```

## Test Results Summary

All cryptographic mechanisms pass entropy requirements:

✅ **Universal QKD (GCP-1)**
- Shannon Entropy: 7.99 bits/byte (aggregate)
- All statistical tests: PASS
- Zero bias: PASS

✅ **NIST PQC Algorithms**
- All algorithms (Kyber, Dilithium, SPHINCS+): PASS
- Entropy quality: EXCELLENT
- Zero bias: PASS

✅ **Compliance Status**
- NIST SP 800-22: PASSED
- Zero-bias requirements: MET
- Distribution uniformity: PASSED

## Thresholds and Pass Criteria

### Shannon Entropy
- Large samples (>1KB): > 7.0 bits/byte
- Small deterministic keys: > 3.0 bits/byte
- Aggregate streams: > 7.5 bits/byte

### Monobit Frequency
- Balance from 0.5: < 0.05
- Acceptable range: 0.45 - 0.55

### Runs Test
- Ratio to expected: 0.9 - 1.1
- Detects non-random patterns

### Serial Correlation
- Absolute correlation: < 0.1
- Detects sequential dependencies

### Chi-Square
- Statistic < critical value (depends on sample size)
- Tests distribution uniformity

### Zero-Bias
- No leading/trailing zeros (4+ bytes)
- No repeated patterns (8+ identical bytes)
- Byte diversity > 30%

## Troubleshooting

### Low Entropy Warning

If entropy tests fail, check:
1. Sample size - small samples naturally have lower entropy
2. Deterministic vs. random - deterministic keys expected to have lower per-key entropy
3. Aggregate analysis - combine multiple keys for better assessment

### Bias Detection

If bias is detected:
1. Review key generation algorithm
2. Check for systematic patterns
3. Ensure proper mixing of entropy sources
4. Verify initialization vectors are not constant

### Test Failures

Common causes:
1. Insufficient sample size
2. Incorrect threshold expectations
3. Platform-specific randomness issues

## References

- NIST SP 800-22: Statistical Test Suite for Random Number Generators
- NIST FIPS 203: ML-KEM (Kyber)
- NIST FIPS 204: ML-DSA (Dilithium)
- NIST FIPS 205: SLH-DSA (SPHINCS+)

## Future Enhancements

Planned improvements:
1. Integration with Dieharder test suite
2. Real-time entropy monitoring for production systems
3. Entropy pool mixing recommendations
4. Extended NIST SP 800-90B compliance testing

## Contact

For questions about entropy testing:
- Review `docs/ENTROPY_ANALYSIS.md` for detailed results
- Check test suite for implementation examples
- See `SECURITY.md` for security policy

---

*Last Updated: 2026-01-05*
*Entropy testing infrastructure v1.0*
