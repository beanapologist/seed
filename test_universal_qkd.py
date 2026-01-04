"""
Unit tests for the Universal QKD Key Generator.

Tests validate:
- Seed initialization and checksum verification
- Basis matching simulation
- Sifted bit collection with realistic efficiency
- XOR folding hardening
- Infinite key stream generation
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
import sys
sys.path.insert(0, '/home/runner/work/seed/seed')
from qkd.algorithms.universal_qkd import (
    HEX_SEED,
    EXPECTED_CHECKSUM,
    verify_seed_checksum,
    basis_match,
    collect_sifted_bits,
    xor_fold_hardening,
    universal_qkd_generator,
    generate_keys,
)


class TestUniversalQKD(unittest.TestCase):
    """Test suite for Universal QKD implementation."""

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

    def test_basis_match_functionality(self):
        """Test basis matching function."""
        # Test cases where bits 1 and 2 match
        # byte = 0b00000000 -> bit1=0, bit2=0 -> match
        self.assertTrue(basis_match(0b00000000))

        # byte = 0b00000110 -> bit1=1, bit2=1 -> match
        self.assertTrue(basis_match(0b00000110))

        # Test cases where bits 1 and 2 don't match
        # byte = 0b00000010 -> bit1=1, bit2=0 -> no match
        self.assertFalse(basis_match(0b00000010))

        # byte = 0b00000100 -> bit1=0, bit2=1 -> no match
        self.assertFalse(basis_match(0b00000100))

    def test_collect_sifted_bits_count(self):
        """Test that exactly 256 sifted bits are collected."""
        state = hashlib.sha256(self.seed).digest()
        counter = 0

        sifted_bits, final_state, final_counter = collect_sifted_bits(state, counter)

        # Should have exactly 256 bits
        self.assertEqual(len(sifted_bits), 256)

        # All bits should be 0 or 1
        self.assertTrue(all(bit in (0, 1) for bit in sifted_bits))

        # State should have changed
        self.assertNotEqual(state, final_state)

        # Counter should have incremented
        self.assertGreater(final_counter, counter)

    def test_collect_sifted_bits_deterministic(self):
        """Test that sifted bit collection is deterministic."""
        state = hashlib.sha256(self.seed).digest()
        counter = 0

        sifted1, state1, counter1 = collect_sifted_bits(state, counter)
        sifted2, state2, counter2 = collect_sifted_bits(state, counter)

        # Same input should produce same output
        self.assertEqual(sifted1, sifted2)
        self.assertEqual(state1, state2)
        self.assertEqual(counter1, counter2)

    def test_collect_sifted_bits_efficiency(self):
        """Test that sifting efficiency is realistic."""
        state = hashlib.sha256(self.seed).digest()
        counter = 0

        sifted_bits, final_state, final_counter = collect_sifted_bits(state, counter)

        # Number of hashes used
        num_hashes = final_counter - counter

        # Each hash produces 32 bytes
        total_bytes_examined = num_hashes * 32

        # Basis matching happens ~50% of the time, we extract 1 bit per matched byte
        # So expected efficiency is ~50% * (1/8) = ~6.25% bits per total bits
        # Or ~50% bytes matched, ~1 bit per matched byte = 0.5 bits per byte average
        efficiency = len(sifted_bits) / total_bytes_examined

        # Efficiency should be between 0.3 and 0.7 bits per byte (allowing variance)
        self.assertGreater(efficiency, 0.3)
        self.assertLess(efficiency, 0.7)

    def test_xor_fold_hardening(self):
        """Test XOR folding produces correct 128-bit key."""
        # Test with known pattern - all 1s
        sifted_bits = [1] * 256
        key = xor_fold_hardening(sifted_bits)

        # Should produce 128 bits (16 bytes)
        self.assertEqual(len(key), 16)

        # All 1s XOR All 1s = All 0s
        self.assertEqual(key, bytes(16))

        # Test with alternating halves
        # First 128 bits: all 1s, Second 128 bits: all 0s
        sifted_bits = [1] * 128 + [0] * 128
        key = xor_fold_hardening(sifted_bits)

        # Each bit should be 1 XOR 0 = 1
        self.assertEqual(key, bytes.fromhex("ff" * 16))

        # Test with zeros
        sifted_bits = [0] * 256
        key = xor_fold_hardening(sifted_bits)

        # All 0s XOR All 0s = All 0s
        self.assertEqual(key, bytes(16))

    def test_universal_qkd_generator_basic(self):
        """Test basic key generation."""
        generator = universal_qkd_generator()

        # Generate first key
        key1 = next(generator)

        # Key should be 128 bits (16 bytes)
        self.assertEqual(len(key1), 16)
        self.assertIsInstance(key1, bytes)

        # Generate second key
        key2 = next(generator)

        # Should be different from first key
        self.assertNotEqual(key1, key2)
        self.assertEqual(len(key2), 16)

    def test_universal_qkd_generator_deterministic(self):
        """Test that generator is deterministic."""
        gen1 = universal_qkd_generator()
        gen2 = universal_qkd_generator()

        # First 10 keys should match
        for _ in range(10):
            key1 = next(gen1)
            key2 = next(gen2)
            self.assertEqual(key1, key2)

    def test_first_key_matches_specification(self):
        """
        Test that the first key matches the protocol specification.

        Expected first key: 3c732e0d04dac163a5cc2b15c7caf42c
        """
        expected_first_key = "3c732e0d04dac163a5cc2b15c7caf42c"

        generator = universal_qkd_generator()
        actual_first_key = next(generator).hex()

        self.assertEqual(
            actual_first_key,
            expected_first_key,
            f"First key does not match specification. "
            f"Expected: {expected_first_key}, Got: {actual_first_key}"
        )

    def test_generate_keys_count(self):
        """Test that correct number of keys are generated."""
        keys = generate_keys(10)
        self.assertEqual(len(keys), 10)

        keys = generate_keys(5)
        self.assertEqual(len(keys), 5)

    def test_generate_keys_format(self):
        """Test that generated keys are in correct format."""
        keys = generate_keys(10)

        for key in keys:
            # Should be hexadecimal string
            self.assertIsInstance(key, str)

            # Should be 32 characters (16 bytes = 128 bits)
            self.assertEqual(len(key), 32)

            # Should be valid hex
            try:
                bytes.fromhex(key)
            except ValueError:
                self.fail(f"Key '{key}' is not valid hexadecimal")

    def test_generate_keys_uniqueness(self):
        """Test that generated keys are unique."""
        keys = generate_keys(100)

        # All keys should be unique
        self.assertEqual(len(keys), len(set(keys)))

    def test_first_10_keys_deterministic(self):
        """
        Test that the first 10 keys are deterministic and repeatable.

        The first key is validated against the protocol specification.
        Additional keys serve as reference test vectors for cross-implementation validation.
        """
        expected_first_key = "3c732e0d04dac163a5cc2b15c7caf42c"

        actual_keys = generate_keys(10)

        # Verify first key matches specification
        self.assertEqual(actual_keys[0], expected_first_key)

        # Verify subsequent keys are deterministic
        actual_keys_2 = generate_keys(10)
        self.assertEqual(actual_keys, actual_keys_2)

    def test_reproducibility(self):
        """Test that multiple runs produce identical results."""
        keys1 = generate_keys(10)
        keys2 = generate_keys(10)

        self.assertEqual(keys1, keys2)

    def test_invalid_seed_raises_error(self):
        """Test that invalid seed checksum raises an error."""
        invalid_seed = "00" * 32

        with self.assertRaises(ValueError) as context:
            gen = universal_qkd_generator(invalid_seed)
            next(gen)

        self.assertIn("checksum verification failed", str(context.exception).lower())

    def test_stream_continues_indefinitely(self):
        """Test that generator can produce many keys without error."""
        generator = universal_qkd_generator()

        # Generate 1000 keys to verify stream works
        keys = set()
        for i in range(1000):
            key = next(generator)
            self.assertEqual(len(key), 16)
            keys.add(key.hex())

        # All should be unique
        self.assertEqual(len(keys), 1000)


class TestUniversalQKDCLI(unittest.TestCase):
    """Test suite for Universal QKD CLI interface."""

    def run_cli(self, args):
        """Helper method to run CLI and capture output."""
        result = subprocess.run(
            [sys.executable, "qkd/algorithms/universal_qkd.py"] + args,
            capture_output=True,
            text=True
        )
        return result

    def test_cli_default_execution(self):
        """Test CLI with default parameters (10 keys)."""
        result = self.run_cli([])
        self.assertEqual(result.returncode, 0)

        # Should have informational output in stderr
        self.assertIn("Universal QKD", result.stderr)
        self.assertIn("GCP-1", result.stderr)

        # Should have keys in stdout
        output_lines = [line for line in result.stdout.strip().split('\n') if line]
        self.assertGreater(len(output_lines), 10)

    def test_cli_first_key(self):
        """Test that CLI produces correct first key."""
        result = self.run_cli(["-n", "1", "--quiet"])
        self.assertEqual(result.returncode, 0)

        first_key = result.stdout.strip()
        self.assertEqual(first_key, "3c732e0d04dac163a5cc2b15c7caf42c")

    def test_cli_custom_num_keys(self):
        """Test CLI with custom number of keys."""
        result = self.run_cli(["-n", "5"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Generating 5 keys", result.stderr)

    def test_cli_quiet_mode(self):
        """Test CLI quiet mode."""
        result = self.run_cli(["-n", "3", "--quiet"])
        self.assertEqual(result.returncode, 0)

        # Stderr should be empty
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
        self.assertEqual(output_data["protocol"], "GCP-1")
        self.assertIn("keys", output_data)
        self.assertEqual(len(output_data["keys"]), 5)
        self.assertEqual(output_data["num_keys"], 5)

        # Verify first key
        self.assertEqual(output_data["keys"][0]["hex"], "3c732e0d04dac163a5cc2b15c7caf42c")

    def test_cli_binary_output(self):
        """Test CLI with binary representation."""
        result = self.run_cli(["-n", "1", "--json", "--binary"])
        self.assertEqual(result.returncode, 0)

        output_data = json.loads(result.stdout)
        self.assertIn("binary", output_data["keys"][0])

        # Binary should be 128 bits
        binary_str = output_data["keys"][0]["binary"]
        self.assertEqual(len(binary_str), 128)
        self.assertTrue(all(c in '01' for c in binary_str))

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

            # Should have 3 keys
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
            self.assertEqual(data["protocol"], "GCP-1")
            self.assertEqual(len(data["keys"]), 5)
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
        self.assertIn("Universal QKD Key Generator", result.stdout)
        self.assertIn("GCP-1", result.stdout)
        self.assertIn("Examples:", result.stdout)


if __name__ == "__main__":
    unittest.main()
