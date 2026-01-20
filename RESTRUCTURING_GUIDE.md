# Repository Restructuring Guide

## Overview

This repository has been restructured to emphasize its focus as a **Quantum Key Distribution (QKD)** project that generates **deterministic keys** with **verified checksums** and **quantum-level security**.

## New Directory Structure

```
seed/
├── qkd/                           # Quantum Key Distribution implementations
│   ├── algorithms/                # Core QKD algorithms
│   │   ├── universal_qkd.py      # Universal QKD Key Generator (GCP-1)
│   │   ├── gqs1.py               # Golden Quantum Standard (GQS-1)
│   │   └── quantum_key_generator.py  # QKGS Service
│   ├── utils/                     # QKD utility functions (for future use)
│   └── README.md
├── checksum/                      # Checksum verification tools
│   ├── verify_binary_representation.py
│   └── README.md
├── formats/                       # Golden seed format examples
│   ├── golden_seed.hex           # Hex representation
│   ├── golden_seed_16.bin        # 16-byte binary
│   ├── golden_seed_32.bin        # 32-byte binary
│   └── README.md
├── examples/                      # Multi-language examples
├── releases/                      # Release builds
├── src/gq/                       # Python package source
└── tests/                        # Test vectors
```

## Migration Guide

### For Users

If you were using scripts directly, update your commands:

**Old:**
```bash
python universal_qkd.py -n 10
python gqs1.py -n 10
python quantum_key_generator.py --algorithm fusion
python verify_binary_representation.py
```

**New:**
```bash
python qkd/algorithms/universal_qkd.py -n 10
python qkd/algorithms/gqs1.py -n 10
python qkd/algorithms/quantum_key_generator.py --algorithm fusion
python checksum/verify_binary_representation.py
```

### For Developers

If you were importing modules, update your imports:

**Old:**
```python
from universal_qkd import universal_qkd_generator
from gqs1 import generate_test_vectors
from quantum_key_generator import QuantumKeyGenerator
from verify_binary_representation import binary_fusion_tap
```

**New (as packages - add repo to path):**
```python
import sys
sys.path.insert(0, '/path/to/seed')

from qkd.algorithms.universal_qkd import universal_qkd_generator
from qkd.algorithms.gqs1 import generate_test_vectors
from qkd.algorithms.quantum_key_generator import QuantumKeyGenerator
from checksum.verify_binary_representation import binary_fusion_tap
```

**Or using the Python package (preferred):**
```python
# After: pip install -e /path/to/seed
from gq import UniversalQKD, GQS1
```

**For golden seed file access:**
```python
import sys
sys.path.insert(0, '/path/to/seed')

from formats import GOLDEN_SEED_16_BIN, GOLDEN_SEED_32_BIN

with open(GOLDEN_SEED_32_BIN, 'rb') as f:
    seed = f.read()
```

### For Golden Seed Files

If you were reading the seed files:

**Old:**
```python
with open('golden_seed_32.bin', 'rb') as f:
    seed = f.read()
```

**New:**
```python
with open('formats/golden_seed_32.bin', 'rb') as f:
    seed = f.read()
```

## Key Changes

### 1. Enhanced QKD Focus
- README emphasizes Quantum Key Distribution as primary purpose
- Documentation highlights deterministic keys with quantum-level security
- All descriptions mention verified checksums

### 2. Organized Structure
- QKD algorithms grouped in `qkd/algorithms/`
- Checksum tools isolated in `checksum/`
- Format files organized in `formats/`
- Each directory has descriptive README

### 3. Updated Keywords
The project now uses these keywords for better discoverability:
- quantum-key-distribution
- qkd
- deterministic-key
- checksum
- checksums
- quantum-security
- verified-keys

### 4. Improved Documentation
- Repository structure documented in main README
- Each subdirectory has explanatory README
- All examples updated with new paths
- Release notes emphasize QKD features

## Benefits

1. **Clearer Purpose**: Repository clearly positions itself as a QKD project
2. **Better Organization**: Related files grouped logically
3. **Improved Discoverability**: Better keywords and metadata
4. **Easier Navigation**: Clear directory structure
5. **Professional Structure**: Follows best practices for Python projects

## Backward Compatibility

All functionality remains identical - only file locations changed. The Python package (`gq`) API is unchanged, so existing package users are not affected.

## Testing

All 90 tests pass with the new structure:
- 28 tests for Universal QKD
- 25 tests for GQS-1
- 18 tests for Binary Verification
- 19 tests for Quantum Key Generator

Run tests with:
```bash
python -m unittest discover -s . -p "test_*.py" -v
```

## Questions?

See the main [README.md](README.md) for detailed usage instructions with the new structure.
