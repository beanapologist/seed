# Contributing to GoldenSeed

Thank you for your interest in contributing to GoldenSeed! We welcome contributions from developers, researchers, artists, and users of all skill levels.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project is dedicated to providing a welcoming and inclusive environment for all contributors. By participating, you agree to:

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences
- Accept responsibility for your actions

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Help us fix it!

1. **Check existing issues** to avoid duplicates
2. **Create a detailed bug report** including:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (Python version, OS, etc.)
   - Code samples or test cases

**Template:**
```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- Python version: 3.11
- OS: Ubuntu 22.04
- GoldenSeed version: 3.0.0
```

### 💡 Suggesting Enhancements

Have an idea to make GoldenSeed better?

1. **Check [Discussions](https://github.com/beanapologist/seed/discussions)** for similar ideas
2. **Open a discussion** to get feedback before implementing
3. **Describe your idea** including:
   - Use case and motivation
   - Proposed solution
   - Potential drawbacks or alternatives
   - Impact on existing functionality

### 📝 Improving Documentation

Documentation improvements are always welcome!

- Fix typos or unclear explanations
- Add examples and tutorials
- Improve API documentation
- Translate documentation
- Create visual guides or diagrams

### 🎨 Contributing Examples

Show others how to use GoldenSeed!

- Procedural generation examples
- Game development integration
- Data compression demonstrations
- Creative coding projects
- Performance benchmarks

### 🔧 Contributing Code

See [Development Workflow](#development-workflow) below.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/seed.git
cd seed
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify setup
pytest
```

### 3. Create a Branch

```bash
# Create a descriptive branch name
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## Development Workflow

### Making Changes

1. **Write tests first** (TDD approach recommended)
2. **Implement your changes**
3. **Run tests** to ensure nothing breaks
4. **Update documentation** if needed
5. **Add examples** if introducing new features

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gq --cov-report=html

# Run specific test file
pytest test_gqs1.py

# Run tests matching pattern
pytest -k "test_deterministic"
```

### Code Quality Checks

```bash
# Format code (if you have black installed)
black src/ tests/

# Lint code (if you have flake8 installed)
flake8 src/ tests/

# Type checking (if you have mypy installed)
mypy src/
```

## Pull Request Process

### Before Submitting

- ✅ All tests pass locally
- ✅ Code follows project style guidelines
- ✅ Documentation updated (if applicable)
- ✅ Commit messages are clear and descriptive
- ✅ Branch is up to date with main

### Submitting Your PR

1. **Push your branch** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub

3. **Fill out the PR template** with:
   - Clear description of changes
   - Related issues (use "Fixes #123" to auto-close)
   - Testing done
   - Screenshots (if applicable)

4. **Respond to feedback** and make requested changes

### PR Template

```markdown
## Description
Brief description of what this PR does

## Related Issues
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for changes
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No breaking changes (or clearly documented)
```

## Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **descriptive variable names**
- Keep functions focused and small
- Add **docstrings** to all public functions/classes
- Use **type hints** where helpful

**Example:**
```python
def generate_chunk(self, x: int, z: int) -> dict:
    """
    Generate terrain for a world chunk at coordinates (x, z).

    Args:
        x: Chunk X coordinate
        z: Chunk Z coordinate

    Returns:
        Dictionary with terrain properties including biome, elevation, etc.
    """
    chunk_bytes = next(self.generator)
    # ... implementation
```

### Commit Messages

Write clear, descriptive commit messages:

**Good:**
- `Add procedural terrain generation example`
- `Fix deterministic behavior on Windows`
- `Improve performance of chunk generation by 25%`

**Bad:**
- `Update code`
- `Fix bug`
- `Changes`

**Format:**
```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain what changed and why, not how.

- Bullet points are fine
- Use present tense: "Add feature" not "Added feature"

Fixes #123
```

## Testing Guidelines

### Test Coverage

- Aim for **>90% code coverage**
- Test edge cases and error conditions
- Include cross-platform compatibility tests
- Add performance benchmarks for critical paths

### Writing Tests

```python
def test_deterministic_generation():
    """Test that same seed produces same output."""
    gen1 = UniversalQKD()
    gen2 = UniversalQKD()

    chunk1 = next(gen1)
    chunk2 = next(gen2)

    assert chunk1 == chunk2, "Generators should produce identical output"
```

### Test Organization

- One test file per source file (e.g., `test_gqs1.py` for `gqs1.py`)
- Group related tests in classes
- Use descriptive test names that explain what is being tested

## Documentation

### Docstrings

Use **Google-style docstrings**:

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Short description of what the function does.

    Longer description with more details if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is negative

    Example:
        >>> example_function(42, "test")
        True
    """
    # ... implementation
```

### README Updates

When adding features, update:
- Installation instructions (if dependencies change)
- Quick Start examples (if API changes)
- API reference (if new public functions)
- Examples section (if new use cases)

## Good First Issues

Looking for a place to start? Check out issues labeled **good first issue**:

- [Good First Issues](https://github.com/beanapologist/seed/labels/good%20first%20issue)

These are typically:
- Well-defined tasks
- Limited in scope
- Good for learning the codebase
- Have clear acceptance criteria

## Community

### Getting Help

- **GitHub Discussions**: Ask questions, share ideas
- **Issue Tracker**: Report bugs, request features
- **Pull Requests**: Get feedback on code

### Stay Connected

- Watch the repository for updates
- Star the repo to show support
- Share your projects using GoldenSeed

## License

By contributing to GoldenSeed, you agree that your contributions will be licensed under the **GPL-3.0+ license** with the same additional use restrictions as the main project.

This means:
- ✓ Your code will be freely available for games, art, education, research
- ❌ Your code cannot be used for military-industrial applications

See [LICENSE](LICENSE) for full details.

---

## Recognition

Contributors are recognized in:
- GitHub contributor graphs
- Release notes (for significant contributions)
- Special mentions for outstanding contributions

Thank you for making GoldenSeed better for everyone!

---

**Questions?** Open a [Discussion](https://github.com/beanapologist/seed/discussions) and we'll help you get started!
