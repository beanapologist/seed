# Quantum-Safe Cryptography Security Checklist

This checklist ensures that post-quantum cryptographic implementations follow best practices and security standards. Use this guide when implementing, reviewing, or deploying quantum-resistant cryptographic systems.

## 1. Algorithm Selection

### NIST-Approved Algorithms ✅

- [ ] **Use only NIST-standardized algorithms**
  - ✅ Kyber-512/768/1024 (NIST FIPS 203 - ML-KEM)
  - ✅ Dilithium2/3/5 (NIST FIPS 204 - ML-DSA)
  - ✅ SPHINCS+-128f/192f/256f (NIST FIPS 205 - SLH-DSA)
  - ✅ Falcon-512/1024 (NIST approved)
  
- [ ] **Choose appropriate security levels**
  - Level 1 (128-bit): Standard applications
  - Level 3 (192-bit): **Recommended** for most use cases
  - Level 5 (256-bit): High-security, long-term protection

- [ ] **Avoid deprecated algorithms**
  - ❌ Non-standardized PQC algorithms
  - ❌ Classical-only cryptography for new long-term systems
  - ❌ Algorithms without NIST approval

### Security Level Recommendations

| Use Case | Recommended Algorithm | Security Level |
|----------|----------------------|----------------|
| Standard web traffic | Kyber-512 | Level 1 |
| Financial transactions | Kyber-768, Dilithium3 | Level 3 |
| Government/Military | Kyber-1024, Dilithium5 | Level 5 |
| Long-term archival | SPHINCS+-256f | Level 5 |

## 2. Implementation Security

### Library Selection

- [ ] **Use certified implementations**
  - ✅ liboqs (Open Quantum Safe)
  - ✅ PQClean
  - ✅ NIST reference implementations
  - ❌ Custom/unaudited implementations

- [ ] **Keep libraries updated**
  - Check for security updates monthly (automate via Dependabot or Renovate)
  - Monitor CVE databases (subscribe to https://nvd.nist.gov/)
  - Subscribe to security mailing lists (liboqs-discuss@openquantumsafe.org)
  - Current liboqs version: 0.10.1 (check https://github.com/open-quantum-safe/liboqs/releases)
  - Automated version check: Run `curl -s https://api.github.com/repos/open-quantum-safe/liboqs/releases/latest | grep tag_name`

### Code Quality

- [ ] **Memory safety**
  - Check all memory allocations
  - Free all allocated memory
  - Use safe string functions
  - Avoid buffer overflows
  - Zero sensitive memory after use

- [ ] **Error handling**
  - Check return values from all crypto operations
  - Handle failures gracefully
  - Don't expose cryptographic errors to attackers
  - Log security events appropriately

- [ ] **Input validation**
  - Validate all key sizes
  - Verify ciphertext lengths
  - Check algorithm parameters
  - Sanitize user inputs

### Example: Secure Memory Handling
```c
// ✅ Good: Check allocation and zero memory
uint8_t *secret_key = malloc(kem->length_secret_key);
if (!secret_key) {
    fprintf(stderr, "Memory allocation failed\n");
    return ERROR;
}

// ... use the key ...

// Zero memory before freeing
memset(secret_key, 0, kem->length_secret_key);
free(secret_key);

// ❌ Bad: No checks, memory leak
uint8_t *secret_key = malloc(kem->length_secret_key);
// ... use without checking if NULL ...
// Memory not zeroed before free
```

## 3. Hybrid Cryptography

### Hybrid Approach (Defense-in-Depth)

- [ ] **Combine classical and PQC**
  - Classical component (RSA, ECDH, AES)
  - PQC component (Kyber, Dilithium)
  - System secure if either component is unbroken

- [ ] **Proper key derivation**
  - Use KDF to combine keys securely
  - Don't simply concatenate or XOR
  - Follow NIST SP 800-56C guidelines

### Example: Hybrid Key Exchange
```python
# ✅ Good: Hybrid approach
from gq import generate_kyber_seed

# Get PQC seed
det_key, pqc_seed = generate_kyber_seed(level=768, context=b"KEYGEN")

# Use with classical crypto
classical_key = ecdh_key_exchange()
combined_key = kdf(classical_key + pqc_seed)

# ❌ Bad: PQC only (no defense-in-depth)
pqc_key = kyber_key_exchange_only()
```

## 4. Key Management

### Key Generation

- [ ] **Use cryptographically secure random number generators**
  - ✅ /dev/urandom on Linux
  - ✅ CryptGenRandom on Windows
  - ✅ Python `secrets` module
  - ❌ `rand()`, `random()`, or time-based seeds

- [ ] **Seed quality validation**
  - Shannon entropy ≥ 4.0 bits/byte for 32-byte seeds
  - Byte diversity ≥ 10%
  - Statistical randomness tests

- [ ] **Context binding**
  - Bind keys to specific use cases
  - Use domain separation
  - Include version/algorithm identifiers

### Key Storage

- [ ] **Protect private keys**
  - Encrypt at rest
  - Use hardware security modules (HSMs) when available
  - Implement access controls
  - Audit key access

- [ ] **Key lifecycle management**
  - Define key rotation schedule
  - Plan for algorithm migration
  - Implement key expiration
  - Secure key destruction

### Key Rotation Schedule

| Key Type | Rotation Period |
|----------|----------------|
| Session keys | Per-session |
| TLS certificates | 90 days |
| Long-term signing keys | 1-2 years |
| Root CA keys | 5+ years |

## 5. Testing and Validation

### Functional Testing

- [ ] **Verify key exchange success**
  - Both parties derive same shared secret
  - Test with known test vectors
  - Cross-implementation validation

- [ ] **Test error conditions**
  - Invalid keys
  - Corrupted ciphertexts
  - Wrong algorithm parameters
  - Memory allocation failures

### Security Testing

- [ ] **Test vector compliance**
  - NIST official test vectors
  - KAT (Known Answer Tests)
  - Cross-platform consistency

- [ ] **Fuzzing**
  - Fuzz public inputs (public keys, ciphertexts)
  - Test malformed data handling
  - Verify no crashes or memory leaks

### Performance Testing

- [ ] **Measure cryptographic operations**
  - Key generation time
  - Encapsulation/decapsulation time
  - Signature generation/verification time
  - Memory usage

### Test Coverage Requirements

- Minimum 80% code coverage
- 100% coverage of error paths
- All security-critical functions tested
- Integration tests with real scenarios

## 6. Operational Security

### Deployment

- [ ] **TLS/Network security**
  - Use hybrid TLS 1.3 with PQC
  - Enable perfect forward secrecy
  - Validate certificates properly
  - Monitor for downgrade attacks

- [ ] **Access controls**
  - Principle of least privilege
  - Role-based access control
  - Audit logging
  - Intrusion detection

### Monitoring

- [ ] **Security monitoring**
  - Log all cryptographic operations
  - Monitor for unusual patterns
  - Alert on failures
  - Track key usage

- [ ] **Performance monitoring**
  - CPU usage
  - Memory consumption
  - Operation latency
  - Throughput

## 7. Side-Channel Protection

### Timing Attacks

- [ ] **Constant-time operations**
  - Key generation
  - Decapsulation
  - Signature verification
  - All secret-dependent branches

- [ ] **Avoid timing leaks**
  - No secret-dependent array indices
  - No secret-dependent memory access patterns
  - Use constant-time comparison functions

### Power Analysis

- [ ] **Hardware protection** (for embedded/HSM)
  - Random delays
  - Power noise injection
  - Masked operations
  - Secure hardware modules

### Cache Attacks

- [ ] **Cache-timing resistance**
  - Avoid secret-dependent table lookups
  - Use cache-oblivious algorithms
  - Clear cache after sensitive operations

## 8. Documentation

### Code Documentation

- [ ] **Document all security assumptions**
- [ ] **Explain algorithm choices**
- [ ] **Provide usage examples**
- [ ] **Document error conditions**
- [ ] **Include performance characteristics**

### Security Documentation

- [ ] **Security policy**
- [ ] **Threat model**
- [ ] **Security architecture**
- [ ] **Incident response plan**
- [ ] **Vulnerability disclosure policy**

### User Documentation

- [ ] **Integration guide**
- [ ] **Configuration options**
- [ ] **Best practices**
- [ ] **Common pitfalls**
- [ ] **Troubleshooting guide**

## 9. Compliance

### Standards Compliance

- [ ] **NIST FIPS 203** (ML-KEM/Kyber)
- [ ] **NIST FIPS 204** (ML-DSA/Dilithium)
- [ ] **NIST FIPS 205** (SLH-DSA/SPHINCS+)
- [ ] **NIST SP 800-56C** (Key derivation)
- [ ] **NIST SP 800-57** (Key management)

### Industry Standards

- [ ] **PCI DSS** (if applicable)
- [ ] **HIPAA** (if applicable)
- [ ] **GDPR** (if applicable)
- [ ] **FedRAMP** (if applicable)

## 10. Maintenance

### Regular Reviews

- [ ] **Quarterly security audits**
- [ ] **Annual penetration testing**
- [ ] **Continuous dependency monitoring**
- [ ] **Code review for all changes**

### Update Procedures

- [ ] **Security patch process**
- [ ] **Algorithm migration plan**
- [ ] **Backward compatibility strategy**
- [ ] **Rollback procedures**

### Incident Response

- [ ] **Security incident response plan**
- [ ] **Breach notification procedures**
- [ ] **Forensics capability**
- [ ] **Recovery procedures**

## 11. Project-Specific Checklist

### OQS Integration

- [x] liboqs v0.10.1 integrated and tested
- [x] Kyber-768 key exchange implemented
- [x] GitHub Actions CI/CD configured
- [x] Documentation complete
- [x] Python NIST PQC compatibility verified
- [x] Hybrid key generation available
- [ ] Dilithium signature test (future)
- [ ] SPHINCS+ signature test (future)
- [ ] Performance benchmarks (future)

### Python Integration

- [x] NIST PQC module (`src/gq/nist_pqc.py`)
- [x] Hybrid key generation functions
- [x] Entropy validation
- [x] Context binding
- [x] Test vectors validated
- [x] All algorithms supported

## Security Review Sign-Off

| Component | Reviewer | Date | Status |
|-----------|----------|------|--------|
| OQS Integration | | | ⏳ Pending |
| Kyber Test | | | ⏳ Pending |
| Python NIST PQC | | | ✅ Verified |
| Documentation | | | ✅ Complete |
| CI/CD Pipeline | | | ✅ Working |

## References

### NIST Resources
- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [FIPS 203 - ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- [FIPS 204 - ML-DSA](https://csrc.nist.gov/pubs/fips/204/final)
- [FIPS 205 - SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final)

### Implementation Guides
- [liboqs Documentation](https://github.com/open-quantum-safe/liboqs/wiki)
- [OQS Project](https://openquantumsafe.org/)
- [PQClean](https://github.com/PQClean/PQClean)

### Security Best Practices
- [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Version**: 1.0  
**Last Updated**: January 5, 2026  
**Next Review**: April 5, 2026
