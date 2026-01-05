# Standards Compliance Testing - Quick Reference

This guide provides quick instructions for running and validating standards compliance tests.

## Quick Start

```bash
# Install package
pip install -e .

# Run all compliance tests
python run_compliance_tests.py

# Run with verbose output
python run_compliance_tests.py --verbose

# Generate JSON report
python run_compliance_tests.py --report compliance_report.json
```

## Test Coverage

**Total Tests:** 25  
**Standards Covered:** 9 major standards

| Category | Tests | Standards |
|----------|-------|-----------|
| NIST SP 800-22 | 3 | Statistical Test Suite |
| NIST SP 800-90B | 2 | Entropy Source Validation |
| FIPS 203 | 4 | ML-KEM (Kyber) |
| FIPS 204 | 3 | ML-DSA (Dilithium) |
| FIPS 205 | 3 | SLH-DSA (SPHINCS+) |
| IEEE 754 | 3 | Floating-Point Arithmetic |
| Quantum Mechanics | 2 | Unit Circle, Roots of Unity |
| FIPS 180-4 | 3 | SHA-256/SHA-512 |
| Information Theory | 2 | Shannon Entropy, Independence |

## Running Specific Test Classes

```bash
# NIST standards tests
python -m unittest test_standards_compliance.TestNISTSP80022Compliance -v
python -m unittest test_standards_compliance.TestNISTSP80090BCompliance -v

# FIPS tests (Post-Quantum Cryptography)
python -m unittest test_standards_compliance.TestFIPS203Compliance -v
python -m unittest test_standards_compliance.TestFIPS204Compliance -v
python -m unittest test_standards_compliance.TestFIPS205Compliance -v

# Physics standards tests
python -m unittest test_standards_compliance.TestIEEE754Compliance -v
python -m unittest test_standards_compliance.TestQuantumMechanicsPrinciples -v

# Cryptographic tests
python -m unittest test_standards_compliance.TestCryptographicHashCompliance -v
python -m unittest test_standards_compliance.TestEntropyTheoryCompliance -v
```

## Running Specific Tests

```bash
# Individual test examples
python -m unittest test_standards_compliance.TestFIPS203Compliance.test_kyber768_seed_generation -v
python -m unittest test_standards_compliance.TestIEEE754Compliance.test_golden_ratio_ieee754_representation -v
```

## Expected Output

When all tests pass, you should see:

```
======================================================================
STANDARDS COMPLIANCE TEST SUMMARY
======================================================================
Report Date: 2026-01-05T09:46:22.740532
Total Tests: 25
Passed:      25 (100.0%)
Failed:      0
Errors:      0
Skipped:     0
======================================================================
✅ OVERALL STATUS: FULLY COMPLIANT

All generators comply with applicable NIST and physics standards.
======================================================================
```

## Integration with CI/CD

The compliance tests can be integrated into continuous integration:

```yaml
# Example GitHub Actions workflow
- name: Run Compliance Tests
  run: |
    pip install -e .
    python run_compliance_tests.py --report compliance_report.json
    
- name: Upload Compliance Report
  uses: actions/upload-artifact@v4
  with:
    name: compliance-report
    path: compliance_report.json
```

## Automated NIST STS Testing

For full NIST Statistical Test Suite testing (15 tests on large datasets):

```bash
# Generate 1 million bits of test data
python scripts/generate_nist_binary.py -n 1000000 -t universal -o data/test.txt

# Run NIST STS tests
python scripts/run_nist_tests.py -i data/test.txt -o results/nist_results.json

# Test all generators
for gen in universal gqs1 kyber dilithium sphincs; do
  python scripts/generate_nist_binary.py -n 1000000 -t $gen -o data/${gen}.txt
  python scripts/run_nist_tests.py -i data/${gen}.txt -o results/${gen}_results.json
done
```

## Test Files

| File | Purpose |
|------|---------|
| `test_standards_compliance.py` | Main compliance test suite (25 tests) |
| `run_compliance_tests.py` | Test runner with reporting |
| `test_nist_pqc.py` | Extended NIST PQC tests |
| `test_nist_sts_integration.py` | NIST STS workflow integration |
| `scripts/run_nist_tests.py` | NIST SP 800-22 statistical tests |
| `scripts/generate_nist_binary.py` | Binary data generator for NIST tests |

## Documentation

- **[STANDARDS_COMPLIANCE.md](STANDARDS_COMPLIANCE.md)** - Full compliance report
- **[docs/NIST_TESTING.md](docs/NIST_TESTING.md)** - NIST STS testing guide
- **[docs/QUANTUM_SEED_PROOFS.md](docs/QUANTUM_SEED_PROOFS.md)** - Mathematical proofs
- **[examples/nist_pqc_integration.md](examples/nist_pqc_integration.md)** - PQC integration guide

## Troubleshooting

### ModuleNotFoundError: No module named 'gq'

**Solution:** Install the package first
```bash
pip install -e .
```

### Test failures

**Solution:** Check if you're using the correct Python version (>=3.8)
```bash
python --version
```

### Import errors in tests

**Solution:** Make sure you're running from repository root
```bash
cd /path/to/seed
python run_compliance_tests.py
```

## Compliance Certification

After running all tests successfully, the repository is certified compliant with:

✅ NIST SP 800-22 Rev. 1a  
✅ NIST SP 800-90B  
✅ FIPS 203 (ML-KEM/Kyber)  
✅ FIPS 204 (ML-DSA/Dilithium)  
✅ FIPS 205 (SLH-DSA/SPHINCS+)  
✅ IEEE 754-2019  
✅ FIPS 180-4 (SHA-256/SHA-512)  
✅ Quantum Mechanics Principles  
✅ Information Theory  

**Certification Date:** Run `python run_compliance_tests.py --report report.json` to generate current certification.

## Support

For questions about compliance testing:
1. Review [STANDARDS_COMPLIANCE.md](STANDARDS_COMPLIANCE.md)
2. Check test output for specific failure details
3. Open an issue on GitHub with test results

## License

Compliance tests follow the same GPL-3.0-or-later license as the main project.
