# Changelog

All notable changes to the Post-Quantum Secure Key Generation Multi-Language Compiler with deterministic keys and verified checksums.

## [4.0.0] - 2026-01-19

### BREAKING CHANGES

> **Note on version numbering**: Version 4.0.0 follows 2.0.0 directly. Version 3.0.0 was skipped to emphasize the severity of the breaking changes in this release and to clearly signal that this is a major departure from previous APIs and naming conventions.

Version 4.0.0 introduces major breaking changes to remove misleading quantum and cryptographic terminology and clarify that this is a deterministic PRNG (Pseudo-Random Number Generator) NOT suitable for cryptographic purposes.

#### Module Renames
- **`universal_qkd.py` → `stream_generator.py`**: The main module has been renamed to reflect its actual purpose as a stream generator rather than quantum key distribution
- **`nist_pqc.py` → `pqc_test_vectors.py`**: Clarified that PQC functionality is for test vector generation only

#### API Changes
- **Class renamed**: `UniversalQKD` → `GoldenStreamGenerator`
- **Function renamed**: `generate_keys()` → `generate_streams()`
- **Generator function renamed**: `universal_qkd_generator()` → `golden_stream_generator()`
- **Terminology update**: All references to "keys" changed to "streams" throughout the codebase

#### Terminology & Documentation
- Removed misleading "quantum" and "cryptography" claims from all documentation
- Package explicitly labeled as "PRNG (Pseudo-Random Number Generator)"
- Enhanced warnings: "NOT FOR CRYPTOGRAPHY" now includes specific examples (passwords, keys, tokens, etc.)
- Updated all docstrings and module descriptions to accurately describe functionality
- README updated to emphasize intended use cases (procedural generation, testing, simulations)

#### CLI Changes
- CLI commands updated to reflect new terminology
- Output headers now show "GoldenSeed PRNG" instead of quantum-related names

### Backward Compatibility

To ease migration, version 4.0.0 maintains backward compatibility through deprecated aliases:
- `UniversalQKD` is available as an alias for `GoldenStreamGenerator`
- `generate_universal_keys()` is available as an alias for `generate_streams()`

**Note**: These deprecated aliases will be removed in a future major version. Users should migrate to the new API names.

### Rationale

The previous naming (QKD, Universal Key Generator) implied cryptographic security and quantum properties that this package does not provide. This version removes all misleading terminology to accurately represent the package as a deterministic PRNG suitable for procedural content generation, reproducible testing, and simulations—but NOT for cryptographic use.

### Migration Guide

Update your imports and function calls:

**Before (v2.x and earlier):**
```python
from gq import UniversalQKD, generate_universal_keys

generator = UniversalQKD()
keys = generate_universal_keys(count=10)
```

**After (v4.0.0):**
```python
from gq import GoldenStreamGenerator, generate_streams

generator = GoldenStreamGenerator()
streams = generate_streams(count=10)
```

**Temporary compatibility (v4.0.0 only):**
```python
# Old names still work but are deprecated
from gq import UniversalQKD, generate_universal_keys  # Will be removed in v5.0.0
```

## [2.0.0] - 2026-01-04

### Major Release Highlights

This release represents a significant milestone in the evolution of the Post-Quantum Secure Key Generation system, introducing comprehensive multi-language support, full NIST PQC compliance, and advanced checksum capabilities. Version 2.0.0 positions this repository as a cutting-edge cryptographic toolset for developers worldwide.

### 🌐 Multi-Language Support

Complete Binary Fusion Tap implementations across all major programming languages:

- **Python** (3.6+) - Full type hints and production-ready
- **JavaScript** (Node.js + Browser) - ES6+ with BigInt support
- **TypeScript** - Strongly typed with comprehensive interfaces
- **Rust** - Memory-safe with zero-cost abstractions
- **Go** - Concurrent-ready with big.Int support
- **C** - High-performance native implementation
- **Java** - Enterprise-ready with BigInteger

**New in v2.0.0:**
- Unified API across all language implementations
- Language-specific documentation and examples in `examples/` directory
- Build and run scripts for each language
- Cross-language validation ensuring identical output
- Configuration files (package.json, Cargo.toml, Makefile, etc.)

### 🔐 NIST Post-Quantum Cryptography (PQC) Compliance

Full integration with NIST-approved post-quantum cryptographic standards:

#### CRYSTALS-Kyber (ML-KEM) - NIST FIPS 203
- **Kyber-512** (Security Level 1) - AES-128 equivalent
- **Kyber-768** (Security Level 3) - AES-192 equivalent  
- **Kyber-1024** (Security Level 5) - AES-256 equivalent

#### CRYSTALS-Dilithium (ML-DSA) - NIST FIPS 204
- **Dilithium2** (Security Level 2) - SHA-256 equivalent
- **Dilithium3** (Security Level 3) - AES-192 equivalent
- **Dilithium5** (Security Level 5) - AES-256 equivalent

#### SPHINCS+ (SLH-DSA) - NIST FIPS 205
- **SPHINCS+-128f** (Security Level 1) - Fast variant
- **SPHINCS+-192f** (Security Level 3) - Medium security
- **SPHINCS+-256f** (Security Level 5) - High security

**New in v2.0.0:**
- Production-ready hybrid key generation API
- `generate_kyber_seed()`, `generate_dilithium_seed()`, `generate_sphincs_seed()` convenience functions
- `PQCAlgorithm` enum for type-safe algorithm selection
- Seed length validation for each algorithm variant
- Security level mappings aligned with NIST standards
- Comprehensive NIST PQC integration guide (`examples/nist_pqc_integration.md`)
- Defense-in-depth security model combining classical and post-quantum approaches

### ✅ Enhanced Checksum Capabilities

Advanced checksum validation with arbitrary bit-strength support:

**New in v2.0.0:**
- Support for arbitrary bit-strength checksums (not limited to 256/512)
- Larger checksum validations for enhanced integrity verification
- SHA-256 and SHA-512 checksum support across all operations
- Integrated checksum verification in all key generation functions
- Checksum validation for seed values and manifested states
- Binary representation verification tool with comprehensive checksums

### 🔄 Ratcheting and Forward Security

Infinite stream generation with cryptographic ratcheting:

**New in v2.0.0:**
- Forward secrecy via state progression and ratcheting mechanisms
- Infinite key stream generation with `generate_hybrid_key_stream()`
- Deterministic state advancement ensuring synchronized key generation
- XOR folding for key hardening
- Basis-matching simulation (~50% efficiency as in real QKD)
- Cryptographic state isolation preventing backward computation

### 🔀 Legacy and Hybrid Support

Comprehensive support for classical and hybrid quantum-classical systems:

**New in v2.0.0:**
- Hybrid key generation combining deterministic keys (GCP-1) with PQC seed material
- Defense-in-depth model: security holds if *either* component remains secure
- Classical security via SHA-256 based deterministic keys
- Quantum resistance via NIST PQC seed generation
- Forward compatibility for post-quantum transition
- Legacy system support through deterministic key generation
- Universal compatibility across all modern architectures

### 📚 Documentation Updates

Complete documentation overhaul for v2.0.0:

- Updated README.md with comprehensive NIST PQC integration examples
- New `examples/nist_pqc_integration.md` guide with integration patterns
- Language-specific guides for all 7 supported languages
- API documentation for hybrid key generation functions
- Security model documentation
- Test vector generation guides
- Cross-language validation examples

### 🏷️ Repository Tags and Discoverability

Enhanced repository metadata for better discoverability:

**Updated tags:**
- `quantum-key-distribution`, `deterministic-key`, `checksum`
- `pqc`, `nist-standards`, `quantum-security`
- `kyber`, `dilithium`, `SPHINCS+`
- `multi-language`, `cryptography`, `hybrid-cryptography`
- `forward-secrecy`, `ratcheting`, `infinite-stream`

### 🧪 Test Coverage

Comprehensive test suite for v2.0.0:

- 18+ tests for NIST PQC hybrid key generation (`test_nist_pqc.py`)
- NIST test vectors validation (`test_nist_pqc_vectors.py`)
- Binary verification tests (`test_binary_verification.py`)
- Large seed verification (`test_large_seed_verification.py`)
- Universal QKD tests (`test_universal_qkd.py`)
- Cross-language validation tests
- Entropy quality validation tests
- Security level mapping tests

### 🚀 Performance & Production Readiness

- Zero external dependencies for maximum security
- Production-grade error handling
- Type-safe interfaces across all languages
- Memory-safe implementations (Rust)
- Concurrent-ready implementations (Go)
- Enterprise-ready implementations (Java)
- Browser-compatible implementations (JavaScript/TypeScript)

### Migration from v1.0.0

Version 2.0.0 is fully backward compatible with v1.0.0:

- All v1.0.0 APIs remain functional
- Original key generation methods unchanged
- Existing integrations continue to work
- New PQC features are opt-in additions

### Known Limitations

- SPHINCS+ implementations require more memory than Kyber/Dilithium
- Large key batch generation may require adequate system resources
- Some languages may have varying performance characteristics

## [1.0.0] - 2026-01-03

### Added
- **Post-Quantum Secure Key Generation System**: Complete implementation with deterministic keys and quantum-resistant security
- **Multi-Language Compiler**: Generate Binary Fusion Tap implementations in 7 languages
  - Python (3.6+)
  - JavaScript (Node.js + Browser)
  - TypeScript (with full type definitions)
  - Rust (memory-safe, zero-cost)
  - Go (concurrent-ready)
  - C (high-performance native)
  - Java (enterprise-ready)

- **Key Generator Service**:
  - Three algorithms: Fusion, Hash, Hybrid
  - Deterministic key generation with verified checksums
  - Configurable key lengths: 128, 256, 512 bits
  - Batch generation
  - JSON/Text output
  - SHA256 checksum validation
  - **NIST PQC Compatible**: Suitable for use with Kyber, Dilithium, FrodoKEM
  - 19 comprehensive unit tests

- **K-Value Explorer**:
  - Analyze Binary Fusion Tap across any k range
  - Visual bit length growth charts
  - Identify special k values (Fibonacci, power-of-2, max ZPE)
  - JSON export for analysis
  - Detailed mode for deep inspection

- **Binary Verification Tool**:
  - Verify binary representations with checksums
  - 8-fold Heartbeat operation
  - ZPE Overflow extraction
  - SHA256/SHA512 checksum support
  - 18 unit tests

- **Release System**:
  - Automated release generation
  - Language-specific READMEs
  - Build/run scripts for each language
  - Configuration files (package.json, Cargo.toml, etc.)
  - Master documentation

### Features

**Binary Fusion Tap Algorithm (Post-Quantum Secure Core):**
1. Seed Generation: Concatenate 1,2,3,...,k (deterministic)
2. 8-fold Heartbeat: Bit-shift left by 3 (×8 multiplication)
3. Phase Offset: Add k parameter for phase alignment
4. ZPE Overflow: XOR extraction for k ≥ 10 (entropy extraction)
5. Checksum Verification: SHA256/SHA512 integrity validation

**Applications:**
- **Post-Quantum Cryptography** - Primary use case, NIST PQC integration
- Secure key generation with verified checksums (Kyber, Dilithium, FrodoKEM compatible)
- Protocol verification and compliance testing
- Quantum-resistant cryptography research
- Deterministic tie-breaking in distributed systems
- API key generation for SaaS platforms
- Cross-platform deterministic systems

### Technical Details

**Key Metrics (k=11):**
- Seed Value: 1234567891011
- Bit Length: 41 → 44 (after heartbeat)
- ZPE Overflow: 59 (0b111011)
- Manifested: 9876543128099

**Test Coverage:**
- 56 total unit tests across all components
- 100% pass rate
- Covers all algorithms and languages
- Integration and unit tests

**Performance:**
- C implementation: Native performance
- Rust: Zero-cost abstractions
- Go: Concurrent-ready
- All implementations produce identical output

### Documentation
- Comprehensive README.md
- Language-specific guides
- API documentation
- Examples for all languages
- Build instructions
- Usage examples

## [Unreleased]

### Planned
- WebAssembly compilation target
- Python package distribution (PyPI)
- npm package for JavaScript/TypeScript
- Cargo crate for Rust
- More k-value analysis tools
- Performance benchmarks
- Additional test vectors

---

Format based on [Keep a Changelog](https://keepachangelog.com/)
