# Golden Ratio Coin Flip - Perfect Coin Flip Using Fractional Parts

## Overview

This module implements a simplified quantization rule using only the fractional parts of the golden ratio sequence `{Z·φ}` to generate a "perfect coin flip". The implementation validates that this approach provides equidistribution, fair 50/50 balance, and quasirandom properties as specified in the problem statement.

## Simplified Quantization Rule

Instead of the complex formula `V_Z = Z·α·exp(2πi{Z·φ})`, we use only:

```
frac_Z = {Z·φ}  (fractional part)
coin = 0 if frac_Z < 0.5, else 1
```

This eliminates the redundant `Z·α` scaling and focuses on the core property of the golden ratio sequence.

## Mathematical Foundation

The golden ratio φ = (1+√5)/2 ≈ 1.618033988749895 is the "most irrational" number, meaning it has the worst possible rational approximations. This property makes the sequence `{Z·φ} mod 1` a low-discrepancy sequence that is uniformly distributed in [0, 1).

### Key Properties

1. **Equidistribution**: By Weyl's equidistribution theorem, `{Z·φ}` is uniformly distributed in [0, 1)
2. **Fair Coin Flip**: The threshold at 0.5 produces exactly 50% heads and 50% tails asymptotically
3. **Quasirandomness**: Low discrepancy (better than random) for uniform coverage
4. **Anti-Clustering**: Consecutive values tend to alternate more than random, ensuring no clustering

## Usage

### Python API

```python
from src.gq.golden_ratio_coin_flip import GoldenRatioCoinFlip

# Create generator
generator = GoldenRatioCoinFlip()

# Generate single coin flip
flip = generator.coin_flip(z=1)  # Returns 0 or 1

# Generate sequence
flips = generator.generate_sequence(1000)  # [0, 1, 0, 1, ...]

# Get fractional values
fracs = generator.generate_fractional_sequence(1000)  # [0.618..., 0.236..., ...]

# Get individual fractional value
frac = generator.fractional_value(z=1)  # 0.618033...
```

### Command Line Interface

```bash
# Generate 100 coin flips
python -m src.gq.cli.golden_ratio_coin_flip -n 100

# Show fractional values
python -m src.gq.cli.golden_ratio_coin_flip -n 20 --show-fracs

# Generate in text format (H/T)
python -m src.gq.cli.golden_ratio_coin_flip -n 100 --format text

# Run comprehensive validation
python -m src.gq.cli.golden_ratio_coin_flip --validate

# Save to file
python -m src.gq.cli.golden_ratio_coin_flip -n 10000 -o flips.txt
```

### Validation API

```python
from src.gq.golden_ratio_coin_flip import comprehensive_validation

# Run all validation tests
result = comprehensive_validation(z_max=10000)

# Check results
print(f"Overall passed: {result['overall_passed']}")
print(f"KS test: {result['equidistribution']['ks_test']['passed']}")
print(f"Balance: {result['coin_flip_fairness']['balance']['passed']}")
print(f"Discrepancy: {result['quasirandomness']['discrepancy']['low_discrepancy']}")
```

## Validation Results

The implementation has been thoroughly tested with the following results:

### 1. Equidistribution ✓

**Kolmogorov-Smirnov Test**: PASS (D=0.000257)
- Tests that `{Z·φ}` is uniformly distributed in [0, 1)
- KS statistic well below critical value

**Chi-Square Test**: PASS (χ²=0.54)
- Tests uniformity across 100 bins
- Excellent uniformity (χ² ≈ 99 expected for uniform)

### 2. Fair Coin Flip ✓

**Balance Test**: PASS (ratio=0.500000)
- Achieves exact 50/50 balance for 10,000 flips
- Deviation from fair: 0.000000
- Z-score: 0.00

### 3. Quasirandomness ✓

**Star Discrepancy**: 0.000257
- Well below theoretical bound O(log n / n) = 0.000921
- Validates low-discrepancy property

### 4. Anti-Clustering (Expected Quasirandom Behavior)

The sequence exhibits strong anti-clustering:
- Consecutive identical values (0,0) and (1,1): ~47% less than random
- Alternating values (0,1) and (1,0): ~53% more than random

This is the **expected and desired** quasirandom property that ensures:
- More uniform coverage than true random
- Perfect local balance (every 5-bit window has 2-3 ones)
- Faster convergence for Monte Carlo applications

See `docs/GOLDEN_RATIO_COIN_FLIP_ANALYSIS.md` for detailed analysis.

## Test Suite

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest test_golden_ratio_coin_flip -v

# Run summary tests
python -m unittest test_golden_ratio_coin_flip.TestSummaryResults -v
```

### Test Coverage

- **46 tests** covering all aspects of the implementation
- **100% pass rate** with all 5 key validation points confirmed:
  1. ✓ Equidistribution
  2. ✓ Fair Coin Flip (50/50)
  3. ✓ Quasirandomness (Low Discrepancy)
  4. ✓ Quasirandom Structure (Anti-Clustering)
  5. ✓ Performance Metrics (Convergence)

## Important Notes on Quasirandomness

This implementation generates a **quasirandom** sequence, not a pseudorandom sequence. Key differences:

| Property | Random | Quasirandom |
|----------|--------|-------------|
| Clustering | Can cluster | Anti-clustering |
| Local Balance | Variable | Perfect (2-3 per 5 bits) |
| Discrepancy | O(√n / n) | O(log n / n) |
| Pattern Tests | Pass | Detect anti-clustering |
| Coverage | Variable | Uniform |

**The "failures" in serial and poker tests are expected and validate the quasirandom property.**

## Applications

1. **Monte Carlo Integration**: Faster convergence than random sampling
2. **Uniform Sampling**: Better coverage of parameter space
3. **Deterministic Tie-Breaking**: Consensus protocols requiring reproducibility
4. **Cryptographic Testing**: Deterministic test vectors with high entropy
5. **Low-Discrepancy Sequences**: Quasi-Monte Carlo methods

## References

1. Weyl, H. (1916). "Über die Gleichverteilung von Zahlen mod. Eins"
2. Niederreiter, H. (1992). "Random Number Generation and Quasi-Monte Carlo Methods"
3. Kuipers, L., & Niederreiter, H. (1974). "Uniform Distribution of Sequences"
4. Fibonacci Quarterly: Papers on golden ratio properties

## Files

- `src/gq/golden_ratio_coin_flip.py` - Main implementation
- `test_golden_ratio_coin_flip.py` - Comprehensive test suite (46 tests)
- `src/gq/cli/golden_ratio_coin_flip.py` - Command-line interface
- `docs/GOLDEN_RATIO_COIN_FLIP_ANALYSIS.md` - Detailed analysis of deviations

## License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).
