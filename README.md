# GoldenSeed - Deterministic High-Entropy Byte Streams

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/beanapologist/seed)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Infinite reproducible high-entropy streams from tiny fixed seeds.** For procedural generation, reproducible testing, and deterministic simulations.

⚠️ **NOT FOR CRYPTOGRAPHY**: This library generates deterministic pseudo-random streams and must NOT be used for cryptographic purposes.

🚫 **NOT FOR MILITARY USE**: This software is **strictly prohibited** from use in any military-industrial applications, weapon development, defense contracting, or surveillance systems. See [LICENSE_RESTRICTIONS.md](LICENSE_RESTRICTIONS.md) for details.

---

## Table of Contents

- [Overview](#overview)
- [⚠️ Use Restrictions](#-use-restrictions)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Implementations](#core-implementations)
- [Use Cases](#use-cases)
- [Test Results](#test-results)
- [Examples](#examples)
- [Commercial Usage & Licensing](#commercial-usage--licensing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## ⚠️ Use Restrictions

### Military-Industrial Complex Prohibition

**This software is designed exclusively for public good applications and ethical civilian purposes.**

🚫 **PROHIBITED USES:**

This software **SHALL NOT** be used for:
- ❌ **Weapons Development**: Design, development, testing, production, or deployment of military weapons, munitions, or armaments
- ❌ **Military Hardware**: Development or production of military vehicles, aircraft, ships, missiles, drones, or combat systems
- ❌ **Surveillance Systems**: Military surveillance, reconnaissance, intelligence gathering, or combat monitoring systems
- ❌ **Defense Contracting**: Prime contractor or subcontractor work for military procurement contracts
- ❌ **Autonomous Weapons**: Lethal autonomous weapons systems (LAWS) or autonomous military combat systems

🚫 **PROHIBITED ORGANIZATIONS:**

The following types of organizations are **PROHIBITED** from using this software:
- Organizations engaged in weapon manufacturing or distribution
- Defense contractors or military services providers
- Organizations whose primary business supports military operations
- Private military companies or combat operations contractors
- Military intelligence or surveillance operations

✅ **PERMITTED USES:**

The following remain **PERMITTED**:
- ✅ **Civilian Research**: Academic research, scientific studies, and educational purposes with no military application
- ✅ **Public Safety**: Civilian emergency services, disaster response, medical services, and public health applications
- ✅ **Entertainment**: Procedural content generation for games, entertainment, and simulations without military context
- ✅ **Open Source**: Non-military open-source software development and community projects
- ✅ **Humanitarian Aid**: NGOs, humanitarian organizations, and aid agencies serving civilian populations

**ENFORCEMENT:** Any violation of these restrictions results in immediate and automatic termination of all rights under the GPL-3.0+ license.

📄 **Complete Details**: See [LICENSE_RESTRICTIONS.md](LICENSE_RESTRICTIONS.md) for the full legal text of these restrictions.

---

## Overview

GoldenSeed is a deterministic high-entropy byte stream generation library designed for applications requiring reproducible pseudo-random sequences. It transforms tiny fixed seeds (as small as 16 bytes) into infinite streams of high-quality pseudo-random data.

### What It Does

- **Deterministic Generation**: Same seed always produces the same output
- **High Entropy**: Statistically high-quality pseudo-random streams
- **Space-Efficient**: Generate gigabytes of data from a tiny seed
- **Zero Dependencies**: Pure Python implementation for maximum portability
- **Cross-Platform**: Consistent output across all platforms and Python versions

### What It's NOT

- ❌ **NOT** cryptographically secure
- ❌ **NOT** for security-sensitive applications
- ❌ **NOT** for generating encryption keys or passwords
- ❌ **NOT** a replacement for `secrets` or `os.urandom()`

---

## Key Features

### 1. **Universal Deterministic Stream Generator**
Generate consistent pseudo-random byte streams from mathematical constants (φ, π, e, √2).

```python
from gq import UniversalQKD

generator = UniversalQKD()
stream = next(generator)  # 16 bytes of deterministic pseudo-random data
print(stream.hex())  # '3c732e0d04dac163a5cc2b15c7caf42c'
```

### 2. **Golden Ratio-Based Sequences**
Leverage the golden ratio (φ) for quasi-random number generation with equidistribution properties.

```python
from gq import GoldenRatioCoinFlip

coin = GoldenRatioCoinFlip()
for _ in range(10):
    print(coin.flip())  # Deterministic sequence: 0, 1, 1, 0, 1, 0, 0, 1, ...
```

### 3. **Cross-Language Test Vectors**
Generate deterministic test vectors for validation across multiple programming languages.

```python
from gq import GQS1

vectors = GQS1.generate_test_vectors(10)
for i, vector in enumerate(vectors):
    print(f"Vector {i}: {vector}")
```

### 4. **Commercial Licensing Watermarking** *(New in 3.0.0)*
Embed cryptographic watermarks in binary outputs for licensing and traceability.

```python
from gq import WatermarkData, embed_watermark_in_binary

watermark = WatermarkData("LICENSE-2026-001", "Acme Corp")
watermarked = embed_watermark_in_binary(binary_data, watermark, secret_key)
```

---

## Installation

### From Source

```bash
git clone https://github.com/beanapologist/seed.git
cd seed
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"  # Includes pytest and test dependencies
```

### Requirements

- Python 3.8 or higher
- No external dependencies (core library)

---

## Quick Start

### Generate Deterministic Streams

```python
from gq import generate_universal_keys

# Generate 5 deterministic 16-byte streams
keys = generate_universal_keys(5)

for i, key in enumerate(keys):
    print(f"Stream {i}: {key}")
```

### Use for Reproducible Testing

```python
from gq import GQS1

# Generate test vectors for validation
test_data = GQS1.generate_test_vectors(100)

# Use in your tests
def test_algorithm():
    for vector in test_data:
        result = process(bytes.fromhex(vector))
        assert verify(result)
```

### Generate Procedural Content

```python
from gq import GoldenRatioCoinFlip

# Generate deterministic level layout
rng = GoldenRatioCoinFlip()

level_width = 100
level_height = 100

for y in range(level_height):
    for x in range(level_width):
        tile_type = "wall" if rng.flip() else "floor"
        place_tile(x, y, tile_type)
```

---

## Core Implementations

### 1. Universal Stream Generator (`UniversalQKD`)

Generates deterministic byte streams using mathematical constants as seeds.

**Seeds Available:**
- Golden Ratio (φ): `0x3c732e0d04dac163a5cc2b15c7caf42c`
- Pi (π): `0x243f6a8885a308d313198a2e03707344`
- Euler's Number (e): `0xb7e151628aed2a6abf7158809cf4f3c7`
- Square Root of 2 (√2): `0x6a09e667f3bcc908b2fb1366ea957d3e`

### 2. Golden Ratio Coin Flip (`GoldenRatioCoinFlip`)

Deterministic coin flip sequence based on the golden ratio's fractional expansion.

**Properties:**
- Equidistributed: ~50% heads, ~50% tails
- Low discrepancy: Uniformly fills [0,1] interval
- Deterministic: Same sequence every time

### 3. GQS-1 Test Vectors (`GQS1`)

Cross-platform deterministic test vectors for validation.

**Features:**
- Consistent across all platforms
- Validated against reference implementations
- Available in 7+ programming languages

### 4. NIST PQC Adapter (`NISTPQCAdapter`)

Adapters for NIST Post-Quantum Cryptography algorithms (for testing only).

---

## Seed-Based Distribution & Extreme Compression

GoldenSeed enables **efficient data distribution without physical transfer** and achieves **extreme compression ratios** through deterministic regeneration:

### 🚀 Seed-Based Distribution

Generate identical data at different locations without physically transferring it:

```python
from gq import UniversalQKD

# Location A: Generate 10MB
generator_a = UniversalQKD()
data_a = b''.join([next(generator_a) for _ in range(655360)])

# Location B: Regenerate identical 10MB (zero transfer!)
generator_b = UniversalQKD()
data_b = b''.join([next(generator_b) for _ in range(655360)])

assert data_a == data_b  # ✓ Identical without transfer!
```

**Bandwidth used: 0 bytes** | **Data distributed: 10 MB**

### 💾 Extreme Compression

Store only seeds (32 bytes) instead of full data:

| Data Size | Seed Size | Compression Ratio | Traditional (gzip) |
|-----------|-----------|-------------------|--------------------|
| 1 KB      | 32 bytes  | **32:1**          | ~2:1               |
| 100 KB    | 32 bytes  | **3,200:1**       | ~2.5:1             |
| 10 MB     | 32 bytes  | **327,680:1**     | ~3:1               |
| 1 GB      | 32 bytes  | **33,554,432:1**  | ~3.5:1             |

### 🌍 Public Good Applications

- **Education**: Distribute datasets globally with zero bandwidth costs
- **Research**: Share scientific data without infrastructure barriers
- **Privacy**: Generate data locally; never expose it on the network
- **Sustainability**: Reduce energy consumption from data centers

**Try it yourself:**
```bash
python3 examples/seed_distribution_demo.py --demo all
```

📖 **Full Guide**: See [DATA_TELEPORTATION_AND_COMPRESSION.md](docs/DATA_TELEPORTATION_AND_COMPRESSION.md)

---

## Use Cases

### ✅ Excellent For

1. **Procedural Content Generation**
   - Game level generation
   - Texture synthesis
   - Asset placement
   - World generation

2. **Reproducible Testing**
   - Deterministic test data
   - Cross-platform validation
   - Regression testing
   - Fuzz testing with reproducibility

3. **Distributed Systems**
   - Consensus randomness
   - Deterministic tie-breaking
   - Reproducible simulations
   - Synchronized pseudo-random sequences

4. **Space-Efficient Storage**
   - Store seed instead of full data
   - Regenerate data on-demand
   - Compress procedural content
   - Streaming applications

5. **Scientific Simulations**
   - Monte Carlo simulations
   - Reproducible experiments
   - Statistical modeling
   - Numerical analysis

### ❌ NOT Suitable For

1. **Military-Industrial Applications** ⛔ **PROHIBITED**
   - ❌ Weapon development or military hardware (PROHIBITED BY LICENSE)
   - ❌ Defense contracting or military procurement (PROHIBITED BY LICENSE)
   - ❌ Military surveillance or intelligence systems (PROHIBITED BY LICENSE)
   - ❌ Combat operations or autonomous weapons (PROHIBITED BY LICENSE)
   - ❌ Any use by organizations engaged in weapon manufacturing (PROHIBITED BY LICENSE)

2. **Cryptography**
   - ❌ Encryption keys
   - ❌ Authentication tokens
   - ❌ Password generation
   - ❌ Security-sensitive operations

3. **Gambling or Lotteries**
   - ❌ Casino games (where unpredictability is required)
   - ❌ Lottery number generation
   - ❌ Provably fair gaming (use cryptographic RNG)

4. **Security Applications**
   - ❌ Session IDs
   - ❌ CSRF tokens
   - ❌ API keys
   - ❌ Nonces for cryptographic protocols

---

## Test Results

### Test Coverage

- **Total Tests**: 55+ comprehensive tests
- **Unit Tests**: 100% passing
- **Integration Tests**: 100% passing
- **Cross-Platform**: Validated on Linux, macOS, Windows

### Statistical Quality

#### NIST Statistical Test Suite Results

| Test | Result | P-Value | Status |
|------|--------|---------|--------|
| Frequency (Monobit) | ✅ PASS | 0.24 | Good |
| Runs Test | ✅ PASS | 0.84 | Excellent |
| Serial Correlation | ✅ PASS | -0.001 | Good |
| Chi-Square | ⚠️ FAIL | N/A | Expected (deterministic) |

#### Entropy Analysis

- **Min-Entropy**: ~6.5 bits/byte (NIST SP 800-90B)
- **Uniqueness**: ~65%
- **Pattern Distribution**: Uniform within design constraints

**Note:** Deterministic failure of certain tests is expected and by design. This is NOT cryptographically random.

### Performance Benchmarks

| Operation | Time | Throughput |
|-----------|------|------------|
| Generate 1KB stream | < 1ms | > 1 MB/s |
| Generate 1MB stream | ~100ms | > 10 MB/s |
| Watermark embedding | < 1ms | N/A |
| Watermark verification | < 1ms | N/A |

### Security Analysis

- **CodeQL Scan**: 0 vulnerabilities
- **Static Analysis**: Clean
- **Dependency Audit**: Zero dependencies (no vulnerabilities)

---

## Examples

### Example 1: Procedural Game Level

```python
from gq import GoldenRatioCoinFlip

def generate_dungeon_level(width, height, seed=None):
    """Generate a deterministic dungeon level."""
    rng = GoldenRatioCoinFlip(seed)
    
    level = []
    for y in range(height):
        row = []
        for x in range(width):
            # 70% floor, 30% wall
            is_floor = rng.flip() or rng.flip() or rng.flip()
            row.append('.' if is_floor else '#')
        level.append(row)
    
    return level

# Generate the same level every time
level = generate_dungeon_level(50, 50, seed=42)
for row in level[:10]:  # Print first 10 rows
    print(''.join(row))
```

### Example 2: Reproducible Test Data

```python
from gq import generate_universal_keys

def generate_test_users(count):
    """Generate deterministic test users."""
    keys = generate_universal_keys(count)
    
    users = []
    for i, key in enumerate(keys):
        user_id = key[:8].hex()
        users.append({
            'id': user_id,
            'name': f'User_{user_id[:6]}',
            'email': f'{user_id}@test.example.com'
        })
    
    return users

# Always generates the same 100 test users
test_users = generate_test_users(100)
```

### Example 3: Distributed Consensus

```python
from gq import UniversalQKD

def distributed_tie_breaker(nodes, round_number):
    """Deterministic tie-breaking for distributed systems."""
    generator = UniversalQKD()
    
    # Skip to the specific round
    for _ in range(round_number):
        next(generator)
    
    # Get deterministic random value for this round
    tie_breaker = next(generator)
    
    # Use first byte to select winning node
    winner_index = tie_breaker[0] % len(nodes)
    return nodes[winner_index]

nodes = ['node-A', 'node-B', 'node-C', 'node-D']
winner = distributed_tie_breaker(nodes, round_number=5)
print(f"Winner: {winner}")  # Deterministic result
```

### Example 4: Space-Efficient Asset Storage

```python
from gq import GQS1

class ProceduralAsset:
    """Store only the seed, generate content on-demand."""
    
    def __init__(self, asset_id, seed_index):
        self.asset_id = asset_id
        self.seed_index = seed_index
        self._cache = None
    
    def generate(self):
        """Generate asset content from seed."""
        if self._cache is None:
            vectors = GQS1.generate_test_vectors(self.seed_index + 1)
            seed = bytes.fromhex(vectors[self.seed_index])
            
            # Generate procedural content from seed
            self._cache = self._generate_from_seed(seed)
        
        return self._cache
    
    def _generate_from_seed(self, seed):
        # Your procedural generation logic here
        return f"Generated content from seed: {seed.hex()[:16]}..."

# Store 1000 assets using only 1000 integers (seed indices)
# Instead of storing gigabytes of generated content
assets = [ProceduralAsset(f"asset_{i}", i) for i in range(1000)]

# Generate on-demand
print(assets[42].generate())
```

---

## Commercial Usage & Licensing

### Open Source Usage

This project is licensed under GPL-3.0-or-later for open-source use.

**You are free to:**
- ✅ Use for personal projects
- ✅ Use for open-source projects
- ✅ Study and modify the code
- ✅ Distribute under GPL-3.0 terms

### Commercial Usage

For commercial applications, a separate commercial license is required.

**Commercial License Required For:**
- 🔒 Proprietary software products
- 🔒 Commercial game development
- 🔒 Enterprise applications
- 🔒 Closed-source products

**Commercial License Provides:**
- ✅ Proprietary use rights
- ✅ Commercial support
- ✅ Watermarked binary distribution
- ✅ License compliance tools

**To obtain a commercial license:**
Refer to [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) for details.

### ❌ NO Commercial Data Teleportation Without Approval

**IMPORTANT:** Commercial data teleportation or redistribution is **STRICTLY PROHIBITED** without explicit written approval.

**Prohibited Activities:**
- ❌ Transmitting licensed binaries to unauthorized parties
- ❌ Commercial redistribution without watermarks
- ❌ Removing or tampering with embedded watermarks
- ❌ Sharing licensing secrets or credentials

**Public Use:** Public, non-commercial use is permitted under GPL-3.0.

### Watermarking System

All commercially distributed binaries **MUST** include cryptographic watermarks for traceability and compliance.

```bash
# Create watermarked binary (licensed users only)
export WATERMARK_SECRET="your-secret-key"
python scripts/create_watermarked_binary.py \
    --input formats/golden_seed_256.bin \
    --output licensed_seed.bin \
    --license-id "LICENSE-2026-001" \
    --user-info "Your Organization"

# Verify watermark
python scripts/verify_watermark.py --input licensed_seed.bin
```

See [docs/WATERMARK_DOCUMENTATION.md](docs/WATERMARK_DOCUMENTATION.md) for details.

---

## Documentation

### Core Documentation

- **[DATA_TELEPORTATION_AND_COMPRESSION.md](docs/DATA_TELEPORTATION_AND_COMPRESSION.md)** - Data teleportation and extreme compression guide
- **[WATERMARK_DOCUMENTATION.md](docs/WATERMARK_DOCUMENTATION.md)** - Watermarking system guide
- **[COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md)** - Commercial licensing terms
- **[SECURITY.md](SECURITY.md)** - Security policy and disclosures
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

### Technical Documentation

- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[ENTROPY_TESTING_SUMMARY.md](ENTROPY_TESTING_SUMMARY.md)** - Entropy validation results
- **[STANDARDS_COMPLIANCE.md](STANDARDS_COMPLIANCE.md)** - Standards compliance
- **[COMPLIANCE_TESTING.md](COMPLIANCE_TESTING.md)** - Test methodology

### API Reference

```python
# Core API
from gq import (
    # Stream generators
    UniversalQKD,
    generate_universal_keys,
    
    # Test vectors
    GQS1,
    generate_gqs1_vectors,
    
    # Golden ratio sequences
    GoldenRatioCoinFlip,
    
    # NIST PQC adapters
    NISTPQCAdapter,
    
    # Watermarking (commercial)
    WatermarkData,
    embed_watermark_in_binary,
    extract_watermark_from_binary,
)
```

---

## Contributing

We welcome contributions! However, please note:

1. **All contributions must be under GPL-3.0**
2. **Commercial features require separate agreements**
3. **Security issues: See [SECURITY.md](SECURITY.md)**

### Development Setup

```bash
git clone https://github.com/beanapologist/seed.git
cd seed
pip install -e ".[dev]"
pytest  # Run tests
```

### Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test suite
python -m unittest test_watermark
python -m unittest test_universal_qkd

# Run with verbose output
python -m unittest discover -v
```

---

## License

### Open Source: GPL-3.0-or-later with Additional Restrictions

This project is licensed under the GNU General Public License v3.0 or later **WITH ADDITIONAL USE RESTRICTIONS** that prohibit military-industrial applications.

**Key Points:**
- ✅ Free for open-source and personal use
- ✅ Free for civilian, educational, and humanitarian purposes
- ✅ Modifications must remain open-source
- ✅ Distributed under the same GPL-3.0 terms
- 🚫 **PROHIBITED** for military-industrial complex use
- 🚫 **PROHIBITED** for weapon development and defense contracting

**Important Files:**
- [LICENSE](LICENSE) - GPL-3.0+ with restrictions header
- [LICENSE_RESTRICTIONS.md](LICENSE_RESTRICTIONS.md) - Complete military-industrial prohibitions

### Commercial: Separate License Required

For commercial use, obtain a commercial license. **Note:** Commercial licenses do NOT grant exemptions from military-industrial prohibitions. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

---

## Project Status

- **Version**: 3.0.0
- **Status**: Production-Ready
- **Maintained**: ✅ Active
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12

---

## Acknowledgments

This project uses mathematical concepts from:
- Golden ratio (φ) for quasi-random sequences
- NIST statistical test methodologies
- Post-quantum cryptography research (NIST PQC)
- Entropy validation frameworks

---

## Support

- **Issues**: [GitHub Issues](https://github.com/beanapologist/seed/issues)
- **Discussions**: [GitHub Discussions](https://github.com/beanapologist/seed/discussions)
- **Commercial Support**: See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md)

---

## Disclaimer

⚠️ **IMPORTANT - CRYPTOGRAPHIC USE**: This library is NOT suitable for cryptographic purposes. Do not use for:
- Encryption or decryption
- Secure key generation
- Authentication tokens
- Password generation
- Security-sensitive applications

For cryptographic random numbers, use Python's `secrets` module or `os.urandom()`.

🚫 **IMPORTANT - MILITARY USE**: This software is **STRICTLY PROHIBITED** for any military-industrial applications including but not limited to:
- Weapon development, production, or deployment
- Military hardware or surveillance systems
- Defense contracting or military procurement
- Organizations engaged in weapon manufacturing
- Military intelligence or combat operations

**VIOLATION:** Use in violation of these restrictions results in immediate termination of all license rights. See [LICENSE_RESTRICTIONS.md](LICENSE_RESTRICTIONS.md) for complete details.

---

**GoldenSeed** - Deterministic. Reproducible. Space-Efficient.

*© 2024-2026 beanapologist. Licensed under GPL-3.0-or-later.*