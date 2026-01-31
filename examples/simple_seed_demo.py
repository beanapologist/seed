#!/usr/bin/env python3
"""
Simple Procedural Seed Demo for GoldenSeed

This demo showcases how different seeds produce unique, deterministic outputs.
Perfect for demonstrating procedural generation concepts.

No external dependencies required - runs with just the golden-seed package!

Usage:
    python3 simple_seed_demo.py [seed_number]

⚠️ NOT FOR CRYPTOGRAPHY: This is for procedural generation demonstrations only.
"""

import sys
import os

# Add parent directory to path for imports
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(repo_root, 'src'))

try:
    from gq import UniversalQKD
except ImportError:
    print("Error: Could not import gq module.")
    print("Run: pip install golden-seed")
    sys.exit(1)


def get_seeded_generator(seed_value):
    """Create a generator at a specific offset."""
    generator = UniversalQKD()
    skip = seed_value % 100
    for _ in range(skip):
        next(generator)
    return generator


def generate_ascii_art(seed_value, width=50, height=8):
    """Generate ASCII art from a seed."""
    generator = get_seeded_generator(seed_value)
    
    chars = " .:-=+*#%@"
    lines = []
    
    for _ in range(height):
        line = []
        remaining = width
        while remaining > 0:
            chunk = next(generator)
            chars_to_take = min(16, remaining)
            line.extend(chars[chunk[i] % len(chars)] for i in range(chars_to_take))
            remaining -= chars_to_take
        lines.append(''.join(line))
    
    return '\n'.join(lines)


def generate_color_palette(seed_value, count=5):
    """Generate a color palette from a seed."""
    generator = get_seeded_generator(seed_value)
    
    colors = []
    for _ in range(count):
        chunk = next(generator)
        r, g, b = chunk[0], chunk[1], chunk[2]
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return colors


def generate_stats(seed_value):
    """Generate statistics from a seed."""
    generator = get_seeded_generator(seed_value)
    
    chunk = next(generator)
    return {
        'complexity': (chunk[0] % 100) + 1,
        'density': (chunk[1] % 10) + 1,
        'variation': (chunk[2] % 100) + 1,
        'harmony': (chunk[3] % 100) + 1,
    }


def generate_pattern(seed_value, size=10):
    """Generate a simple character pattern."""
    generator = get_seeded_generator(seed_value)
    
    chars = "█▓▒░ "
    lines = []
    
    for _ in range(size):
        chunk = next(generator)
        line = ''.join(chars[b % len(chars)] for b in chunk[:size])
        lines.append(line)
    
    return '\n'.join(lines)


def display_demo(seed_value):
    """Display complete demo."""
    print("=" * 70)
    print(f"  GOLDENSEED PROCEDURAL GENERATION DEMO")
    print(f"  Seed: {seed_value}")
    print("=" * 70)
    print()
    
    print("🎨 ASCII Art Pattern:")
    print("-" * 70)
    art = generate_ascii_art(seed_value, width=60, height=8)
    print(art)
    print()
    
    print("🎨 Color Palette:")
    print("-" * 70)
    colors = generate_color_palette(seed_value, count=6)
    for i, color in enumerate(colors, 1):
        print(f"  Color {i}: {color}")
    print()
    
    print("📊 Pattern Statistics:")
    print("-" * 70)
    stats = generate_stats(seed_value)
    for key, value in stats.items():
        bar = "█" * (value // 10)
        print(f"  {key.capitalize():12s}: {value:3d} {bar}")
    print()
    
    print("🔲 Character Grid:")
    print("-" * 70)
    pattern = generate_pattern(seed_value, size=12)
    print(pattern)
    print()
    
    print("=" * 70)
    print("  ✨ Each seed produces unique, deterministic output!")
    print("  🔁 Same seed always produces the same results")
    print("  🎲 Try different seeds to see infinite variations")
    print("=" * 70)


def show_comparison():
    """Show comparison of different seeds."""
    print()
    print("=" * 70)
    print("  SEED COMPARISON: Different Seeds → Different Outputs")
    print("=" * 70)
    print()
    
    seeds = [0, 42, 100, 999, 12345]
    for seed in seeds:
        pattern = generate_pattern(seed, size=8)
        first_line = pattern.split('\n')[0]
        print(f"Seed {seed:5d} | {first_line}")
    
    print()
    print("=" * 70)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        try:
            seed_value = int(sys.argv[1])
        except ValueError:
            print("Error: Seed must be an integer")
            print("Usage: python3 simple_seed_demo.py [seed_number]")
            sys.exit(1)
    else:
        seed_value = 42
    
    display_demo(seed_value)
    show_comparison()
    
    print()
    print("💡 Try different seeds:")
    print(f"   python3 {os.path.basename(__file__)} 0")
    print(f"   python3 {os.path.basename(__file__)} 999")
    print(f"   python3 {os.path.basename(__file__)} 12345")
    print()


if __name__ == "__main__":
    main()
