#!/usr/bin/env python3
"""
Unit Tests for Watermark Module

Tests validate:
- Watermark data structure and encoding
- Cryptographic signature generation and verification
- Binary embedding and extraction
- Error handling and edge cases
- Compliance with COMMERCIAL_LICENSE.md requirements
"""

import unittest
import time
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.gq.watermark import (
    WatermarkData,
    WatermarkError,
    encode_watermark,
    decode_watermark,
    embed_watermark_in_binary,
    extract_watermark_from_binary,
    check_watermark_present,
)


class TestWatermarkData(unittest.TestCase):
    """Test suite for WatermarkData class."""
    
    def test_watermark_creation(self):
        """Test creating a watermark with valid data."""
        license_id = "LICENSE-2026-001"
        user_info = "Test User"
        
        watermark = WatermarkData(license_id, user_info)
        
        self.assertEqual(watermark.license_id, license_id)
        self.assertEqual(watermark.user_info, user_info)
        self.assertIsInstance(watermark.timestamp, float)
        self.assertGreater(watermark.timestamp, 0)
    
    def test_watermark_with_custom_timestamp(self):
        """Test creating a watermark with custom timestamp."""
        license_id = "LICENSE-2026-002"
        user_info = "Test User"
        timestamp = 1704067200.0  # 2024-01-01 00:00:00 UTC
        
        watermark = WatermarkData(license_id, user_info, timestamp)
        
        self.assertEqual(watermark.timestamp, timestamp)
    
    def test_watermark_license_id_max_length(self):
        """Test license ID at maximum length."""
        license_id = "A" * 64
        user_info = "Test"
        
        watermark = WatermarkData(license_id, user_info)
        self.assertEqual(len(watermark.license_id), 64)
    
    def test_watermark_license_id_too_long(self):
        """Test that license ID exceeding limit raises error."""
        license_id = "A" * 65
        user_info = "Test"
        
        with self.assertRaises(WatermarkError):
            WatermarkData(license_id, user_info)
    
    def test_watermark_user_info_max_length(self):
        """Test user info at maximum length."""
        license_id = "LICENSE-001"
        user_info = "B" * 128
        
        watermark = WatermarkData(license_id, user_info)
        self.assertEqual(len(watermark.user_info), 128)
    
    def test_watermark_user_info_too_long(self):
        """Test that user info exceeding limit raises error."""
        license_id = "LICENSE-001"
        user_info = "B" * 129
        
        with self.assertRaises(WatermarkError):
            WatermarkData(license_id, user_info)
    
    def test_watermark_to_dict(self):
        """Test converting watermark to dictionary."""
        license_id = "LICENSE-2026-003"
        user_info = "Test User"
        timestamp = 1704067200.0
        
        watermark = WatermarkData(license_id, user_info, timestamp)
        data_dict = watermark.to_dict()
        
        self.assertEqual(data_dict['license_id'], license_id)
        self.assertEqual(data_dict['user_info'], user_info)
        self.assertEqual(data_dict['timestamp'], timestamp)
        self.assertIn('timestamp_readable', data_dict)
    
    def test_watermark_repr(self):
        """Test watermark string representation."""
        watermark = WatermarkData("LICENSE-001", "Test")
        repr_str = repr(watermark)
        
        self.assertIn("WatermarkData", repr_str)
        self.assertIn("LICENSE-001", repr_str)


class TestWatermarkEncoding(unittest.TestCase):
    """Test suite for watermark encoding and decoding."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.secret = "test-secret-key-12345"
        self.watermark = WatermarkData(
            "LICENSE-2026-TEST",
            "Test Organization",
            1704067200.0
        )
    
    def test_encode_watermark(self):
        """Test encoding a watermark."""
        encoded = encode_watermark(self.watermark, self.secret)
        
        self.assertIsInstance(encoded, bytes)
        self.assertEqual(len(encoded), WatermarkData.WATERMARK_SIZE)
        
        # Check magic bytes
        self.assertEqual(encoded[:4], WatermarkData.MAGIC)
        
        # Check version
        self.assertEqual(encoded[4], WatermarkData.VERSION)
    
    def test_decode_watermark(self):
        """Test decoding a watermark."""
        encoded = encode_watermark(self.watermark, self.secret)
        decoded = decode_watermark(encoded, self.secret)
        
        self.assertEqual(decoded.license_id, self.watermark.license_id)
        self.assertEqual(decoded.user_info, self.watermark.user_info)
        self.assertAlmostEqual(decoded.timestamp, self.watermark.timestamp, places=6)
    
    def test_encode_decode_roundtrip(self):
        """Test encoding and decoding produces same data."""
        encoded = encode_watermark(self.watermark, self.secret)
        decoded = decode_watermark(encoded, self.secret)
        
        self.assertEqual(decoded.license_id, self.watermark.license_id)
        self.assertEqual(decoded.user_info, self.watermark.user_info)
        self.assertAlmostEqual(decoded.timestamp, self.watermark.timestamp, places=6)
    
    def test_decode_invalid_secret(self):
        """Test that decoding with wrong secret fails."""
        encoded = encode_watermark(self.watermark, self.secret)
        
        with self.assertRaises(WatermarkError) as context:
            decode_watermark(encoded, "wrong-secret")
        
        self.assertIn("Signature verification failed", str(context.exception))
    
    def test_decode_invalid_magic(self):
        """Test that decoding invalid magic bytes fails."""
        encoded = encode_watermark(self.watermark, self.secret)
        
        # Corrupt magic bytes
        corrupted = b'XXXX' + encoded[4:]
        
        with self.assertRaises(WatermarkError) as context:
            decode_watermark(corrupted, self.secret)
        
        self.assertIn("Invalid magic bytes", str(context.exception))
    
    def test_decode_invalid_version(self):
        """Test that decoding invalid version fails."""
        encoded = encode_watermark(self.watermark, self.secret)
        
        # Change version byte
        corrupted = encoded[:4] + b'\xFF' + encoded[5:]
        
        with self.assertRaises(WatermarkError) as context:
            decode_watermark(corrupted, self.secret)
        
        self.assertIn("Unsupported version", str(context.exception))
    
    def test_decode_too_short(self):
        """Test that decoding too-short data fails."""
        short_data = b'SEED\x01' + b'\x00' * 10
        
        with self.assertRaises(WatermarkError) as context:
            decode_watermark(short_data, self.secret)
        
        self.assertIn("Invalid watermark size", str(context.exception))
    
    def test_encode_with_special_characters(self):
        """Test encoding watermark with special characters."""
        watermark = WatermarkData(
            "LICENSE-2026-ÜNÏ€ÖDE",
            "Tëst Ôrgånïzåtïön 日本語",
            1704067200.0
        )
        
        encoded = encode_watermark(watermark, self.secret)
        decoded = decode_watermark(encoded, self.secret)
        
        self.assertEqual(decoded.license_id, watermark.license_id)
        self.assertEqual(decoded.user_info, watermark.user_info)


class TestBinaryEmbedding(unittest.TestCase):
    """Test suite for embedding watermarks in binary data."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.secret = "test-secret-key-12345"
        self.watermark = WatermarkData(
            "LICENSE-2026-EMBED",
            "Embed Test User",
            1704067200.0
        )
        self.binary_data = b'\x00\x01\x02\x03\x04\x05\x06\x07' * 32
    
    def test_embed_watermark(self):
        """Test embedding watermark in binary data."""
        watermarked = embed_watermark_in_binary(
            self.binary_data, self.watermark, self.secret
        )
        
        self.assertGreater(len(watermarked), len(self.binary_data))
        self.assertEqual(
            len(watermarked),
            len(self.binary_data) + WatermarkData.WATERMARK_SIZE
        )
        
        # Original data should be at the beginning
        self.assertEqual(
            watermarked[:len(self.binary_data)],
            self.binary_data
        )
    
    def test_extract_watermark(self):
        """Test extracting watermark from binary data."""
        watermarked = embed_watermark_in_binary(
            self.binary_data, self.watermark, self.secret
        )
        
        original, extracted = extract_watermark_from_binary(
            watermarked, self.secret
        )
        
        self.assertEqual(original, self.binary_data)
        self.assertEqual(extracted.license_id, self.watermark.license_id)
        self.assertEqual(extracted.user_info, self.watermark.user_info)
    
    def test_embed_extract_roundtrip(self):
        """Test full roundtrip of embed and extract."""
        watermarked = embed_watermark_in_binary(
            self.binary_data, self.watermark, self.secret
        )
        
        original, extracted = extract_watermark_from_binary(
            watermarked, self.secret
        )
        
        # Original data should be unchanged
        self.assertEqual(original, self.binary_data)
        
        # Watermark should be intact
        self.assertEqual(extracted.license_id, self.watermark.license_id)
        self.assertEqual(extracted.user_info, self.watermark.user_info)
        self.assertAlmostEqual(
            extracted.timestamp, self.watermark.timestamp, places=6
        )
    
    def test_check_watermark_present(self):
        """Test checking if watermark is present."""
        # Binary without watermark
        self.assertFalse(check_watermark_present(self.binary_data))
        
        # Binary with watermark
        watermarked = embed_watermark_in_binary(
            self.binary_data, self.watermark, self.secret
        )
        self.assertTrue(check_watermark_present(watermarked))
    
    def test_check_watermark_too_small(self):
        """Test checking watermark in too-small data."""
        small_data = b'\x00\x01\x02\x03'
        self.assertFalse(check_watermark_present(small_data))
    
    def test_extract_from_non_watermarked(self):
        """Test extracting from non-watermarked data fails."""
        with self.assertRaises(WatermarkError):
            extract_watermark_from_binary(self.binary_data, self.secret)
    
    def test_extract_too_small(self):
        """Test extracting from too-small data fails."""
        small_data = b'\x00\x01\x02\x03'
        
        with self.assertRaises(WatermarkError) as context:
            extract_watermark_from_binary(small_data, self.secret)
        
        self.assertIn("too small", str(context.exception))


class TestDeterministicProperties(unittest.TestCase):
    """Test that watermarks don't affect deterministic properties."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.secret = "test-secret-key-12345"
    
    def test_original_data_preserved(self):
        """Test that original binary data is preserved exactly."""
        original = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF'
        watermark = WatermarkData("LIC-001", "User")
        
        watermarked = embed_watermark_in_binary(original, watermark, self.secret)
        extracted_original, _ = extract_watermark_from_binary(watermarked, self.secret)
        
        # Original data must be byte-for-byte identical
        self.assertEqual(original, extracted_original)
    
    def test_multiple_embeddings_independent(self):
        """Test that multiple embeddings produce different watermarks."""
        original = b'\x00\x11\x22\x33'
        
        watermark1 = WatermarkData("LIC-001", "User1", 1704067200.0)
        watermark2 = WatermarkData("LIC-002", "User2", 1704067300.0)
        
        watermarked1 = embed_watermark_in_binary(original, watermark1, self.secret)
        watermarked2 = embed_watermark_in_binary(original, watermark2, self.secret)
        
        # Watermarked data should be different
        self.assertNotEqual(watermarked1, watermarked2)
        
        # But original data should be the same in both
        extracted1, wm1 = extract_watermark_from_binary(watermarked1, self.secret)
        extracted2, wm2 = extract_watermark_from_binary(watermarked2, self.secret)
        
        self.assertEqual(extracted1, extracted2)
        self.assertEqual(extracted1, original)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_binary_data(self):
        """Test watermarking empty binary data."""
        secret = "test-secret"
        watermark = WatermarkData("LIC-001", "User")
        
        watermarked = embed_watermark_in_binary(b'', watermark, secret)
        
        # Should contain only the watermark
        self.assertEqual(len(watermarked), WatermarkData.WATERMARK_SIZE)
        
        # Should be extractable
        original, extracted = extract_watermark_from_binary(watermarked, secret)
        self.assertEqual(original, b'')
        self.assertEqual(extracted.license_id, "LIC-001")
    
    def test_large_binary_data(self):
        """Test watermarking large binary data."""
        secret = "test-secret"
        watermark = WatermarkData("LIC-001", "User")
        
        # 1MB of data
        large_data = b'\x42' * (1024 * 1024)
        
        watermarked = embed_watermark_in_binary(large_data, watermark, secret)
        original, extracted = extract_watermark_from_binary(watermarked, secret)
        
        self.assertEqual(original, large_data)
        self.assertEqual(extracted.license_id, "LIC-001")
    
    def test_minimal_license_id(self):
        """Test with minimal license ID."""
        watermark = WatermarkData("A", "User")
        secret = "secret"
        
        encoded = encode_watermark(watermark, secret)
        decoded = decode_watermark(encoded, secret)
        
        self.assertEqual(decoded.license_id, "A")
    
    def test_minimal_user_info(self):
        """Test with minimal user info."""
        watermark = WatermarkData("LICENSE", "U")
        secret = "secret"
        
        encoded = encode_watermark(watermark, secret)
        decoded = decode_watermark(encoded, secret)
        
        self.assertEqual(decoded.user_info, "U")
    
    def test_timestamp_precision(self):
        """Test that timestamp precision is preserved."""
        timestamp = time.time()
        watermark = WatermarkData("LIC", "User", timestamp)
        secret = "secret"
        
        encoded = encode_watermark(watermark, secret)
        decoded = decode_watermark(encoded, secret)
        
        # Should be very close (within microsecond precision)
        self.assertAlmostEqual(decoded.timestamp, timestamp, places=6)


if __name__ == '__main__':
    unittest.main()
