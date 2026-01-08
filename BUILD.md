# Building GoldenSeed Packages

This guide explains how to build distribution packages for **GoldenSeed** for various platforms and package managers.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Building Python Packages](#building-python-packages)
- [Building JavaScript Packages](#building-javascript-packages)
- [Cross-Platform Testing](#cross-platform-testing)
- [Automated Builds](#automated-builds)

---

## Prerequisites

### For Python Package Building

```bash
# Install build tools
pip install build twine

# Optional: For checking package quality
pip install check-manifest
```

### For JavaScript Package Building

```bash
# Ensure Node.js is installed (14.0.0+)
node --version

# No additional dependencies required
```

---

## Building Python Packages

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info
```

### 2. Build Source Distribution and Wheel

```bash
# Build both source distribution (.tar.gz) and wheel (.whl)
python -m build

# This creates:
# - dist/golden-seed-3.0.0.tar.gz
# - dist/golden_seed-3.0.0-py3-none-any.whl
```

### 3. Verify Package Quality

```bash
# Check package with twine
twine check dist/*

# Expected output:
# Checking dist/golden-seed-3.0.0.tar.gz: PASSED
# Checking dist/golden_seed-3.0.0-py3-none-any.whl: PASSED
```

### 4. Test Installation

```bash
# Install from wheel
pip install dist/golden_seed-3.0.0-py3-none-any.whl

# Or install from source distribution
pip install dist/golden-seed-3.0.0.tar.gz

# Verify
python -c "import gq; print(gq.__version__)"
```

---

## Building JavaScript Packages

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/
```

### 2. Build Distribution

```bash
# Run build script
node build-js.js

# This creates:
# - dist/index.js (main entry point)
# - dist/index.d.ts (TypeScript definitions)
# - dist/binary_fusion_tap.js (implementation)
```

### 3. Test JavaScript Package

```bash
# Test with Node.js
node test-js-package.js

# Or test manually
node -e "const gs = require('./dist/index.js'); console.log('PHI:', gs.PHI);"
```

### 4. Create npm Package

```bash
# Create tarball for distribution
npm pack

# This creates:
# - beanapologist-golden-seed-3.0.0.tgz
```

### 5. Test npm Package

```bash
# Install locally
npm install ./beanapologist-golden-seed-3.0.0.tgz

# Test
node -e "const gs = require('@beanapologist/golden-seed'); console.log(gs.PHI);"
```

---

## Cross-Platform Testing

### Test on Linux

```bash
# Using Docker
docker run -v $(pwd):/workspace -w /workspace python:3.11 bash -c "
  pip install build && 
  python -m build && 
  pip install dist/*.whl && 
  python -c 'import gq; print(gq.__version__)'
"
```

### Test on macOS

```bash
# Install and test
./install.sh
python3 -c "import gq; print(gq.__version__)"
```

### Test on Windows

```cmd
REM Run installation script
install.bat

REM Verify
python -c "import gq; print(gq.__version__)"
```

---

## Automated Builds

### GitHub Actions

The repository includes GitHub Actions workflows for automated building and testing:

#### Build and Test Workflow

**File**: `.github/workflows/build-packages.yml`

Triggers:
- Push to main, develop, or copilot/* branches
- Pull requests to main or develop
- Manual workflow dispatch

Jobs:
- **build-python**: Builds Python packages on multiple OS and Python versions
- **build-javascript**: Builds JavaScript packages on multiple OS and Node.js versions
- **test-installation-scripts**: Tests installation scripts
- **package-quality**: Runs quality checks

#### Publish Workflow

**File**: `.github/workflows/publish-packages.yml`

Triggers:
- Release published on GitHub
- Manual workflow dispatch

Jobs:
- **publish-pypi**: Publishes to PyPI
- **publish-npm**: Publishes to npm
- **create-release-artifacts**: Creates and uploads release artifacts

### Manual Workflow Trigger

```bash
# Using GitHub CLI
gh workflow run build-packages.yml

# Or via GitHub UI:
# Actions > Build and Test Packages > Run workflow
```

---

## Build Verification Checklist

Before releasing:

- [ ] **Clean build environment**
  ```bash
  rm -rf dist/ build/ *.egg-info node_modules/
  ```

- [ ] **Build Python package**
  ```bash
  python -m build
  twine check dist/*
  ```

- [ ] **Build JavaScript package**
  ```bash
  node build-js.js
  node test-js-package.js
  ```

- [ ] **Test Python installation**
  ```bash
  pip install dist/*.whl
  python -c "import gq; print(gq.__version__)"
  gq-universal --help
  ```

- [ ] **Test JavaScript installation**
  ```bash
  npm pack
  npm install ./beanapologist-golden-seed-*.tgz
  node -e "const gs = require('@beanapologist/golden-seed'); console.log(gs.PHI);"
  ```

- [ ] **Test on multiple platforms**
  - Linux (Ubuntu, Fedora, Arch)
  - macOS (Intel, Apple Silicon)
  - Windows (10, 11)

- [ ] **Verify metadata**
  - Version number matches in all files
  - License files included
  - README and documentation up to date

- [ ] **Run tests**
  ```bash
  python -m unittest discover -v
  ```

---

## Troubleshooting

### Python Build Issues

**Issue**: "No module named 'build'"
```bash
pip install build
```

**Issue**: "Package not found after installation"
```bash
# Reinstall in editable mode
pip install -e .
```

**Issue**: "twine check fails"
```bash
# Rebuild package
rm -rf dist/ build/ *.egg-info
python -m build
```

### JavaScript Build Issues

**Issue**: "Cannot find module 'fs'"
```bash
# Ensure Node.js is properly installed
node --version
```

**Issue**: "Binary fusion tap not copied"
```bash
# Check source file exists
ls releases/binary-fusion-tap-v2.0.0/javascript/binary_fusion_tap.js
```

**Issue**: "npm pack fails"
```bash
# Ensure dist/ directory exists and contains built files
node build-js.js
ls dist/
```

---

## Additional Resources

- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [Python Packaging Guide](https://packaging.python.org/)
- [npm Publishing Guide](https://docs.npmjs.com/cli/v8/commands/npm-publish)

---

**GoldenSeed** - Professional Cross-Platform Package Building
