"""
Unit tests for Seed File Checksum Verification Tool.

Tests validate:
- File size validation (arbitrary bit sizes, with optional minimum)
- SHA-256 checksum calculation and verification
- SHA-512 checksum calculation and verification
- Manifested data calculation and checksums
- Batch verification functionality
- JSON output format
- Error handling for missing files
"""

import unittest
import sys
import os
import json
import tempfile
from pathlib import Path

# Add checksum directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from checksum.verify_large_seeds import (
    calculate_file_checksums,
    get_file_info,
    verify_seed_file,
    verify_manifested_data,
    load_expected_checksums,
    verify_batch
)


class TestLargeSeedVerification(unittest.TestCase):
    """Test suite for seed file checksum verification."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by multiple tests."""
        cls.test_seed_132 = 'formats/golden_seed_132.bin'
        cls.test_seed_256 = 'formats/golden_seed_256.bin'
        cls.test_seed_512 = 'formats/golden_seed_512.bin'
        cls.test_checksums_file = 'formats/test_checksums.json'

    def test_file_size_validation_1056_bits(self):
        """Test that 1056-bit (132-byte) file can be validated."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        info = get_file_info(self.test_seed_132)
        
        self.assertEqual(info['size_bytes'], 132)
        self.assertEqual(info['size_bits'], 1056)
        # With min_bits=0 (default), any size should pass
        self.assertGreaterEqual(info['size_bits'], 0)
        # With min_bits=1056, this should meet requirement
        self.assertGreaterEqual(info['size_bits'], 1056)

    def test_file_size_validation_2048_bits(self):
        """Test that 2048-bit (256-byte) file can be validated."""
        if not os.path.exists(self.test_seed_256):
            self.skipTest(f"Test file not found: {self.test_seed_256}")
        
        info = get_file_info(self.test_seed_256)
        
        self.assertEqual(info['size_bytes'], 256)
        self.assertEqual(info['size_bits'], 2048)
        self.assertGreaterEqual(info['size_bits'], 0)

    def test_file_size_validation_4096_bits(self):
        """Test that 4096-bit (512-byte) file can be validated."""
        if not os.path.exists(self.test_seed_512):
            self.skipTest(f"Test file not found: {self.test_seed_512}")
        
        info = get_file_info(self.test_seed_512)
        
        self.assertEqual(info['size_bytes'], 512)
        self.assertEqual(info['size_bits'], 4096)
        self.assertGreaterEqual(info['size_bits'], 0)

    def test_checksum_calculation_format(self):
        """Test that checksums are calculated in correct format."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        checksums = calculate_file_checksums(self.test_seed_132)
        
        # SHA-256 should be 64 hex characters
        self.assertIn('sha256', checksums)
        self.assertEqual(len(checksums['sha256']), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in checksums['sha256']))
        
        # SHA-512 should be 128 hex characters
        self.assertIn('sha512', checksums)
        self.assertEqual(len(checksums['sha512']), 128)
        self.assertTrue(all(c in '0123456789abcdef' for c in checksums['sha512']))

    def test_checksum_verification_with_expected_values(self):
        """Test checksum verification against expected values."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        if not os.path.exists(self.test_checksums_file):
            self.skipTest(f"Checksums file not found: {self.test_checksums_file}")
        
        # Load expected checksums
        with open(self.test_checksums_file, 'r') as f:
            expected_checksums_map = json.load(f)
        
        filename = os.path.basename(self.test_seed_132)
        expected = expected_checksums_map[filename]
        
        result = verify_seed_file(self.test_seed_132, expected)
        
        self.assertTrue(result['exists'])
        self.assertTrue(result['meets_size_requirement'])
        self.assertEqual(result['status'], 'PASSED')
        self.assertTrue(result['sha256_valid'])
        self.assertTrue(result['sha512_valid'])

    def test_verify_seed_file_structure(self):
        """Test that verify_seed_file returns correct structure."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        result = verify_seed_file(self.test_seed_132)
        
        # Check required fields
        self.assertIn('filepath', result)
        self.assertIn('exists', result)
        self.assertIn('meets_size_requirement', result)
        self.assertIn('size_bytes', result)
        self.assertIn('size_bits', result)
        self.assertIn('sha256', result)
        self.assertIn('sha512', result)
        self.assertIn('status', result)

    def test_verify_nonexistent_file(self):
        """Test verification of non-existent file."""
        result = verify_seed_file('nonexistent_file.bin')
        
        self.assertFalse(result['exists'])
        self.assertEqual(result['status'], 'FAILED')
        self.assertIn('error', result)

    def test_verify_small_file(self):
        """Test that files of any size can be verified when min_bits=0 (default)."""
        # Create a temporary small file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            temp_file = f.name
            f.write(b'0' * 100)  # 800 bits
        
        try:
            # With default min_bits=0, this should pass
            result = verify_seed_file(temp_file, min_bits=0)
            
            self.assertTrue(result['exists'])
            self.assertTrue(result['meets_size_requirement'])
            self.assertEqual(result['size_bits'], 800)
            
            # With min_bits=1000, this should fail
            result_with_min = verify_seed_file(temp_file, min_bits=1000)
            self.assertFalse(result_with_min['meets_size_requirement'])
            self.assertIn('error', result_with_min)
        finally:
            os.unlink(temp_file)

    def test_manifested_data_calculation(self):
        """Test manifested data calculation using formula: (seed * 8) + k."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        k = 11
        result = verify_manifested_data(self.test_seed_132, k)
        
        self.assertEqual(result['k'], k)
        self.assertEqual(result['status'], 'CALCULATED')
        self.assertIn('manifested_sha256', result)
        self.assertIn('manifested_sha512', result)
        self.assertIn('manifested_bit_length', result)
        
        # Manifested should be 3 bits longer (due to * 8 + 11)
        self.assertEqual(result['manifested_bit_length'], 1059)

    def test_manifested_data_checksums_format(self):
        """Test that manifested data checksums are in correct format."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        result = verify_manifested_data(self.test_seed_132)
        
        # SHA-256 should be 64 hex characters
        self.assertEqual(len(result['manifested_sha256']), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in result['manifested_sha256']))
        
        # SHA-512 should be 128 hex characters
        self.assertEqual(len(result['manifested_sha512']), 128)
        self.assertTrue(all(c in '0123456789abcdef' for c in result['manifested_sha512']))

    def test_batch_verification(self):
        """Test batch verification of multiple files."""
        test_files = [
            self.test_seed_132,
            self.test_seed_256,
            self.test_seed_512
        ]
        
        # Skip if files don't exist
        existing_files = [f for f in test_files if os.path.exists(f)]
        if not existing_files:
            self.skipTest("Test files not found")
        
        results = verify_batch(existing_files, self.test_checksums_file)
        
        self.assertEqual(len(results), len(existing_files))
        
        for result in results:
            self.assertTrue(result['exists'])
            self.assertTrue(result['meets_size_requirement'])
            self.assertIn(result['status'], ['PASSED', 'CALCULATED'])

    def test_load_expected_checksums(self):
        """Test loading expected checksums from JSON file."""
        if not os.path.exists(self.test_checksums_file):
            self.skipTest(f"Checksums file not found: {self.test_checksums_file}")
        
        checksums = load_expected_checksums(self.test_checksums_file)
        
        self.assertIsInstance(checksums, dict)
        self.assertIn('golden_seed_132.bin', checksums)
        
        for filename, data in checksums.items():
            self.assertIn('size_bytes', data)
            self.assertIn('size_bits', data)
            self.assertIn('sha256', data)
            self.assertIn('sha512', data)

    def test_checksum_consistency(self):
        """Test that checksums are consistent across multiple calculations."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        checksums1 = calculate_file_checksums(self.test_seed_132)
        checksums2 = calculate_file_checksums(self.test_seed_132)
        
        self.assertEqual(checksums1['sha256'], checksums2['sha256'])
        self.assertEqual(checksums1['sha512'], checksums2['sha512'])

    def test_manifested_bit_length_increase(self):
        """Test that manifested data increases bit length by 3 bits."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        info = get_file_info(self.test_seed_132)
        result = verify_manifested_data(self.test_seed_132, k=11)
        
        # For (seed * 8) + 11, the bit length should increase by 3 bits
        expected_bit_length = info['size_bits'] + 3
        self.assertEqual(result['manifested_bit_length'], expected_bit_length)

    def test_all_test_seeds_meet_requirements(self):
        """Test that all test seed files can be validated."""
        test_files = [
            self.test_seed_132,
            self.test_seed_256,
            self.test_seed_512
        ]
        
        for filepath in test_files:
            if os.path.exists(filepath):
                info = get_file_info(filepath)
                # With min_bits=0 (default), all files should pass
                self.assertGreaterEqual(
                    info['size_bits'],
                    0,
                    f"{filepath} should be a valid file"
                )

    def test_checksum_mismatch_detection(self):
        """Test that checksum mismatches are properly detected."""
        if not os.path.exists(self.test_seed_132):
            self.skipTest(f"Test file not found: {self.test_seed_132}")
        
        # Provide incorrect expected checksum
        wrong_checksums = {
            'sha256': '0' * 64,
            'sha512': '0' * 128
        }
        
        result = verify_seed_file(self.test_seed_132, wrong_checksums)
        
        self.assertFalse(result['sha256_valid'])
        self.assertFalse(result['sha512_valid'])
        self.assertEqual(result['status'], 'FAILED')

    def test_arbitrary_bit_size_small(self):
        """Test checksum verification for small arbitrary bit sizes (64 bits)."""
        # Create a temporary 8-byte (64-bit) file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            temp_file = f.name
            f.write(b'testdata')  # 8 bytes = 64 bits
        
        try:
            result = verify_seed_file(temp_file, min_bits=0)
            
            self.assertTrue(result['exists'])
            self.assertTrue(result['meets_size_requirement'])
            self.assertEqual(result['size_bits'], 64)
            self.assertIsNotNone(result['sha256'])
            self.assertIsNotNone(result['sha512'])
            self.assertEqual(len(result['sha256']), 64)
            self.assertEqual(len(result['sha512']), 128)
        finally:
            os.unlink(temp_file)

    def test_arbitrary_bit_size_custom_minimum(self):
        """Test custom minimum bit size requirements."""
        # Create files of various sizes
        test_cases = [
            (50, 400),   # 50 bytes = 400 bits
            (100, 800),  # 100 bytes = 800 bits
            (200, 1600), # 200 bytes = 1600 bits
        ]
        
        for byte_size, bit_size in test_cases:
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                temp_file = f.name
                f.write(b'0' * byte_size)
            
            try:
                # Should pass with min_bits=0
                result = verify_seed_file(temp_file, min_bits=0)
                self.assertTrue(result['meets_size_requirement'])
                self.assertEqual(result['size_bits'], bit_size)
                
                # Test with custom minimum below actual size
                result = verify_seed_file(temp_file, min_bits=bit_size - 100)
                self.assertTrue(result['meets_size_requirement'])
                
                # Test with custom minimum above actual size
                result = verify_seed_file(temp_file, min_bits=bit_size + 100)
                self.assertFalse(result['meets_size_requirement'])
            finally:
                os.unlink(temp_file)

    def test_very_large_bit_size(self):
        """Test checksum verification for very large bit sizes (16KB = 128Kbit)."""
        # Create a temporary 16KB file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            temp_file = f.name
            f.write(b'A' * 16384)  # 16KB
        
        try:
            result = verify_seed_file(temp_file, min_bits=0)
            
            self.assertTrue(result['exists'])
            self.assertTrue(result['meets_size_requirement'])
            self.assertEqual(result['size_bits'], 131072)  # 16KB * 8
            self.assertIsNotNone(result['sha256'])
            self.assertIsNotNone(result['sha512'])
            self.assertEqual(result['status'], 'CALCULATED')
        finally:
            os.unlink(temp_file)

    def test_batch_verification_with_min_bits(self):
        """Test batch verification with custom minimum bit size."""
        # Create temporary files of various sizes
        temp_files = []
        try:
            for size in [50, 100, 200]:
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                    temp_files.append(f.name)
                    f.write(b'0' * size)
            
            # Verify with min_bits=0 (all should pass)
            results = verify_batch(temp_files, min_bits=0)
            self.assertEqual(len(results), 3)
            for result in results:
                self.assertTrue(result['meets_size_requirement'])
            
            # Verify with min_bits=1000 (only the largest should pass: 200 bytes = 1600 bits)
            results = verify_batch(temp_files, min_bits=1000)
            # 50 bytes = 400 bits (fail), 100 bytes = 800 bits (fail), 200 bytes = 1600 bits (pass)
            self.assertFalse(results[0]['meets_size_requirement'])
            self.assertFalse(results[1]['meets_size_requirement'])
            self.assertTrue(results[2]['meets_size_requirement'])
        finally:
            for f in temp_files:
                if os.path.exists(f):
                    os.unlink(f)


class TestVerificationIntegration(unittest.TestCase):
    """Integration tests for the verification workflow."""

    def test_full_verification_workflow(self):
        """Test the complete verification workflow."""
        test_files = [
            'formats/golden_seed_132.bin',
            'formats/golden_seed_256.bin',
            'formats/golden_seed_512.bin'
        ]
        
        existing_files = [f for f in test_files if os.path.exists(f)]
        if not existing_files:
            self.skipTest("Test files not found")
        
        checksums_file = 'formats/test_checksums.json'
        if not os.path.exists(checksums_file):
            checksums_file = None
        
        # Run batch verification
        results = verify_batch(existing_files, checksums_file)
        
        # All should pass
        for result in results:
            self.assertIn(result['status'], ['PASSED', 'CALCULATED'])
            self.assertTrue(result['meets_size_requirement'])

    def test_json_output_structure(self):
        """Test that JSON output has correct structure."""
        test_files = ['formats/golden_seed_132.bin']
        
        if not os.path.exists(test_files[0]):
            self.skipTest(f"Test file not found: {test_files[0]}")
        
        results = verify_batch(test_files)
        
        # Ensure results can be serialized to JSON
        json_str = json.dumps(results)
        parsed = json.loads(json_str)
        
        self.assertEqual(len(parsed), 1)
        self.assertIsInstance(parsed[0], dict)


if __name__ == '__main__':
    unittest.main()
