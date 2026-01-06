#!/usr/bin/env python3
"""
Watermark Verification Tool

This script provides verification capabilities for watermarked binary files,
allowing validation of embedded licensing data and ensuring compliance with
COMMERCIAL_LICENSE.md requirements.

Usage:
    python scripts/verify_watermark.py \\
        --input <watermarked_binary> \\
        --secret <secret_key>
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import gq module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.gq.watermark import (
        extract_watermark_from_binary,
        check_watermark_present,
        WatermarkError,
    )
except ImportError:
    print("ERROR: Unable to import watermark module. Please install the package first:")
    print("  pip install -e .")
    sys.exit(1)


def verify_watermark(input_file: Path, secret: str, 
                      json_output: bool = False) -> dict:
    """
    Verify watermark in a binary file.
    
    Args:
        input_file: Path to watermarked binary file
        secret: Secret key for watermark verification
        json_output: If True, return JSON-formatted output
        
    Returns:
        Dictionary containing verification results
    """
    result = {
        'file': str(input_file),
        'watermarked': False,
        'verified': False,
        'error': None,
        'watermark': None,
    }
    
    try:
        # Read binary file
        with open(input_file, 'rb') as f:
            binary_data = f.read()
        
        result['file_size'] = len(binary_data)
        
        # Check if watermark is present
        if not check_watermark_present(binary_data):
            result['error'] = 'No watermark found in binary file'
            return result
        
        result['watermarked'] = True
        
        # Extract and verify watermark
        original_data, watermark = extract_watermark_from_binary(binary_data, secret)
        
        result['verified'] = True
        result['original_size'] = len(original_data)
        result['watermark'] = watermark.to_dict()
        
        return result
        
    except WatermarkError as e:
        result['error'] = f"Watermark error: {e}"
        return result
    except Exception as e:
        result['error'] = f"Error: {e}"
        return result


def print_verification_result(result: dict, json_output: bool = False) -> None:
    """
    Print verification results in human-readable or JSON format.
    
    Args:
        result: Verification result dictionary
        json_output: If True, output in JSON format
    """
    if json_output:
        print(json.dumps(result, indent=2))
        return
    
    # Human-readable output
    print("=" * 70)
    print("WATERMARK VERIFICATION RESULTS")
    print("=" * 70)
    print(f"\nFile: {result['file']}")
    print(f"Size: {result['file_size']:,} bytes")
    
    print(f"\nWatermark Present: {'✓ YES' if result['watermarked'] else '✗ NO'}")
    
    if result['error']:
        print(f"\n❌ Verification Failed")
        print(f"   {result['error']}")
        print("=" * 70)
        return
    
    if result['verified']:
        print(f"Signature Verified: ✓ YES")
        print(f"\nOriginal Binary Size: {result['original_size']:,} bytes")
        print(f"Watermark Size: {result['file_size'] - result['original_size']:,} bytes")
        
        print("\n" + "-" * 70)
        print("LICENSING INFORMATION")
        print("-" * 70)
        
        watermark = result['watermark']
        print(f"License ID: {watermark['license_id']}")
        print(f"User/Organization: {watermark['user_info']}")
        print(f"Timestamp: {watermark['timestamp_readable']}")
        print(f"Unix Time: {watermark['timestamp']}")
        
        print("\n" + "-" * 70)
        print("COMPLIANCE STATUS")
        print("-" * 70)
        print("✓ Binary is properly licensed for commercial distribution")
        print("✓ Watermark signature is valid and authentic")
        print("\nThis binary is subject to terms in COMMERCIAL_LICENSE.md")
        
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Verify watermarks in binary files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify a watermarked binary
  python scripts/verify_watermark.py \\
      --input output/watermarked_seed.bin \\
      --secret "your-secret-key"
  
  # Verify using environment variable for secret
  export WATERMARK_SECRET="your-secret-key"
  python scripts/verify_watermark.py \\
      --input output/watermarked_seed.bin
  
  # Output verification results as JSON
  python scripts/verify_watermark.py \\
      --input output/watermarked_seed.bin \\
      --secret "your-secret-key" \\
      --json

Return Codes:
  0 - Watermark verified successfully
  1 - Watermark verification failed or error occurred
  2 - No watermark found in file
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=Path,
        required=True,
        help='Input watermarked binary file path'
    )
    
    parser.add_argument(
        '--secret',
        type=str,
        help='Secret key for watermark verification (or set WATERMARK_SECRET env var)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    args = parser.parse_args()
    
    # Get secret from args or environment
    secret = args.secret or os.environ.get('WATERMARK_SECRET')
    
    if not secret:
        print("ERROR: Secret key is required. Provide via --secret or WATERMARK_SECRET env var.",
              file=sys.stderr)
        sys.exit(1)
    
    # Validate input file exists
    if not args.input.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Verify watermark
    result = verify_watermark(args.input, secret, args.json)
    
    # Print results
    print_verification_result(result, args.json)
    
    # Exit with appropriate code
    if result['verified']:
        sys.exit(0)
    elif not result['watermarked']:
        sys.exit(2)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
