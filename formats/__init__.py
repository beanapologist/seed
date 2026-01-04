"""
Golden Seed Formats Module

This module provides access to golden seed values in various binary and hex formats.

The golden seed files are stored in this directory:
- golden_seed.hex: Hex representation
- golden_seed_16.bin: 16-byte binary seed (iφ)
- golden_seed_32.bin: 32-byte binary seed (iφ + 2×φ for consensus)
"""

import os

# Get the directory where this module is located
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths to the seed files
GOLDEN_SEED_HEX = os.path.join(_MODULE_DIR, 'golden_seed.hex')
GOLDEN_SEED_16_BIN = os.path.join(_MODULE_DIR, 'golden_seed_16.bin')
GOLDEN_SEED_32_BIN = os.path.join(_MODULE_DIR, 'golden_seed_32.bin')

__all__ = ['GOLDEN_SEED_HEX', 'GOLDEN_SEED_16_BIN', 'GOLDEN_SEED_32_BIN']
