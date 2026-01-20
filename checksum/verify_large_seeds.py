#!/usr/bin/env python3
"""
Large Seed Checksum Verification Tool

This script verifies checksums for seed files exceeding 1056 bits (132 bytes).
It validates data integrity using SHA-256 and SHA-512 checksums for larger
binary seeds used in cryptographic applications.

Features:
- Validates existence of input files with 1056+ bit sizes
- Executes SHA-256 and SHA-512 checksum verification
- Outputs integrity results for seed and manifested binary data
- Supports batch verification of multiple seed files
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def calculate_file_checksums(filepath: str) -> Dict[str, str]:
    """
    Calculate SHA-256 and SHA-512 checksums for a file.
    
    Args:
        filepath: Path to the file to checksum
        
    Returns:
        Dictionary containing sha256 and sha512 checksums
    """
    sha256_hash = hashlib.sha256()
    sha512_hash = hashlib.sha512()
    
    with open(filepath, 'rb') as f:
        # Read in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
            sha512_hash.update(chunk)
    
    return {
        'sha256': sha256_hash.hexdigest(),
        'sha512': sha512_hash.hexdigest()
    }


def get_file_info(filepath: str) -> Dict[str, int]:
    """
    Get file size information in bytes and bits.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Dictionary containing size_bytes and size_bits
    """
    size_bytes = os.path.getsize(filepath)
    return {
        'size_bytes': size_bytes,
        'size_bits': size_bytes * 8
    }


def verify_seed_file(filepath: str, expected_checksums: Dict = None) -> Dict:
    """
    Verify a seed file's existence, size, and checksums.
    
    Args:
        filepath: Path to the seed file
        expected_checksums: Optional dict with 'sha256' and/or 'sha512' keys
        
    Returns:
        Dictionary containing verification results
    """
    result = {
        'filepath': filepath,
        'exists': False,
        'meets_size_requirement': False,
        'size_bytes': 0,
        'size_bits': 0,
        'sha256': None,
        'sha512': None,
        'sha256_valid': None,
        'sha512_valid': None,
        'status': 'FAILED'
    }
    
    # Check if file exists
    if not os.path.exists(filepath):
        result['error'] = f"File not found: {filepath}"
        return result
    
    result['exists'] = True
    
    # Get file size
    file_info = get_file_info(filepath)
    result.update(file_info)
    
    # Check if size meets 1056+ bit requirement
    if result['size_bits'] >= 1056:
        result['meets_size_requirement'] = True
    else:
        result['error'] = f"File size {result['size_bits']} bits is less than required 1056 bits"
        return result
    
    # Calculate checksums
    checksums = calculate_file_checksums(filepath)
    result['sha256'] = checksums['sha256']
    result['sha512'] = checksums['sha512']
    
    # Verify against expected checksums if provided
    if expected_checksums:
        if 'sha256' in expected_checksums:
            result['sha256_valid'] = (result['sha256'] == expected_checksums['sha256'])
        if 'sha512' in expected_checksums:
            result['sha512_valid'] = (result['sha512'] == expected_checksums['sha512'])
        
        # Overall status
        sha256_check = result['sha256_valid'] if result['sha256_valid'] is not None else True
        sha512_check = result['sha512_valid'] if result['sha512_valid'] is not None else True
        
        if sha256_check and sha512_check:
            result['status'] = 'PASSED'
        else:
            result['status'] = 'FAILED'
            result['error'] = 'Checksum mismatch'
    else:
        # No expected checksums to compare, just report calculated values
        result['status'] = 'CALCULATED'
    
    return result


def verify_manifested_data(seed_filepath: str, k: int = 11) -> Dict:
    """
    Verify manifested binary data derived from seed using formula: manifested = (seed * 8) + k
    
    Args:
        seed_filepath: Path to the seed file
        k: Tap parameter (default 11)
        
    Returns:
        Dictionary containing manifested data verification results
    """
    result = {
        'seed_filepath': seed_filepath,
        'k': k,
        'manifested_sha256': None,
        'manifested_sha512': None,
        'status': 'FAILED'
    }
    
    if not os.path.exists(seed_filepath):
        result['error'] = f"Seed file not found: {seed_filepath}"
        return result
    
    # Read seed as big integer
    with open(seed_filepath, 'rb') as f:
        seed_bytes = f.read()
    
    seed_value = int.from_bytes(seed_bytes, byteorder='big')
    
    # Calculate manifested value: (seed * 8) + k
    manifested_value = (seed_value * 8) + k
    
    # Convert manifested value back to bytes
    byte_length = (manifested_value.bit_length() + 7) // 8
    manifested_bytes = manifested_value.to_bytes(byte_length, byteorder='big')
    
    # Calculate checksums for manifested data
    result['manifested_sha256'] = hashlib.sha256(manifested_bytes).hexdigest()
    result['manifested_sha512'] = hashlib.sha512(manifested_bytes).hexdigest()
    result['manifested_bit_length'] = manifested_value.bit_length()
    result['manifested_byte_length'] = byte_length
    result['status'] = 'CALCULATED'
    
    return result


def load_expected_checksums(checksum_file: str) -> Dict:
    """
    Load expected checksums from JSON file.
    
    Args:
        checksum_file: Path to JSON file containing expected checksums
        
    Returns:
        Dictionary mapping filenames to their expected checksums
    """
    with open(checksum_file, 'r') as f:
        return json.load(f)


def verify_batch(seed_files: List[str], checksum_file: str = None) -> List[Dict]:
    """
    Verify multiple seed files in batch.
    
    Args:
        seed_files: List of seed file paths to verify
        checksum_file: Optional path to JSON file with expected checksums
        
    Returns:
        List of verification result dictionaries
    """
    results = []
    expected_checksums_map = {}
    
    # Load expected checksums if provided
    if checksum_file and os.path.exists(checksum_file):
        expected_checksums_map = load_expected_checksums(checksum_file)
    
    for filepath in seed_files:
        filename = os.path.basename(filepath)
        expected = expected_checksums_map.get(filename)
        
        # Verify seed file
        result = verify_seed_file(filepath, expected)
        results.append(result)
    
    return results


def print_verification_report(results: List[Dict], include_manifested: bool = False):
    """
    Print a formatted verification report.
    
    Args:
        results: List of verification result dictionaries
        include_manifested: Whether to include manifested data verification
    """
    print("=" * 80)
    print("LARGE SEED CHECKSUM VERIFICATION REPORT")
    print("=" * 80)
    print()
    
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASSED' or r['status'] == 'CALCULATED')
    failed = sum(1 for r in results if r['status'] == 'FAILED')
    
    print(f"Total Files: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result['filepath']}")
        print(f"    Status: {result['status']}")
        
        if result['exists']:
            print(f"    Size: {result['size_bytes']} bytes ({result['size_bits']} bits)")
            print(f"    Meets 1056+ bit requirement: {'✅ YES' if result['meets_size_requirement'] else '❌ NO'}")
            
            if result['sha256']:
                print(f"    SHA-256: {result['sha256']}")
                if result['sha256_valid'] is not None:
                    print(f"             {'✅ VALID' if result['sha256_valid'] else '❌ INVALID'}")
            
            if result['sha512']:
                print(f"    SHA-512: {result['sha512'][:64]}...")
                if result['sha512_valid'] is not None:
                    print(f"             {'✅ VALID' if result['sha512_valid'] else '❌ INVALID'}")
        
        if 'error' in result:
            print(f"    Error: {result['error']}")
        
        # Include manifested data verification if requested
        if include_manifested and result['exists'] and result['meets_size_requirement']:
            manifested = verify_manifested_data(result['filepath'])
            print(f"    Manifested Data (k={manifested['k']}):")
            print(f"      Bit Length: {manifested.get('manifested_bit_length', 'N/A')}")
            print(f"      SHA-256: {manifested.get('manifested_sha256', 'N/A')}")
            print(f"      SHA-512: {manifested.get('manifested_sha512', 'N/A')[:64]}...")
        
        print()
    
    print("=" * 80)
    
    return passed == total


def main():
    """Main entry point for the verification tool."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verify checksums for seed files exceeding 1056 bits'
    )
    parser.add_argument(
        'seed_files',
        nargs='*',
        help='Seed files to verify (default: all 1056+ bit seeds in formats/)'
    )
    parser.add_argument(
        '--checksums',
        default='formats/test_checksums.json',
        help='JSON file containing expected checksums'
    )
    parser.add_argument(
        '--manifested',
        action='store_true',
        help='Include manifested data verification'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    args = parser.parse_args()
    
    # Determine which files to verify
    if args.seed_files:
        seed_files = args.seed_files
    else:
        # Default: verify all large seed files in formats/
        formats_dir = Path('formats')
        seed_files = [
            str(formats_dir / 'golden_seed_132.bin'),
            str(formats_dir / 'golden_seed_256.bin'),
            str(formats_dir / 'golden_seed_512.bin'),
        ]
    
    # Run verification
    results = verify_batch(seed_files, args.checksums if os.path.exists(args.checksums) else None)
    
    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        success = print_verification_report(results, include_manifested=args.manifested)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
