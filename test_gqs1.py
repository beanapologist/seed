"""
Unit tests for the Golden Quantum Standard (GQS-1) implementation.

Tests validate:
- Seed initialization and checksum verification
- Hash-DRBG ratchet function
- Quantum sifting simulation
- XOR folding hardening
- Complete test vector generation
- Cross-implementation consistency
- CLI argument parsing and file I/O
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
import hashlib
from unittest.mock import patch
import sys
import os
# Add current directory (repository root) to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from qkd.algorithms.gqs1 import (
    HEX_SEED,
    EXPECTED_CHECKSUM,
    verify_seed_checksum,
    hash_drbg_ratchet,
    simulate_quantum_sifting,
    xor_fold_hardening,
    generate_key,
    generate_test_vectors,
)


class TestGQS1(unittest.TestCase):
    """Test suite for GQS-1 implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.seed = bytes.fromhex(HEX_SEED)
    
    def test_seed_initialization(self):
        """Test that seed can be properly initialized from hex."""
        self.assertEqual(len(self.seed), 32)
        self.assertEqual(self.seed.hex(), HEX_SEED)
    
    def test_seed_checksum_verification(self):
        """Test that seed checksum verification works correctly."""
        # Valid seed should pass
        self.assertTrue(verify_seed_checksum(self.seed))
        
        # Verify actual checksum matches expected
        actual_checksum = hashlib.sha256(self.seed).hexdigest()
        self.assertEqual(actual_checksum, EXPECTED_CHECKSUM)
        
        # Invalid seed should fail
        invalid_seed = bytes(32)  # All zeros
        self.assertFalse(verify_seed_checksum(invalid_seed))
    
    def test_hash_drbg_ratchet_deterministic(self):
        """Test that Hash-DRBG ratchet produces deterministic output."""
        state = self.seed
        counter = 1
        
        # Same input should produce same output
        result1 = hash_drbg_ratchet(state, counter)
        result2 = hash_drbg_ratchet(state, counter)
        self.assertEqual(result1, result2)
        
        # Output should be 32 bytes (256 bits)
        self.assertEqual(len(result1), 32)
    
    def test_hash_drbg_ratchet_different_counters(self):
        """Test that different counters produce different states."""
        state = self.seed
        
        result1 = hash_drbg_ratchet(state, 1)
        result2 = hash_drbg_ratchet(state, 2)
        
        # Different counters should produce different outputs
        self.assertNotEqual(result1, result2)
    
    def test_hash_drbg_ratchet_different_states(self):
        """Test that different states produce different outputs."""
        counter = 1
        
        result1 = hash_drbg_ratchet(self.seed, counter)
        result2 = hash_drbg_ratchet(result1, counter)
        
        # Different states should produce different outputs
        self.assertNotEqual(result1, result2)
    
    def test_simulate_quantum_sifting(self):
        """Test quantum sifting simulation."""
        test_bits = bytes.fromhex("0123456789abcdef" * 4)
        sifted = simulate_quantum_sifting(test_bits)
        
        # Should return bytes
        self.assertIsInstance(sifted, bytes)
        
        # For our deterministic implementation, output length matches input
        self.assertEqual(len(sifted), len(test_bits))
    
    def test_xor_fold_hardening(self):
        """Test XOR folding hardening reduces 256 bits to 128 bits."""
        # Test with known pattern
        input_bits = bytes.fromhex("ff" * 32)  # All 1s
        hardened = xor_fold_hardening(input_bits)
        
        # Should produce 128 bits (16 bytes)
        self.assertEqual(len(hardened), 16)
        
        # All 1s XOR All 1s = All 0s
        self.assertEqual(hardened, bytes(16))
        
        # Test with alternating pattern
        first_half = bytes.fromhex("aa" * 16)   # 10101010...
        second_half = bytes.fromhex("55" * 16)  # 01010101...
        input_bits = first_half + second_half
        hardened = xor_fold_hardening(input_bits)
        
        # 10101010 XOR 01010101 = 11111111
        self.assertEqual(hardened, bytes.fromhex("ff" * 16))
    
    def test_generate_key(self):
        """Test single key generation."""
        state = self.seed
        counter = 1
        
        key, next_state = generate_key(state, counter)
        
        # Key should be 128 bits (16 bytes)
        self.assertEqual(len(key), 16)
        
        # Next state should be 256 bits (32 bytes)
        self.assertEqual(len(next_state), 32)
        
        # Next state should be different from input state
        self.assertNotEqual(state, next_state)
    
    def test_generate_key_deterministic(self):
        """Test that key generation is deterministic."""
        state = self.seed
        counter = 1
        
        key1, next_state1 = generate_key(state, counter)
        key2, next_state2 = generate_key(state, counter)
        
        self.assertEqual(key1, key2)
        self.assertEqual(next_state1, next_state2)
    
    def test_generate_test_vectors_count(self):
        """Test that correct number of test vectors are generated."""
        vectors = generate_test_vectors(10)
        self.assertEqual(len(vectors), 10)
        
        vectors = generate_test_vectors(5)
        self.assertEqual(len(vectors), 5)
    
    def test_generate_test_vectors_format(self):
        """Test that test vectors are in correct format."""
        vectors = generate_test_vectors(10)
        
        for vector in vectors:
            # Should be hexadecimal string
            self.assertIsInstance(vector, str)
            
            # Should be 32 characters (16 bytes = 128 bits)
            self.assertEqual(len(vector), 32)
            
            # Should be valid hex
            try:
                bytes.fromhex(vector)
            except ValueError:
                self.fail(f"Vector '{vector}' is not valid hexadecimal")
    
    def test_generate_test_vectors_uniqueness(self):
        """Test that generated test vectors are unique."""
        vectors = generate_test_vectors(10)
        
        # All vectors should be unique
        self.assertEqual(len(vectors), len(set(vectors)))
    
    def test_first_10_test_vectors(self):
        """
        Test that the first 10 test vectors match expected values.
        
        These are the canonical test vectors for GQS-1 compliance.
        Any implementation should produce these exact values.
        """
        expected_vectors = [
            "a01611f01e8207a27c1529c3650c4838",
            "255a98839109b593c97580ce561471d7",
            "f9e3d43664f3192b84d90f58ee584d83",
            "96424e78558928d84ce6caff9c0db6b6",
            "b3cf328d72fabeefea0dd08e03ecf916",
            "f28408d2d0346064dcaba3e12af9be41",
            "2814128f48ec28a58ecb252c061a15f9",
            "12b4c98b607be0fc17d8466b2dc8fa8d",
            "f77e98348d239044998b668b312f70ed",
            "017e9869c72a529f25f8dcf1fa869b98",
        ]
        
        actual_vectors = generate_test_vectors(10)
        
        # Validate each vector matches expected
        for i, (expected, actual) in enumerate(zip(expected_vectors, actual_vectors), 1):
            self.assertEqual(
                actual,
                expected,
                f"Test vector {i} does not match. Expected: {expected}, Got: {actual}"
            )
    
    def test_reproducibility(self):
        """Test that multiple runs produce identical results."""
        vectors1 = generate_test_vectors(10)
        vectors2 = generate_test_vectors(10)
        
        self.assertEqual(vectors1, vectors2)
    
    def test_invalid_seed_raises_error(self):
        """Test that invalid seed checksum raises an error."""
        # Patch the HEX_SEED constant to use an invalid seed
        with patch('qkd.algorithms.gqs1.HEX_SEED', "00" * 32):
            with self.assertRaises(ValueError) as context:
                generate_test_vectors(1)
            
            self.assertIn("checksum verification failed", str(context.exception).lower())


class TestGQS1Integration(unittest.TestCase):
    """Integration tests for complete GQS-1 workflow."""

    def test_complete_workflow(self):
        """Test complete workflow from seed to test vectors."""
        # Initialize seed
        seed = bytes.fromhex(HEX_SEED)

        # Verify checksum
        self.assertTrue(verify_seed_checksum(seed))

        # Generate test vectors
        vectors = generate_test_vectors(10)

        # Verify properties
        self.assertEqual(len(vectors), 10)
        self.assertTrue(all(len(v) == 32 for v in vectors))
        self.assertTrue(all(isinstance(v, str) for v in vectors))

        # Verify uniqueness
        self.assertEqual(len(set(vectors)), 10)


class TestGQS1CLI(unittest.TestCase):
    """Test suite for GQS-1 CLI interface."""

    def run_cli(self, args):
        """Helper method to run CLI and capture output."""
        result = subprocess.run(
            [sys.executable, "qkd/algorithms/gqs1.py"] + args,
            capture_output=True,
            text=True
        )
        return result

    def test_cli_default_execution(self):
        """Test CLI with default parameters (10 vectors)."""
        result = self.run_cli([])
        self.assertEqual(result.returncode, 0)

        # Should have informational output in stderr
        self.assertIn("GQS-1", result.stderr)

        # Should have 10 vectors in stdout
        output_lines = [line for line in result.stdout.strip().split('\n') if line]
        # With headers, should have more than 10 lines
        self.assertGreater(len(output_lines), 10)

    def test_cli_custom_num_keys(self):
        """Test CLI with custom number of keys."""
        result = self.run_cli(["-n", "5"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Generating 5 test vectors", result.stderr)

    def test_cli_quiet_mode(self):
        """Test CLI quiet mode."""
        result = self.run_cli(["-n", "3", "--quiet"])
        self.assertEqual(result.returncode, 0)

        # Stderr should be empty or minimal
        self.assertEqual(result.stderr, "")

        # Should have exactly 3 hex strings in output
        output_lines = [line for line in result.stdout.strip().split('\n') if line]
        self.assertEqual(len(output_lines), 3)

        # Each line should be 32 chars (hex string)
        for line in output_lines:
            self.assertEqual(len(line), 32)

    def test_cli_json_output(self):
        """Test CLI JSON output format."""
        result = self.run_cli(["-n", "5", "--json"])
        self.assertEqual(result.returncode, 0)

        # Parse JSON output
        output_data = json.loads(result.stdout)

        # Verify JSON structure
        self.assertIn("protocol", output_data)
        self.assertEqual(output_data["protocol"], "GQS-1")
        self.assertIn("vectors", output_data)
        self.assertEqual(len(output_data["vectors"]), 5)
        self.assertEqual(output_data["num_vectors"], 5)

    def test_cli_file_output(self):
        """Test CLI file output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            result = self.run_cli(["-n", "3", "-o", temp_file, "--quiet"])
            self.assertEqual(result.returncode, 0)

            # Read output file
            with open(temp_file, 'r') as f:
                content = f.read()

            # Should have 3 vectors
            lines = [line for line in content.strip().split('\n') if line]
            self.assertEqual(len(lines), 3)

            # Each should be valid hex
            for line in lines:
                self.assertEqual(len(line), 32)
                bytes.fromhex(line)  # Should not raise
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_cli_json_file_output(self):
        """Test CLI JSON file output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            result = self.run_cli(["-n", "5", "--json", "-o", temp_file])
            self.assertEqual(result.returncode, 0)

            # Read and parse JSON file
            with open(temp_file, 'r') as f:
                data = json.load(f)

            # Verify JSON content
            self.assertEqual(data["protocol"], "GQS-1")
            self.assertEqual(len(data["vectors"]), 5)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_cli_verify_only(self):
        """Test CLI verify-only mode."""
        result = self.run_cli(["--verify-only"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("verified successfully", result.stderr)

    def test_cli_invalid_num_keys(self):
        """Test CLI with invalid number of keys."""
        result = self.run_cli(["-n", "0"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR", result.stderr)

    def test_cli_help(self):
        """Test CLI help message."""
        result = self.run_cli(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Generate GQS-1 compliant test vectors", result.stdout)
        self.assertIn("Examples:", result.stdout)


if __name__ == "__main__":
    unittest.main()
