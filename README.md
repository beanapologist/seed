# Universal Binary Golden Seed - Hex Representation

Language-agnostic, pure machine representation

**iφ = 0 + i × φ** where **φ = (1 + √5)/2 ≈ 1.618033988749895**

## Seed Values

### 16-byte seed (iφ):
```
0000000000000000A8F4979B77E3F93F
```

### 32-byte seed (iφ + 2×φ for consensus):
```
0000000000000000A8F4979B77E3F93FA8F4979B77E3F93FA8F4979B77E3F93F
```

## Usage in any language

1. **Read binary file as raw bytes**
   - Use `golden_seed_16.bin` for 16-byte seed
   - Use `golden_seed_32.bin` for 32-byte seed

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
```python
with open('golden_seed_32.bin', 'rb') as f:
    seed = f.read(32)

# XOR with block hash for tie-breaking
block_hash = b'\x00' * 32  # Your block hash here
result = bytes(a ^ b for a, b in zip(block_hash, seed))
```

### C/C++
```c
#include <stdio.h>
#include <stdint.h>

int main() {
    FILE *f = fopen("golden_seed_32.bin", "rb");
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
    let seed = fs::read("golden_seed_32.bin").unwrap();
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
    seed, _ := os.ReadFile("golden_seed_32.bin")
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
const seed = fs.readFileSync('golden_seed_32.bin');
const blockHash = Buffer.alloc(32);  // Your block hash here
const result = Buffer.from(blockHash.map((b, i) => b ^ seed[i]));
```

### Java
```java
import java.nio.file.Files;
import java.nio.file.Paths;

byte[] seed = Files.readAllBytes(Paths.get("golden_seed_32.bin"));
byte[] blockHash = new byte[32];  // Your block hash here
byte[] result = new byte[32];
for (int i = 0; i < 32; i++) {
    result[i] = (byte)(blockHash[i] ^ seed[i]);
}
```

## Files

- **golden_seed.hex** - Hex representation (this file format)
- **golden_seed_16.bin** - 16-byte binary seed
- **golden_seed_32.bin** - 32-byte binary seed
- **gqs1.py** - Golden Quantum Standard (GQS-1) test vector generator
- **test_gqs1.py** - Unit tests for GQS-1 implementation

## Golden Quantum Standard (GQS-1) Test Vectors

The repository includes an implementation of the Golden Quantum Standard (GQS-1) protocol for generating deterministic test vectors for quantum key distribution testing and compliance.

### Overview

GQS-1 provides a standardized method for generating reproducible 128-bit cryptographic keys using:
1. A deterministic seed (the 32-byte golden seed)
2. Hash-DRBG ratchet mechanism for state evolution
3. Quantum sifting simulation (basis matching)
4. XOR folding for information-theoretic hardening

### Protocol Specification

#### 1. Seed Initialization
- **Hex Seed**: `0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f`
- **SHA-256 Checksum**: `096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f`

#### 2. Hash-DRBG Ratchet
The system state evolves deterministically using:
```
S_{n+1} = SHA-256(S_n || Counter)
```
Where `Counter` is a 4-byte big-endian integer.

#### 3. Quantum Sifting
In real quantum key distribution, Alice and Bob retain only bits where their measurement bases match. For deterministic test vectors, this is simulated by using the DRBG output directly.

#### 4. Hardening via XOR Folding
The 256-bit DRBG output is hardened into a 128-bit key by:
- Splitting into two 128-bit halves
- XOR-ing the halves together

This provides information-theoretic security enhancement.

### First 10 Test Vectors

These canonical test vectors ensure cross-implementation consistency:

```
Key  1: a01611f01e8207a27c1529c3650c4838
Key  2: 255a98839109b593c97580ce561471d7
Key  3: f9e3d43664f3192b84d90f58ee584d83
Key  4: 96424e78558928d84ce6caff9c0db6b6
Key  5: b3cf328d72fabeefea0dd08e03ecf916
Key  6: f28408d2d0346064dcaba3e12af9be41
Key  7: 2814128f48ec28a58ecb252c061a15f9
Key  8: 12b4c98b607be0fc17d8466b2dc8fa8d
Key  9: f77e98348d239044998b668b312f70ed
Key 10: 017e9869c72a529f25f8dcf1fa869b98
```

### Usage

#### Generate Test Vectors
```python
from gqs1 import generate_test_vectors

# Generate first 10 test vectors
vectors = generate_test_vectors(10)
for i, key in enumerate(vectors, 1):
    print(f"Key {i}: {key}")
```

#### Run Tests
```bash
python3 -m unittest test_gqs1.py -v
```

#### Generate and Display
```bash
python3 gqs1.py
```

### Purpose

The GQS-1 test vectors serve multiple purposes:

1. **Compliance Testing**: Verify that different implementations of the protocol produce identical results
2. **Interoperability**: Ensure cross-platform and cross-language compatibility
3. **Regression Testing**: Detect unintended changes in the protocol implementation
4. **Security Validation**: Provide known-good outputs for security audits

Any implementation of GQS-1, in any programming language, should produce these exact test vectors when initialized with the same seed.

## Security

See [SECURITY.md](SECURITY.md) for security policy and vulnerability reporting.

## License

This seed is part of the COINjecture protocol and follows the same license as the main codebase.
