# Installation Guide

This guide provides detailed installation instructions for **GoldenSeed** across different platforms and package managers.

## Table of Contents

- [Quick Start](#quick-start)
- [Python Package (PyPI)](#python-package-pypi)
- [JavaScript/Node.js Package (npm)](#javascriptnodejs-package-npm)
- [Platform-Specific Installation](#platform-specific-installation)
- [Development Installation](#development-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Using Installation Scripts

**Linux / macOS:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

---

## Python Package (PyPI)

### Requirements

- Python 3.8 or higher
- pip (Python package installer)

### Installation Methods

#### Method 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/beanapologist/seed.git
cd seed

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

#### Method 2: Install from Source (Standard)

```bash
git clone https://github.com/beanapologist/seed.git
cd seed
pip install .
```

#### Method 3: Install from PyPI (When Published)

```bash
pip install golden-seed
```

### Verify Python Installation

```python
# Test the installation
python3 -c "import gq; print(f'GoldenSeed v{gq.__version__}')"

# Generate a deterministic stream
python3 -c "from gq import UniversalQKD; print(next(UniversalQKD()).hex())"
```

Expected output:
```
GoldenSeed v3.0.0
3c732e0d04dac163a5cc2b15c7caf42c
```

---

## JavaScript/Node.js Package (npm)

### Requirements

- Node.js 14.0.0 or higher
- npm (Node package manager)

### Installation Methods

#### Method 1: Install from Source

```bash
# Clone the repository
git clone https://github.com/beanapologist/seed.git
cd seed

# Build the JavaScript distribution
npm install
npm run build

# Link locally for development
npm link
```

#### Method 2: Install from npm (When Published)

```bash
npm install @beanapologist/golden-seed
```

### Verify JavaScript Installation

```javascript
// test.js
const goldenSeed = require('@beanapologist/golden-seed');

console.log('Golden Ratio (φ):', goldenSeed.PHI);

const sequence = goldenSeed.goldenRatioSequence(0, 5);
console.log('Sequence:', sequence);

const coinFlips = Array.from({length: 10}, (_, i) => 
  goldenSeed.goldenRatioCoinFlip(i) ? 'H' : 'T'
).join('');
console.log('Coin flips:', coinFlips);
```

Run:
```bash
node test.js
```

---

## Platform-Specific Installation

### Linux

#### Ubuntu / Debian

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Clone and install GoldenSeed
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh
```

#### Fedora / RHEL / CentOS

```bash
# Install Python and pip
sudo dnf install python3 python3-pip

# Clone and install GoldenSeed
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh
```

#### Arch Linux

```bash
# Install Python and pip
sudo pacman -S python python-pip

# Clone and install GoldenSeed
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh
```

---

### macOS

#### Using Homebrew

```bash
# Install Python (if not already installed)
brew install python3

# Clone and install GoldenSeed
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh
```

#### Using System Python

```bash
# macOS comes with Python 3
# Clone and install GoldenSeed
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh
```

---

### Windows

#### Method 1: Using Windows Installer Script

1. Install Python from [python.org](https://www.python.org/downloads/) (3.8+)
2. Ensure "Add Python to PATH" is checked during installation
3. Open Command Prompt or PowerShell
4. Run:

```cmd
git clone https://github.com/beanapologist/seed.git
cd seed
install.bat
```

#### Method 2: Manual Installation

```cmd
# Install Python from python.org
# Open Command Prompt

# Clone repository
git clone https://github.com/beanapologist/seed.git
cd seed

# Install package
pip install -e .

# Verify
python -c "import gq; print(gq.__version__)"
```

#### Using Windows Subsystem for Linux (WSL)

```bash
# In WSL terminal
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh
```

---

## Development Installation

### Python Development Setup

```bash
# Clone repository
git clone https://github.com/beanapologist/seed.git
cd seed

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
python -m unittest discover -v

# Or use pytest (if installed)
pytest -v
```

### JavaScript Development Setup

```bash
# Clone repository
git clone https://github.com/beanapologist/seed.git
cd seed

# Install dependencies and build
npm install
npm run build

# Run tests
npm test
```

---

## Verification

### Test CLI Commands

After installation, test the command-line tools:

```bash
# Universal stream generator
gq-universal --help

# Test vector generator
gq-test-vectors --count 5

# Golden ratio coin flip
gq-coin-flip --flips 20
```

### Run Test Suite

```bash
# Python tests
cd seed
python -m unittest discover

# Run specific test
python -m unittest test_universal_qkd
```

### Import in Python

```python
from gq import (
    UniversalQKD,
    GQS1,
    GoldenRatioCoinFlip,
    generate_universal_keys,
)

# Generate deterministic stream
generator = UniversalQKD()
stream = next(generator)
print(f"Stream: {stream.hex()}")

# Generate test vectors
vectors = GQS1.generate_test_vectors(5)
print(f"Test vectors: {vectors}")

# Golden ratio coin flips
coin = GoldenRatioCoinFlip()
flips = [coin.flip() for _ in range(10)]
print(f"Coin flips: {flips}")
```

### Use in JavaScript

```javascript
const gs = require('@beanapologist/golden-seed');

// Generate golden ratio sequence
const sequence = gs.goldenRatioSequence(0, 10);
console.log('Sequence:', sequence);

// Generate test vectors
const vectors = gs.generateTestVectors(5);
console.log('Test vectors:', vectors);
```

---

## Troubleshooting

### Python Installation Issues

#### "pip: command not found"

**Solution:**
```bash
# Linux
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

#### "Module 'gq' not found"

**Solution:**
```bash
# Reinstall in editable mode
pip install -e .

# Or check Python path
python -c "import sys; print(sys.path)"
```

#### Permission Denied

**Solution:**
```bash
# Use --user flag
pip install --user -e .

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -e .
```

### JavaScript Installation Issues

#### "npm: command not found"

**Solution:**
Install Node.js from [nodejs.org](https://nodejs.org/)

#### Build Fails

**Solution:**
```bash
# Clean and rebuild
rm -rf dist/ node_modules/
npm install
npm run build
```

### Platform-Specific Issues

#### macOS: "xcrun: error"

**Solution:**
```bash
xcode-select --install
```

#### Windows: "Python is not recognized"

**Solution:**
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH in Environment Variables

#### Linux: "externally-managed-environment"

**Solution:**
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Virtual Environment (Recommended)

Using a virtual environment is recommended to avoid conflicts:

### Python

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install package
pip install -e .

# Deactivate when done
deactivate
```

---

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Node.js**: 14.0.0 or higher (for JavaScript package)
- **RAM**: 512 MB
- **Disk Space**: 50 MB

### Supported Platforms

- ✅ Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- ✅ macOS (10.14+)
- ✅ Windows (10, 11)
- ✅ Windows Subsystem for Linux (WSL)
- ✅ BSD systems

### Supported Python Versions

- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12

---

## Additional Resources

- **README**: [README.md](README.md) - Overview and quick start
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md) - Publishing to PyPI/npm
- **API Documentation**: [README.md#api-reference](README.md#api-reference)
- **Examples**: [examples/](examples/) - Usage examples
- **Issues**: [GitHub Issues](https://github.com/beanapologist/seed/issues)

---

## Getting Help

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/beanapologist/seed/issues)
2. Search [GitHub Discussions](https://github.com/beanapologist/seed/discussions)
3. Open a new issue with:
   - Your OS and version
   - Python/Node.js version
   - Full error message
   - Steps to reproduce

---

**GoldenSeed** - Deterministic. Reproducible. Cross-Platform.
