# Deployment Guide

This guide provides instructions for publishing **GoldenSeed** to package managers (PyPI and npm) and creating release distributions.

## Table of Contents

- [Overview](#overview)
- [PyPI Deployment (Python)](#pypi-deployment-python)
- [npm Deployment (JavaScript)](#npm-deployment-javascript)
- [GitHub Releases](#github-releases)
- [Version Management](#version-management)
- [Pre-Release Checklist](#pre-release-checklist)
- [Post-Release Tasks](#post-release-tasks)

---

## Overview

GoldenSeed supports multiple deployment targets:

- **PyPI** - Python Package Index for pip installation
- **npm** - Node Package Manager for JavaScript/Node.js
- **GitHub Releases** - Source distributions and compiled releases

---

## PyPI Deployment (Python)

### Prerequisites

1. PyPI account ([register here](https://pypi.org/account/register/))
2. Install build tools:

```bash
pip install build twine
```

### Build Distribution Packages

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build

# This creates:
# - dist/golden-seed-3.0.0.tar.gz (source distribution)
# - dist/golden_seed-3.0.0-py3-none-any.whl (wheel)
```

### Test on Test PyPI (Recommended)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ golden-seed
```

### Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# Enter your PyPI credentials when prompted
# Or use API token:
twine upload --username __token__ --password pypi-YOUR-TOKEN-HERE dist/*
```

### Configure PyPI Credentials (Optional)

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-PRODUCTION-TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-TOKEN
```

### Verify PyPI Deployment

```bash
# Install from PyPI
pip install golden-seed

# Test import
python -c "import gq; print(gq.__version__)"
```

---

## npm Deployment (JavaScript)

### Prerequisites

1. npm account ([register here](https://www.npmjs.com/signup))
2. Login to npm:

```bash
npm login
```

### Build JavaScript Distribution

```bash
# Clean previous builds
rm -rf dist/ node_modules/

# Install dependencies
npm install

# Build distribution
npm run build

# This creates:
# - dist/index.js (main entry point)
# - dist/index.d.ts (TypeScript definitions)
# - dist/binary_fusion_tap.js (implementation)
```

### Test Package Locally

```bash
# Create tarball
npm pack

# This creates: beanapologist-golden-seed-3.0.0.tgz

# Test installation locally
npm install ./beanapologist-golden-seed-3.0.0.tgz

# Test in Node.js
node -e "const gs = require('@beanapologist/golden-seed'); console.log(gs.PHI);"
```

### Publish to npm

```bash
# Dry run (recommended first)
npm publish --dry-run

# Publish to npm
npm publish --access public

# For scoped packages, use:
npm publish --access public
```

### Verify npm Deployment

```bash
# Install from npm
npm install @beanapologist/golden-seed

# Test in Node.js
node -e "const gs = require('@beanapologist/golden-seed'); console.log('Version:', gs.PHI);"
```

---

## GitHub Releases

### Create Release

1. **Tag the version:**

```bash
git tag -a v3.0.0 -m "Release version 3.0.0"
git push origin v3.0.0
```

2. **Build release artifacts:**

```bash
# Python source distribution
python -m build

# JavaScript distribution
npm run build
npm pack

# Create release directory
mkdir -p release-artifacts/
cp dist/golden-seed-3.0.0.tar.gz release-artifacts/
cp dist/golden_seed-3.0.0-py3-none-any.whl release-artifacts/
cp beanapologist-golden-seed-3.0.0.tgz release-artifacts/
```

3. **Create GitHub Release:**

Go to https://github.com/beanapologist/seed/releases/new

- Tag: v3.0.0
- Title: GoldenSeed v3.0.0
- Description: (See template below)
- Attach artifacts from `release-artifacts/`

### Release Notes Template

```markdown
# GoldenSeed v3.0.0

## 📦 Installation

**Python (PyPI):**
```bash
pip install golden-seed
```

**JavaScript (npm):**
```bash
npm install @beanapologist/golden-seed
```

**From Source:**
```bash
git clone https://github.com/beanapologist/seed.git
cd seed
./install.sh  # Linux/macOS
install.bat   # Windows
```

## ✨ New Features

- Cross-platform packaging for PyPI and npm
- Automated installation scripts for Windows, macOS, and Linux
- Enhanced documentation and deployment guides

## 📚 Documentation

- [Installation Guide](INSTALLATION.md)
- [Deployment Guide](DEPLOYMENT.md)
- [README](README.md)

## 📦 Release Artifacts

- `golden-seed-3.0.0.tar.gz` - Python source distribution
- `golden_seed-3.0.0-py3-none-any.whl` - Python wheel
- `beanapologist-golden-seed-3.0.0.tgz` - npm package

## 🔗 Links

- **PyPI**: https://pypi.org/project/golden-seed/
- **npm**: https://www.npmjs.com/package/@beanapologist/golden-seed
- **Documentation**: https://github.com/beanapologist/seed#readme

## ⚠️ Important Notes

- NOT FOR CRYPTOGRAPHY: This library is for procedural generation and testing only
- PROHIBITED for military-industrial applications (see LICENSE_RESTRICTIONS.md)

---

**Full Changelog**: https://github.com/beanapologist/seed/blob/main/CHANGELOG.md
```

---

## Version Management

### Update Version Numbers

Update version in multiple files before release:

1. **`pyproject.toml`**:
```toml
version = "3.0.0"
```

2. **`setup.py`**:
```python
version="3.0.0",
```

3. **`package.json`**:
```json
"version": "3.0.0",
```

4. **`src/gq/__init__.py`**:
```python
__version__ = "3.0.0"
```

5. **`VERSION`**:
```
3.0.0
```

### Automated Version Update Script

```bash
#!/bin/bash
# update-version.sh

NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./update-version.sh <version>"
    exit 1
fi

# Update all version files
sed -i "s/version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
sed -i "s/version=\".*\"/version=\"$NEW_VERSION\"/" setup.py
sed -i "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" package.json
sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" src/gq/__init__.py
echo "$NEW_VERSION" > VERSION

echo "✓ Updated version to $NEW_VERSION"
```

---

## Pre-Release Checklist

Before publishing a release:

- [ ] **Update version numbers** in all files
- [ ] **Update CHANGELOG.md** with new features and fixes
- [ ] **Run all tests** and ensure they pass
  ```bash
  python -m unittest discover -v
  ```
- [ ] **Test installation** from source
  ```bash
  pip install -e .
  python -c "import gq; print(gq.__version__)"
  ```
- [ ] **Build and test Python package**
  ```bash
  python -m build
  twine check dist/*
  ```
- [ ] **Build and test JavaScript package**
  ```bash
  npm run build
  npm test
  ```
- [ ] **Update documentation** if needed
- [ ] **Review LICENSE and restrictions**
- [ ] **Test on multiple platforms** (Linux, macOS, Windows)
- [ ] **Create git tag**
  ```bash
  git tag -a v3.0.0 -m "Release v3.0.0"
  ```

---

## Post-Release Tasks

After publishing:

- [ ] **Announce release** on GitHub Discussions
- [ ] **Update documentation** website (if applicable)
- [ ] **Test installation** from PyPI and npm
  ```bash
  pip install --upgrade golden-seed
  npm install @beanapologist/golden-seed
  ```
- [ ] **Monitor for issues** on GitHub
- [ ] **Update badges** in README if needed

---

## Continuous Integration / Continuous Deployment

### GitHub Actions Workflow (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish Package

on:
  release:
    types: [published]

jobs:
  publish-pypi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*

  publish-npm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build package
        run: npm run build
      
      - name: Publish to npm
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npm publish --access public
```

### Required Secrets

Add these secrets to your GitHub repository:

- `PYPI_API_TOKEN` - PyPI API token
- `NPM_TOKEN` - npm authentication token

---

## Troubleshooting

### PyPI Upload Fails

**Error: "Invalid distribution"**
```bash
# Check package
twine check dist/*

# Rebuild if needed
rm -rf dist/ build/ *.egg-info
python -m build
```

**Error: "File already exists"**
```bash
# Version already published - increment version number
```

### npm Publish Fails

**Error: "You must be logged in"**
```bash
npm login
npm whoami  # Verify login
```

**Error: "Package name already exists"**
```bash
# Use scoped package name: @beanapologist/golden-seed
```

---

## Publishing Checklist Summary

1. ✅ Update version numbers
2. ✅ Run tests
3. ✅ Build packages
4. ✅ Test locally
5. ✅ Upload to Test PyPI (optional)
6. ✅ Upload to PyPI
7. ✅ Publish to npm
8. ✅ Create GitHub Release
9. ✅ Update documentation
10. ✅ Announce release

---

## Additional Resources

- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [npm Publishing Guide](https://docs.npmjs.com/cli/v8/commands/npm-publish)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

---

**GoldenSeed** - Streamlined Deployment for Cross-Platform Excellence
