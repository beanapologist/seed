#!/usr/bin/env python3
"""
Watermark Creation Tool for Licensed Binary Generation

This script provides an interface for creating binary files with embedded
watermarks for licensed users. It ensures compliance with COMMERCIAL_LICENSE.md
requirements.

Usage:
    python scripts/create_watermarked_binary.py \\
        --input <input_binary> \\
        --output <output_binary> \\
        --license-id <license_id> \\
        --user-info <user_info> \\
        --secret <secret_key>
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path to import gq module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.gq.watermark import (
        WatermarkData,
        embed_watermark_in_binary,
        WatermarkError,
    )
except ImportError:
    print("ERROR: Unable to import watermark module. Please install the package first:")
    print("  pip install -e .")
    sys.exit(1)


def create_watermarked_binary(input_file: Path, output_file: Path,
                               license_id: str, user_info: str,
                               secret: str) -> None:
    """
    Create a watermarked binary file.
    
    Args:
        input_file: Path to input binary file
        output_file: Path to output watermarked binary file
        license_id: Unique license identifier
        user_info: User or organization information
        secret: Secret key for watermark signature
    """
    try:
        # Read input binary
        print(f"Reading input file: {input_file}")
        with open(input_file, 'rb') as f:
            binary_data = f.read()
        
        print(f"  Size: {len(binary_data)} bytes")
        
        # Create watermark
        print(f"\nCreating watermark...")
        print(f"  License ID: {license_id}")
        print(f"  User Info: {user_info}")
        
        watermark = WatermarkData(license_id, user_info)
        print(f"  Timestamp: {watermark.to_dict()['timestamp_readable']}")
        
        # Embed watermark
        print(f"\nEmbedding watermark...")
        watermarked_data = embed_watermark_in_binary(binary_data, watermark, secret)
        
        watermark_size = len(watermarked_data) - len(binary_data)
        print(f"  Watermark size: {watermark_size} bytes")
        print(f"  Total size: {len(watermarked_data)} bytes")
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write watermarked binary
        print(f"\nWriting watermarked file: {output_file}")
        with open(output_file, 'wb') as f:
            f.write(watermarked_data)
        
        print(f"\n✓ Watermarked binary created successfully!")
        print(f"  Output: {output_file}")
        print(f"  Size: {len(watermarked_data)} bytes")
        
        # Compliance notice
        print("\n" + "=" * 70)
        print("COMPLIANCE NOTICE")
        print("=" * 70)
        print("This watermarked binary is subject to the terms in COMMERCIAL_LICENSE.md.")
        print("Redistribution without authorization is prohibited.")
        print("=" * 70)
        
    except WatermarkError as e:
        print(f"\n❌ Watermark error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create watermarked binary files for licensed distribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Watermark a binary file
  python scripts/create_watermarked_binary.py \\
      --input formats/golden_seed_256.bin \\
      --output output/watermarked_seed.bin \\
      --license-id "LICENSE-2026-001" \\
      --user-info "Acme Corp" \\
      --secret "your-secret-key"
  
  # Watermark using environment variable for secret
  export WATERMARK_SECRET="your-secret-key"
  python scripts/create_watermarked_binary.py \\
      --input formats/golden_seed_256.bin \\
      --output output/watermarked_seed.bin \\
      --license-id "LICENSE-2026-001" \\
      --user-info "Acme Corp"

Compliance:
  All watermarked binaries are subject to COMMERCIAL_LICENSE.md terms.
  Unauthorized redistribution is prohibited.
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=Path,
        required=True,
        help='Input binary file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=True,
        help='Output watermarked binary file path'
    )
    
    parser.add_argument(
        '--license-id',
        type=str,
        required=True,
        help='Unique license identifier (max 64 characters)'
    )
    
    parser.add_argument(
        '--user-info',
        type=str,
        required=True,
        help='User or organization information (max 128 characters)'
    )
    
    parser.add_argument(
        '--secret',
        type=str,
        help='Secret key for watermark signature (or set WATERMARK_SECRET env var)'
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
    
    # Validate license ID and user info lengths
    if len(args.license_id) > 64:
        print("ERROR: License ID exceeds 64 characters", file=sys.stderr)
        sys.exit(1)
    
    if len(args.user_info) > 128:
        print("ERROR: User info exceeds 128 characters", file=sys.stderr)
        sys.exit(1)
    
    # Create watermarked binary
    create_watermarked_binary(
        args.input,
        args.output,
        args.license_id,
        args.user_info,
        secret
    )


if __name__ == '__main__':
    main()
