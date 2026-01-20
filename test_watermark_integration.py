#!/usr/bin/env python3
"""
Integration Test for Watermark System

This test demonstrates the complete workflow of creating, embedding, and verifying
watermarks in binary files, ensuring compliance with COMMERCIAL_LICENSE.md.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.gq.watermark import (
    WatermarkData,
    embed_watermark_in_binary,
    extract_watermark_from_binary,
    check_watermark_present,
)


class TestWatermarkIntegration(unittest.TestCase):
    """Integration tests for watermark system with real binary files."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.secret = "integration-test-secret-key"
        self.test_dir = tempfile.mkdtemp()
        
    def test_golden_seed_watermarking(self):
        """Test watermarking the golden seed binary files."""
        # Test with golden_seed_16.bin
        golden_seed_path = Path('formats/golden_seed_16.bin')
        
        if not golden_seed_path.exists():
            self.skipTest("Golden seed file not found")
        
        # Read original golden seed
        with open(golden_seed_path, 'rb') as f:
            original_data = f.read()
        
        print(f"Original golden seed size: {len(original_data)} bytes")
        
        # Create watermark
        watermark = WatermarkData(
            license_id="LICENSE-INTEGRATION-001",
            user_info="Integration Test User"
        )
        
        # Embed watermark
        watermarked_data = embed_watermark_in_binary(
            original_data, watermark, self.secret
        )
        
        print(f"Watermarked data size: {len(watermarked_data)} bytes")
        
        # Verify watermark is present
        self.assertTrue(check_watermark_present(watermarked_data))
        
        # Extract and verify
        extracted_data, extracted_watermark = extract_watermark_from_binary(
            watermarked_data, self.secret
        )
        
        # Verify original data is preserved
        self.assertEqual(extracted_data, original_data)
        
        # Verify watermark data
        self.assertEqual(extracted_watermark.license_id, watermark.license_id)
        self.assertEqual(extracted_watermark.user_info, watermark.user_info)
        
        print("✓ Golden seed watermarking successful")
    
    def test_large_binary_watermarking(self):
        """Test watermarking larger binary files."""
        golden_seed_path = Path('formats/golden_seed_256.bin')
        
        if not golden_seed_path.exists():
            self.skipTest("Golden seed 256 file not found")
        
        # Read original
        with open(golden_seed_path, 'rb') as f:
            original_data = f.read()
        
        # Create watermark with maximum field sizes
        watermark = WatermarkData(
            license_id="LICENSE-2026-LARGE-BIN-" + "X" * 38,  # 64 chars total
            user_info="Large Binary Test Organization " + "Y" * 95  # 128 chars total
        )
        
        # Embed watermark
        watermarked_data = embed_watermark_in_binary(
            original_data, watermark, self.secret
        )
        
        # Write to file
        output_path = Path(self.test_dir) / 'watermarked_large.bin'
        with open(output_path, 'wb') as f:
            f.write(watermarked_data)
        
        # Read back and verify
        with open(output_path, 'rb') as f:
            read_data = f.read()
        
        extracted_data, extracted_watermark = extract_watermark_from_binary(
            read_data, self.secret
        )
        
        # Verify integrity
        self.assertEqual(extracted_data, original_data)
        self.assertEqual(extracted_watermark.license_id, watermark.license_id)
        self.assertEqual(extracted_watermark.user_info, watermark.user_info)
        
        print(f"✓ Large binary watermarking successful ({len(original_data)} bytes)")
    
    def test_multiple_binaries_distinct_watermarks(self):
        """Test that multiple binaries get distinct watermarks."""
        original_data = b'\x00\x01\x02\x03' * 64
        
        watermarks = []
        watermarked_binaries = []
        
        # Create multiple watermarked versions
        for i in range(5):
            watermark = WatermarkData(
                license_id=f"LICENSE-2026-{i:03d}",
                user_info=f"User {i}"
            )
            watermarks.append(watermark)
            
            watermarked = embed_watermark_in_binary(
                original_data, watermark, self.secret
            )
            watermarked_binaries.append(watermarked)
        
        # Verify all watermarked binaries are different
        for i in range(len(watermarked_binaries)):
            for j in range(i + 1, len(watermarked_binaries)):
                self.assertNotEqual(
                    watermarked_binaries[i],
                    watermarked_binaries[j]
                )
        
        # Verify each can be extracted correctly
        for i, watermarked in enumerate(watermarked_binaries):
            extracted_data, extracted_watermark = extract_watermark_from_binary(
                watermarked, self.secret
            )
            
            self.assertEqual(extracted_data, original_data)
            self.assertEqual(
                extracted_watermark.license_id,
                watermarks[i].license_id
            )
            self.assertEqual(
                extracted_watermark.user_info,
                watermarks[i].user_info
            )
        
        print("✓ Multiple distinct watermarks verified")
    
    def test_workflow_simulation(self):
        """Simulate the complete licensed distribution workflow."""
        print("\n" + "="*70)
        print("SIMULATING COMMERCIAL LICENSING WORKFLOW")
        print("="*70)
        
        # Step 1: License issuance
        print("\nStep 1: License Issuance")
        license_id = "LICENSE-2026-ACME-001"
        user_info = "Acme Corporation"
        secret = "acme-secret-key-do-not-share"
        print(f"  Issued License: {license_id}")
        print(f"  Licensee: {user_info}")
        print(f"  Secret Key: {secret[:10]}...")
        
        # Step 2: Binary generation
        print("\nStep 2: Binary Generation")
        # Simulate generating a binary output
        binary_output = b'\xDE\xAD\xBE\xEF' * 128
        print(f"  Generated binary: {len(binary_output)} bytes")
        
        # Step 3: Watermark embedding
        print("\nStep 3: Watermark Embedding")
        watermark = WatermarkData(license_id, user_info)
        watermarked_binary = embed_watermark_in_binary(
            binary_output, watermark, secret
        )
        print(f"  Watermarked binary: {len(watermarked_binary)} bytes")
        print(f"  Watermark size: {len(watermarked_binary) - len(binary_output)} bytes")
        
        # Step 4: Distribution
        print("\nStep 4: Distribution")
        print("  Binary distributed to end users...")
        
        # Step 5: Verification (by authorized party)
        print("\nStep 5: Verification")
        if check_watermark_present(watermarked_binary):
            print("  ✓ Watermark detected")
            
            try:
                _, verified_watermark = extract_watermark_from_binary(
                    watermarked_binary, secret
                )
                print("  ✓ Signature verified")
                print(f"  License ID: {verified_watermark.license_id}")
                print(f"  Licensee: {verified_watermark.user_info}")
                print(f"  Timestamp: {verified_watermark.to_dict()['timestamp_readable']}")
                print("\n  ✓ Binary is properly licensed for commercial distribution")
            except Exception as e:
                print(f"  ✗ Verification failed: {e}")
        else:
            print("  ✗ No watermark found")
        
        print("="*70)
        
        # Verify the workflow succeeded
        extracted_data, verified_watermark = extract_watermark_from_binary(
            watermarked_binary, secret
        )
        self.assertEqual(extracted_data, binary_output)
        self.assertEqual(verified_watermark.license_id, license_id)
        self.assertEqual(verified_watermark.user_info, user_info)


class TestDeterministicProperties(unittest.TestCase):
    """Test that watermarks preserve deterministic properties."""
    
    def test_deterministic_output_preservation(self):
        """Verify that deterministic outputs are preserved byte-for-byte."""
        try:
            from src.gq.gqs1 import generate_test_vectors
            
            # Generate deterministic output
            vectors = generate_test_vectors(10)
            # Validate hex strings before conversion
            for v in vectors:
                if not all(c in '0123456789abcdefABCDEF' for c in v):
                    raise ValueError(f"Invalid hex string: {v}")
            deterministic_output = b''.join(bytes.fromhex(v) for v in vectors)
        except (ImportError, ValueError):
            # Fallback to simple deterministic data
            deterministic_output = bytes(range(256))
        
        # Create watermark
        secret = "test-secret"
        watermark = WatermarkData("LIC-001", "User")
        
        # Embed watermark
        watermarked = embed_watermark_in_binary(
            deterministic_output, watermark, secret
        )
        
        # Extract and verify
        extracted, _ = extract_watermark_from_binary(watermarked, secret)
        
        # Original deterministic output must be preserved exactly
        self.assertEqual(extracted, deterministic_output)
        
        print("✓ Deterministic properties preserved")


class TestComplianceRequirements(unittest.TestCase):
    """Test compliance with COMMERCIAL_LICENSE.md requirements."""
    
    def test_traceability(self):
        """Verify watermarks provide traceability."""
        secret = "test-secret"
        
        # Create watermarked binary
        watermark = WatermarkData(
            license_id="LICENSE-2026-TRACE-001",
            user_info="Traceable User Corp"
        )
        original = b'\x00' * 100
        watermarked = embed_watermark_in_binary(original, watermark, secret)
        
        # Extract and verify traceability
        _, extracted = extract_watermark_from_binary(watermarked, secret)
        
        self.assertEqual(extracted.license_id, "LICENSE-2026-TRACE-001")
        self.assertEqual(extracted.user_info, "Traceable User Corp")
        self.assertIsNotNone(extracted.timestamp)
        
        print("✓ Traceability requirement satisfied")
    
    def test_authorization_enforcement(self):
        """Verify that wrong secret prevents verification."""
        secret1 = "authorized-secret"
        secret2 = "unauthorized-secret"
        
        # Create watermarked binary with authorized secret
        watermark = WatermarkData("LIC-001", "User")
        original = b'\x00' * 100
        watermarked = embed_watermark_in_binary(original, watermark, secret1)
        
        # Authorized verification should succeed
        _, verified = extract_watermark_from_binary(watermarked, secret1)
        self.assertEqual(verified.license_id, "LIC-001")
        
        # Unauthorized verification should fail
        from src.gq.watermark import WatermarkError
        with self.assertRaises(WatermarkError):
            extract_watermark_from_binary(watermarked, secret2)
        
        print("✓ Authorization enforcement verified")


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
