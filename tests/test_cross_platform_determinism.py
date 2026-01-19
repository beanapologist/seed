"""
Cross-Platform Determinism Test Suite for STL (Standardized Test Library)

This test suite validates deterministic behavior across different platforms,
architectures, and environments to ensure reproducibility.

Tests validate:
- Reproducibility across different Python versions
- Platform-independent behavior (endianness handling)
- Consistent behavior across different OS environments
- IEEE 754 floating-point consistency
- Hash function consistency across platforms
"""

import unittest
import hashlib
import sys
import os
import struct
import platform
from typing import List

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gq import UniversalQKD, GQS1
from qkd.algorithms.universal_qkd import (
    HEX_SEED,
    EXPECTED_CHECKSUM,
    verify_seed_checksum,
    universal_qkd_generator,
)
from gq.gqs1_core import (
    hash_drbg_ratchet,
    generate_test_vectors,
)


class TestPlatformIndependence(unittest.TestCase):
    """Test suite for platform-independent behavior."""
    
    def test_seed_checksum_verification_platform_independent(self):
        """Test that seed checksum is platform-independent."""
        seed = bytes.fromhex(HEX_SEED)
        
        # Calculate checksum
        checksum = hashlib.sha256(seed).hexdigest()
        
        # Should match expected checksum regardless of platform
        self.assertEqual(checksum, EXPECTED_CHECKSUM)
        
        # Verify function should return True
        self.assertTrue(verify_seed_checksum(seed))
    
    def test_first_key_deterministic_across_platforms(self):
        """Test that the first generated key is deterministic."""
        # This is the known first key from the specification
        EXPECTED_FIRST_KEY = "3c732e0d04dac163a5cc2b15c7caf42c"
        
        generator = universal_qkd_generator()
        first_key = next(generator)
        
        # Should match expected value
        self.assertEqual(first_key.hex(), EXPECTED_FIRST_KEY)
    
    def test_key_sequence_deterministic(self):
        """Test that key sequence is deterministic across runs."""
        # Generate reference sequence
        generator1 = universal_qkd_generator()
        sequence1 = [next(generator1) for _ in range(100)]
        
        # Generate again
        generator2 = universal_qkd_generator()
        sequence2 = [next(generator2) for _ in range(100)]
        
        # Should be identical
        self.assertEqual(sequence1, sequence2)
    
    def test_gqs1_first_vector_deterministic(self):
        """Test that GQS-1 first test vector is deterministic."""
        # Known first vector from specification
        EXPECTED_FIRST_VECTOR = "a01611f01e8207a27c1529c3650c4838"
        
        vectors = generate_test_vectors(1)
        
        # generate_test_vectors returns hex strings
        self.assertEqual(vectors[0], EXPECTED_FIRST_VECTOR)
    
    def test_hash_output_endianness_independence(self):
        """Test that hash outputs are endianness-independent."""
        test_input = b"test input data"
        
        # SHA-256 should produce same output regardless of endianness
        hash_output = hashlib.sha256(test_input).digest()
        
        # Verify length
        self.assertEqual(len(hash_output), 32)
        
        # Convert to hex and back
        hex_output = hash_output.hex()
        reconstructed = bytes.fromhex(hex_output)
        
        # Should be identical
        self.assertEqual(hash_output, reconstructed)


class TestReproducibilityAcrossEnvironments(unittest.TestCase):
    """Test suite for reproducibility across different environments."""
    
    def test_reproducible_with_fresh_generator(self):
        """Test that fresh generators produce same sequence."""
        sequences = []
        
        for _ in range(10):
            generator = universal_qkd_generator()
            sequence = [next(generator) for _ in range(20)]
            sequences.append(sequence)
        
        # All sequences should be identical
        for i in range(1, len(sequences)):
            self.assertEqual(sequences[0], sequences[i])
    
    def test_reproducible_state_evolution(self):
        """Test that state evolution is reproducible."""
        seed = bytes.fromhex(HEX_SEED)
        
        # Evolve state multiple times
        evolutions = []
        
        for trial in range(5):
            state = hashlib.sha256(seed).digest()
            states = [state]
            
            for i in range(100):
                state = hash_drbg_ratchet(state, i)
                states.append(state)
            
            evolutions.append(states)
        
        # All evolutions should be identical
        for i in range(1, len(evolutions)):
            self.assertEqual(evolutions[0], evolutions[i])
    
    def test_no_randomness_sources_used(self):
        """Test that no system randomness is used (fully deterministic)."""
        # Generate keys multiple times and verify they're always the same
        results = []
        
        for _ in range(5):
            generator = universal_qkd_generator()
            keys = [next(generator) for _ in range(50)]
            results.append(keys)
        
        # All results should be identical (no randomness)
        for i in range(1, len(results)):
            self.assertEqual(results[0], results[i])


class TestIEEE754Consistency(unittest.TestCase):
    """Test suite for IEEE 754 floating-point consistency."""
    
    def test_golden_ratio_representation(self):
        """Test that golden ratio is represented consistently."""
        # Golden ratio: φ = (1 + √5) / 2 ≈ 1.618033988749895
        phi = (1 + 5 ** 0.5) / 2
        
        # Should be close to expected value (use 12 places for cross-platform compatibility)
        expected_phi = 1.618033988749895
        self.assertAlmostEqual(phi, expected_phi, places=12)
        
        # Test IEEE 754 binary representation
        phi_bytes = struct.pack('<d', phi)  # Little-endian double
        
        # Should be 8 bytes
        self.assertEqual(len(phi_bytes), 8)
        
        # Reconstruct
        reconstructed_phi = struct.unpack('<d', phi_bytes)[0]
        self.assertEqual(phi, reconstructed_phi)
    
    def test_seed_binary_representation_consistency(self):
        """Test that seed binary representation is consistent."""
        seed = bytes.fromhex(HEX_SEED)
        
        # Should be 32 bytes
        self.assertEqual(len(seed), 32)
        
        # Convert to hex and back
        hex_repr = seed.hex()
        reconstructed = bytes.fromhex(hex_repr)
        
        # Should be identical
        self.assertEqual(seed, reconstructed)
        self.assertEqual(hex_repr, HEX_SEED)
    
    def test_integer_arithmetic_consistency(self):
        """Test that integer arithmetic is consistent across platforms."""
        # Test various integer operations
        test_values = [0, 1, 255, 256, 65535, 2**32 - 1, 2**64 - 1]
        
        for value in test_values:
            # Bit shift operations
            shifted = value << 3  # Multiply by 8
            self.assertEqual(shifted, value * 8)
            
            # XOR operations
            xor_result = value ^ 0xFF
            self.assertIsInstance(xor_result, int)
            
            # Modulo operations
            if value > 0:
                mod_result = value % 256
                self.assertGreaterEqual(mod_result, 0)
                self.assertLess(mod_result, 256)


class TestHashFunctionConsistency(unittest.TestCase):
    """Test suite for hash function consistency."""
    
    def test_sha256_deterministic(self):
        """Test that SHA-256 is deterministic."""
        test_inputs = [
            b"",
            b"test",
            b"The quick brown fox jumps over the lazy dog",
            bytes(range(256)),
        ]
        
        for test_input in test_inputs:
            # Hash multiple times
            hashes = [hashlib.sha256(test_input).digest() for _ in range(10)]
            
            # All should be identical
            for i in range(1, len(hashes)):
                self.assertEqual(hashes[0], hashes[i])
    
    def test_sha256_known_vectors(self):
        """Test SHA-256 with known test vectors."""
        # Known test vectors from FIPS 180-4
        test_vectors = [
            (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
            (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ]
        
        for input_data, expected_hex in test_vectors:
            result = hashlib.sha256(input_data).hexdigest()
            self.assertEqual(result, expected_hex)
    
    def test_hash_concatenation_consistency(self):
        """Test that hash concatenation is consistent."""
        state = bytes.fromhex(HEX_SEED)
        counter_str = "1"
        
        # Hash state || counter
        combined = state + counter_str.encode('utf-8')
        hash1 = hashlib.sha256(combined).digest()
        
        # Hash again
        hash2 = hashlib.sha256(combined).digest()
        
        # Should be identical
        self.assertEqual(hash1, hash2)


class TestByteOrderIndependence(unittest.TestCase):
    """Test suite for byte order independence."""
    
    def test_hex_string_conversion_independence(self):
        """Test that hex string conversion is byte-order independent."""
        # Test with various byte patterns
        test_patterns = [
            bytes([0x00, 0x01, 0x02, 0x03]),
            bytes([0xFF, 0xFE, 0xFD, 0xFC]),
            bytes([0x12, 0x34, 0x56, 0x78]),
        ]
        
        for pattern in test_patterns:
            # Convert to hex and back
            hex_str = pattern.hex()
            reconstructed = bytes.fromhex(hex_str)
            
            # Should be identical
            self.assertEqual(pattern, reconstructed)
    
    def test_integer_to_bytes_consistency(self):
        """Test that integer to bytes conversion is consistent."""
        test_values = [0, 1, 255, 256, 65535, 16777215]
        
        for value in test_values:
            # Determine required byte length
            byte_length = max(1, (value.bit_length() + 7) // 8)
            
            # Convert to bytes (big-endian)
            bytes_big = value.to_bytes(byte_length, byteorder='big')
            
            # Convert back
            reconstructed = int.from_bytes(bytes_big, byteorder='big')
            
            # Should be identical
            self.assertEqual(value, reconstructed)
    
    def test_counter_encoding_consistency(self):
        """Test that counter encoding is consistent."""
        state = bytes(32)
        
        # Test various counter values
        counters = [0, 1, 100, 1000, 10000, 999999]
        
        for counter in counters:
            # Encode counter as string
            counter_str = str(counter)
            
            # Hash with state
            combined = state + counter_str.encode('utf-8')
            hash_result = hashlib.sha256(combined).digest()
            
            # Should produce deterministic output
            self.assertEqual(len(hash_result), 32)
            
            # Hash again
            hash_result2 = hashlib.sha256(combined).digest()
            self.assertEqual(hash_result, hash_result2)


class TestCrossVersionCompatibility(unittest.TestCase):
    """Test suite for cross-version compatibility."""
    
    def test_python_version_info(self):
        """Test Python version and log for reference."""
        version = sys.version_info
        
        # Should be Python 3.x
        self.assertGreaterEqual(version.major, 3)
        
        # Log version
        print(f"\nPython version: {version.major}.{version.minor}.{version.micro}")
        print(f"Platform: {platform.system()} {platform.machine()}")
    
    def test_known_key_vectors_match(self):
        """Test that known key vectors match expected values."""
        # These are known-good values that should work across all platforms
        known_vectors = [
            ("3c732e0d04dac163a5cc2b15c7caf42c", 0),  # First key
        ]
        
        generator = universal_qkd_generator()
        
        for expected_hex, position in known_vectors:
            # Generate keys up to position
            for _ in range(position + 1):
                key = next(generator)
            
            # Check against expected
            self.assertEqual(key.hex(), expected_hex,
                           f"Key at position {position} does not match")
    
    def test_known_gqs1_vectors_match(self):
        """Test that known GQS-1 vectors match expected values."""
        # Known-good first vector
        EXPECTED_FIRST = "a01611f01e8207a27c1529c3650c4838"
        
        vectors = generate_test_vectors(1)
        
        # generate_test_vectors returns hex strings
        self.assertEqual(vectors[0], EXPECTED_FIRST)


class TestSystemInformationLogging(unittest.TestCase):
    """Test suite that logs system information for debugging."""
    
    def test_log_system_information(self):
        """Log system information for cross-platform debugging."""
        info = {
            "Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "Platform": platform.system(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Python Implementation": platform.python_implementation(),
            "Byte Order": sys.byteorder,
        }
        
        print("\n" + "=" * 60)
        print("System Information:")
        print("=" * 60)
        for key, value in info.items():
            print(f"{key:25s}: {value}")
        print("=" * 60)
        
        # Basic sanity checks
        self.assertIn(info["Platform"], ["Linux", "Windows", "Darwin"])
        self.assertIn(info["Byte Order"], ["little", "big"])
        
        # Test passes if we can log the information
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
