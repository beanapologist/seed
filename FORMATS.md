# Golden Seed - Format Support

Complete documentation of all supported formats for the Universal Binary Golden Seed.

## Format Overview

The golden seed is available in **8 different formats** to support diverse use cases, programming languages, and integration scenarios.

| Format | File | Size | Use Case |
|--------|------|------|----------|
| Binary (LE) | `golden_seed_16.bin` | 16 bytes | Direct binary usage, optimal performance |
| Binary (BE) | `golden_seed_16_be.bin` | 16 bytes | Big-endian systems, cross-platform compatibility |
| Hexadecimal | `golden_seed.hex` | 561 bytes | Human-readable reference |
| Base64 | `golden_seed_16.b64` | 24 bytes | Web APIs, JSON payloads |
| JSON | `golden_seed_16.json` | 300 bytes | Configuration, data interchange |
| CSV | `golden_seed_16.csv` | 612 bytes | Spreadsheets, data analysis |
| Text Reference | `golden_seed_formats.txt` | 2.1K | All formats at a glance |
| Extended (32B) | `golden_seed_32.bin` | 32 bytes | Consensus, tie-breaking |

## 16-Byte Seed Formats

### 1. Binary (Little-Endian) - `golden_seed_16.bin`

**Format**: IEEE 754 double-precision floating point, little-endian byte order

**Hex**: `0000000000000000A8F4979B77E3F93F`

**Usage**: Optimal for performance-critical code
```python
with open('golden_seed_16.bin', 'rb') as f:
    seed = f.read(16)
```

**Byte Layout**:
```
Offset 0-7:   00 00 00 00 00 00 00 00  (Real: 0.0)
Offset 8-15:  A8 F4 97 9B 77 E3 F9 3F  (Imag: φ)
```

### 2. Binary (Big-Endian) - `golden_seed_16_be.bin`

**Format**: IEEE 754 double-precision floating point, big-endian byte order

**Hex**: `00000000000000003FF9E3779B97F4A8`

**Usage**: Big-endian systems, compatibility verification
```python
with open('golden_seed_16_be.bin', 'rb') as f:
    seed = f.read(16)
```

**Byte Layout**:
```
Offset 0-7:   00 00 00 00 00 00 00 00  (Real: 0.0)
Offset 8-15:  3F F9 E3 77 9B 97 F4 A8  (Imag: φ)
```

### 3. Hexadecimal - `golden_seed.hex`

**Format**: ASCII text representation with comments

**Content**:
```
# 16-byte seed (iφ):
0000000000000000A8F4979B77E3F93F
```

**Usage**: Human-readable reference, verification
```bash
xxd -r -p golden_seed.hex > golden_seed_16.bin
```

### 4. Base64 - `golden_seed_16.b64`

**Format**: Base64-encoded binary (RFC 4648)

**Content**: `AAAAAAAAAACo9Jebd+P5Pw==`

**Usage**: Web APIs, JSON payloads, data transmission
```python
import base64
with open('golden_seed_16.b64', 'r') as f:
    seed = base64.b64decode(f.read())
```

**Decode**: `base64 -d golden_seed_16.b64 | xxd`

### 5. JSON - `golden_seed_16.json`

**Format**: JSON object with metadata

**Content**:
```json
{
  "name": "golden_seed_16",
  "description": "16-byte golden seed (iφ representation)",
  "format": "IEEE 754 little-endian complex",
  "bytes": 16,
  "real_part": 0.0,
  "imaginary_part": 1.618033988749895,
  "hex": "0000000000000000A8F4979B77E3F93F",
  "base64": "AAAAAAAAAACo9Jebd+P5Pw=="
}
```

**Usage**: Configuration files, API responses
```python
import json
with open('golden_seed_16.json') as f:
    seed_data = json.load(f)
    hex_value = seed_data['hex']
```

### 6. CSV - `golden_seed_16.csv`

**Format**: Comma-separated values for spreadsheet import

**Content**:
```csv
byte_offset,hex_value,decimal_value,description
0,00,0,Real part (0.0) - byte 1
...
15,3F,63,Imaginary part (φ) - byte 8
```

**Usage**: Data analysis, documentation, verification tables
```bash
# Import into Excel/Google Sheets or process with:
python -c "import csv; reader = csv.DictReader(open('golden_seed_16.csv')); print(list(reader))"
```

### 7. Text Reference - `golden_seed_formats.txt`

**Format**: Human-readable text with all format representations

**Content**: Includes hex, base64, decimal bytes, and conversion formulas

**Usage**: Quick reference, documentation, education

## 32-Byte Seed Formats

### Extended Seed - `golden_seed_32.bin` and variants

The 32-byte consensus extension combines:
- **Bytes 0-15**: iφ seed (original 16-byte seed)
- **Bytes 16-23**: φ pattern (imaginary part repeated)
- **Bytes 24-31**: φ pattern (imaginary part repeated)

**Structure**:
```
┌─ iφ seed (16 bytes) ─┬── φ pattern ──┬── φ pattern ──┐
│ Real (8B) + Imag (8B)│ (8 bytes)      │ (8 bytes)      │
└──────────────────────┴────────────────┴────────────────┘
0                      16               24               32
```

**Available Formats**:
- `golden_seed_32.bin` - Little-endian binary
- `golden_seed_32_be.bin` - Big-endian binary
- `golden_seed_32.b64` - Base64 encoded
- `golden_seed_32.json` - JSON representation

**Hex Values**:
- LE: `0000000000000000A8F4979B77E3F93FA8F4979B77E3F93FA8F4979B77E3F93F`
- BE: `00000000000000003FF9E3779B97F4A83FF9E3779B97F4A83FF9E3779B97F4A8`

## Format Conversion Recipes

### Binary → Hex
```bash
xxd -p golden_seed_16.bin
od -A x -t x1z -v golden_seed_16.bin
hexdump -C golden_seed_16.bin
```

### Hex → Binary
```bash
xxd -r -p golden_seed.hex > golden_seed_16.bin
echo "0000000000000000A8F4979B77E3F93F" | xxd -r -p > golden_seed_16.bin
```

### Binary → Base64
```bash
base64 < golden_seed_16.bin
openssl base64 -in golden_seed_16.bin
python -c "import base64; print(base64.b64encode(open('golden_seed_16.bin', 'rb').read()).decode())"
```

### Base64 → Binary
```bash
base64 -d < golden_seed_16.b64 > golden_seed_16.bin
echo "AAAAAAAAAACo9Jebd+P5Pw==" | base64 -d > golden_seed_16.bin
```

### Binary → JSON
```python
import json, base64
with open('golden_seed_16.bin', 'rb') as f:
    data = f.read()
json.dump({
    'hex': data.hex().upper(),
    'base64': base64.b64encode(data).decode(),
    'bytes': len(data)
}, open('seed.json', 'w'), indent=2)
```

### Little-Endian ↔ Big-Endian
```python
import struct
with open('golden_seed_16.bin', 'rb') as f:
    le_data = f.read()
# Extract doubles
real = struct.unpack('<d', le_data[:8])[0]
imag = struct.unpack('<d', le_data[8:16])[0]
# Pack in big-endian
be_data = struct.pack('>d', real) + struct.pack('>d', imag)
```

## Language-Specific Usage

### Python
```python
import struct, base64

# From binary
with open('golden_seed_16.bin', 'rb') as f:
    seed = f.read()

# From base64
seed = base64.b64decode('AAAAAAAAAACo9Jebd+P5Pw==')

# From JSON
import json
with open('golden_seed_16.json') as f:
    seed = bytes.fromhex(json.load(f)['hex'])

# Parse as complex number
real = struct.unpack('<d', seed[:8])[0]
imag = struct.unpack('<d', seed[8:16])[0]
```

### JavaScript/Node.js
```javascript
const fs = require('fs');
const base64 = require('base64-js');

// From binary
const seed = fs.readFileSync('golden_seed_16.bin');

// From base64
const seed = Buffer.from('AAAAAAAAAACo9Jebd+P5Pw==', 'base64');

// From JSON
const seedData = JSON.parse(fs.readFileSync('golden_seed_16.json'));
const seed = Buffer.from(seedData.hex, 'hex');
```

### Go
```go
import (
    "encoding/base64"
    "encoding/hex"
    "io/ioutil"
)

// From binary
seed, _ := ioutil.ReadFile("golden_seed_16.bin")

// From base64
seed, _ := base64.StdEncoding.DecodeString("AAAAAAAAAACo9Jebd+P5Pw==")

// From hex
seed, _ := hex.DecodeString("0000000000000000A8F4979B77E3F93F")
```

### Rust
```rust
use std::fs;

// From binary
let seed = fs::read("golden_seed_16.bin").unwrap();

// From base64
use base64::{Engine as _, engine::general_purpose};
let seed = general_purpose::STANDARD
    .decode("AAAAAAAAAACo9Jebd+P5Pw==")
    .unwrap();
```

### Java
```java
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

// From binary
byte[] seed = Files.readAllBytes(Paths.get("golden_seed_16.bin"));

// From base64
byte[] seed = Base64.getDecoder()
    .decode("AAAAAAAAAACo9Jebd+P5Pw==");
```

## File Integrity Checksums

All format files are cryptographically equivalent and should produce identical checksums when converted to the canonical binary format.

**16-Byte Seed Checksums**:
```
SHA256: 87f829d95b15b08db9e5d84ff06665d077b267cfc39a5fa13a9e002b3e4239c5
SHA512: 6c1e6ffdcfa8a1e4cfcfaeedb8b3b4f64a8de3d1b690e61e7ce48e80da9bcd7127bc890a3e74bb3d1c92bc5052b1076c0fe9b86eff210f497ecd0104eb544483
```

**32-Byte Seed Checksums**:
```
SHA256: 096412ca0482ab0f519bc0e4ded667475c45495047653a21aa11e2c7c578fa6f
SHA512: fcfdc7392214fa5bc36c7a9edaa725fa366bb83f7bc2e4d5006688e4d0b07c56eea2c2d3fcb5fbf6c63e0217973d05ed358e7b8ad71df1812f1fb212c6ac8498
```

## Verification

To verify format conversions are lossless:

```bash
# All formats should convert to the same binary
base64 -d golden_seed_16.b64 > /tmp/from_base64.bin
xxd -r -p golden_seed.hex > /tmp/from_hex.bin
jq -r '.hex' golden_seed_16.json | xxd -r -p > /tmp/from_json.bin

# Verify checksums match
sha256sum /tmp/from_*.bin golden_seed_16.bin
```

## Format Selection Guide

| Use Case | Recommended Format |
|----------|-------------------|
| Performance-critical code | Binary (LE) |
| Cross-platform systems | Binary (LE) + (BE) |
| Web APIs / JSON | Base64 or JSON |
| Human review | Hex or Text Reference |
| Data analysis / Excel | CSV |
| Configuration files | JSON |
| Documentation | Text Reference |
| Embedded systems | Binary (LE) |

---

**Last Updated**: December 30, 2025  
**Supported Formats**: 8  
**Verification Methods**: SHA256, SHA512, Format Conversion
