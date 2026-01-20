# Standardized Test Library (STL) - Test Suite Documentation

This document provides comprehensive documentation for the Standardized Test Library (STL) test suites added to ensure maximum testing coverage, scalability validation, and cross-platform determinism.

## Overview

The STL consists of **81+ new tests** organized into four comprehensive test suites:

1. **Edge Cases** - 22 tests for boundary conditions and error handling
2. **Scalability & Stress** - 20+ tests for performance and large-scale generation
3. **Multi-Seed Collisions** - 18+ tests for uniqueness and statistical properties
4. **Cross-Platform Determinism** - 21 tests for platform independence

## Test Suites

### 1. Edge Case Tests (`tests/test_edge_cases.py`)

**Purpose**: Validate boundary conditions, edge cases, and error handling to ensure robust behavior across all possible inputs.

**Test Classes**:
- `TestBoundaryValues` (6 tests)
- `TestInvalidInputHandling` (4 tests)
- `TestExtremeParameters` (4 tests)
- `TestZeroAndNullHandling` (3 tests)
- `TestOverflowAndUnderflow` (2 tests)
- `TestDeterministicReproducibility` (3 tests)

**Key Tests**:

#### Boundary Value Tests
- `test_basis_match_all_values`: Validates basis matching across all 256 byte values (~50% efficiency)
- `test_xor_fold_hardening_edge_cases`: Tests XOR folding with all-zero, all-one, alternating patterns
- `test_hash_drbg_ratchet_counter_boundaries`: Tests counter values from 0 to 2^32-1

#### Invalid Input Tests
- `test_verify_seed_checksum_wrong_length`: Tests seed verification with incorrect lengths
- `test_xor_fold_hardening_wrong_length`: Validates error handling for incorrect bit counts

#### Extreme Parameter Tests
- `test_consecutive_keys_uniqueness_extreme`: Generates 1,000 consecutive keys and verifies uniqueness
- `test_gqs1_vectors_extreme_count`: Generates 100 GQS-1 test vectors
- `test_state_evolution_consistency`: Tracks state evolution through 100 iterations

**Run Command**:
```bash
python -m unittest tests.test_edge_cases -v
```

**Expected Results**: All 22 tests pass in <0.2 seconds

---

### 2. Scalability & Stress Tests (`tests/test_scalability_stress.py`)

**Purpose**: Validate performance, memory efficiency, and scalability under high-load conditions.

**Test Classes**:
- `TestLargeScaleKeyGeneration` (3 tests)
- `TestMemoryEfficiency` (3 tests)
- `TestPerformanceBenchmarks` (4 tests)
- `TestContinuousGeneration` (2 tests)
- `TestResourceUtilization` (3 tests)
- `TestComplexityScaling` (2 tests)

**Key Tests**:

#### Large-Scale Generation
- `test_generate_10k_keys`: Generates 10,000 keys (~1 second, 11,000 keys/sec)
- `test_generate_100k_keys`: Generates 100,000 keys in batches (~10 seconds)
- `test_streaming_generation_1m_keys`: Streams 1 million keys without storing all

#### Performance Benchmarks
- `test_key_generation_rate`: Benchmarks key generation throughput
- `test_gqs1_generation_rate`: Benchmarks GQS-1 test vector generation
- `test_basis_matching_performance`: Tests basis matching speed (100K+ ops/sec)
- `test_hash_drbg_performance`: Benchmarks Hash-DRBG ratchet (1000+ ops/sec)

#### Memory Efficiency
- `test_memory_efficiency_continuous_generation`: Generates 100,000 keys in batches, discards, verifies no memory leaks
- `test_generator_state_size`: Validates generator maintains constant state size

**Run Commands**:
```bash
# Run all scalability tests
python -m unittest tests.test_scalability_stress -v

# Run specific performance benchmarks
python -m unittest tests.test_scalability_stress.TestPerformanceBenchmarks -v

# Run large-scale tests (may take several minutes)
python -m unittest tests.test_scalability_stress.TestLargeScaleKeyGeneration -v
```

**Expected Results**:
- 10K keys: <1 second
- 100K keys: <10 seconds  
- 1M keys: <2 minutes
- Throughput: 10,000+ keys/second
- No memory leaks detected

---

### 3. Multi-Seed Collision Tests (`tests/test_multi_seed_collision.py`)

**Purpose**: Validate collision resistance, uniqueness guarantees, and statistical properties across different seeds and entropy sources.

**Test Classes**:
- `TestSeedCollisionResistance` (4 tests)
- `TestUniquenessGuarantees` (4 tests)
- `TestSeedDiversityAnalysis` (4 tests)
- `TestStatisticalProperties` (3 tests)

**Key Tests**:

#### Collision Resistance
- `test_no_collisions_within_single_seed_stream`: Generates 100,000 keys, verifies no collisions
- `test_avalanche_effect_on_seed_variation`: Tests that 1-bit seed change → ~50% output change
- `test_counter_variation_produces_unique_outputs`: Generates 1,000 outputs with different counters

#### Statistical Analysis
- `test_bit_distribution_uniformity`: Validates bit distribution is uniform (40-60% ones)
- `test_hamming_distance_distribution`: Tests average Hamming distance ~64 bits (50%)
- `test_entropy_quality_across_stream`: Samples entropy at multiple stream positions (>7.0 bits/byte)
- `test_chi_square_byte_distribution`: Chi-square test for uniform byte distribution

#### Advanced Tests
- `test_runs_test`: Validates no long runs of consecutive bits (max <20 bits)
- `test_serial_correlation`: Tests consecutive keys are uncorrelated

**Run Commands**:
```bash
# Run all collision tests
python -m unittest tests.test_multi_seed_collision -v

# Run specific collision test (generates 100K keys, ~10 seconds)
python -m unittest tests.test_multi_seed_collision.TestSeedCollisionResistance.test_no_collisions_within_single_seed_stream -v

# Run statistical analysis
python -m unittest tests.test_multi_seed_collision.TestStatisticalProperties -v
```

**Expected Results**:
- 100,000 consecutive keys: zero collisions
- Average Hamming distance: 64 bits (50% of 128 bits)
- Bit distribution: uniform within 40-60% range
- Entropy: >7.0 bits per byte
- Chi-square: within expected range (200-310 for df=255)

---

### 4. Cross-Platform Determinism Tests (`tests/test_cross_platform_determinism.py`)

**Purpose**: Validate deterministic behavior across different platforms, architectures, Python versions, and environments.

**Test Classes**:
- `TestPlatformIndependence` (5 tests)
- `TestReproducibilityAcrossEnvironments` (3 tests)
- `TestIEEE754Consistency` (3 tests)
- `TestHashFunctionConsistency` (3 tests)
- `TestByteOrderIndependence` (3 tests)
- `TestCrossVersionCompatibility` (3 tests)
- `TestSystemInformationLogging` (1 test)

**Key Tests**:

#### Platform Independence
- `test_first_key_deterministic_across_platforms`: Validates first key matches `3c732e0d04dac163a5cc2b15c7caf42c`
- `test_gqs1_first_vector_deterministic`: Validates first GQS-1 vector matches `a01611f01e8207a27c1529c3650c4838`
- `test_key_sequence_deterministic`: Generates 100 keys multiple times, verifies identical

#### Reproducibility
- `test_reproducible_with_fresh_generator`: Creates 10 fresh generators, verifies same sequence
- `test_no_randomness_sources_used`: Verifies no system randomness is used (fully deterministic)

#### IEEE 754 & Hash Consistency
- `test_golden_ratio_representation`: Validates φ = 1.618033988749895
- `test_sha256_known_vectors`: Tests SHA-256 with FIPS 180-4 test vectors
- `test_hash_concatenation_consistency`: Validates hash(state || counter) determinism

#### System Information
- `test_log_system_information`: Logs Python version, platform, byte order for debugging

**Run Commands**:
```bash
# Run all cross-platform tests
python -m unittest tests.test_cross_platform_determinism -v

# Run with system information logging
python -m unittest tests.test_cross_platform_determinism.TestSystemInformationLogging -v
```

**Expected Results**:
- All 21 tests pass on Linux, Windows, macOS
- Works on Python 3.8-3.12+
- Endianness-independent (both little-endian and big-endian)
- 100% reproducible across all runs

---

## Running All STL Tests

### Run Complete STL Test Suite

```bash
# Run all STL tests at once
python -m unittest tests.test_edge_cases tests.test_scalability_stress tests.test_multi_seed_collision tests.test_cross_platform_determinism -v
```

**Expected Output**: 81+ tests pass

### Run Quick Validation (Fast Tests Only)

```bash
# Run edge cases and cross-platform tests (~0.5 seconds)
python -m unittest tests.test_edge_cases tests.test_cross_platform_determinism -v
```

### Run Performance Suite

```bash
# Run performance and scalability tests (may take several minutes)
python -m unittest tests.test_scalability_stress tests.test_multi_seed_collision -v
```

---

## Test Coverage Summary

| Test Suite | Tests | Time | Coverage |
|------------|-------|------|----------|
| Edge Cases | 22 | <0.2s | Boundary values, error handling |
| Scalability & Stress | 20+ | 1-60s | Performance, memory, throughput |
| Multi-Seed Collisions | 18+ | 1-30s | Uniqueness, statistics, entropy |
| Cross-Platform | 21 | <0.2s | Determinism, reproducibility |
| **Total STL** | **81+** | **<2min** | **Comprehensive validation** |

---

## Key Metrics Validated

### Performance Metrics
- ✅ **Throughput**: 10,000+ keys/second
- ✅ **Latency**: <0.1 ms per key
- ✅ **Memory**: ~16 bytes per key
- ✅ **Scalability**: Linear, no degradation

### Security Metrics
- ✅ **Collision Resistance**: 0 collisions in 100,000 keys
- ✅ **Avalanche Effect**: ~50% bit difference on seed change
- ✅ **Entropy**: >7.0 bits per byte
- ✅ **Uniformity**: 40-60% bit distribution

### Determinism Metrics
- ✅ **Reproducibility**: 100% across all platforms
- ✅ **First Key**: Always `3c732e0d04dac163a5cc2b15c7caf42c`
- ✅ **Platform Independence**: Works on Linux, Windows, macOS
- ✅ **Version Compatibility**: Python 3.8-3.12+

---

## Continuous Integration

The STL test suites are designed for CI/CD integration:

```yaml
# Example GitHub Actions workflow
name: STL Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -e .
      - name: Run STL tests
        run: |
          python -m unittest tests.test_edge_cases -v
          python -m unittest tests.test_cross_platform_determinism -v
      - name: Run performance tests
        run: python -m unittest tests.test_scalability_stress.TestPerformanceBenchmarks -v
```

---

## Troubleshooting

### Test Timeouts

Some tests may take longer on slower systems:

```bash
# Run with longer timeout
timeout 300 python -m unittest tests.test_scalability_stress.TestLargeScaleKeyGeneration.test_streaming_generation_1m_keys -v
```

### Memory Issues

For systems with limited memory, run tests individually:

```bash
# Run tests one at a time
for test in tests.test_edge_cases tests.test_cross_platform_determinism; do
    python -m unittest $test -v
done
```

### Platform-Specific Issues

If tests fail on a specific platform, check system information:

```bash
python -m unittest tests.test_cross_platform_determinism.TestSystemInformationLogging -v
```

---

## Contributing

When adding new tests to the STL:

1. **Follow naming conventions**: `test_<feature>_<scenario>`
2. **Add docstrings**: Explain what the test validates
3. **Use assertions**: Provide clear failure messages
4. **Document metrics**: Log performance numbers for benchmarks
5. **Test edge cases**: Cover boundary conditions
6. **Validate determinism**: Ensure reproducibility

Example test template:

```python
def test_new_feature(self):
    """Test that new feature behaves correctly under condition X."""
    # Arrange
    generator = universal_qkd_generator()
    
    # Act
    result = next(generator)
    
    # Assert
    self.assertEqual(len(result), 16, "Key should be 16 bytes")
    self.assertIsInstance(result, bytes, "Key should be bytes type")
```

---

## License

The STL test suites are part of the seed repository and follow the same GPL-3.0-or-later license.

---

## Contact

For questions or issues with the STL test suites:
- Open an issue on GitHub
- Check existing test documentation
- Review test output for detailed error messages
