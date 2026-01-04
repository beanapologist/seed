# Security Policy

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability in this project, **please** open a public GitHub issue. Instead, please report it responsibly by:

### Private Disclosure
- **Email**: Contact the repository maintainer privately with details about the vulnerability
- **GitHub Security Advisory**: Use [GitHub's private vulnerability reporting feature](https://github.com/beanapologist/seed/security/advisories)
- Include steps to reproduce and potential impact assessment

### What to Include
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

## Scope

This security policy covers:
- Binary seed files integrity
- Documentation accuracy
- Supply chain security
- Dependency vulnerabilities (if any)

## Out of Scope

The following are **not** considered security vulnerabilities:
- Educational/documentation improvements
- Code style or formatting issues
- Feature requests

## Security Features

### Binary Integrity
All released binaries include cryptographic checksums for verification:

**v1.0.0 Checksums:**
```
golden_seed_16.bin:
  SHA256: 87f829d95b15b08db9e5d84ff06665d077b267cfc39a5fa13a9e002b3e4239c5
  SHA512: 6c1e6ffdcfa8a1e4cfcfaeedb8b3b4f64a8de3d1b690e61e7ce48e80da9bcd7127bc890a3e74bb3d1c92bc5052b1076c0fe9b86eff210f497ecd0104eb544483

golden_seed_32.bin:
  SHA256: 096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f
  SHA512: fcfdc7392214fa5bc36c7a9edaa725fa366bb83f7bc2e4d5006688e4d0b07c56eea2c2d3fcb5fbf6c63e0217973d05ed358e7b8ad71df1812f1fb212c6ac8498

golden_seed.hex:
  SHA256: 9569db82634b232aebe75ef131dc00bdd033b8127dfcf296035f53434b6c2ccd
  SHA512: 6203cf0086ed52854deb4e6ba83ea1eba2054430ad7a9ee52510a6f730db7a122d96858c2f4d9ff657a0451d3a9ff36285b7d3f9454206fc0e20d7d6a2bb695f
```

### Verify Downloads
To verify the integrity of downloaded files:

**Linux/macOS:**
```bash
sha256sum -c <<EOF
87f829d95b15b08db9e5d84ff06665d077b267cfc39a5fa13a9e002b3e4239c5  golden_seed_16.bin
096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f  golden_seed_32.bin
9569db82634b232aebe75ef131dc00bdd033b8127dfcf296035f53434b6c2ccd  golden_seed.hex
EOF
```

**Python:**
```python
import hashlib

def verify_file(filepath, expected_sha256):
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_sha256
```

## Security Best Practices

### For Users
1. **Verify checksums** before using downloaded binaries
2. **Use from official releases** only (https://github.com/beanapologist/seed/releases)
3. **Keep your systems updated** to benefit from security patches
4. **Report suspicious behavior** through proper channels
5. **Use NIST PQC algorithms** when implementing post-quantum secure systems

### For Contributors
1. **Don't commit secrets** - use `.gitignore` for sensitive files
2. **Review code** before submitting pull requests
3. **Test thoroughly** - especially with different byte orders and platforms
4. **Document security implications** of changes
5. **Consider quantum-resistance** in cryptographic implementations

## NIST Post-Quantum Cryptography (PQC) Alignment

This project implements **production-ready hybrid key generation** aligned with NIST-approved Post-Quantum Cryptography standards:

### Supported NIST PQC Standards

- **NIST FIPS 203 (ML-KEM/Kyber)**: Key Encapsulation Mechanism
  - Kyber-512 (Level 1), Kyber-768 (Level 3), Kyber-1024 (Level 5)
  - Provides IND-CCA2 security under Module-LWE assumption
  
- **NIST FIPS 204 (ML-DSA/Dilithium)**: Digital Signature Algorithm
  - Dilithium2 (Level 2), Dilithium3 (Level 3), Dilithium5 (Level 5)
  - Provides EUF-CMA security under Module-LWE and Module-SIS assumptions
  
- **NIST FIPS 205 (SLH-DSA/SPHINCS+)**: Stateless Hash-Based Signatures
  - SPHINCS+-128f, SPHINCS+-192f, SPHINCS+-256f
  - Provides EUF-CMA security with only hash function security assumptions

### Hybrid Security Model

The system implements a **defense-in-depth approach**:

1. **Classical Component**: Deterministic keys from GCP-1 protocol (SHA-256 based)
   - Provides 128-bit quantum security against Grover's algorithm
   - Enables deterministic reproducibility for consensus systems
   
2. **PQC Component**: Quantum-resistant seed material for NIST algorithms
   - Full protection against Shor's and Grover's quantum attacks
   - Forward-compatible with post-quantum transition
   
3. **Hybrid Security**: System remains secure as long as **either** component is unbroken

### PQC Best Practices

#### For Users

1. **Use Hybrid Approach**: Always combine deterministic keys with PQC seeds
   ```python
   from gq import generate_kyber_seed
   det_key, pqc_seed = generate_kyber_seed(level=768, context=b"KEYGEN")
   ```

2. **Validate Seed Quality**: Check entropy before using PQC seeds
   ```python
   from gq import validate_pqc_seed_entropy
   metrics = validate_pqc_seed_entropy(pqc_seed)
   assert metrics['passes_basic_checks'], "Seed quality check failed"
   ```

3. **Use Context Binding**: Bind keys to specific use cases
   ```python
   key_exchange_seed = generate_kyber_seed(level=768, context=b"KEY_EXCHANGE")
   signature_seed = generate_dilithium_seed(level=3, context=b"SIGNATURE")
   ```

4. **Choose Appropriate Security Levels**:
   - Level 1 (Kyber-512, SPHINCS+-128f): Standard security
   - Level 3 (Kyber-768, Dilithium3): **Recommended** for most applications
   - Level 5 (Kyber-1024, Dilithium5): High security / long-term protection

5. **Test Against NIST Vectors**: Regularly validate compliance
   ```bash
   python -m unittest test_nist_pqc_vectors -v
   ```

6. **Use Certified Implementations**: Integrate with liboqs, PQClean, or other certified libraries

7. **Implement Key Rotation**: Follow NIST guidelines for key lifecycle management

#### For Contributors

1. **Maintain NIST Compliance**: All PQC-related changes must pass compliance tests
   ```bash
   python -m unittest test_nist_pqc -v
   python -m unittest test_nist_pqc_vectors -v
   ```

2. **Validate Entropy Quality**: Ensure all PQC seeds meet minimum entropy requirements
   - Shannon entropy ≥ 4.0 bits/byte for 32-byte seeds
   - Byte diversity ≥ 10%

3. **Document Security Properties**: Clearly state security assumptions and guarantees

4. **Follow NIST Guidelines**: 
   - NIST SP 800-208 for hash-based signatures
   - NIST FIPS 203-205 for algorithm parameters
   
5. **Test Determinism**: Verify reproducibility for consensus applications

6. **Check CI/CD**: Ensure NIST PQC compliance workflow passes
   - `.github/workflows/nist-pqc-compliance.yml`

### Security Testing

The project includes comprehensive security testing:

```bash
# Run all security tests
python -m unittest discover -p "test_*.py" -v

# Run NIST PQC specific tests
python -m unittest test_nist_pqc test_nist_pqc_vectors -v

# Check entropy quality
python -c "
from gq import generate_hybrid_key, PQCAlgorithm, validate_pqc_seed_entropy
_, seed = generate_hybrid_key(PQCAlgorithm.KYBER768)
metrics = validate_pqc_seed_entropy(seed)
print(f'Entropy: {metrics[\"shannon_entropy\"]:.2f} bits/byte')
print(f'Quality check: {\"PASS\" if metrics[\"passes_basic_checks\"] else \"FAIL\"}')
"
```

### Known Security Considerations

1. **Quantum Security Timeline**: While PQC algorithms are standardized, quantum computers capable of breaking classical crypto don't yet exist at scale. The hybrid approach provides protection now and in the future.

2. **Implementation Security**: This library provides **seed material** for PQC algorithms. Actual key generation, encryption, and signing must use certified PQC implementations (liboqs, PQClean, etc.).

3. **Side-Channel Attacks**: For hardware security modules (HSMs) and secure enclaves, ensure PQC implementations are resistant to timing and power analysis attacks.

4. **Key Management**: Follow NIST SP 800-57 for key management best practices in hybrid systems.

5. **Algorithm Agility**: Design systems to allow algorithm upgrades as NIST standards evolve.

### Reporting Security Issues

For security vulnerabilities in NIST PQC implementation:
1. Check if issue affects hybrid key generation or just integration patterns
2. Include NIST standard reference (FIPS 203, 204, or 205)
3. Provide test case demonstrating the issue
4. Suggest fixes aligned with NIST guidelines

## Release Signing

We sign release artifacts with GPG to provide provenance and integrity guarantees.

To enable automatic signing during GitHub Actions releases, add the following secret to the repository:

- `GPG_PRIVATE_KEY`: Base64-encoded ASCII-armored private key used to sign release artifacts.

The repository includes a workflow `.github/workflows/sign-release.yml` that:

- Generates `checksums.txt` (SHA256 + SHA512) for published assets using `scripts/generate_checksums.sh`.
- Imports the `GPG_PRIVATE_KEY` on the runner (if provided), creates an ASCII-armored detached signature `checksums.txt.sig`.
- Uploads `checksums.txt` and `checksums.txt.sig` to the GitHub Release.

If you prefer not to store a private key on GitHub, you can generate checksums locally and sign them yourself before uploading them to the release.

## No Warranties

This project is provided "as-is" without warranties or guarantees. Users are responsible for validating the appropriateness of this seed for their use cases, especially in security-critical applications.

## Acknowledgments

We appreciate responsible vulnerability disclosure and security research that helps improve this project.

---

**Last Updated:** December 30, 2025
