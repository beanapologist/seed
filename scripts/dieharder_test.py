#!/usr/bin/env python3
"""
Dieharder Entropy Testing Integration

This script generates random numbers from the cryptographic PRNG/DRBG and pipes them
into Dieharder for comprehensive statistical testing.

Dieharder is a comprehensive random number testing suite developed by Robert G. Brown
at Duke University. It includes tests from DIEHARD, STS (Statistical Test Suite), and
additional tests for evaluating random number generators.

Usage:
    # Generate data and run all Dieharder tests
    python scripts/dieharder_test.py --tests all --output dieharder_results.txt

    # Generate data and run specific test
    python scripts/dieharder_test.py --tests birthdays --size 10MB

    # Test Universal QKD generator
    python scripts/dieharder_test.py --generator universal_qkd --tests all

    # Test NIST PQC hybrid key generator
    python scripts/dieharder_test.py --generator nist_pqc --algorithm kyber768 --tests all
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gq import UniversalQKD, generate_hybrid_key, generate_hybrid_key_stream, PQCAlgorithm


class DieharderTester:
    """Interface for running Dieharder statistical tests on cryptographic generators."""
    
    # Dieharder test suite options
    DIEHARDER_TESTS = {
        'all': -1,  # Run all tests
        'birthdays': 0,
        'operm5': 1,
        'rank_32x32': 2,
        'rank_6x8': 3,
        'bitstream': 4,
        'opso': 5,
        'oqso': 6,
        'dna': 7,
        'count_1s_stream': 8,
        'count_1s_byte': 9,
        'parking_lot': 10,
        'minimum_distance': 11,
        'random_spheres': 12,
        'squeeze': 13,
        'sums': 14,
        'runs': 15,
        'craps': 16,
        'sts_monobit': 100,
        'sts_runs': 101,
        'sts_serial': 102
    }
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Dieharder tester.
        
        Args:
            verbose: Print detailed output during testing
        """
        self.verbose = verbose
        self._check_dieharder_installed()
        
    def _check_dieharder_installed(self):
        """Check if Dieharder is installed and available."""
        try:
            result = subprocess.run(
                ['dieharder', '-h'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if self.verbose:
                print("✓ Dieharder is installed and available")
        except FileNotFoundError:
            print("ERROR: Dieharder is not installed.")
            print("\nTo install Dieharder:")
            print("  Ubuntu/Debian: sudo apt-get install dieharder")
            print("  Fedora/RHEL:   sudo dnf install dieharder")
            print("  macOS:         brew install dieharder")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Could not verify Dieharder installation: {e}")
            sys.exit(1)
            
    def generate_random_data(
        self,
        generator_type: str,
        size_bytes: int,
        algorithm: Optional[PQCAlgorithm] = None
    ) -> bytes:
        """
        Generate random data from the specified cryptographic generator.
        
        Args:
            generator_type: Type of generator ('universal_qkd' or 'nist_pqc')
            size_bytes: Number of bytes to generate
            algorithm: PQC algorithm (required if generator_type is 'nist_pqc')
            
        Returns:
            Random data as bytes
        """
        if self.verbose:
            print(f"\nGenerating {size_bytes:,} bytes of random data...")
            print(f"Generator: {generator_type}")
            if algorithm:
                print(f"Algorithm: {algorithm.value}")
        
        data = bytearray()
        
        if generator_type == 'universal_qkd':
            generator = UniversalQKD()
            while len(data) < size_bytes:
                key = next(generator)
                data.extend(key)
                if self.verbose and len(data) % (1024 * 1024) == 0:
                    print(f"  Generated: {len(data):,} bytes")
                    
        elif generator_type == 'nist_pqc':
            if not algorithm:
                raise ValueError("algorithm must be specified for nist_pqc generator")
            
            # Generate hybrid keys and extract PQC seeds
            while len(data) < size_bytes:
                det_key, pqc_seed = generate_hybrid_key(algorithm)
                # Use both deterministic key and PQC seed for maximum data
                data.extend(det_key)
                data.extend(pqc_seed)
                if self.verbose and len(data) % (1024 * 1024) == 0:
                    print(f"  Generated: {len(data):,} bytes")
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")
            
        # Trim to exact size
        data = bytes(data[:size_bytes])
        
        if self.verbose:
            print(f"✓ Generated {len(data):,} bytes")
            
        return data
        
    def run_dieharder_test(
        self,
        data: bytes,
        test: str = 'all',
        output_file: Optional[str] = None
    ) -> dict:
        """
        Run Dieharder statistical test on the provided data.
        
        Args:
            data: Random data to test
            test: Test name or 'all' for all tests
            output_file: Optional file to save results
            
        Returns:
            Dictionary with test results
        """
        if test not in self.DIEHARDER_TESTS:
            raise ValueError(f"Unknown test: {test}. Available: {list(self.DIEHARDER_TESTS.keys())}")
            
        test_id = self.DIEHARDER_TESTS[test]
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Running Dieharder Test: {test}")
            print(f"Data Size: {len(data):,} bytes")
            print(f"{'='*60}\n")
        
        # Write data to temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as tmp:
            tmp.write(data)
            tmp_path = tmp.name
            
        try:
            # Run dieharder with the data file
            cmd = [
                'dieharder',
                '-d', str(test_id),  # Test number
                '-g', '201',  # Read from file (generator 201)
                '-f', tmp_path,  # Input file
            ]
            
            if self.verbose:
                print(f"Running command: {' '.join(cmd)}")
                print("\nDieharder Output:")
                print("-" * 60)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            output = result.stdout + result.stderr
            
            if self.verbose:
                print(output)
                print("-" * 60)
            
            # Parse results
            test_results = self._parse_dieharder_output(output)
            
            # Save to file if requested
            if output_file:
                self._save_results(test_results, output, output_file)
                if self.verbose:
                    print(f"\n✓ Results saved to: {output_file}")
                    
            return test_results
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    def _parse_dieharder_output(self, output: str) -> dict:
        """
        Parse Dieharder output to extract test results.
        
        Args:
            output: Raw Dieharder output
            
        Returns:
            Dictionary with parsed results
        """
        results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'tests': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'weak': 0,
                'failed': 0
            }
        }
        
        # Parse each test result line
        for line in output.split('\n'):
            line = line.strip()
            
            # Look for result lines (contain PASSED, WEAK, or FAILED)
            if 'PASSED' in line or 'WEAK' in line or 'FAILED' in line:
                results['tests'].append(line)
                results['summary']['total'] += 1
                
                if 'PASSED' in line:
                    results['summary']['passed'] += 1
                elif 'WEAK' in line:
                    results['summary']['weak'] += 1
                elif 'FAILED' in line:
                    results['summary']['failed'] += 1
                    
        return results
        
    def _save_results(self, results: dict, raw_output: str, output_file: str):
        """
        Save test results to file.
        
        Args:
            results: Parsed test results
            raw_output: Raw Dieharder output
            output_file: Output file path
        """
        with open(output_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("Dieharder Statistical Test Results\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Timestamp: {results['timestamp']}\n\n")
            
            f.write("Summary:\n")
            f.write("-"*60 + "\n")
            f.write(json.dumps(results['summary'], indent=2))
            f.write("\n\n")
            
            f.write("Raw Dieharder Output:\n")
            f.write("-"*60 + "\n")
            f.write(raw_output)
            f.write("\n")


def parse_size(size_str: str) -> int:
    """
    Parse size string (e.g., '10MB', '1GB') to bytes.
    
    Args:
        size_str: Size string with optional unit suffix
        
    Returns:
        Size in bytes
    """
    size_str = size_str.upper().strip()
    
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024
    }
    
    for suffix, multiplier in multipliers.items():
        if size_str.endswith(suffix):
            value = float(size_str[:-len(suffix)])
            return int(value * multiplier)
            
    # No suffix, assume bytes
    return int(size_str)


def main():
    """Main entry point for Dieharder testing."""
    parser = argparse.ArgumentParser(
        description="Run Dieharder statistical tests on cryptographic generators"
    )
    parser.add_argument(
        '--generator',
        type=str,
        default='universal_qkd',
        choices=['universal_qkd', 'nist_pqc'],
        help='Generator to test'
    )
    parser.add_argument(
        '--algorithm',
        type=str,
        default='kyber768',
        help='PQC algorithm (for nist_pqc generator): kyber512, kyber768, kyber1024, dilithium2, dilithium3, dilithium5, sphincs_plus_128f'
    )
    parser.add_argument(
        '--tests',
        type=str,
        default='all',
        help=f'Test to run (available: {", ".join(DieharderTester.DIEHARDER_TESTS.keys())})'
    )
    parser.add_argument(
        '--size',
        type=str,
        default='10MB',
        help='Amount of data to generate (e.g., 10MB, 1GB)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='dieharder_results.txt',
        help='Output file for test results'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    # Parse algorithm if testing NIST PQC
    algorithm = None
    if args.generator == 'nist_pqc':
        algorithm_map = {
            'kyber512': PQCAlgorithm.KYBER512,
            'kyber768': PQCAlgorithm.KYBER768,
            'kyber1024': PQCAlgorithm.KYBER1024,
            'dilithium2': PQCAlgorithm.DILITHIUM2,
            'dilithium3': PQCAlgorithm.DILITHIUM3,
            'dilithium5': PQCAlgorithm.DILITHIUM5,
            'sphincs_plus_128f': PQCAlgorithm.SPHINCS_PLUS_128F,
        }
        algorithm = algorithm_map.get(args.algorithm.lower())
        if not algorithm:
            print(f"ERROR: Unknown algorithm: {args.algorithm}")
            print(f"Available: {', '.join(algorithm_map.keys())}")
            return 1
            
    # Parse size
    size_bytes = parse_size(args.size)
    
    print("="*60)
    print("Dieharder Statistical Testing")
    print("="*60)
    print(f"Generator: {args.generator}")
    if algorithm:
        print(f"Algorithm: {algorithm.value}")
    print(f"Test Suite: {args.tests}")
    print(f"Data Size: {size_bytes:,} bytes ({args.size})")
    print(f"Output File: {args.output}")
    print("="*60)
    
    # Create tester
    tester = DieharderTester(verbose=not args.quiet)
    
    # Generate random data
    data = tester.generate_random_data(
        args.generator,
        size_bytes,
        algorithm
    )
    
    # Run tests
    results = tester.run_dieharder_test(
        data,
        args.tests,
        args.output
    )
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Total Tests: {results['summary']['total']}")
    print(f"Passed: {results['summary']['passed']}")
    print(f"Weak: {results['summary']['weak']}")
    print(f"Failed: {results['summary']['failed']}")
    print("="*60)
    
    # Exit with error code if any tests failed
    if results['summary']['failed'] > 0:
        print("\n⚠ WARNING: Some tests failed!")
        return 1
    elif results['summary']['weak'] > 0:
        print("\n⚠ WARNING: Some tests were weak")
        return 0
    else:
        print("\n✓ All tests passed!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
