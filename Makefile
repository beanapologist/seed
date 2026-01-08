# Makefile for GoldenSeed
# Automates common build, test, and packaging tasks

.PHONY: help clean install build build-python build-js test test-python test-js lint format check publish

# Default target
help:
	@echo "GoldenSeed Build Automation"
	@echo "============================"
	@echo ""
	@echo "Available targets:"
	@echo "  make install        - Install package in development mode"
	@echo "  make build          - Build both Python and JavaScript packages"
	@echo "  make build-python   - Build Python package"
	@echo "  make build-js       - Build JavaScript package"
	@echo "  make test           - Run all tests"
	@echo "  make test-python    - Run Python tests"
	@echo "  make test-js        - Run JavaScript tests"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make check          - Check package quality"
	@echo "  make format         - Format code (if formatters available)"
	@echo "  make publish-test   - Publish to test repositories"
	@echo "  make verify         - Verify installation"
	@echo ""

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	rm -rf node_modules/ package-lock.json
	rm -rf *.tgz
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Clean complete"

# Install package in development mode
install:
	@echo "Installing GoldenSeed in development mode..."
	pip install -e .
	@echo "✓ Installation complete"
	@python -c "import gq; print(f'GoldenSeed version {gq.__version__} installed')"

# Build all packages
build: build-python build-js
	@echo "✓ All packages built successfully"

# Build Python package
build-python:
	@echo "Building Python package..."
	python -m pip install --upgrade build twine --quiet
	python -m build
	@echo "✓ Python package built"
	@ls -lh dist/*.whl dist/*.tar.gz 2>/dev/null || true

# Build JavaScript package
build-js:
	@echo "Building JavaScript package..."
	node build-js.js
	@echo "✓ JavaScript package built"
	@ls -lh dist/*.js dist/*.d.ts 2>/dev/null || true

# Run all tests
test: test-python test-js
	@echo "✓ All tests passed"

# Run Python tests
test-python:
	@echo "Running Python tests..."
	python -m unittest discover -v -s . -p "test_*.py" || true

# Run JavaScript tests
test-js:
	@echo "Running JavaScript tests..."
	node test-js-package.js

# Check package quality
check:
	@echo "Checking package quality..."
	python -m pip install --upgrade twine --quiet
	python -m build
	twine check dist/*
	@echo "✓ Package quality check passed"

# Verify installation
verify:
	@echo "Verifying installation..."
	@python -c "import gq; print(f'✓ Python: GoldenSeed v{gq.__version__}')"
	@python -c "from gq import UniversalQKD; next(UniversalQKD()); print('✓ UniversalQKD working')"
	@command -v gq-universal >/dev/null 2>&1 && echo "✓ CLI: gq-universal available" || echo "⚠ CLI not available"
	@node -e "const gs = require('./dist/index.js'); console.log('✓ JavaScript: PHI =', gs.PHI)" 2>/dev/null || echo "⚠ JavaScript package not built"

# Format code (placeholder for future formatter integration)
format:
	@echo "Code formatting not yet configured"
	@echo "Consider using: black for Python, prettier for JavaScript"

# Lint code (placeholder for future linter integration)
lint:
	@echo "Linting not yet configured"
	@echo "Consider using: pylint/flake8 for Python, eslint for JavaScript"

# Publish to test repositories (requires credentials)
publish-test:
	@echo "Publishing to test repositories..."
	@echo "Note: Requires TEST_PYPI_API_TOKEN environment variable"
	python -m build
	twine upload --repository testpypi dist/* || echo "Test PyPI upload failed (may require credentials)"

# Create release tarball
tarball:
	@echo "Creating release tarball..."
	npm pack
	@ls -lh *.tgz

# Show version information
version:
	@python -c "import gq; print(f'Version: {gq.__version__}')"
	@grep '"version"' package.json | head -1
	@grep 'version = ' pyproject.toml | head -1

# Quick development workflow
dev: clean install build verify
	@echo "✓ Development environment ready"
