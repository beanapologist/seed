# NIST Compliance Testing

This document describes the compliance testing framework for GoldenSeed.

## Overview

GoldenSeed is a **deterministic byte stream generator** designed for procedural generation and reproducible simulations, not cryptographic applications. The compliance testing focuses on validating deterministic behavior and cross-platform consistency.

## Testing Framework

### Current Test Suite

The repository includes comprehensive testing through GitHub Actions workflows:

1. **Main Test Suite** (`.github/workflows/test.yml`)
   - Unit tests across Python 3.8-3.12
   - Cross-platform determinism validation
   - Test vector verification
   - Package integrity checks

2. **Verify Math Workflow** (`.github/workflows/verify-math.yml`)
   - Mathematical correctness validation
   - Golden ratio algorithm verification

3. **Build Packages Workflow** (`.github/workflows/build-packages.yml`)
   - Multi-language build verification
   - Package consistency checks

### Test Vector Validation

GoldenSeed maintains reference test vectors in:
- `tests/test_vectors.json` - Core test vectors
- `tests/quantum_seed_test_vectors_sample.json` - Extended test vectors
- `tests/nist_pqc_test_vectors.json` - Post-quantum cryptography test vectors

All implementations (Python, JavaScript, C, C++, Go, Rust, Java) must produce identical output matching these test vectors.

## NIST Statistical Test Suite (STS)

### Status

The NIST Statistical Test Suite workflow has been disabled as part of the DRBG refactoring (see `.github/workflows/nist-sts.yml`). 

**Note**: GoldenSeed is not intended as a cryptographic DRBG (Deterministic Random Bit Generator). The focus is on:
- Deterministic behavior
- Cross-platform consistency
- Procedural generation quality
- Reproducible simulations

### Historical Context

Previous versions included NIST STS validation scripts that were removed to focus on core functionality. The current test suite provides adequate validation for GoldenSeed's intended use cases.

## Compliance Standards

### What GoldenSeed Complies With

✅ **Determinism**: Same seed → same output (always)  
✅ **Cross-Platform**: Identical results on all platforms  
✅ **Multi-Language**: Byte-for-byte consistency across implementations  
✅ **Zero Dependencies**: Pure Python, no external dependencies  
✅ **Test Coverage**: Comprehensive test suite with CI/CD validation  

### What GoldenSeed Does NOT Claim

❌ **Cryptographic Security**: Not a CSPRNG  
❌ **NIST SP 800-90A Compliance**: Not a cryptographic DRBG  
❌ **Cryptographic Randomness**: Not suitable for keys, IVs, nonces  

## Running Compliance Tests

```bash
# Install dependencies
pip install -e .
pip install pytest

# Run full test suite
python -m pytest tests/ -v

# Run cross-platform tests
python -m pytest tests/test_cross_platform_determinism.py -v

# Verify test vectors
python -m pytest tests/test_universal_qkd.py -v
python -m pytest tests/test_gqs1.py -v
```

## Continuous Integration

All compliance tests run automatically on:
- Every push to main/develop branches
- Every pull request
- Manual workflow dispatch

See current test status: [GitHub Actions](https://github.com/beanapologist/seed/actions)

## Use Case Validation

GoldenSeed is validated for:
- 🎮 **Procedural Generation**: Games, worlds, dungeons
- 🧪 **Reproducible Testing**: Deterministic test data
- 🎨 **Generative Art**: Algorithmic art and music
- 🎲 **Deterministic Simulations**: Physics, Monte Carlo with reproducibility
- 💾 **Data Compression**: Extreme compression ratios via seed storage

## Important Notice

⚠️ **DO NOT USE FOR CRYPTOGRAPHY**

GoldenSeed is explicitly **not designed for**:
- Generating cryptographic keys
- Creating initialization vectors (IVs)
- Producing nonces for encryption
- Any security-critical applications

For cryptographic needs, use proven cryptographic libraries like:
- Python: `secrets` module, `cryptography` library
- JavaScript: `crypto.getRandomValues()`
- System CSPRNGs: `/dev/urandom`, `CryptGenRandom`, etc.

## See Also

- [Entropy Testing Documentation](ENTROPY_TESTING.md)
- [Main Test Workflow](../.github/workflows/test.yml)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)
