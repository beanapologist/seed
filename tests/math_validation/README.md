# Mathematical Validation Tests

This directory contains comprehensive tests for validating the mathematical correctness and deterministic behavior of the Golden Ratio-based DRNG implementation.

## Test Files

- `test_math_and_determinism.py` - Comprehensive test suite with 30 test cases covering:
  - Mathematical validation (Golden Ratio, modular arithmetic, XOR folding)
  - Deterministic behavior (same seed consistency, cross-seed validation)
  - Statistical properties (uniformity, entropy, bit balance)

## Running Tests

Run all mathematical validation tests:
```bash
pytest tests/math_validation/ -v
```

Run specific test classes:
```bash
pytest tests/math_validation/test_math_and_determinism.py::TestGoldenRatioMathematicalCorrectness -v
```

## CI/CD Integration

These tests are automatically run by the "Verify Math and Determinism" GitHub Actions workflow defined in `.github/workflows/verify-math.yml`.
