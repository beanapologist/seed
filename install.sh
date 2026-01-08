#!/bin/bash

# GoldenSeed Installation Script for Unix-like Systems (Linux, macOS)
# This script installs the golden-seed package from source

set -e

echo "=================================="
echo "GoldenSeed Installation"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=macOS;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "Platform detected: ${PLATFORM}"
echo ""

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python 3 found: ${PYTHON_VERSION}"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 not found. Please install pip3."
    exit 1
fi

echo ""
echo "Installing golden-seed package..."
echo ""

# Install package in development mode
pip3 install -e . || {
    print_error "Installation failed"
    exit 1
}

print_success "Package installed successfully!"
echo ""

# Verify installation
echo "Verifying installation..."
python3 -c "import gq; print(f'GoldenSeed version {gq.__version__} installed successfully')" 2>/dev/null || {
    print_error "Installation verification failed"
    echo "The package was installed but could not be imported. This may indicate:"
    echo "  - Path issues with Python modules"
    echo "  - Missing dependencies"
    echo "  - Installation errors"
    exit 1
}

print_success "Installation verified!"
echo ""

# Show CLI commands
echo "Available CLI commands:"
echo "  • gq-universal       - Universal deterministic stream generator"
echo "  • gq-test-vectors    - Generate test vectors"
echo "  • gq-coin-flip       - Golden ratio coin flip generator"
echo ""

print_success "Installation complete!"
echo ""
echo "To get started, try:"
echo "  python3 -c 'from gq import UniversalQKD; print(next(UniversalQKD()).hex())'"
echo ""
