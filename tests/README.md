# Quantum Seed Foundations - Test Suite

This directory contains comprehensive tests validating the Quantum Seed principle.

## Test Files

### `test_quantum_seed_foundations.py`

Comprehensive test suite with 24 tests validating:

1. **8th Roots of Unity Alignment** (5 tests)
   - Verifies evenly spaced angles (π/4 intervals)
   - Confirms unit magnitude for all roots
   - Tests multiplication closure property
   - Validates return to origin after 8 steps
   - Confirms E overflow alignment with quantum structure

2. **E Irreducibility** (5 tests)
   - Proves E is genuinely nonzero (not exactly zero)
   - Validates boundedness within IEEE 754 limits
   - Confirms dependency on machine epsilon
   - Tests irreducibility across multiple trials
   - Verifies deterministic behavior

3. **Quantum Coherence** (3 tests)
   - Tests 8-step rotations for quantum coherence
   - Validates phase conservation across rotations
   - Confirms E varies coherently with step size

4. **Cryptographic Properties** (4 tests)
   - Tests extraction of cryptographic bits from E
   - Validates Shannon entropy quality
   - NIST monobit frequency test
   - NIST runs test

5. **Property-Based Tests** (3 tests)
   - Deterministic generation across diverse inputs
   - E bounds property (always bounded)
   - E nonzero property for non-aligned angles

6. **Integration Tests** (4 tests)
   - Full pipeline from unit circle to cryptographic seed
   - Architecture-wide reproducibility
   - NIST PQC compatibility
   - Multiple seed generation with uniqueness

**Run the tests:**
```bash
python -m unittest tests.test_quantum_seed_foundations -v
```

**Expected result:** All 24 tests pass ✅

### `generate_quantum_test_vectors.py`

Script to generate comprehensive test vectors for statistical analysis.

**Usage:**
```bash
# Generate 10,000 test vectors (default)
python tests/generate_quantum_test_vectors.py

# Generate custom number of vectors
python tests/generate_quantum_test_vectors.py 50000

# Specify output file
python tests/generate_quantum_test_vectors.py 10000 my_vectors.json
```

**Features:**
- Multiple sampling strategies (uniform random, 8th root aligned, special angles, golden ratio)
- Statistical analysis (mean, median, std dev, distribution)
- Determinism verification
- JSON output with metadata

**Output:**
- Generates `quantum_seed_test_vectors.json` (large file, ~4MB for 10K vectors)
- Provides statistical summary on console
- Includes cryptographic seed hashes for each vector

### `quantum_seed_test_vectors_sample.json`

Sample of 100 test vectors included in the repository for quick validation.

The full 10,000+ vector dataset can be generated using the script above.

## Test Vector Schema

Each test vector contains:

```json
{
  "id": 0,
  "strategy": "uniform_random",
  "theta_0_radians": 1.2345,
  "theta_step_radians": 0.7854,
  "theta_0_degrees": 70.73,
  "theta_step_degrees": 45.0,
  "E_overflow": 5.234e-16,
  "crypto_seed_hex": "a4c8f2...",
  "crypto_seed_sha256": "abc123..."
}
```

## Statistical Summary (10,000 vectors)

```
E Overflow Statistics:
  Mean:     5.52 × 10⁻¹⁶
  Median:   4.97 × 10⁻¹⁶
  Std Dev:  3.10 × 10⁻¹⁶
  Min:      0.00 × 10⁻¹⁶ (perfect alignment cases)
  Max:      1.69 × 10⁻¹⁵

Distribution:
  E = 0:           65 vectors (0.65%)
  0 < E < 10⁻¹⁴:   9935 vectors (99.35%)
  
Deterministic Rate: 100.00%
```

## Documentation

See `docs/QUANTUM_SEED_PROOFS.md` for:
- Mathematical proofs of irreducibility
- Zero-Point Energy interpretation
- IEEE 754 precision analysis
- Cryptographic properties validation
- NIST PQC integration guide
- Cross-architecture reproducibility

## Integration with Existing Tests

This test suite complements existing tests:

- `test_binary_verification.py` - Binary Fusion Tap with ZPE overflow
- `test_entropy.py` - Entropy analysis
- `test_nist_pqc.py` - NIST PQC integration
- `test_universal_qkd.py` - Universal key generation

All tests work together to provide comprehensive validation of the Golden Quantum system.

## Continuous Integration

These tests are automatically run as part of the CI pipeline:

```yaml
- name: Run Quantum Seed Foundations tests
  run: |
    python -m unittest tests.test_quantum_seed_foundations -v
```

## Requirements

The test suite has **zero external dependencies** - it uses only Python standard library:
- `unittest` - Test framework
- `cmath` - Complex number mathematics
- `math` - Mathematical functions
- `struct` - IEEE 754 binary packing
- `hashlib` - Cryptographic hashing
- `json` - JSON output for test vectors

No additional packages need to be installed!

## Contributing

When adding new tests:

1. Follow the existing structure (TestCase classes by category)
2. Include docstrings explaining what is being validated
3. Use descriptive assertion messages
4. Ensure deterministic behavior (use fixed seeds for random tests)
5. Add corresponding documentation to `docs/QUANTUM_SEED_PROOFS.md`

## License

These tests are part of the Golden Quantum package and follow the same GPL-3.0-or-later license.
