# Entropy Validation with μ = e^{i·3π/4} Rotation

This directory contains a comprehensive test suite that validates claims about floating-point E overflow as a cryptographic entropy source, with modifications to use **μ = e^{i·3π/4}** as the center of rotation.

## Overview

The original entropy validation tests (`validate_entropy_source.py`) use standard π/4 stepping around the unit circle. This modified test suite (`validate_entropy_source_mu_rotation.py`) uses **μ = e^{i·3π/4}** as the rotation center to determine if this mathematical transformation affects:

- Determinism and reproducibility
- Predictability and attack resistance
- Entropy quality and cryptographic suitability
- Alignment with NIST SP 800-90B standards

## Test Categories

The test suite includes 6 comprehensive test categories:

### 1. Predictability/Determinism Tests (4 tests)
- Validates that E overflow is completely deterministic
- Tests bit-level reproducibility
- Verifies perfect prediction from input angles
- Confirms mathematical formula consistency

### 2. Known-Answer Tests (KAT) / Cross-Platform Precision (3 tests)
- Tests against known E overflow values
- Validates cross-platform consistency
- Documents platform metadata
- Verifies IEEE 754 compliance

### 3. Min-Entropy Estimation (NIST SP 800-90B) (4 tests)
- Measures uniqueness ratios
- Estimates entropy via compression
- Calculates min-entropy using frequency analysis
- Simulates NIST SP 800-90B assessment

### 4. Seeded Prediction Attack (2 tests)
- Tests perfect prediction from observed values
- Validates angle recovery from E patterns
- Demonstrates state information leakage

### 5. Statistical Randomness Tests (3 tests)
- Chi-square test for uniform distribution
- Runs test for bit independence
- Serial correlation analysis

### 6. Physics-Based Validation (ZPE Claim Impact) (4 tests)
- Environmental independence testing
- E magnitude consistency with machine epsilon
- Scaling behavior analysis
- Physical interpretation of μ rotation

## Running the Tests

### Run μ Rotation Tests Only

```bash
# Run all μ rotation tests
python -m unittest tests.validate_entropy_source_mu_rotation -v

# Run specific test category
python -m unittest tests.validate_entropy_source_mu_rotation.TestDeterminismAndReproducibility -v
python -m unittest tests.validate_entropy_source_mu_rotation.TestMinEntropyEstimation -v
```

### Run Comparison Tests

The comparison script runs both standard and μ rotation tests, then generates a comprehensive comparison report:

```bash
# Run comparison and display report
python scripts/compare_entropy_tests.py

# Run comparison and save report to file
python scripts/compare_entropy_tests.py --output docs/ENTROPY_COMPARISON_MU_ROTATION.md

# Run with verbose output (shows all test details)
python scripts/compare_entropy_tests.py --verbose
```

## Test Results Summary

### All Tests Pass: 23/23 ✅

The μ rotation test suite successfully demonstrates that:

✅ **E overflow is deterministic** (100% reproducible)  
✅ **E overflow is perfectly predictable** (100% prediction accuracy)  
✅ **E overflow has low min-entropy** (0.72 bits, far below cryptographic requirements)  
✅ **E overflow is highly compressible** (17.88% compression ratio)  
✅ **E overflow fails statistical randomness tests** (non-uniform distribution)  
✅ **E overflow is IEEE 754 rounding error** (magnitude O(ε), not quantum phenomena)

### Key Finding

**Changing the rotation center to μ = e^{i·3π/4} does NOT alter the fundamental criticisms raised against E overflow as a cryptographic entropy source.**

The μ rotation is a mathematical transformation that:
- Changes the specific E overflow values produced
- Does NOT introduce randomness or unpredictability
- Does NOT improve entropy quality
- Does NOT make E overflow suitable for cryptographic use

## Comparison Report

The comprehensive comparison report is available at:
- **File:** `docs/ENTROPY_COMPARISON_MU_ROTATION.md`
- **Generated:** 2026-01-05

### Key Comparisons

| Category | Standard Rotation | μ Rotation | Change? |
|----------|------------------|------------|---------|
| Determinism | PASS (100%) | PASS (100%) | ❌ No |
| Predictability | 100% accurate | 100% accurate | ❌ No |
| Min-Entropy | Low (<20 bits) | Low (0.72 bits) | ❌ No |
| Statistical Randomness | FAIL | FAIL | ❌ No |
| Cryptographic Suitability | ❌ FAIL | ❌ FAIL | ❌ No |

## Mathematical Background

### Standard Rotation
```
position = e^{i·start_angle}
for each step:
    position *= e^{i·π/4}
```

After 8 steps of π/4, the position should return to the starting point (modulo 2π), but IEEE 754 rounding errors accumulate.

### μ Rotation
```
μ = e^{i·3π/4} ≈ -0.707107 + 0.707107i
position = μ · e^{i·start_angle}
for each step:
    position *= e^{i·π/4}
```

The μ rotation shifts the starting position by 135° in the complex plane. This is equivalent to a change of reference frame, but does not alter the accumulation of IEEE 754 rounding errors.

### Why μ Doesn't Help

1. **Still Deterministic**: The μ rotation is a deterministic transformation. For any given starting angle, the E overflow is perfectly predictable.

2. **Same Error Source**: Both methods accumulate IEEE 754 rounding errors from complex multiplication. The magnitude remains O(ε).

3. **No Randomness Added**: Changing the rotation center is a mathematical operation that does not introduce genuine randomness or quantum effects.

4. **Patterns Remain**: Both methods produce highly compressible outputs with detectable patterns.

## Detailed Test Output

### Sample Output from μ Rotation Tests

```
Min-entropy with μ rotation: 0.72 bits
Most common E value appears 6086/10000 times (60.9%)

Compression ratio with μ rotation: 0.1788
Original size: 80000 bytes
Compressed size: 14307 bytes
WARNING: High compressibility indicates low entropy

Uniqueness ratio with μ rotation: 0.1310 (131/1000)
WARNING: Low uniqueness suggests E is not a good entropy source

Prediction success rate with μ rotation: 100% (90/90 predictions correct)

Chi-square test with μ rotation:
  Chi-square value: 837.42
  Critical value (α=0.05): ~293
  Result: Non-uniform distribution detected
```

## Conclusions

### Answer to Research Question

**Does using μ = e^{i·3π/4} as the center of rotation alter the fundamental criticisms raised against the entropy source?**

**Answer: NO**

The μ rotation:
- ❌ Does NOT introduce genuine entropy
- ❌ Does NOT prevent perfect prediction
- ❌ Does NOT improve cryptographic suitability
- ❌ Does NOT represent quantum phenomena
- ❌ Does NOT change the fundamental nature of IEEE 754 rounding errors

### Recommendation

**Neither standard rotation nor μ rotation should be used as a source of cryptographic entropy.**

For cryptographic applications, use:
- Hardware Random Number Generators (HRNG/TRNG)
- Operating system entropy pools (/dev/urandom, CryptGenRandom)
- NIST-approved DRBGs seeded from hardware entropy

## File Structure

```
tests/
├── validate_entropy_source.py              # Original tests (standard rotation)
├── validate_entropy_source_mu_rotation.py  # Modified tests (μ rotation)
├── README_MU_ROTATION.md                   # This file
└── quantum_seed_test_vectors_sample.json   # Test vectors

scripts/
└── compare_entropy_tests.py                # Comparison script

docs/
└── ENTROPY_COMPARISON_MU_ROTATION.md       # Comparison report
```

## References

- NIST SP 800-90B: Recommendation for the Entropy Sources Used for Random Bit Generation
- IEEE 754-2008: Standard for Floating-Point Arithmetic
- NIST SP 800-22: A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications

## Authors

Test suite developed for validation of cryptographic entropy source claims.

## License

GPL-3.0-or-later (same as parent repository)
