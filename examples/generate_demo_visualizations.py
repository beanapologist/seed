#!/usr/bin/env python3
"""
Generate Demo Visualizations for GoldenSeed

Creates animated GIFs and static images demonstrating:
1. Procedural noise generation (Perlin-like)
2. Infinite terrain generation
3. Deterministic color patterns
4. Stream distribution visualization

Usage:
    python3 generate_demo_visualizations.py [--output-dir demos]

Requirements:
    pip install matplotlib numpy pillow

⚠️ NOT FOR CRYPTOGRAPHY: These are demonstrations only.
"""

import sys
import os
import argparse
from pathlib import Path

# Add parent directory to path for imports
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, 'src'))

try:
    from gq import UniversalQKD
except ImportError:
    print("Error: Could not import gq module.")
    print("Run: pip install -e .")
    sys.exit(1)

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from matplotlib.colors import LinearSegmentedColormap
except ImportError:
    print("Error: Missing visualization dependencies.")
    print("Run: pip install matplotlib numpy pillow")
    sys.exit(1)


def generate_noise_field(width=256, height=256, seed_offset=0):
    """
    Generate a 2D noise field using GoldenSeed.

    Args:
        width: Field width in pixels
        height: Field height in pixels
        seed_offset: Seed offset for variation

    Returns:
        2D numpy array of noise values (0-255)
    """
    generator = UniversalQKD()

    # Skip to seed offset
    for _ in range(seed_offset):
        next(generator)

    # Generate noise field
    field = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(0, width, 16):  # Process 16 pixels at a time
            chunk = next(generator)
            for i in range(min(16, width - x)):
                if x + i < width:
                    field[y, x + i] = chunk[i]

    return field


def generate_terrain_heightmap(width=256, height=256, seed_offset=0):
    """
    Generate a procedural terrain heightmap.

    Args:
        width: Map width
        height: Map height
        seed_offset: Seed for different terrains

    Returns:
        2D array representing terrain elevation
    """
    generator = UniversalQKD()

    for _ in range(seed_offset):
        next(generator)

    # Generate base heightmap
    heightmap = np.zeros((height, width), dtype=np.float32)

    # Multi-octave generation for more natural terrain
    octaves = 3
    for octave in range(octaves):
        scale = 2 ** octave
        amplitude = 1.0 / scale

        for y in range(height):
            for x in range(0, width, 16):
                chunk = next(generator)
                for i in range(min(16, width - x)):
                    if x + i < width:
                        heightmap[y, x + i] += chunk[i] * amplitude

    # Normalize to 0-1
    heightmap = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min())

    return heightmap


def generate_color_pattern(width=256, height=256, seed_offset=0):
    """
    Generate colorful procedural patterns.

    Args:
        width: Pattern width
        height: Pattern height
        seed_offset: Seed offset

    Returns:
        RGB image array
    """
    generator = UniversalQKD()

    for _ in range(seed_offset):
        next(generator)

    # Generate RGB channels separately
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for channel in range(3):
        for y in range(height):
            for x in range(0, width, 16):
                chunk = next(generator)
                for i in range(min(16, width - x)):
                    if x + i < width:
                        image[y, x + i, channel] = chunk[i]

    return image


def create_static_demos(output_dir):
    """Create static demonstration images."""
    print("Generating static demos...")

    # 1. Noise field
    print("  - Noise field...")
    noise = generate_noise_field(512, 512, seed_offset=0)

    plt.figure(figsize=(10, 10))
    plt.imshow(noise, cmap='gray')
    plt.title('GoldenSeed Procedural Noise', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_dir / 'noise_demo.png', dpi=150, bbox_inches='tight')
    plt.close()

    # 2. Terrain heightmap
    print("  - Terrain heightmap...")
    terrain = generate_terrain_heightmap(512, 512, seed_offset=100)

    # Custom terrain colormap (water -> sand -> grass -> mountain -> snow)
    colors = ['#1a5490', '#2b7bb9', '#b8a57a', '#5a8f4f', '#8b7355', '#ffffff']
    n_bins = 256
    cmap = LinearSegmentedColormap.from_list('terrain', colors, N=n_bins)

    plt.figure(figsize=(10, 10))
    plt.imshow(terrain, cmap=cmap)
    plt.title('GoldenSeed Procedural Terrain', fontsize=16, fontweight='bold')
    plt.colorbar(label='Elevation', shrink=0.8)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_dir / 'terrain_demo.png', dpi=150, bbox_inches='tight')
    plt.close()

    # 3. Color patterns
    print("  - Color patterns...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    for idx, ax in enumerate(axes.flat):
        pattern = generate_color_pattern(256, 256, seed_offset=idx * 1000)
        ax.imshow(pattern)
        ax.set_title(f'Seed {idx * 1000}', fontsize=12, fontweight='bold')
        ax.axis('off')

    fig.suptitle('GoldenSeed Procedural Color Patterns', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'color_patterns_demo.png', dpi=150, bbox_inches='tight')
    plt.close()

    # 4. Determinism demonstration
    print("  - Determinism demo...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    seed_offset = 42
    for i in range(3):
        noise = generate_noise_field(256, 256, seed_offset=seed_offset)
        axes[i].imshow(noise, cmap='viridis')
        axes[i].set_title(f'Generation #{i+1}\n(Same Seed: {seed_offset})',
                         fontsize=12, fontweight='bold')
        axes[i].axis('off')

    fig.suptitle('Deterministic: Same Seed → Same Output',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'determinism_demo.png', dpi=150, bbox_inches='tight')
    plt.close()


def create_animated_demos(output_dir):
    """Create animated GIF demonstrations."""
    print("Generating animated demos...")

    # 1. Animated noise evolution
    print("  - Animated noise evolution...")

    fig, ax = plt.subplots(figsize=(8, 8))

    def update_noise(frame):
        ax.clear()
        noise = generate_noise_field(256, 256, seed_offset=frame * 10)
        ax.imshow(noise, cmap='plasma')
        ax.set_title(f'GoldenSeed Procedural Noise\nSeed Offset: {frame * 10}',
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        return ax,

    anim = FuncAnimation(fig, update_noise, frames=30, interval=100, blit=False)
    writer = PillowWriter(fps=10)
    anim.save(output_dir / 'noise_animated.gif', writer=writer)
    plt.close()

    # 2. Animated terrain evolution
    print("  - Animated terrain evolution...")

    fig, ax = plt.subplots(figsize=(8, 8))

    colors = ['#1a5490', '#2b7bb9', '#b8a57a', '#5a8f4f', '#8b7355', '#ffffff']
    cmap = LinearSegmentedColormap.from_list('terrain', colors, N=256)

    def update_terrain(frame):
        ax.clear()
        terrain = generate_terrain_heightmap(256, 256, seed_offset=frame * 50)
        im = ax.imshow(terrain, cmap=cmap)
        ax.set_title(f'GoldenSeed Procedural Terrain\nSeed: {frame * 50}',
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        return ax,

    anim = FuncAnimation(fig, update_terrain, frames=20, interval=200, blit=False)
    writer = PillowWriter(fps=5)
    anim.save(output_dir / 'terrain_animated.gif', writer=writer)
    plt.close()

    # 3. Animated color patterns
    print("  - Animated color patterns...")

    fig, ax = plt.subplots(figsize=(8, 8))

    def update_colors(frame):
        ax.clear()
        pattern = generate_color_pattern(256, 256, seed_offset=frame * 100)
        ax.imshow(pattern)
        ax.set_title(f'GoldenSeed Procedural Art\nSeed: {frame * 100}',
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        return ax,

    anim = FuncAnimation(fig, update_colors, frames=25, interval=150, blit=False)
    writer = PillowWriter(fps=8)
    anim.save(output_dir / 'colors_animated.gif', writer=writer)
    plt.close()


def create_comparison_demo(output_dir):
    """Create comparison visualization."""
    print("Generating comparison demo...")

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

    # Different seed offsets
    seed_offsets = [0, 100, 500, 1000, 2000, 5000, 10000, 20000,
                    50000, 100000, 500000, 1000000]

    for idx, seed_offset in enumerate(seed_offsets):
        row = idx // 4
        col = idx % 4
        ax = fig.add_subplot(gs[row, col])

        noise = generate_noise_field(128, 128, seed_offset=seed_offset)
        ax.imshow(noise, cmap='twilight')
        ax.set_title(f'Seed {seed_offset:,}', fontsize=9, fontweight='bold')
        ax.axis('off')

    fig.suptitle('GoldenSeed: Infinite Unique Outputs from Different Seeds',
                 fontsize=16, fontweight='bold')
    plt.savefig(output_dir / 'seed_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()


def create_banner_image(output_dir):
    """Create a banner image for the README."""
    print("Generating banner image...")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: Noise
    noise = generate_noise_field(256, 256, seed_offset=0)
    axes[0].imshow(noise, cmap='plasma')
    axes[0].set_title('Procedural Noise', fontsize=14, fontweight='bold')
    axes[0].axis('off')

    # Panel 2: Terrain
    terrain = generate_terrain_heightmap(256, 256, seed_offset=100)
    colors = ['#1a5490', '#2b7bb9', '#b8a57a', '#5a8f4f', '#8b7355', '#ffffff']
    cmap = LinearSegmentedColormap.from_list('terrain', colors, N=256)
    axes[1].imshow(terrain, cmap=cmap)
    axes[1].set_title('Infinite Worlds', fontsize=14, fontweight='bold')
    axes[1].axis('off')

    # Panel 3: Colors
    pattern = generate_color_pattern(256, 256, seed_offset=500)
    axes[2].imshow(pattern)
    axes[2].set_title('Deterministic Generation', fontsize=14, fontweight='bold')
    axes[2].axis('off')

    fig.suptitle('GoldenSeed: Deterministic High-Entropy Streams',
                 fontsize=18, fontweight='bold', y=0.98)

    # Add subtitle
    fig.text(0.5, 0.02,
             'Same seed always produces the same output • Zero dependencies • Cross-platform',
             ha='center', fontsize=12, style='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.savefig(output_dir / 'banner.png', dpi=150, bbox_inches='tight',
                facecolor='#1a1a2e', edgecolor='none')
    plt.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate demo visualizations for GoldenSeed',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('demos'),
        help='Output directory for generated images (default: demos/)'
    )

    parser.add_argument(
        '--static-only',
        action='store_true',
        help='Generate only static images (skip animations)'
    )

    parser.add_argument(
        '--animated-only',
        action='store_true',
        help='Generate only animations (skip static images)'
    )

    args = parser.parse_args()

    # Create output directory
    args.output_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("  GOLDENSEED VISUALIZATION GENERATOR")
    print("=" * 70)
    print()
    print(f"Output directory: {args.output_dir}")
    print()

    try:
        if not args.animated_only:
            create_static_demos(args.output_dir)
            create_comparison_demo(args.output_dir)
            create_banner_image(args.output_dir)

        if not args.static_only:
            create_animated_demos(args.output_dir)

        print()
        print("=" * 70)
        print("  GENERATION COMPLETE!")
        print("=" * 70)
        print()
        print(f"Generated files in: {args.output_dir}")
        print()
        print("To use in README.md:")
        print(f"  ![Demo](demos/banner.png)")
        print(f"  ![Animated](demos/noise_animated.gif)")
        print()

    except KeyboardInterrupt:
        print("\n\nGeneration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
