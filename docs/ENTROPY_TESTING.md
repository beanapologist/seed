# Entropy Validation

This document describes the entropy validation testing performed on GoldenSeed.

## Overview

GoldenSeed generates deterministic high-entropy byte streams from fixed seeds. While not designed for cryptographic applications, the output exhibits high-quality statistical properties suitable for procedural generation and deterministic simulations.

## Testing Approach

GoldenSeed's entropy quality is validated through:

1. **Unit Tests** - Core functionality tests in `tests/test_universal_qkd.py` and `tests/test_gqs1.py`
2. **Cross-Platform Tests** - Determinism validation across platforms in `tests/test_cross_platform_determinism.py`
3. **Compression Capacity Tests** - Stream quality validation in `tests/test_compression_capacity.py`
4. **Edge Case Tests** - Boundary condition testing in `tests/test_edge_cases.py`

## Test Results

All tests are run as part of the continuous integration pipeline. See the [test workflow](.github/workflows/test.yml) for current status.

### Key Validations

- ✅ **Determinism**: Same seed produces identical output across platforms
- ✅ **Stream Consistency**: Output matches reference test vectors
- ✅ **Cross-Platform**: Python 3.8+ on Linux, macOS, and Windows
- ✅ **Multi-Language**: Identical output in Python, JavaScript, C, C++, Go, Rust, and Java

## Running Tests Locally

```bash
# Install test dependencies
pip install -e .
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_universal_qkd.py -v
python -m pytest tests/test_cross_platform_determinism.py -v
python -m pytest tests/test_compression_capacity.py -v
```

## Statistical Properties

GoldenSeed uses the golden ratio (Φ) for deterministic entropy generation:

- Binary fusion operations with bit rotation
- Position-based state evolution
- Reproducible across all implementations
- Infinite stream generation without state limitations

## Important Notes

⚠️ **GoldenSeed is NOT for cryptography**. It is designed for:
- Procedural content generation
- Reproducible testing
- Deterministic simulations
- Space-efficient data storage

For cryptographic applications, use proven cryptographic PRNGs like those in Python's `secrets` module or platform-specific CSPRNGs.

## See Also

- [Test Suite Documentation](../tests/)
- [Main README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
