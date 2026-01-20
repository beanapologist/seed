"""
Unit tests for Binary Representation Verification.

Tests validate:
- Binary representation calculation
- Manifested value computation
- Bit length calculations
- Formula verification: manifested = (seed * 8) + k
- Checksum integrity validation
- Binary Fusion Tap with 8-fold Heartbeat
- ZPE Overflow extraction via XOR
"""

import unittest
import sys
import os
# Add current directory (repository root) to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from checksum.verify_binary_representation import (
    verify_binary_representation,
    calculate_checksum,
    verify_checksum_integrity,
    binary_fusion_tap
)


class TestBinaryVerification(unittest.TestCase):
    """Test suite for binary representation verification."""

    def test_verify_binary_representation_k11(self):
        """Test binary verification with k=11 and seed_11=1234567891011."""
        k = 11
        seed_11 = 1234567891011

        results = verify_binary_representation(k, seed_11)

        # Verify the results
        self.assertEqual(results['k'], 11)
        self.assertEqual(results['seed_value'], 1234567891011)
        self.assertEqual(results['seed_bit_length'], 41)
        self.assertEqual(results['manifested_bit_length'], 44)
        self.assertEqual(
            results['manifested_binary'],
            '0b10001111101110001111110110000100001000100011'
        )

    def test_manifested_formula(self):
        """Test that manifested = (seed * 8) + k is correctly calculated."""
        k = 11
        seed_value = 1234567891011
        expected_manifested = (seed_value * 8) + k

        results = verify_binary_representation(k, seed_value)

        self.assertEqual(results['manifested_value'], expected_manifested)
        self.assertEqual(results['manifested_value'], 9876543128099)

    def test_bit_length_calculation(self):
        """Test that bit lengths are correctly calculated."""
        k = 11
        seed_value = 1234567891011

        results = verify_binary_representation(k, seed_value)

        # Verify seed bit length
        expected_seed_bits = len(bin(seed_value)) - 2  # Remove '0b' prefix
        self.assertEqual(results['seed_bit_length'], expected_seed_bits)

        # Verify manifested bit length
        manifested = (seed_value * 8) + k
        expected_manifested_bits = len(bin(manifested)) - 2
        self.assertEqual(results['manifested_bit_length'], expected_manifested_bits)

    def test_binary_representation_format(self):
        """Test that binary representations have correct format."""
        k = 11
        seed_value = 1234567891011

        results = verify_binary_representation(k, seed_value)

        # Check that binary strings start with '0b'
        self.assertTrue(results['seed_binary'].startswith('0b'))
        self.assertTrue(results['manifested_binary'].startswith('0b'))

    def test_different_k_values(self):
        """Test verification with different k values."""
        seed_value = 1234567891011

        for k in [1, 5, 11, 15, 31]:
            results = verify_binary_representation(k, seed_value)

            # Verify formula holds for different k values
            expected_manifested = (seed_value * 8) + k
            self.assertEqual(results['manifested_value'], expected_manifested)
            self.assertEqual(results['k'], k)

    def test_bit_length_increase(self):
        """Test that manifested value increases bit length appropriately."""
        k = 11
        seed_value = 1234567891011

        results = verify_binary_representation(k, seed_value)

        # Multiplying by 8 shifts left by 3 bits, so manifested should be larger
        bit_increase = results['manifested_bit_length'] - results['seed_bit_length']

        # The increase should be 3 bits (from shift left by 3) or possibly 4
        # depending on carries
        self.assertGreaterEqual(bit_increase, 3)
        self.assertLessEqual(bit_increase, 4)

    def test_checksum_calculation(self):
        """Test that checksums are correctly calculated."""
        seed_value = 1234567891011
        
        # Calculate checksum
        checksum = calculate_checksum(seed_value, 'sha256')
        
        # Verify it's a valid hex string of correct length (64 chars for SHA256)
        self.assertEqual(len(checksum), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in checksum))
        
        # Verify consistency - same input should produce same checksum
        checksum2 = calculate_checksum(seed_value, 'sha256')
        self.assertEqual(checksum, checksum2)

    def test_checksum_in_verification_results(self):
        """Test that verification results include checksum fields."""
        k = 11
        seed_value = 1234567891011
        
        results = verify_binary_representation(k, seed_value)
        
        # Check that checksum fields are present
        self.assertIn('seed_sha256', results)
        self.assertIn('manifested_sha256', results)
        self.assertIn('seed_checksum_valid', results)
        self.assertIn('manifested_checksum_valid', results)
        
        # Check that checksums are valid hex strings
        self.assertEqual(len(results['seed_sha256']), 64)
        self.assertEqual(len(results['manifested_sha256']), 64)
        
        # Check that validation flags are True by default
        self.assertTrue(results['seed_checksum_valid'])
        self.assertTrue(results['manifested_checksum_valid'])

    def test_checksum_integrity_validation(self):
        """Test checksum integrity validation with expected values."""
        seed_value = 1234567891011
        manifested_value = (seed_value * 8) + 11
        
        # Get actual checksums
        actual_seed_checksum = calculate_checksum(seed_value, 'sha256')
        actual_manifested_checksum = calculate_checksum(manifested_value, 'sha256')
        
        # Verify with correct checksums
        result = verify_checksum_integrity(
            seed_value, 
            manifested_value,
            actual_seed_checksum,
            actual_manifested_checksum
        )
        
        self.assertTrue(result['seed_checksum_valid'])
        self.assertTrue(result['manifested_checksum_valid'])
        
        # Verify with incorrect checksums
        result = verify_checksum_integrity(
            seed_value,
            manifested_value,
            'incorrect_checksum',
            'incorrect_checksum'
        )
        
        self.assertFalse(result['seed_checksum_valid'])
        self.assertFalse(result['manifested_checksum_valid'])

    def test_checksum_algorithm_sha512(self):
        """Test checksum calculation with SHA512 algorithm."""
        seed_value = 1234567891011
        
        # Calculate SHA512 checksum
        checksum = calculate_checksum(seed_value, 'sha512')
        
        # Verify it's a valid hex string of correct length (128 chars for SHA512)
        self.assertEqual(len(checksum), 128)
        self.assertTrue(all(c in '0123456789abcdef' for c in checksum))

    def test_known_checksum_values(self):
        """Test against known checksum values for seed_11."""
        k = 11
        seed_11 = 1234567891011
        
        results = verify_binary_representation(k, seed_11)
        
        # These are the expected checksums for seed_11
        expected_seed_sha256 = '7f1665ab9f8c74fd60bd4fdcb10382b63727e10db9d568d385930695cc2f0454'
        expected_manifested_sha256 = '677b205682ad566fcee652f80a4e8a538a265dc849da0d86fc0e5282b4cbf115'
        
        self.assertEqual(results['seed_sha256'], expected_seed_sha256)
        self.assertEqual(results['manifested_sha256'], expected_manifested_sha256)


class TestBinaryFusionTap(unittest.TestCase):
    """Test suite for binary fusion tap with 8-fold heartbeat and ZPE overflow."""

    def test_binary_fusion_tap_k11(self):
        """Test binary fusion tap for k=11 (the 'New Dimension')."""
        blueprint = binary_fusion_tap(11)

        self.assertEqual(blueprint['k'], 11)
        self.assertEqual(blueprint['seed_value'], 1234567891011)
        self.assertEqual(
            blueprint['tap_state'],
            '0b10001111101110001111110110000100001000100011'
        )
        self.assertEqual(blueprint['zpe_overflow'], '0b111011')
        self.assertEqual(blueprint['zpe_overflow_decimal'], 59)

    def test_8fold_heartbeat(self):
        """Test that 8-fold heartbeat correctly shifts left by 3."""
        k = 11
        blueprint = binary_fusion_tap(k)

        seed_val = blueprint['seed_value']
        heartbeat_val = seed_val << 3  # Shift left by 3
        manifested = heartbeat_val + k

        # Verify the tap state matches the calculated manifested value
        self.assertEqual(int(blueprint['tap_state'], 2), manifested)

    def test_zpe_overflow_below_k10(self):
        """Test that ZPE overflow is 0 for k < 10."""
        for k in range(1, 10):
            blueprint = binary_fusion_tap(k)
            self.assertEqual(blueprint['zpe_overflow_decimal'], 0)

    def test_zpe_overflow_k10_and_above(self):
        """Test that ZPE overflow is calculated for k >= 10."""
        for k in [10, 11, 12, 15]:
            blueprint = binary_fusion_tap(k)

            # Overflow should be non-zero for k >= 10
            self.assertGreater(blueprint['zpe_overflow_decimal'], 0)

            # Verify XOR calculation
            seed_val = blueprint['seed_value']
            manifested = (seed_val << 3) + k
            expected_overflow = manifested ^ (seed_val * 8)

            self.assertEqual(blueprint['zpe_overflow_decimal'], expected_overflow)

    def test_seed_generation(self):
        """Test that seed is correctly generated from concatenated sequence."""
        # Test k=5: "12345" -> 12345
        blueprint = binary_fusion_tap(5)
        self.assertEqual(blueprint['seed_value'], 12345)

        # Test k=11: "1234567891011" -> 1234567891011
        blueprint = binary_fusion_tap(11)
        self.assertEqual(blueprint['seed_value'], 1234567891011)

    def test_binary_seed_format(self):
        """Test that binary seed has correct format."""
        blueprint = binary_fusion_tap(11)

        # Should start with '0b'
        self.assertTrue(blueprint['binary_seed'].startswith('0b'))
        self.assertTrue(blueprint['tap_state'].startswith('0b'))
        self.assertTrue(blueprint['zpe_overflow'].startswith('0b'))

    def test_heartbeat_equivalence(self):
        """Test that (seed << 3) is equivalent to (seed * 8)."""
        k = 11
        seed_val = int("".join(map(str, range(1, k + 1))))

        heartbeat_shift = seed_val << 3
        heartbeat_mult = seed_val * 8

        self.assertEqual(heartbeat_shift, heartbeat_mult)


if __name__ == '__main__':
    unittest.main()
