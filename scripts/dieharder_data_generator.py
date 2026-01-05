#!/usr/bin/env python3
"""
Dieharder / TestU01 Data Generator

This script generates binary data from E overflow values for analysis with
external randomness testing tools like Dieharder and TestU01.

Dieharder: Battery of tests for random number generators
TestU01: Comprehensive statistical test suite

This script generates data files that can be fed into those tools for
comprehensive randomness testing.

Usage:
    # Generate binary file for Dieharder
    python scripts/dieharder_data_generator.py --samples 10000000 --output e_random.bin
    
    # Then test with Dieharder (must be installed separately):
    dieharder -g 201 -f e_random.bin -a

Requirements:
    - None (pure Python)
    - Dieharder must be installed separately for actual testing
    - TestU01 requires C compilation
"""

import argparse
import struct
import sys
import os
import hashlib

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.validate_entropy_source import compute_e_overflow


# Default constants
DEFAULT_DIEHARDER_SAMPLES = 10000000  # 10M samples = 40MB for comprehensive testing


def generate_dieharder_format(n_samples: int) -> bytes:
    """
    Generate data in format suitable for Dieharder testing.
    
    Dieharder expects binary data, typically 32-bit unsigned integers.
    We'll generate these from E overflow values.
    
    Args:
        n_samples: Number of 32-bit integers to generate
    
    Returns:
        Raw bytes containing uint32 values derived from E overflow
    """
    print(f"Generating {n_samples} samples for Dieharder...")
    
    result = bytearray()
    angle = 0.0
    
    for i in range(n_samples):
        # Generate E overflow
        e = compute_e_overflow(angle)
        
        # Hash E to get 32-bit value
        # (This extracts deterministic but "random-looking" bits from E)
        e_bytes = struct.pack('d', e)
        h = hashlib.sha256(e_bytes).digest()
        
        # Take first 4 bytes as uint32
        uint32_val = struct.unpack('I', h[:4])[0]
        result.extend(struct.pack('I', uint32_val))
        
        angle += 0.001
        
        if (i + 1) % 100000 == 0:
            print(f"  Generated {i + 1}/{n_samples} samples...")
    
    print(f"Generated {len(result)} bytes")
    return bytes(result)


def generate_raw_bits(n_bytes: int) -> bytes:
    """
    Generate raw bit stream from E overflow.
    
    Args:
        n_bytes: Number of bytes to generate
    
    Returns:
        Raw bytes derived from E overflow
    """
    print(f"Generating {n_bytes} bytes of raw bits...")
    
    result = bytearray()
    angle = 0.0
    
    for i in range(n_bytes):
        # Generate E overflow
        e = compute_e_overflow(angle)
        
        # Extract bits from IEEE 754 representation
        e_bytes = struct.pack('d', e)
        
        # Hash to get uniform byte
        h = hashlib.sha256(e_bytes).digest()
        result.append(h[0])
        
        angle += 0.0001
        
        if (i + 1) % 100000 == 0:
            print(f"  Generated {i + 1}/{n_bytes} bytes...")
    
    print(f"Generated {len(result)} bytes")
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(
        description='Generate data from E overflow for Dieharder/TestU01 testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 10M samples for Dieharder (40 MB)
  %(prog)s --samples 10000000 --output e_dieharder.bin
  
  # Generate raw bits
  %(prog)s --raw-bits --bytes 10000000 --output e_bits.bin
  
  # Then test with Dieharder (install separately):
  dieharder -g 201 -f e_dieharder.bin -a
  
  # For smaller quick test:
  dieharder -g 201 -f e_dieharder.bin -d 0

Dieharder Installation:
  Ubuntu/Debian: sudo apt-get install dieharder
  macOS: brew install dieharder
  Build from source: http://webhome.phy.duke.edu/~rgb/General/dieharder.php

TestU01 Installation:
  Download from: http://simul.iro.umontreal.ca/testu01/tu01.html
  Requires C compilation and programming knowledge
        """
    )
    
    parser.add_argument('--samples', type=int,
                       help='Number of uint32 samples to generate')
    parser.add_argument('--bytes', type=int,
                       help='Number of bytes to generate (for raw bits)')
    parser.add_argument('--output', type=str,
                       help='Output filename for binary data')
    parser.add_argument('--raw-bits', action='store_true',
                       help='Generate raw bit stream instead of uint32 values')
    parser.add_argument('--info', action='store_true',
                       help='Display information about Dieharder testing')
    
    args = parser.parse_args()
    
    # Check if output is required
    if not args.info and not args.output:
        parser.error("--output is required (unless using --info)")
        return 1
    
    if args.info:
        print("""
Dieharder/TestU01 Random Number Testing
========================================

This tool generates binary data from E overflow for analysis with Dieharder
and TestU01 statistical test suites.

Expected Results for E Overflow:
  - Many tests will FAIL or WEAK
  - Chi-square tests will show non-uniformity
  - Correlation tests will detect patterns
  - Conclusion: NOT suitable as random number source

Why Test with Dieharder/TestU01:
  - Industry-standard RNG testing
  - Comprehensive battery of tests
  - Detects subtle statistical flaws
  - Authoritative results

Dieharder Tests Include:
  - Birthday spacings
  - Overlapping permutations
  - Ranks of matrices
  - Monkey tests
  - Count the 1's tests
  - Parking lot test
  - Minimum distance test
  - Random spheres test
  - Squeeze test
  - Overlapping sums test
  - Runs test
  - Craps test

Installation:
  Ubuntu/Debian: sudo apt-get install dieharder
  macOS: brew install dieharder
  
Usage After Generation:
  1. Generate: python %(prog)s --samples 10000000 --output e_data.bin
  2. Test all: dieharder -g 201 -f e_data.bin -a
  3. Quick test: dieharder -g 201 -f e_data.bin -d 0
  
Interpretation:
  - PASSED: Test passed at confidence level
  - WEAK: Test marginally passed
  - FAILED: Test failed, indicating non-randomness
  
For E overflow, expect many FAILED/WEAK results, confirming it's not random.
        """ % {'prog': sys.argv[0]})
        return 0
    
    # Check arguments
    if args.raw_bits:
        if args.bytes is None:
            parser.error("--bytes required when using --raw-bits")
        data = generate_raw_bits(args.bytes)
    else:
        if args.samples is None:
            parser.error("--samples required (or use --raw-bits with --bytes)")
        data = generate_dieharder_format(args.samples)
    
    # Write to file
    print(f"Writing data to {args.output}...")
    with open(args.output, 'wb') as f:
        f.write(data)
    
    print(f"\nSuccess! Generated {len(data)} bytes")
    print(f"File: {args.output}")
    print(f"\nNext steps:")
    print(f"  1. Install Dieharder (see --info)")
    print(f"  2. Run: dieharder -g 201 -f {args.output} -a")
    print(f"  3. Or quick test: dieharder -g 201 -f {args.output} -d 0")
    print(f"\nExpected: Many tests will FAIL, showing E is not random")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
