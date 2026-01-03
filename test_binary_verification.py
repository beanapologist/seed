"""
Unit tests for Binary Representation Verification.

Tests validate:
- Binary representation calculation
- Manifested value computation
- Bit length calculations
- Formula verification: manifested = (seed * 8) + k
"""

import unittest
from verify_binary_representation import verify_binary_representation


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


if __name__ == '__main__':
    unittest.main()
