#!/usr/bin/env python3
"""
NIST SP 800-90B Integration Script

This script generates binary data from E overflow values for analysis with
external NIST SP 800-90B entropy assessment tools.

NIST provides official tools for entropy assessment:
- https://github.com/usnistgov/SP800-90B_EntropyAssessment

This script generates data files that can be fed into those tools for
official NIST compliance testing.

Usage:
    # Generate binary file for NIST tool analysis
    python scripts/nist_sp800_90b_data_generator.py --samples 1000000 --output e_overflow_data.bin
    
    # Then use NIST tool (must be installed separately):
    ea_iid e_overflow_data.bin 8
    ea_non_iid e_overflow_data.bin 8

Requirements:
    - None (pure Python)
    - NIST tool must be installed separately for actual testing
"""

import argparse
import struct
import sys
import os
import cmath
import math

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.validate_entropy_source import compute_e_overflow


# Default constants
DEFAULT_NIST_SAMPLES = 1000000  # Default number of samples for NIST testing (1M samples = 8MB)


def generate_e_overflow_samples(n_samples: int) -> bytes:
    """
    Generate E overflow samples as raw binary data.
    
    Args:
        n_samples: Number of E overflow values to generate
    
    Returns:
        Raw bytes containing E overflow values
    """
    print(f"Generating {n_samples} E overflow samples...")
    
    # Generate E values from sequential angles
    e_values = []
    for i in range(n_samples):
        angle = i * 0.001  # Small increments
        e = compute_e_overflow(angle)
        e_values.append(e)
        
        if (i + 1) % 10000 == 0:
            print(f"  Generated {i + 1}/{n_samples} samples...")
    
    # Convert to bytes (IEEE 754 double precision)
    data = b''.join(struct.pack('d', e) for e in e_values)
    
    print(f"Generated {len(data)} bytes of data")
    return data


def generate_e_overflow_bits(n_samples: int) -> bytes:
    """
    Generate E overflow samples as bit sequence for NIST tools.
    
    Args:
        n_samples: Number of bytes to generate
    
    Returns:
        Raw bytes where each byte represents 8 bits from E overflow
    """
    print(f"Generating {n_samples} bytes from E overflow bits...")
    
    result = bytearray()
    angle = 0.0
    
    for i in range(n_samples):
        # Generate E overflow
        e = compute_e_overflow(angle)
        
        # Extract bits from IEEE 754 representation
        e_bytes = struct.pack('d', e)
        
        # Use XOR of all bytes to create one output byte
        # (This extracts bit-level information from E)
        byte_val = 0
        for b in e_bytes:
            byte_val ^= b
        
        result.append(byte_val)
        angle += 0.001
        
        if (i + 1) % 10000 == 0:
            print(f"  Generated {i + 1}/{n_samples} bytes...")
    
    print(f"Generated {len(result)} bytes")
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(
        description='Generate binary data from E overflow for NIST SP 800-90B testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1M samples for NIST testing
  %(prog)s --samples 1000000 --output e_data.bin
  
  # Generate bit sequence
  %(prog)s --samples 1000000 --output e_bits.bin --bits
  
  # Then test with NIST tools (install separately):
  ea_iid e_data.bin 8
  ea_non_iid e_data.bin 8

NIST Tool Installation:
  git clone https://github.com/usnistgov/SP800-90B_EntropyAssessment
  cd SP800-90B_EntropyAssessment/cpp
  make
  sudo make install
        """
    )
    
    parser.add_argument('--samples', type=int, default=DEFAULT_NIST_SAMPLES,
                       help=f'Number of samples to generate (default: {DEFAULT_NIST_SAMPLES})')
    parser.add_argument('--output', type=str,
                       help='Output filename for binary data')
    parser.add_argument('--bits', action='store_true',
                       help='Generate bit sequence instead of raw E values')
    parser.add_argument('--info', action='store_true',
                       help='Display information about NIST testing')
    
    args = parser.parse_args()
    
    # Check if output is required
    if not args.info and not args.output:
        parser.error("--output is required (unless using --info)")
        return 1
    
    if args.info:
        print("""
NIST SP 800-90B Entropy Assessment
===================================

This tool generates binary data from E overflow for analysis with NIST's
official entropy assessment tools.

Expected Results for E Overflow:
  - Min-entropy: Very low (~0.7 bits as measured in validation tests)
  - IID assumption: Will likely FAIL (data is not independent)
  - Non-IID tests: Will show deterministic patterns
  
Why Test with NIST Tools:
  - Official entropy assessment methodology
  - Authoritative results for compliance testing
  - Comprehensive battery of tests

Installation:
  1. Clone NIST tool: git clone https://github.com/usnistgov/SP800-90B_EntropyAssessment
  2. Build: cd SP800-90B_EntropyAssessment/cpp && make
  3. Install: sudo make install
  
Usage After Generation:
  1. Generate data: python %(prog)s --samples 1000000 --output e_data.bin
  2. Run IID test: ea_iid e_data.bin 8
  3. Run non-IID: ea_non_iid e_data.bin 8
  
Interpretation:
  - E overflow should show very low entropy
  - Tests should detect deterministic patterns
  - Results will confirm E is not suitable for cryptography
        """ % {'prog': sys.argv[0]})
        return 0
    
    # Generate data
    if args.bits:
        data = generate_e_overflow_bits(args.samples)
    else:
        data = generate_e_overflow_samples(args.samples)
    
    # Write to file
    print(f"Writing data to {args.output}...")
    with open(args.output, 'wb') as f:
        f.write(data)
    
    print(f"\nSuccess! Generated {len(data)} bytes")
    print(f"File: {args.output}")
    print(f"\nNext steps:")
    print(f"  1. Install NIST SP 800-90B tools (see --info)")
    print(f"  2. Run: ea_iid {args.output} 8")
    print(f"  3. Run: ea_non_iid {args.output} 8")
    print(f"\nExpected: Low entropy, deterministic patterns detected")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
