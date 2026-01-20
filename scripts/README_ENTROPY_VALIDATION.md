# Entropy Validation Scripts

This directory contains scripts for comprehensive entropy validation of E overflow claims using industry-standard tools.

## Overview

These scripts support validation of claims that floating-point E overflow from unit circle rotations serves as an entropy source. They generate data files compatible with:

1. **NIST SP 800-90B** - Official entropy assessment tools
2. **Dieharder** - Comprehensive random number generator test suite
3. **TestU01** - Statistical test library

## Scripts

### 1. nist_sp800_90b_data_generator.py

Generates binary data from E overflow for NIST SP 800-90B entropy assessment.

**Usage:**
```bash
# Display information
python scripts/nist_sp800_90b_data_generator.py --info

# Generate 1M samples (8 MB)
python scripts/nist_sp800_90b_data_generator.py --samples 1000000 --output e_data.bin

# Generate bit sequence
python scripts/nist_sp800_90b_data_generator.py --samples 1000000 --output e_bits.bin --bits
```

**NIST Tool Installation:**
```bash
git clone https://github.com/usnistgov/SP800-90B_EntropyAssessment
cd SP800-90B_EntropyAssessment/cpp
make
sudo make install
```

**Testing:**
```bash
ea_iid e_data.bin 8      # IID assumption test
ea_non_iid e_data.bin 8  # Non-IID entropy assessment
```

**Expected Results:**
- Min-entropy: Very low (~0.7 bits)
- IID test: FAIL (data not independent)
- Non-IID: Detects deterministic patterns

### 2. dieharder_data_generator.py

Generates binary data from E overflow for Dieharder randomness testing.

**Usage:**
```bash
# Display information
python scripts/dieharder_data_generator.py --info

# Generate 10M samples (40 MB)
python scripts/dieharder_data_generator.py --samples 10000000 --output e_random.bin

# Generate raw bit stream
python scripts/dieharder_data_generator.py --raw-bits --bytes 10000000 --output e_bits.bin
```

**Dieharder Installation:**
```bash
# Ubuntu/Debian
sudo apt-get install dieharder

# macOS
brew install dieharder
```

**Testing:**
```bash
# Run all tests
dieharder -g 201 -f e_random.bin -a

# Quick test (one test)
dieharder -g 201 -f e_random.bin -d 0

# Specific test
dieharder -g 201 -f e_random.bin -d 2
```

**Expected Results:**
- Many tests: FAILED or WEAK
- Chi-square tests: Show non-uniformity
- Correlation tests: Detect patterns
- Conclusion: NOT suitable as RNG

### 3. generate_entropy_report.py

Generates comprehensive entropy analysis reports (already exists in repository).

## Validation Workflow

### Step 1: Run Built-in Tests
```bash
# Run comprehensive validation tests
python -m unittest tests.validate_entropy_source -v

# This runs 21 tests covering:
# - Determinism and reproducibility
# - Known-answer tests
# - Min-entropy estimation
# - Prediction attacks
# - Statistical randomness
# - Physics-based ZPE validation
```

### Step 2: NIST SP 800-90B Testing (Optional)
```bash
# Generate data
python scripts/nist_sp800_90b_data_generator.py --samples 1000000 --output nist_data.bin

# Install NIST tools (if not already installed)
# See script --info for installation instructions

# Run tests
ea_iid nist_data.bin 8
ea_non_iid nist_data.bin 8

# Expected: Low entropy, deterministic patterns detected
```

### Step 3: Dieharder Testing (Optional)
```bash
# Generate data
python scripts/dieharder_data_generator.py --samples 10000000 --output dh_data.bin

# Install Dieharder (if not already installed)
# Ubuntu: sudo apt-get install dieharder
# macOS: brew install dieharder

# Run tests
dieharder -g 201 -f dh_data.bin -a

# Expected: Many FAILED/WEAK results indicating non-randomness
```

## Results Summary

Based on comprehensive testing:

✅ **E overflow is deterministic** (not random)
✅ **E overflow has 0.73 bits min-entropy** (catastrophically low)
✅ **E overflow fails statistical tests** (chi-square, runs test)
✅ **E overflow is perfectly predictable** (can be computed from input)
✅ **E overflow is not ZPE** (wrong energy scale, IEEE 754 dependent)

## Documentation

- **Comprehensive Report**: `docs/ENTROPY_VALIDATION_TESTS.md`
- **Test Implementation**: `tests/validate_entropy_source.py`
- **Test Results**: See report and test output

## Recommendations

**DO NOT use E overflow as:**
- Cryptographic entropy source
- Random number generator
- Source of unpredictability

**E overflow IS:**
- IEEE 754 floating-point rounding error
- Completely deterministic
- Predictable from input parameters
- Not related to quantum Zero-Point Energy

## External Tools

### NIST SP 800-90B
- **Source**: https://github.com/usnistgov/SP800-90B_EntropyAssessment
- **Documentation**: NIST SP 800-90B standard
- **Purpose**: Official entropy assessment for cryptographic applications

### Dieharder
- **Source**: http://webhome.phy.duke.edu/~rgb/General/dieharder.php
- **Package**: Available in most Linux distributions
- **Purpose**: Comprehensive RNG testing

### TestU01
- **Source**: http://simul.iro.umontreal.ca/testu01/tu01.html
- **Installation**: Requires C compilation
- **Purpose**: Extensive statistical test library

## Notes

1. NIST and Dieharder tools must be installed separately
2. These scripts have no dependencies (pure Python)
3. Generated binary files can be large (10-100 MB)
4. Test execution may take several minutes to hours
5. Results consistently confirm E overflow is not random

## Support

For questions about:
- Test methodology: See `docs/ENTROPY_VALIDATION_TESTS.md`
- Test implementation: See `tests/validate_entropy_source.py`
- NIST tools: See official NIST documentation
- Dieharder: See Dieharder documentation

---

**Last Updated**: January 5, 2026
**Status**: Complete and validated
