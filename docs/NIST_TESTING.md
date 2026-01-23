# NIST Testing

This document describes NIST-related testing and validation for GoldenSeed.

## Overview

GoldenSeed is a **deterministic byte stream generator** designed for procedural generation and reproducible simulations. This document addresses NIST testing considerations and the project's relationship with NIST standards.

## Important Disclaimer

⚠️ **GoldenSeed is NOT a cryptographic random number generator**

GoldenSeed does **not** claim compliance with:
- NIST SP 800-90A (Recommendation for Random Number Generation Using Deterministic Random Bit Generators)
- NIST SP 800-90B (Recommendation for the Entropy Sources Used for Random Bit Generation)
- NIST SP 800-90C (Recommendation for Random Bit Generator (RBG) Constructions)

## NIST Statistical Test Suite (STS)

### Historical Context

Previous versions of GoldenSeed included NIST Statistical Test Suite (STS) validation. These tests were removed during the DRBG refactoring as documented in:

- `.github/workflows/nist-sts.yml` (disabled workflow)
- `REFACTORING_SUMMARY.md`

### Current Status

The NIST STS workflow is **disabled** because:

1. **Scope Change**: GoldenSeed focuses on deterministic procedural generation, not cryptographic randomness
2. **Use Case Alignment**: Primary use cases don't require cryptographic-grade entropy
3. **Clear Boundaries**: Explicit non-cryptographic positioning reduces misuse risk

## What GoldenSeed Tests

Instead of cryptographic validation, GoldenSeed focuses on:

### 1. Determinism Validation
```python
# Same seed always produces same output
gen1 = UniversalQKD()
gen2 = UniversalQKD()
assert next(gen1) == next(gen2)  # Always passes
```

### 2. Cross-Platform Consistency
```python
# Identical output across Python, JavaScript, C, C++, Go, Rust, Java
# First chunk hex: 3c732e0d04dac163a5cc2b15c7caf42c
```

### 3. Reference Test Vectors
```python
# Output must match stored test vectors
with open('tests/test_vectors.json') as f:
    reference = json.load(f)
    
generated = generate_universal_keys(10)
assert generated == reference['protocols']['GCP-1']['test_vectors']
```

### 4. Mathematical Correctness
```python
# Golden ratio algorithm verification
# See: .github/workflows/verify-math.yml
```

## Test Coverage

Current test suite includes:

| Test Category | File | Purpose |
|--------------|------|---------|
| Core Functionality | `test_universal_qkd.py` | Basic generator tests |
| Algorithm | `test_gqs1.py` | GQS-1 protocol validation |
| Determinism | `test_cross_platform_determinism.py` | Platform consistency |
| Capacity | `test_compression_capacity.py` | Stream generation capacity |
| Edge Cases | `test_edge_cases.py` | Boundary conditions |
| Golden Ratio | `test_golden_ratio_coin_flip.py` | Mathematical properties |

## Running Tests

```bash
# Install dependencies
pip install -e .
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src/gq --cov-report=term-missing
```

## NIST Post-Quantum Cryptography (PQC)

### Context

The `CHANGELOG.md` references NIST PQC integration. This refers to:

1. **Test Vector Compatibility**: GoldenSeed can generate test data for PQC algorithm validation
2. **Deterministic Seed Generation**: Reproducible seeds for testing PQC implementations
3. **NOT Cryptographic Use**: GoldenSeed should not be used to generate actual cryptographic keys

### PQC Test Vectors

File: `tests/nist_pqc_test_vectors.json`

Contains reference test vectors for:
- CRYSTALS-Kyber (ML-KEM) - NIST FIPS 203
- CRYSTALS-Dilithium (ML-DSA) - NIST FIPS 204
- SPHINCS+ (SLH-DSA) - NIST FIPS 205

**Usage**: Validating PQC implementations with deterministic test inputs, **not** generating real keys.

## Continuous Integration

All tests run automatically via GitHub Actions:

```yaml
# .github/workflows/test.yml
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Cross-platform determinism
- Test vector validation
- Package integrity checks
```

See current status: [GitHub Actions](https://github.com/beanapologist/seed/actions)

## Statistical Properties

While not NIST STS validated, GoldenSeed output exhibits:

✅ **Uniform byte distribution** (0-255 range)  
✅ **Low autocorrelation** in bit patterns  
✅ **No short cycles** in tested ranges  
✅ **Consistent cross-platform** behavior  
✅ **Deterministic** reproducibility  

## When to Use GoldenSeed

✅ **Good for:**
- Procedural world generation (games)
- Reproducible test data
- Deterministic simulations
- Generative art and music
- Data distribution via seeds

❌ **Bad for:**
- Cryptographic key generation
- Password generation
- Session token creation
- Security-critical randomness
- Any cryptographic application

## Recommended Alternatives for Cryptography

If you need cryptographic randomness, use:

| Platform | Recommended |
|----------|-------------|
| Python | `secrets` module |
| JavaScript | `crypto.getRandomValues()` |
| C/C++ | `CryptGenRandom`, `/dev/urandom` |
| Go | `crypto/rand` package |
| Rust | `rand` crate with `OsRng` |
| Java | `SecureRandom` class |

## Compliance Summary

| Standard | Status | Notes |
|----------|--------|-------|
| NIST SP 800-90A | ❌ Not Applicable | Not a cryptographic DRBG |
| NIST SP 800-90B | ❌ Not Applicable | Not an entropy source |
| NIST STS | ⚠️ Not Tested | Removed during refactoring |
| Determinism | ✅ Validated | Core requirement |
| Cross-Platform | ✅ Validated | Tested extensively |
| Test Vectors | ✅ Validated | Reference-based testing |

## Conclusion

GoldenSeed is a deterministic byte stream generator with well-defined, non-cryptographic use cases. It prioritizes:

1. **Determinism** over randomness
2. **Reproducibility** over unpredictability
3. **Cross-platform consistency** over platform optimization
4. **Procedural generation** over security

For cryptographic applications, use established cryptographic libraries and NIST-validated DRBGs.

## See Also

- [Entropy Analysis](ENTROPY_ANALYSIS.md)
- [Entropy Testing](ENTROPY_TESTING.md)
- [Compliance Testing](COMPLIANCE_TESTING.md)
- [Main README](../README.md)
- [Security Policy](../SECURITY.md)
