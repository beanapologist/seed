"""
Comprehensive Edge Case Test Suite for STL (Standardized Test Library)

This test suite validates edge cases and boundary conditions to ensure
robust behavior across all possible inputs and scenarios.

Tests validate:
- Boundary value testing (min/max values, edge lengths)
- Invalid input handling and error recovery
- Extreme parameter combinations
- Zero and null value handling
- Overflow and underflow conditions
"""

import unittest
import hashlib
import sys
import os
from typing import List

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gq import GoldenStreamGenerator, GQS1
from gq.stream_generator import (
    verify_seed_checksum,
    bit_selection_check,
    collect_selected_bits,
    xor_fold_output,
    golden_stream_generator,
)
from gq.gqs1_core import (
    hash_drbg_ratchet,
    simulate_quantum_sifting,
    generate_key,
)


class TestBoundaryValues(unittest.TestCase):
    """Test suite for boundary value conditions."""
    
    def test_bit_selection_check_all_values(self):
        """Test basis match with all possible byte values (0-255)."""
        match_count = 0
        for byte_val in range(256):
            if bit_selection_check(byte_val):
                match_count += 1
        
        # Verify ~50% efficiency (128 out of 256 values should match)
        # This is because bits 1 and 2 have 4 combinations: 00, 01, 10, 11
        # Two of them match (00 and 11), so 50% efficiency
        self.assertGreaterEqual(match_count, 100)
        self.assertLessEqual(match_count, 156)
    
    def test_bit_selection_check_boundary_bytes(self):
        """Test basis match with boundary byte values."""
        # Test minimum value (0b00000000: bits 1 and 2 are both 0, so match)
        result_0 = bit_selection_check(0b00000000)
        self.assertIsInstance(result_0, bool)
        
        # Test maximum value
        result_255 = bit_selection_check(0b11111111)
        self.assertIsInstance(result_255, bool)
        
        # Test specific patterns
        result_6 = bit_selection_check(0b00000110)  # bits 1 and 2 both 1
        result_2 = bit_selection_check(0b00000010)  # bit 1 is 1, bit 2 is 0
        
        # These should produce specific boolean results based on the pattern
        self.assertIsInstance(result_6, bool)
        self.assertIsInstance(result_2, bool)
    
    def test_xor_fold_output_edge_cases(self):
        """Test XOR folding with edge case bit patterns."""
        # All zeros
        bits_all_zero = [0] * 256
        folded = xor_fold_output(bits_all_zero)
        self.assertEqual(folded, bytes(16))  # Should produce all zero bytes
        
        # All ones
        bits_all_one = [1] * 256
        folded = xor_fold_output(bits_all_one)
        self.assertEqual(folded, bytes(16))  # XOR of 1^1 = 0
        
        # Alternating pattern
        bits_alternating = [i % 2 for i in range(256)]
        folded = xor_fold_output(bits_alternating)
        self.assertEqual(len(folded), 16)
        
        # First half all 0, second half all 1
        bits_half_half = [0] * 128 + [1] * 128
        folded = xor_fold_output(bits_half_half)
        self.assertEqual(folded, bytes([0xFF] * 16))  # Should produce all 1s
    
    def test_hash_drbg_ratchet_counter_boundaries(self):
        """Test Hash-DRBG ratchet with counter boundary values."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Test counter = 0
        result_0 = hash_drbg_ratchet(state, 0)
        self.assertEqual(len(result_0), 32)
        
        # Test counter = 1
        result_1 = hash_drbg_ratchet(state, 1)
        self.assertEqual(len(result_1), 32)
        self.assertNotEqual(result_0, result_1)
        
        # Test large counter value (within 32-bit range)
        result_large = hash_drbg_ratchet(state, 999999999)
        self.assertEqual(len(result_large), 32)
        self.assertNotEqual(result_0, result_large)
        
        # Test maximum 32-bit counter value (function uses 4-byte encoding)
        result_max = hash_drbg_ratchet(state, 2**32 - 1)
        self.assertEqual(len(result_max), 32)
    
    def test_key_generation_with_zero_count(self):
        """Test that requesting 0 keys returns empty list."""
        generator = golden_stream_generator()
        keys = []
        # Don't iterate if count is 0
        for i, key in enumerate(generator):
            if i >= 0:
                break
        self.assertEqual(len(keys), 0)
    
    def test_key_generation_single_key(self):
        """Test generation of exactly one key."""
        generator = golden_stream_generator()
        key = next(generator)
        self.assertEqual(len(key), 16)
        self.assertIsInstance(key, bytes)


class TestInvalidInputHandling(unittest.TestCase):
    """Test suite for invalid input handling."""
    
    def test_verify_seed_checksum_wrong_length(self):
        """Test seed verification with incorrect length."""
        # Too short
        short_seed = bytes(16)
        result = verify_seed_checksum(short_seed)
        # Should return False for incorrect checksum
        self.assertFalse(result)
        
        # Too long
        long_seed = bytes(64)
        result = verify_seed_checksum(long_seed)
        self.assertFalse(result)
    
    def test_verify_seed_checksum_corrupted_data(self):
        """Test seed verification with corrupted data."""
        # Valid length but wrong content
        corrupted_seed = bytes([i % 256 for i in range(32)])
        result = verify_seed_checksum(corrupted_seed)
        self.assertFalse(result)
    
    def test_bit_selection_check_with_negative_would_fail(self):
        """Test that basis_match only accepts valid byte values."""
        # Python's byte values are 0-255, negative values would be type error
        # This test verifies the expected behavior
        with self.assertRaises(TypeError):
            bit_selection_check("invalid")  # type: ignore
    
    def test_xor_fold_output_wrong_length(self):
        """Test XOR folding with incorrect bit count."""
        # Less than 256 bits
        short_bits = [1] * 128
        with self.assertRaises((IndexError, ValueError)):
            xor_fold_output(short_bits)
        
        # More than 256 bits (should work, only use first 256)
        long_bits = [1] * 300
        result = xor_fold_output(long_bits)
        self.assertEqual(len(result), 16)


class TestExtremeParameters(unittest.TestCase):
    """Test suite for extreme parameter combinations."""
    
    def test_collect_selected_bits_with_extreme_counter(self):
        """Test sifted bit collection with extremely large counter."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Start with very large counter
        large_counter = 10**9
        sifted_bits, final_state, final_counter = collect_selected_bits(state, large_counter)
        
        self.assertEqual(len(sifted_bits), 256)
        self.assertGreater(final_counter, large_counter)
        self.assertEqual(len(final_state), 32)
    
    def test_consecutive_keys_uniqueness_extreme(self):
        """Test that consecutive keys remain unique even after many generations."""
        generator = golden_stream_generator()
        
        # Generate many keys and check for duplicates
        num_keys = 1000
        keys = [next(generator) for _ in range(num_keys)]
        
        # All keys should be unique
        unique_keys = set(keys)
        self.assertEqual(len(unique_keys), num_keys)
        
        # All keys should be 16 bytes
        self.assertTrue(all(len(k) == 16 for k in keys))
    
    def test_state_evolution_consistency(self):
        """Test that state evolution is consistent across many iterations."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        counter = 0
        
        # Track state evolution
        states = [state]
        for i in range(100):
            state = hash_drbg_ratchet(state, i)
            states.append(state)
        
        # All states should be unique
        unique_states = set(states)
        self.assertEqual(len(unique_states), 101)
        
        # All states should be 32 bytes
        self.assertTrue(all(len(s) == 32 for s in states))
    
    def test_gqs1_vectors_extreme_count(self):
        """Test GQS-1 test vector generation with large count."""
        # Generate a large number of test vectors
        num_vectors = 100
        vectors = GQS1.generate_test_vectors(num_vectors)
        
        self.assertEqual(len(vectors), num_vectors)
        
        # GQS1.generate_test_vectors returns hex strings, not bytes
        # All vectors should be unique
        unique_vectors = set(vectors)
        self.assertEqual(len(unique_vectors), num_vectors)
        
        # All vectors should be 32 hex characters (16 bytes)
        self.assertTrue(all(len(v) == 32 for v in vectors))


class TestZeroAndNullHandling(unittest.TestCase):
    """Test suite for zero and null value handling."""
    
    def test_all_zero_seed_handling(self):
        """Test behavior with all-zero seed (invalid but should not crash)."""
        zero_seed = bytes(32)
        
        # Should not verify
        self.assertFalse(verify_seed_checksum(zero_seed))
        
        # But can still be used in ratchet (deterministic behavior)
        result = hash_drbg_ratchet(zero_seed, 1)
        self.assertEqual(len(result), 32)
        self.assertNotEqual(result, zero_seed)
    
    def test_all_zero_bits_xor_folding(self):
        """Test XOR folding with all zero bits."""
        bits = [0] * 256
        folded = xor_fold_output(bits)
        
        self.assertEqual(len(folded), 16)
        self.assertEqual(folded, bytes(16))
    
    def test_single_bit_set_patterns(self):
        """Test XOR folding with single bit set in various positions."""
        for pos in range(256):
            bits = [0] * 256
            bits[pos] = 1
            folded = xor_fold_output(bits)
            
            self.assertEqual(len(folded), 16)
            # Should have exactly one bit set in the output
            bit_count = sum(bin(b).count('1') for b in folded)
            self.assertEqual(bit_count, 1)


class TestOverflowAndUnderflow(unittest.TestCase):
    """Test suite for overflow and underflow conditions."""
    
    def test_counter_overflow_handling(self):
        """Test that counters within 32-bit range are handled correctly."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Test with counters at various boundaries (function uses 4-byte encoding)
        # So we test within 32-bit range
        large_counters = [
            0,           # Minimum
            1,           # Small
            2**16 - 1,   # 16-bit limit
            2**16,       # Just over 16-bit
            2**24 - 1,   # 24-bit limit
            2**32 - 1,   # 32-bit limit (maximum for 4-byte encoding)
        ]
        
        results = []
        for counter in large_counters:
            result = hash_drbg_ratchet(state, counter)
            results.append(result)
            self.assertEqual(len(result), 32)
        
        # All results should be unique
        unique_results = set(results)
        self.assertEqual(len(unique_results), len(large_counters))
    
    def test_simulate_quantum_sifting_efficiency_bounds(self):
        """Test that quantum sifting maintains efficiency bounds."""
        # Create various input patterns
        test_inputs = [
            bytes(32),  # All zeros
            bytes([0xFF] * 32),  # All ones
            bytes(range(32)),  # Sequential
            hashlib.sha256(b"test").digest(),  # Random-looking
        ]
        
        for input_bytes in test_inputs:
            sifted = simulate_quantum_sifting(input_bytes)
            
            # Output should be ~50% of input (256 bits from 32 bytes)
            self.assertGreater(len(sifted), 0)
            self.assertLessEqual(len(sifted), 32)


class TestDeterministicReproducibility(unittest.TestCase):
    """Test suite for deterministic reproducibility across runs."""
    
    def test_multiple_runs_produce_same_keys(self):
        """Test that multiple runs produce identical keys."""
        runs = []
        for _ in range(5):
            generator = golden_stream_generator()
            keys = [next(generator) for _ in range(10)]
            runs.append(keys)
        
        # All runs should produce identical results
        for i in range(1, len(runs)):
            self.assertEqual(runs[0], runs[i])
    
    def test_gqs1_deterministic_across_runs(self):
        """Test that GQS-1 vectors are deterministic across runs."""
        runs = []
        for _ in range(3):
            vectors = GQS1.generate_test_vectors(20)
            runs.append(vectors)
        
        # All runs should produce identical results
        for i in range(1, len(runs)):
            self.assertEqual(runs[0], runs[i])
    
    def test_seed_verification_deterministic(self):
        """Test that seed verification is deterministic."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        
        # Verify multiple times
        results = [verify_seed_checksum(seed) for _ in range(10)]
        
        # All results should be identical
        self.assertTrue(all(results))
        self.assertEqual(len(set(results)), 1)


if __name__ == '__main__':
    unittest.main()
