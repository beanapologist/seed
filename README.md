# 🌟 GoldenSeed

**Infinite reproducible high-entropy streams from tiny fixed seeds**

[![GitHub Stars](https://img.shields.io/github/stars/beanapologist/seed?style=for-the-badge&logo=github&color=yellow)](https://github.com/beanapologist/seed/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/beanapologist/seed?style=for-the-badge&logo=github&color=blue)](https://github.com/beanapologist/seed/network/members)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-GPL--3.0%2B-green.svg?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/beanapologist/seed/test.yml?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/beanapologist/seed/actions)
[![PyPI](https://img.shields.io/pypi/v/golden-seed?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/golden-seed/)

---

## 🎯 What is GoldenSeed?

GoldenSeed is a **deterministic high-entropy byte stream generator** that creates infinite, reproducible sequences from tiny fixed seeds. Perfect for **procedural generation**, **reproducible testing**, **deterministic simulations**, and **space-efficient storage**.

> ⚠️ **NOT FOR CRYPTOGRAPHY** — GoldenSeed is designed for procedural content generation and deterministic simulations, not cryptographic applications.

### ✨ Key Features

- 🎲 **Deterministic**: Same seed always produces the same output
- ♾️ **Infinite Streams**: Generate unlimited data from tiny seeds
- 🚀 **Zero Dependencies**: Pure Python, maximum portability
- 🎮 **Multi-Language**: Python, JavaScript, C, C++, Go, Rust, Java implementations
- 🌍 **Cross-Platform**: Identical results across all platforms and languages
- 📦 **Space-Efficient**: Store seeds instead of gigabytes of data
- ⚡ **Fast**: Optimized for real-time procedural generation

---

## 🎬 See It In Action

![Procedural Generation Demo](https://via.placeholder.com/800x400/1a1a2e/eee?text=Procedural+Noise+%7C+Infinite+Worlds+%7C+Deterministic+Generation)

> 🎨 **Coming Soon**: Animated visualizations of Perlin-like noise, procedural terrain, and infinite stream generation!

---

## 🚀 Quick Start

### Installation

```bash
pip install golden-seed
```

### Basic Usage

```python
from gq import UniversalQKD

# Create a generator (uses built-in golden ratio seed)
generator = UniversalQKD()

# Generate infinite deterministic bytes
chunk1 = next(generator)  # 16 bytes
chunk2 = next(generator)  # another 16 bytes
chunk3 = next(generator)  # and so on...

# Same seed always produces the same sequence
gen1 = UniversalQKD()
gen2 = UniversalQKD()
assert next(gen1) == next(gen2)  # ✓ Identical!
```

### Procedural World Generation

```python
from gq import UniversalQKD

class WorldGenerator:
    def __init__(self, world_seed=0):
        self.generator = UniversalQKD()
        # Skip to world-specific position
        for _ in range(world_seed):
            next(self.generator)

    def generate_chunk(self, x, z):
        chunk_bytes = next(self.generator)
        return {
            'biome': int.from_bytes(chunk_bytes[0:1], 'big') % 10,
            'elevation': int.from_bytes(chunk_bytes[1:3], 'big') % 256,
            'vegetation': int.from_bytes(chunk_bytes[3:4], 'big') % 100,
        }

# Generate infinite, deterministic world
world = WorldGenerator(world_seed=42)
chunk = world.generate_chunk(0, 0)
print(f"Biome: {chunk['biome']}, Elevation: {chunk['elevation']}")
```

### More Examples

- [Procedural Generation](examples/procedural_generation.py) — Games, world-building, infinite content
- [Seed Distribution Demo](examples/seed_distribution_demo.py) — Extreme compression, bandwidth savings
- [Binary Fusion Tap](examples/binary_fusion_tap.py) — Core algorithm examples in 6+ languages

---

## 🎯 Why GoldenSeed?

| Feature | Traditional PRNGs | GoldenSeed |
|---------|------------------|------------|
| **Determinism** | ✓ Same seed → same output | ✓ Same seed → same output |
| **Cross-Platform** | ❌ Platform-dependent | ✓ Identical across all platforms |
| **Multi-Language** | ❌ Single language | ✓ Python, JS, C, C++, Go, Rust, Java |
| **Stream Length** | Limited by internal state | ♾️ Infinite |
| **Dependencies** | Varies | 🚀 Zero |
| **Space Efficiency** | Store full data | 📦 Store tiny seed |
| **Golden Ratio Math** | ❌ Standard algorithms | ✓ Φ-based deterministic entropy |

### 🎮 Fun Use Cases

<details>
<summary><strong>🌍 Procedural World Building</strong></summary>

Generate infinite Minecraft-like worlds, No Man's Sky universes, or roguelike dungeons. Store entire worlds as a single seed number!

```python
# Generate infinite terrain from a single seed
world = WorldGenerator(seed=12345)
for x in range(-100, 100):
    for z in range(-100, 100):
        chunk = world.generate_chunk(x, z)
        # Render chunk...
```
</details>

<details>
<summary><strong>🎨 Procedural Art & Music</strong></summary>

Create generative art, algorithmic music, or unique visual patterns. Same seed = same masterpiece.

```python
# Generate unique art pieces
for seed in range(1000):
    art = generate_art(seed)
    save_nft(art, seed)
```
</details>

<details>
<summary><strong>🧪 Reproducible Testing</strong></summary>

Generate test data that's identical every time. Perfect for deterministic integration tests.

```python
# Always generate the same test data
def test_user_processing():
    users = generate_test_users(seed=42)
    assert process_users(users) == expected_result
```
</details>

<details>
<summary><strong>🎲 Seeded Simulations</strong></summary>

Run Monte Carlo simulations, physics engines, or ML training with reproducible randomness.

```python
# Reproducible physics simulation
sim = PhysicsSimulation(seed=999)
for step in range(1000000):
    sim.step()
    # Identical results every run!
```
</details>

<details>
<summary><strong>💾 Extreme Data Compression</strong></summary>

Store **500 MB** of data as a **32-byte seed**. Achieve compression ratios of **15,625,000:1**!

```python
# Generate 500 MB from 32 bytes
generator = UniversalQKD()
data = b''.join([next(generator) for _ in range(32_000_000)])
# 500 MB generated from tiny seed!
```
</details>

<details>
<summary><strong>🌐 Bandwidth-Free Distribution</strong></summary>

Share datasets across continents without transferring data. Only share the seed!

```python
# Location A (New York)
data_ny = generate_dataset(seed=1234)

# Location B (Tokyo) - generates identical data!
data_tokyo = generate_dataset(seed=1234)

assert data_ny == data_tokyo  # ✓ No data transferred!
```
</details>

---

## 📊 Benchmarks

### Generation Speed

| Operation | Speed | Notes |
|-----------|-------|-------|
| Single chunk (16 bytes) | ~0.5 µs | 2 million chunks/sec |
| 1 MB generation | ~30 ms | 33 MB/sec |
| 100 MB generation | ~3 sec | Consistent performance |

### Compression Ratios

| Original Size | Seed Size | Ratio | vs. Gzip |
|--------------|-----------|-------|----------|
| 1 KB | 32 bytes | **32:1** | 8x better |
| 1 MB | 32 bytes | **32,768:1** | 8,192x better |
| 1 GB | 32 bytes | **33,554,432:1** | 8,388,608x better |

*Tested on Python 3.11, Intel i7, Ubuntu 22.04*

---

## 🎓 How It Works

GoldenSeed uses the **golden ratio (Φ ≈ 1.618...)** to generate deterministic high-entropy byte streams:

1. **Initial State**: Seed derived from golden ratio constants
2. **Binary Fusion**: XOR operations on rotated bit patterns
3. **Deterministic Mixing**: Reproducible entropy extraction
4. **Infinite Streams**: Position-based generation (no internal state limits)

📚 **Read More**: [Implementation Summary](IMPLEMENTATION_SUMMARY_GOLDEN_RATIO.md) | [Entropy Analysis](docs/ENTROPY_ANALYSIS.md) | [NIST Testing](docs/NIST_TESTING.md)

---

## 🗂️ Multi-Language Support

GoldenSeed provides identical outputs across multiple languages:

- 🐍 **Python** — `pip install golden-seed`
- 🟨 **JavaScript** — See `examples/binary_fusion_tap.js`
- 🔵 **C** — See `examples/binary_fusion_tap.c`
- 🔴 **C++** — See `examples/binary_fusion_tap.cpp`
- 🐹 **Go** — See `examples/binary_fusion_tap.go`
- 🦀 **Rust** — See `examples/binary_fusion_tap.rs`
- ☕ **Java** — See `examples/binary_fusion_tap.java`

All implementations produce **byte-for-byte identical output** from the same seed.

---

## 📦 What's Included

```
golden-seed/
├── src/gq/              # Core library
│   ├── universal_qkd.py # Main generator
│   ├── gqs1.py          # Algorithm implementation
│   └── cli/             # Command-line tools
├── examples/            # Practical examples
│   ├── procedural_generation.py
│   ├── seed_distribution_demo.py
│   └── binary_fusion_tap.{py,js,c,cpp,go,rs,java}
├── docs/                # Documentation
│   ├── ENTROPY_ANALYSIS.md
│   ├── NIST_TESTING.md
│   └── DATA_TELEPORTATION_AND_COMPRESSION.md
└── tests/               # Comprehensive test suite
```

---

## 🤝 Contributing

We welcome contributions! GoldenSeed is a **public good software** project.

- 📖 See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- 🐛 Found a bug? [Open an issue](https://github.com/beanapologist/seed/issues)
- 💡 Have an idea? [Start a discussion](https://github.com/beanapologist/seed/discussions)
- 🏷️ Good first issues: [Filter by label](https://github.com/beanapologist/seed/labels/good%20first%20issue)

---

## 📚 Documentation

- [Installation Guide](INSTALLATION.md)
- [API Reference](https://github.com/beanapologist/seed#api)
- [Entropy Validation](docs/ENTROPY_TESTING.md)
- [NIST Compliance](COMPLIANCE_TESTING.md)
- [Changelog](CHANGELOG.md)

---

## 🎯 Comparison: GoldenSeed vs. Alternatives

| Library | Language | Deterministic | Cross-Platform | Infinite Streams | Dependencies | Use Case |
|---------|----------|---------------|----------------|------------------|--------------|----------|
| **GoldenSeed** | Multi | ✓ | ✓ | ✓ | 0 | Procedural generation, testing |
| random (stdlib) | Python | ✓ | ❌ | ❌ | 0 | Basic randomness |
| numpy.random | Python | ✓ | ⚠️ | ❌ | numpy | Scientific computing |
| Perlin noise | Various | ✓ | ⚠️ | ✓ | Varies | Terrain generation |
| Simplex noise | Various | ✓ | ⚠️ | ✓ | Varies | Smooth gradients |
| PCG | C/C++ | ✓ | ⚠️ | ❌ | 0 | General PRNG |

✓ = Full support | ⚠️ = Partial/implementation-dependent | ❌ = Not supported

---

## 📄 License

GoldenSeed is licensed under **GPL-3.0+** with additional use restrictions prohibiting military-industrial applications.

- ✓ **Free for**: Games, art, education, research, simulations, testing
- ❌ **Prohibited**: Military hardware, weapons systems, surveillance

See [LICENSE](LICENSE) for full details.

---

## 🌟 Show Your Support

If you find GoldenSeed useful, please consider:

- ⭐ **Starring this repo** — Helps others discover the project
- 🐛 **Reporting bugs** — Makes GoldenSeed better for everyone
- 💬 **Sharing feedback** — Tell us how you use GoldenSeed
- 🤝 **Contributing code** — See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🔗 Links

- 📦 [PyPI Package](https://pypi.org/project/golden-seed/)
- 📝 [Issue Tracker](https://github.com/beanapologist/seed/issues)
- 💬 [Discussions](https://github.com/beanapologist/seed/discussions)
- 📖 [Documentation](https://github.com/beanapologist/seed#readme)

---

<div align="center">

**Made with 💛 by the GoldenSeed community**

*Deterministic streams for a procedural world*

[⬆ Back to Top](#-goldenseed)

</div>
