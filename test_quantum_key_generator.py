"""
Unit tests for Post-Quantum Secure Key Generator Service.

Tests validate:
- Key generation algorithms (Fusion, Hash, Hybrid)
- Key length validation (128, 256, 512 bits)
- Batch key generation
- Checksum integrity
- Entropy sources and randomness
"""

import unittest
import sys
import os
# Add current directory (repository root) to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from qkd.algorithms.quantum_key_generator import PQKeyGenerator


class TestPQKeyGenerator(unittest.TestCase):
    """Test suite for Post-Quantum Secure Key Generator Service."""

    def test_generator_initialization(self):
        """Test that generator initializes with valid parameters."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        self.assertEqual(gen.algorithm, 'fusion')
        self.assertEqual(gen.key_length, 256)

    def test_invalid_algorithm(self):
        """Test that invalid algorithm raises ValueError."""
        with self.assertRaises(ValueError):
            PQKeyGenerator(algorithm='invalid', key_length=256)

    def test_invalid_key_length(self):
        """Test that invalid key length raises ValueError."""
        with self.assertRaises(ValueError):
            PQKeyGenerator(algorithm='fusion', key_length=1024)

    def test_fusion_key_generation(self):
        """Test Binary Fusion Tap key generation."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        key_data = gen.generate_fusion_key(k=11)

        # Verify key structure
        self.assertIn('key', key_data)
        self.assertIn('key_length', key_data)
        self.assertIn('algorithm', key_data)
        self.assertIn('checksum', key_data)

        # Verify key length in hex (256 bits = 64 hex chars)
        self.assertEqual(len(key_data['key']), 64)
        self.assertEqual(key_data['key_length'], 256)
        self.assertEqual(key_data['algorithm'], 'fusion')

    def test_hash_key_generation(self):
        """Test hash-based key generation."""
        gen = PQKeyGenerator(algorithm='hash', key_length=256)
        key_data = gen.generate_hash_key()

        # Verify key structure
        self.assertIn('key', key_data)
        self.assertEqual(len(key_data['key']), 64)
        self.assertEqual(key_data['algorithm'], 'hash')

    def test_hybrid_key_generation(self):
        """Test hybrid key generation."""
        gen = PQKeyGenerator(algorithm='hybrid', key_length=256)
        key_data = gen.generate_hybrid_key(k=11)

        # Verify key structure
        self.assertIn('key', key_data)
        self.assertIn('fusion_contribution', key_data)
        self.assertIn('zpe_overflow', key_data)
        self.assertEqual(len(key_data['key']), 64)
        self.assertEqual(key_data['algorithm'], 'hybrid')

    def test_key_length_128(self):
        """Test 128-bit key generation."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=128)
        key_data = gen.generate_key(k=11)

        # 128 bits = 32 hex characters
        self.assertEqual(len(key_data['key']), 32)
        self.assertEqual(key_data['key_length'], 128)

    def test_key_length_512(self):
        """Test 512-bit key generation."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=512)
        key_data = gen.generate_key(k=11)

        # 512 bits = 128 hex characters
        self.assertEqual(len(key_data['key']), 128)
        self.assertEqual(key_data['key_length'], 512)

    def test_batch_generation(self):
        """Test batch key generation."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        keys = gen.generate_batch(5, k=11)

        # Verify batch size
        self.assertEqual(len(keys), 5)

        # Verify each key
        for i, key_data in enumerate(keys):
            self.assertIn('key', key_data)
            self.assertEqual(key_data['batch_index'], i)
            self.assertEqual(len(key_data['key']), 64)

    def test_key_uniqueness_in_batch(self):
        """Test that batch-generated keys are unique."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        keys = gen.generate_batch(10, k=11)

        # Extract all keys
        key_values = [k['key'] for k in keys]

        # Verify all keys are unique
        self.assertEqual(len(key_values), len(set(key_values)))

    def test_deterministic_fusion_key(self):
        """Test that fusion keys are deterministic for same parameters."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)

        key1 = gen.generate_fusion_key(k=11)
        key2 = gen.generate_fusion_key(k=11)

        # Without salt, keys should be identical
        self.assertEqual(key1['key'], key2['key'])

    def test_fusion_key_with_salt(self):
        """Test that salt changes fusion keys."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)

        salt1 = b'salt123'
        salt2 = b'salt456'

        key1 = gen.generate_fusion_key(k=11, salt=salt1)
        key2 = gen.generate_fusion_key(k=11, salt=salt2)

        # Different salts should produce different keys
        self.assertNotEqual(key1['key'], key2['key'])

    def test_hash_key_randomness(self):
        """Test that hash keys are random when no seed provided."""
        gen = PQKeyGenerator(algorithm='hash', key_length=256)

        key1 = gen.generate_hash_key()
        key2 = gen.generate_hash_key()

        # Without seed, keys should be different
        self.assertNotEqual(key1['key'], key2['key'])

    def test_hash_key_deterministic_with_seed(self):
        """Test that hash keys are deterministic with same seed."""
        gen = PQKeyGenerator(algorithm='hash', key_length=256)

        seed = 123456789
        key1 = gen.generate_hash_key(seed=seed)
        key2 = gen.generate_hash_key(seed=seed)

        # Same seed should produce same key
        self.assertEqual(key1['key'], key2['key'])

    def test_checksum_validity(self):
        """Test that checksums are valid hex strings."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        key_data = gen.generate_key(k=11)

        checksum = key_data['checksum']

        # SHA256 checksum should be 64 hex characters
        self.assertEqual(len(checksum), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in checksum))

    def test_different_k_values(self):
        """Test fusion keys with different k values."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)

        key_k11 = gen.generate_fusion_key(k=11)
        key_k12 = gen.generate_fusion_key(k=12)
        key_k15 = gen.generate_fusion_key(k=15)

        # Different k values should produce different keys
        self.assertNotEqual(key_k11['key'], key_k12['key'])
        self.assertNotEqual(key_k11['key'], key_k15['key'])
        self.assertNotEqual(key_k12['key'], key_k15['key'])

    def test_hybrid_entropy_mixing(self):
        """Test that hybrid algorithm properly mixes entropy sources."""
        gen = PQKeyGenerator(algorithm='hybrid', key_length=256)

        # Generate with external entropy
        entropy1 = b'external_entropy_source_1'
        entropy2 = b'external_entropy_source_2'

        key1 = gen.generate_hybrid_key(k=11, entropy_source=entropy1)
        key2 = gen.generate_hybrid_key(k=11, entropy_source=entropy2)

        # Different entropy sources should produce different keys
        self.assertNotEqual(key1['key'], key2['key'])

    def test_key_hex_format(self):
        """Test that keys are valid hexadecimal strings."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        key_data = gen.generate_key(k=11)

        key_hex = key_data['key']

        # Should be valid hex
        try:
            int(key_hex, 16)
            valid_hex = True
        except ValueError:
            valid_hex = False

        self.assertTrue(valid_hex)

    def test_zpe_overflow_in_fusion_keys(self):
        """Test that ZPE overflow is included in fusion key metadata."""
        gen = PQKeyGenerator(algorithm='fusion', key_length=256)
        key_data = gen.generate_fusion_key(k=11)

        self.assertIn('zpe_overflow', key_data)
        self.assertIn('tap_state', key_data)

        # For k=11, ZPE overflow should be 0b111011
        self.assertEqual(key_data['zpe_overflow'], '0b111011')


if __name__ == '__main__':
    unittest.main()
