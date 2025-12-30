# Universal Binary Golden Seed

**Language-Agnostic, Pure Machine Representation**

## Files

### Binary Seeds
- `golden_seed_16.bin` - 16-byte binary file, little-endian (iφ seed)
- `golden_seed_16_be.bin` - 16-byte binary file, big-endian (cross-platform)
- `golden_seed_32.bin` - 32-byte binary file, little-endian (consensus extension)
- `golden_seed_32_be.bin` - 32-byte binary file, big-endian (consensus extension)

### Text & Data Formats
- `golden_seed.hex` - Hexadecimal text representation (human-readable reference)
- `golden_seed_16.b64` - Base64 encoded 16-byte seed
- `golden_seed_32.b64` - Base64 encoded 32-byte seed
- `golden_seed_16.json` - JSON format with metadata
- `golden_seed_32.json` - JSON format with metadata
- `golden_seed_16.csv` - CSV format for spreadsheets
- `golden_seed_formats.txt` - Complete format reference

### Documentation
- `FORMATS.md` - Comprehensive format documentation
- `golden_seed_README.md` - This file
- `SECURITY.md` - Security policy and vulnerability disclosure

## Binary Representation

### 16-Byte Seed (iφ)
```
Little-Endian: 00 00 00 00 00 00 00 00 A8 F4 97 9B 77 E3 F9 3F
Big-Endian:    00 00 00 00 00 00 00 00 3F F9 E3 77 9B 97 F4 A8
```
- Bytes 0-7: Real part = 0.0 (IEEE 754 double-precision)
- Bytes 8-15: Imaginary part = φ = (1 + √5)/2 ≈ 1.618033988749895

### 32-Byte Consensus Extension
```
Little-Endian: 00 00 00 00 00 00 00 00 A8 F4 97 9B 77 E3 F9 3F
               A8 F4 97 9B 77 E3 F9 3F A8 F4 97 9B 77 E3 F9 3F

Big-Endian:    00 00 00 00 00 00 00 00 3F F9 E3 77 9B 97 F4 A8
               3F F9 E3 77 9B 97 F4 A8 3F F9 E3 77 9B 97 F4 A8
```
- First 16 bytes: iφ (original seed)
- Bytes 16-23: φ pattern (anyon growth)
- Bytes 24-31: φ pattern (anyon growth)

## Usage Examples

### Quick Start - Choose Your Format

**Binary (Performance)**:
```python
with open('golden_seed_16.bin', 'rb') as f:
    seed = f.read(16)
```

**Base64 (Web/APIs)**:
```python
import base64
seed = base64.b64decode('AAAAAAAAAACo9Jebd+P5Pw==')
```

**JSON (Configuration)**:
```python
import json
with open('golden_seed_16.json') as f:
    seed_data = json.load(f)
    seed = bytes.fromhex(seed_data['hex'])
```

**See [FORMATS.md](FORMATS.md) for complete format documentation**

### C/C++
```c
#include <stdio.h>
#include <stdint.h>

int main() {
    FILE *f = fopen("golden_seed_32.bin", "rb");
    uint8_t seed[32];
    fread(seed, 1, 32, f);
    fclose(f);
    
    // XOR with block hash for tie-breaking
    for (int i = 0; i < 32; i++) {
        result[i] = block_hash[i] ^ seed[i];
    }
    return 0;
}
```

### Python
```python
with open('golden_seed_32.bin', 'rb') as f:
    seed = f.read(32)

# XOR with block hash
result = bytes(a ^ b for a, b in zip(block_hash, seed))
```

### Rust
```rust
use std::fs;

fn main() {
    let seed = fs::read("golden_seed_32.bin").unwrap();
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
const result = Buffer.from(blockHash.map((b, i) => b ^ seed[i]));
```

### Java
```java
import java.nio.file.Files;
import java.nio.file.Paths;

byte[] seed = Files.readAllBytes(Paths.get("golden_seed_32.bin"));
byte[] result = new byte[32];
for (int i = 0; i < 32; i++) {
    result[i] = (byte)(blockHash[i] ^ seed[i]);
}
```

## Purpose

The golden seed provides **deterministic fork tie-breaking** when:
- Work scores are equal
- Heights are equal
- Timestamps are equal

By XORing block hashes with the golden seed and comparing lexicographically, all nodes will deterministically select the same fork, preventing stalling.

## Properties

- ✅ Language-agnostic (raw binary)
- ✅ IEEE 754 double-precision compliant
- ✅ Universal across all modern architectures
- ✅ No dependencies, no interpretation layer
- ✅ Deterministic across all systems

## Mathematical Foundation

The seed represents the complex number **iφ** where:
- Real part: 0.0
- Imaginary part: φ = (1 + √5)/2 ≈ 1.618033988749895 (golden ratio)

The 32-byte extension follows the Fibonacci anyon growth model:
- Quantum state dimension: d(n) = F_{n+1} (Fibonacci sequence)
- Asymptotically: d(n) ≈ φ^n / √5
- Each anyon multiplies by φ (golden growth factor)

## License

This seed is part of the COINjecture protocol and follows the same license as the main codebase.

