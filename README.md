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

## Security

See [SECURITY.md](SECURITY.md) for security policy and vulnerability reporting.

## License

This seed is part of the COINjecture protocol and follows the same license as the main codebase.
