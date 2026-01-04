# Quantum Key Distribution (QKD) - Deterministic Keys with Verified Checksums

## Overview

This repository implements a **Quantum Key Distribution (QKD)** system that generates **deterministic keys** with **quantum-level security** using **verified checksums**. The system provides cryptographically strong keys through Binary Fusion Tap technology with 8-fold Heartbeat and ZPE Overflow extraction.

**Key Features:**
- 🔐 **Deterministic Key Generation** - Reproducible keys from golden seed values
- ✅ **Verified Checksums** - SHA256/SHA512 integrity validation for all operations
- 🔬 **Quantum-Level Security** - Quantum-inspired cryptographic algorithms
- 🌐 **Universal Compatibility** - Language-agnostic binary representation
- 📊 **Forward Secrecy** - Cryptographic ratcheting with state progression

## License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later). See the LICENSE file for details.

## Mathematical Foundation

Language-agnostic, pure machine representation based on the golden ratio:

**iφ = 0 + i × φ** where **φ = (1 + √5)/2 ≈ 1.618033988749895**

## Installation

### As a Python Package

Install the `golden-quantum` package for programmatic access:

```bash
# Install from source (development mode)
pip install -e .

# Or install from PyPI (when published)
pip install golden-quantum
```

## Repository Structure

```
seed/
├── qkd/                    # Quantum Key Distribution algorithms (importable package)
│   ├── algorithms/         # Core QKD implementations
│   │   ├── universal_qkd.py       # Universal QKD Key Generator (GCP-1)
│   │   ├── gqs1.py                # Golden Quantum Standard (GQS-1)
│   │   └── quantum_key_generator.py  # QKGS Service
│   └── utils/             # QKD utility functions
├── checksum/              # Checksum verification tools (importable package)
│   └── verify_binary_representation.py
├── formats/               # Golden seed format examples (importable package)
│   ├── golden_seed.hex    # Hex representation
│   ├── golden_seed_16.bin # 16-byte binary
│   └── golden_seed_32.bin # 32-byte binary
├── examples/              # Example implementations
└── releases/              # Multi-language release builds
```

**Note:** All directories (`qkd`, `checksum`, `formats`) are now importable Python packages with `__init__.py` files.

### Standalone Scripts

The repository includes standalone CLI scripts that work without installation:
- `qkd/algorithms/universal_qkd.py` - Universal QKD Key Generator (GCP-1)
- `qkd/algorithms/gqs1.py` - Golden Quantum Standard Test Vectors (GQS-1)
- `checksum/verify_binary_representation.py` - Binary representation verification with checksum validation
- `qkd/algorithms/quantum_key_generator.py` - Quantum Key Generator Service (QKGS) - SaaS-ready key generation
- `language_compiler.py` - Multi-language compiler for Binary Fusion Tap (Python, JS, Rust, Go, C, Java, TypeScript)

## Quick Start

### Python Package API

**Option 1: Using the installed package (recommended):**

```python
from gq import UniversalQKD, GQS1

# Generate keys using GCP-1 (Universal QKD)
generator = UniversalQKD()
key = next(generator)
print(key.hex())  # 3c732e0d04dac163a5cc2b15c7caf42c

# Generate test vectors using GQS-1
vectors = GQS1.generate_test_vectors(10)
print(vectors[0])  # a01611f01e8207a27c1529c3650c4838
```

**Option 2: Importing from repository directories:**

```python
import sys
sys.path.insert(0, '/path/to/seed')

from qkd.algorithms.universal_qkd import universal_qkd_generator
from qkd.algorithms.gqs1 import generate_test_vectors
from checksum.verify_binary_representation import binary_fusion_tap
from formats import GOLDEN_SEED_16_BIN, GOLDEN_SEED_32_BIN

# Use the functions
generator = universal_qkd_generator()
key = next(generator)
print(key.hex())
```

### Command Line Tools

```bash
# After pip install -e .
gq-universal -n 10          # Generate 10 universal QKD keys
gq-test-vectors -n 10       # Generate 10 GQS-1 test vectors

# Or use standalone scripts from the repository
python qkd/algorithms/universal_qkd.py -n 10
python qkd/algorithms/gqs1.py -n 10
```

## Seed Values with Verified Checksums

The golden seed values are stored in the `formats/` directory with multiple representations for cross-platform compatibility.

### 16-byte seed (iφ):
```
0000000000000000A8F4979B77E3F93F
```
**File:** `formats/golden_seed_16.bin`

### 32-byte seed (iφ + 2×φ for consensus):
```
0000000000000000A8F4979B77E3F93FA8F4979B77E3F93FA8F4979B77E3F93F
```
**File:** `formats/golden_seed_32.bin`

### Checksum Verification

All seed values and generated keys include SHA256 checksum verification to ensure data integrity:

```bash
# Verify binary representation with checksums
python checksum/verify_binary_representation.py
```

## Usage in any language

1. **Read binary file as raw bytes**
   - Use `formats/golden_seed_16.bin` for 16-byte seed
   - Use `formats/golden_seed_32.bin` for 32-byte seed

2. **Interpret as IEEE 754 double-precision (little-endian complex)**
   - Bytes 0-7: Real part = 0.0
   - Bytes 8-15: Imaginary part = φ ≈ 1.618033988749895

3. **XOR with block hashes for deterministic tie-breaking**
   - Provides deterministic fork resolution when work scores are equal
   - All nodes will select the same fork, preventing stalling

4. **No dependencies, no interpretation layer**
   - Pure binary representation
   - Works across all modern architectures
   - Language-agnostic implementation

## Example Code

> **Note:** The examples below are simplified for clarity. Production code should include comprehensive error handling appropriate for your language and use case.

### Python

**Library Usage:**
```python
with open('formats/golden_seed_32.bin', 'rb') as f:
    seed = f.read(32)

# XOR with block hash for tie-breaking
block_hash = b'\x00' * 32  # Your block hash here
result = bytes(a ^ b for a, b in zip(block_hash, seed))
```

**Universal QKD Key Generator (GCP-1):**

This repository includes a production-grade Universal QKD (Quantum Key Distribution) key generator implementing the Golden Consensus Protocol v1.0 (`qkd/algorithms/universal_qkd.py`). This protocol provides:

- Deterministic, synchronized key generation across nodes
- Cryptographic forward secrecy via state ratcheting
- Basis-matching simulation (~50% efficiency, mimicking quantum systems)
- XOR folding for key hardening
- Infinite key stream generation

```bash
# Generate 10 keys (default)
python qkd/algorithms/universal_qkd.py

# Generate 100 keys
python qkd/algorithms/universal_qkd.py -n 100

# Output in JSON format with binary representation
python qkd/algorithms/universal_qkd.py -n 20 --json --binary

# Save to file
python qkd/algorithms/universal_qkd.py -n 50 -o keys.txt

# Quiet mode (keys only, no headers)
python qkd/algorithms/universal_qkd.py -n 5 --quiet

# Verify seed checksum only
python qkd/algorithms/universal_qkd.py --verify-only

# Save JSON output to file
python qkd/algorithms/universal_qkd.py -n 100 --json -o keys.json
```

First key (for cross-implementation validation):
```
3c732e0d04dac163a5cc2b15c7caf42c
```

**GQS-1 Test Vector Generation:**

For test vector generation and compliance testing, use `qkd/algorithms/gqs1.py`:

```bash
# Generate 10 test vectors (default)
python qkd/algorithms/gqs1.py

# Generate 100 test vectors
python qkd/algorithms/gqs1.py -n 100

# Output in JSON format
python qkd/algorithms/gqs1.py -n 20 --json

# Save to file
python qkd/algorithms/gqs1.py -n 50 -o vectors.txt

# Quiet mode (vectors only, no headers)
python qkd/algorithms/gqs1.py -n 5 --quiet

# Verify seed checksum only
python qkd/algorithms/gqs1.py --verify-only
```

For more options, run:
```bash
python qkd/algorithms/gqs1.py --help
python qkd/algorithms/universal_qkd.py --help
```

**Binary Representation Verification with Checksums:**

Verify binary representations of seed values and their manifested forms with integrated checksum validation:

```bash
# Run verification for k=11 with seed_11=1234567891011
python checksum/verify_binary_representation.py
```

This tool demonstrates the relationship between seed values and their manifested binary forms using the formula:
```
manifested = (seed * 8) + k
```

The tool includes SHA256 checksum validation for integrity verification:
- Calculates SHA256 checksums for both seed and manifested values
- Verifies data integrity during transmission or storage
- Can validate against known expected checksums

Example output:
```
Seed_11 Bit Length: 41
Manifested Bit Length: 44
Binary Tap (k=11): 0b10001111101110001111110110000100001000100011

Seed SHA256: 7f1665ab9f8c74fd60bd4fdcb10382b63727e10db9d568d385930695cc2f0454
Manifested SHA256: 677b205682ad566fcee652f80a4e8a538a265dc849da0d86fc0e5282b4cbf115
```

**Quantum Key Generator Service (QKGS):**

Enterprise-grade SaaS-ready key generation service using Binary Fusion Tap technology with deterministic keys and verified checksums:

```bash
# Generate single 256-bit key using Binary Fusion algorithm
python qkd/algorithms/quantum_key_generator.py --algorithm fusion --length 256

# Generate 10 hybrid keys (Fusion + Hash + Entropy mixing)
python qkd/algorithms/quantum_key_generator.py --algorithm hybrid --count 10 --k 11

# Generate 512-bit keys in JSON format for API integration
python qkd/algorithms/quantum_key_generator.py --algorithm fusion --length 512 --format json

# Generate batch of hash-based keys and save to file
python qkd/algorithms/quantum_key_generator.py --algorithm hash --count 100 --output keys.json
```

**Key Generation Algorithms:**

1. **Fusion** - Uses Binary Fusion Tap with 8-fold Heartbeat and ZPE Overflow
   - Deterministic for same k parameter (unless salted)
   - Optimal for protocol verification and testing
   - Includes quantum-inspired entropy extraction

2. **Hash** - Cryptographic hash-based generation with key stretching
   - Secure random generation (uses `secrets` module)
   - 1000-iteration key stretching for enhanced security
   - Deterministic when seed is provided

3. **Hybrid** - Combined approach (Fusion + Hash + External Entropy)
   - Maximum entropy mixing from multiple sources
   - Best for production key generation
   - Combines deterministic and random components

**Supported Key Lengths:** 128, 256, 512 bits

**Applications:**
- Secure key generation for encryption systems
- Protocol verification and compliance testing
- Quantum-inspired cryptography research
- Deterministic tie-breaking in distributed systems
- API key generation for SaaS platforms

Example output:
```
Key #1:
  Algorithm: FUSION
  Key Length: 256 bits
  Key: 9e4ae62505036d21d8e18c67e3670f8a34576401b5dc269a7ebab421d0dd4b00
  K Parameter: 11
  ZPE Overflow: 0b111011
  Checksum (SHA256): 1ee118404614d235601a858389ca55f7...
```

**Multi-Language Compiler:**

Generate Binary Fusion Tap implementations in any programming language:

```bash
# List all supported languages
python language_compiler.py --list

# Generate Python implementation
python language_compiler.py --language python -o my_keygen.py

# Generate Rust implementation
python language_compiler.py --language rust -o binary_fusion.rs

# Generate ALL languages at once (Python, JS, TS, Rust, Go, C, Java)
python language_compiler.py --all
```

**Supported Languages:**
- **Python** - Full implementation with type hints
- **JavaScript** - ES6+ with BigInt support
- **TypeScript** - Strongly typed with interfaces
- **Rust** - Memory-safe with zero-cost abstractions
- **Go** - Concurrent-ready with big.Int
- **C** - High-performance native implementation
- **Java** - Enterprise-ready with BigInteger

Each generated implementation includes:
- Complete Binary Fusion Tap algorithm
- 8-fold Heartbeat operation
- ZPE Overflow extraction
- Example usage code
- Consistent API across languages

Example: Generate and use Rust implementation:
```bash
python language_compiler.py --language rust -o keygen.rs
rustc keygen.rs && ./keygen
```

### Language-Specific Examples

### C/C++
```c
#include <stdio.h>
#include <stdint.h>

int main() {
    FILE *f = fopen("formats/golden_seed_32.bin", "rb");
    if (!f) return 1;
    
    uint8_t seed[32];
    if (fread(seed, 1, 32, f) != 32) {
        fclose(f);
        return 1;
    }
    fclose(f);
    
    // XOR with block hash for tie-breaking
    uint8_t block_hash[32] = { /* your block hash */ };
    uint8_t result[32];
    for (int i = 0; i < 32; i++) {
        result[i] = block_hash[i] ^ seed[i];
    }
    return 0;
}
```

### Rust
```rust
use std::fs;

fn main() {
    let seed = fs::read("formats/golden_seed_32.bin").unwrap();
    let block_hash = vec![0u8; 32];  // Your block hash here
    let result: Vec<u8> = block_hash.iter()
        .zip(seed.iter())
        .map(|(a, b)| a ^ b)
        .collect();
}
```

### Go
```go
package main

import "os"

func main() {
    seed, _ := os.ReadFile("formats/golden_seed_32.bin")
    blockHash := make([]byte, 32)  // Your block hash here
    result := make([]byte, 32)
    for i := range seed {
        result[i] = blockHash[i] ^ seed[i]
    }
}
```

### JavaScript/Node.js
```javascript
const fs = require('fs');
const seed = fs.readFileSync('formats/golden_seed_32.bin');
const blockHash = Buffer.alloc(32);  // Your block hash here
const result = Buffer.from(blockHash.map((b, i) => b ^ seed[i]));
```

### Java
```java
import java.nio.file.Files;
import java.nio.file.Paths;

byte[] seed = Files.readAllBytes(Paths.get("formats/golden_seed_32.bin"));
byte[] blockHash = new byte[32];  // Your block hash here
byte[] result = new byte[32];
for (int i = 0; i < 32; i++) {
    result[i] = (byte)(blockHash[i] ^ seed[i]);
}
```

## Files

See the `formats/` directory for golden seed files:
- **formats/golden_seed.hex** - Hex representation
- **formats/golden_seed_16.bin** - 16-byte binary seed (iφ)
- **formats/golden_seed_32.bin** - 32-byte binary seed (iφ + 2×φ for consensus)

See the `qkd/` directory for Quantum Key Distribution implementations:
- **qkd/algorithms/universal_qkd.py** - Universal QKD Key Generator (GCP-1)
- **qkd/algorithms/gqs1.py** - Golden Quantum Standard Test Vectors (GQS-1)
- **qkd/algorithms/quantum_key_generator.py** - QKGS Service

See the `checksum/` directory for verification tools:
- **checksum/verify_binary_representation.py** - Binary verification with checksums

## Security

See [SECURITY.md](SECURITY.md) for security policy and vulnerability reporting.

## License

This seed is part of the COINjecture protocol and follows the same license as the main codebase.
