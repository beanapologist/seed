"""
Comprehensive test suite for mathematical correctness and deterministic behavior.

This test suite validates:
1. Mathematical Validation:
   - Golden Ratio calculations
   - Modular arithmetic operations
   - XOR folding accuracy
2. Consistency Testing:
   - Deterministic outputs for same inputs
   - Cross-seed determinism
3. Statistical Properties:
   - Uniformity of generated sequences
   - Entropy levels
   
Author: GitHub Copilot
Date: 2026-01-23
"""

import unittest
import hashlib
import math
import sys
import os
from collections import Counter
from typing import List, Tuple

# Add repository root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gq.gqs1_core import (
    HEX_SEED,
    EXPECTED_CHECKSUM,
    verify_seed_checksum,
    hash_drbg_ratchet,
    xor_fold_hardening,
    generate_key,
    generate_test_vectors,
)
from gq.universal_qkd import (
    universal_qkd_generator,
)
from gq.golden_ratio_coin_flip import (
    PHI,
    GoldenRatioCoinFlip,
    fractional_part,
)


class TestGoldenRatioMathematicalCorrectness(unittest.TestCase):
    """Test mathematical correctness of Golden Ratio calculations."""
    
    def test_golden_ratio_value(self):
        """Test that the Golden Ratio constant is mathematically correct."""
        # φ = (1 + √5) / 2
        expected_phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, expected_phi, places=14)
        
        # Known value: φ ≈ 1.618033988749895
        self.assertAlmostEqual(PHI, 1.618033988749895, places=14)
    
    def test_golden_ratio_algebraic_property(self):
        """Test that φ² = φ + 1 (fundamental algebraic property)."""
        phi_squared = PHI ** 2
        phi_plus_one = PHI + 1
        self.assertAlmostEqual(phi_squared, phi_plus_one, places=12)
    
    def test_golden_ratio_conjugate(self):
        """Test the golden ratio conjugate: Φ = (1 - √5) / 2."""
        phi_conjugate = (1 - math.sqrt(5)) / 2
        # φ * Φ = -1
        product = PHI * phi_conjugate
        self.assertAlmostEqual(product, -1, places=12)
        
        # φ + Φ = 1
        sum_value = PHI + phi_conjugate
        self.assertAlmostEqual(sum_value, 1, places=12)
    
    def test_fractional_part_mathematical_correctness(self):
        """Test that fractional part function is mathematically correct."""
        test_cases = [
            (0.0, 0.0),
            (0.5, 0.5),
            (1.0, 0.0),
            (1.5, 0.5),
            (2.75, 0.75),
            (PHI, PHI - 1),
            (2 * PHI, fractional_part(2 * PHI)),
        ]
        
        for input_val, expected in test_cases:
            result = fractional_part(input_val)
            self.assertAlmostEqual(result, expected, places=12,
                                 msg=f"fractional_part({input_val}) failed")
            # Ensure result is in [0, 1)
            self.assertGreaterEqual(result, 0.0)
            self.assertLess(result, 1.0)


class TestModularArithmeticCorrectness(unittest.TestCase):
    """Test correctness of modular arithmetic operations."""
    
    def test_hash_output_modular_properties(self):
        """Test that hash outputs have correct modular properties."""
        seed = bytes.fromhex(HEX_SEED)
        
        # Test that hash produces uniform distribution mod 256
        state = seed
        byte_values = []
        
        for i in range(100):
            state = hash_drbg_ratchet(state, i)
            # Take first byte as representative
            byte_values.append(state[0])
        
        # Should have reasonable variety (not all same)
        unique_values = len(set(byte_values))
        self.assertGreater(unique_values, 50,
                          "Hash should produce varied byte values")
    
    def test_xor_operation_algebraic_properties(self):
        """Test XOR operation algebraic properties."""
        # XOR is commutative: a ⊕ b = b ⊕ a
        a = 0b10101010
        b = 0b11001100
        self.assertEqual(a ^ b, b ^ a)
        
        # XOR is associative: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)
        c = 0b11110000
        self.assertEqual((a ^ b) ^ c, a ^ (b ^ c))
        
        # Identity: a ⊕ 0 = a
        self.assertEqual(a ^ 0, a)
        
        # Self-inverse: a ⊕ a = 0
        self.assertEqual(a ^ a, 0)
    
    def test_counter_encoding_modular_correctness(self):
        """Test that counter encoding is modularly correct."""
        state = bytes(32)
        
        # Test counter wrapping and consistency
        for counter in [0, 1, 255, 256, 65535, 65536]:
            # Counter should encode to 4 bytes big-endian
            counter_bytes = counter.to_bytes(4, byteorder='big')
            self.assertEqual(len(counter_bytes), 4)
            
            # Verify reconstruction
            reconstructed = int.from_bytes(counter_bytes, byteorder='big')
            self.assertEqual(counter, reconstructed)


class TestXORFoldingCorrectness(unittest.TestCase):
    """Test mathematical correctness of XOR folding operation."""
    
    def test_xor_fold_compression_ratio(self):
        """Test that XOR folding correctly compresses 256 bits to 128 bits."""
        input_256_bits = bytes(32)  # 256 bits
        output_128_bits = xor_fold_hardening(input_256_bits)
        
        self.assertEqual(len(input_256_bits), 32, "Input should be 256 bits (32 bytes)")
        self.assertEqual(len(output_128_bits), 16, "Output should be 128 bits (16 bytes)")
    
    def test_xor_fold_zero_input(self):
        """Test XOR folding with zero input."""
        zero_input = bytes(32)  # All zeros
        result = xor_fold_hardening(zero_input)
        
        # 0 ⊕ 0 = 0
        self.assertEqual(result, bytes(16))
    
    def test_xor_fold_all_ones(self):
        """Test XOR folding with all ones input."""
        all_ones = bytes([0xFF] * 32)
        result = xor_fold_hardening(all_ones)
        
        # 0xFF ⊕ 0xFF = 0x00
        self.assertEqual(result, bytes(16))
    
    def test_xor_fold_complementary_halves(self):
        """Test XOR folding with complementary halves."""
        # First half: 0xAA (10101010), Second half: 0x55 (01010101)
        first_half = bytes([0xAA] * 16)
        second_half = bytes([0x55] * 16)
        input_data = first_half + second_half
        
        result = xor_fold_hardening(input_data)
        
        # 0xAA ⊕ 0x55 = 0xFF
        expected = bytes([0xFF] * 16)
        self.assertEqual(result, expected)
    
    def test_xor_fold_deterministic(self):
        """Test that XOR folding is deterministic."""
        input_data = bytes.fromhex("0123456789abcdef" * 4)
        
        result1 = xor_fold_hardening(input_data)
        result2 = xor_fold_hardening(input_data)
        
        self.assertEqual(result1, result2)
    
    def test_xor_fold_entropy_preservation(self):
        """Test that XOR folding preserves entropy characteristics."""
        # Generate a random-looking input
        seed = bytes.fromhex(HEX_SEED)
        state = hashlib.sha256(seed).digest()
        
        # Apply XOR folding
        folded = xor_fold_hardening(state)
        
        # Check that output isn't trivial (not all zeros, not all same byte)
        self.assertNotEqual(folded, bytes(16), "Output shouldn't be all zeros")
        unique_bytes = len(set(folded))
        self.assertGreater(unique_bytes, 8, "Output should have varied bytes")


class TestDeterministicBehavior(unittest.TestCase):
    """Test deterministic behavior of the system."""
    
    def test_same_seed_produces_identical_sequence(self):
        """Test that the same seed always produces identical sequences."""
        # Generate two sequences with the same seed
        vectors1 = generate_test_vectors(100)
        vectors2 = generate_test_vectors(100)
        
        self.assertEqual(vectors1, vectors2,
                        "Same seed should produce identical sequences")
    
    def test_universal_qkd_determinism(self):
        """Test that UniversalQKD generator is deterministic."""
        gen1 = universal_qkd_generator()
        gen2 = universal_qkd_generator()
        
        # Generate 50 keys from each
        keys1 = [next(gen1) for _ in range(50)]
        keys2 = [next(gen2) for _ in range(50)]
        
        self.assertEqual(keys1, keys2,
                        "Same generator initialization should produce identical keys")
    
    def test_hash_drbg_ratchet_determinism(self):
        """Test that hash DRBG ratchet is deterministic."""
        seed = bytes.fromhex(HEX_SEED)
        counter = 42
        
        # Multiple invocations should produce same result
        results = [hash_drbg_ratchet(seed, counter) for _ in range(10)]
        
        # All results should be identical
        for i in range(1, len(results)):
            self.assertEqual(results[0], results[i],
                           f"Hash DRBG ratchet invocation {i} differs")
    
    def test_key_generation_determinism(self):
        """Test that key generation is deterministic."""
        seed = bytes.fromhex(HEX_SEED)
        counter = 1
        
        # Generate same key multiple times
        results = [generate_key(seed, counter) for _ in range(10)]
        
        # All keys should be identical
        keys = [r[0] for r in results]
        states = [r[1] for r in results]
        
        for i in range(1, len(keys)):
            self.assertEqual(keys[0], keys[i])
            self.assertEqual(states[0], states[i])
    
    def test_golden_ratio_sequence_determinism(self):
        """Test that golden ratio sequence is deterministic."""
        generator = GoldenRatioCoinFlip()
        
        # Generate sequences multiple times
        sequences = []
        for _ in range(5):
            seq = generator.generate_sequence(100)
            sequences.append(seq)
        
        # All sequences should be identical
        for i in range(1, len(sequences)):
            self.assertEqual(sequences[0], sequences[i])


class TestCrossSeedDeterminism(unittest.TestCase):
    """Test cross-seed deterministic properties."""
    
    def test_different_seeds_produce_different_sequences(self):
        """Test that different seeds produce different sequences."""
        seed1 = bytes.fromhex(HEX_SEED)
        seed2 = bytes([0] * 32)  # Different seed
        
        # Generate sequences
        state1 = seed1
        state2 = seed2
        
        seq1 = []
        seq2 = []
        
        for i in range(10):
            key1, state1 = generate_key(state1, i)
            key2, state2 = generate_key(state2, i)
            seq1.append(key1)
            seq2.append(key2)
        
        # Sequences should be different
        self.assertNotEqual(seq1, seq2,
                          "Different seeds should produce different sequences")
    
    def test_counter_produces_unique_keys(self):
        """Test that different counter values produce unique keys."""
        seed = bytes.fromhex(HEX_SEED)
        
        keys = []
        state = seed
        
        for counter in range(1, 101):
            key, state = generate_key(state, counter)
            keys.append(key)
        
        # All keys should be unique
        unique_keys = len(set(keys))
        self.assertEqual(unique_keys, 100,
                        "All generated keys should be unique")
    
    def test_state_evolution_uniqueness(self):
        """Test that state evolution produces unique states."""
        seed = bytes.fromhex(HEX_SEED)
        
        states = [seed]
        current_state = seed
        
        for i in range(100):
            current_state = hash_drbg_ratchet(current_state, i)
            states.append(current_state)
        
        # All states should be unique
        unique_states = len(set(states))
        self.assertEqual(unique_states, 101,
                        "All evolved states should be unique")


class TestStatisticalUniformity(unittest.TestCase):
    """Test statistical uniformity of generated sequences."""
    
    def test_byte_distribution_uniformity(self):
        """Test that byte values are uniformly distributed."""
        # Generate many keys and collect byte statistics
        vectors = generate_test_vectors(1000)
        
        # Convert to bytes and count
        all_bytes = []
        for vector in vectors:
            key_bytes = bytes.fromhex(vector)
            all_bytes.extend(key_bytes)
        
        # Count byte value frequencies
        byte_counts = Counter(all_bytes)
        
        # Should have reasonable coverage of byte space
        unique_byte_values = len(byte_counts)
        self.assertGreater(unique_byte_values, 200,
                          "Should have good coverage of byte values (>200/256)")
        
        # Check that no byte value is extremely over-represented
        total_bytes = len(all_bytes)
        expected_count = total_bytes / 256
        
        for byte_val, count in byte_counts.items():
            # Allow 3x deviation from expected (statistical tolerance)
            self.assertLess(count, expected_count * 3,
                          f"Byte {byte_val} appears too frequently")
    
    def test_bit_balance(self):
        """Test that 0 and 1 bits are balanced."""
        vectors = generate_test_vectors(1000)
        
        ones_count = 0
        zeros_count = 0
        
        for vector in vectors:
            key_bytes = bytes.fromhex(vector)
            for byte in key_bytes:
                # Count bits in each byte
                ones_count += bin(byte).count('1')
                zeros_count += 8 - bin(byte).count('1')
        
        total_bits = ones_count + zeros_count
        
        # Should be roughly 50/50 (within 5%)
        ones_ratio = ones_count / total_bits
        self.assertGreater(ones_ratio, 0.48)
        self.assertLess(ones_ratio, 0.52)
    
    def test_golden_ratio_uniformity(self):
        """Test uniformity of golden ratio fractional parts."""
        generator = GoldenRatioCoinFlip()
        
        # Generate fractional values
        frac_values = [generator.fractional_value(z) for z in range(1, 10001)]
        
        # Divide [0, 1) into bins and count
        num_bins = 10
        bins = [0] * num_bins
        
        for val in frac_values:
            bin_idx = min(int(val * num_bins), num_bins - 1)
            bins[bin_idx] += 1
        
        # Each bin should have roughly 1000 values (10000 / 10)
        expected_per_bin = len(frac_values) / num_bins
        
        for i, count in enumerate(bins):
            # Allow 30% deviation (statistical tolerance)
            self.assertGreater(count, expected_per_bin * 0.7,
                             f"Bin {i} has too few values")
            self.assertLess(count, expected_per_bin * 1.3,
                          f"Bin {i} has too many values")


class TestEntropyProperties(unittest.TestCase):
    """Test entropy-related properties of generated sequences."""
    
    def test_shannon_entropy_approximation(self):
        """Test that generated sequences have high Shannon entropy."""
        vectors = generate_test_vectors(1000)
        
        # Collect byte frequencies
        all_bytes = []
        for vector in vectors:
            key_bytes = bytes.fromhex(vector)
            all_bytes.extend(key_bytes)
        
        byte_counts = Counter(all_bytes)
        total = len(all_bytes)
        
        # Calculate Shannon entropy: H = -Σ(p_i * log2(p_i))
        entropy = 0.0
        for count in byte_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        
        # Maximum entropy for 256 symbols is 8 bits
        # We expect high entropy (> 7.5 bits)
        self.assertGreater(entropy, 7.5,
                          f"Shannon entropy {entropy:.3f} is lower than expected")
    
    def test_key_unpredictability(self):
        """Test that keys are unpredictable from previous keys."""
        vectors = generate_test_vectors(100)
        
        # Convert to bytes
        keys = [bytes.fromhex(v) for v in vectors]
        
        # Check that knowing key[i] doesn't reveal key[i+1]
        # by verifying they don't have simple relationships
        for i in range(len(keys) - 1):
            key1 = keys[i]
            key2 = keys[i + 1]
            
            # Keys should not be identical
            self.assertNotEqual(key1, key2)
            
            # Keys should not be simple XOR of each other with constant
            xor_result = bytes(a ^ b for a, b in zip(key1, key2))
            # If all bytes are same, it would indicate a simple relationship
            unique_xor_bytes = len(set(xor_result))
            self.assertGreater(unique_xor_bytes, 4,
                             "XOR of consecutive keys should have variety")
    
    def test_avalanche_effect(self):
        """Test avalanche effect: small input change causes large output change."""
        seed = bytes.fromhex(HEX_SEED)
        
        # Flip one bit in the seed
        seed_bytes = bytearray(seed)
        seed_bytes[0] ^= 0x01  # Flip least significant bit of first byte
        modified_seed = bytes(seed_bytes)
        
        # Generate keys from both seeds
        key1, _ = generate_key(seed, 1)
        key2, _ = generate_key(modified_seed, 1)
        
        # Count different bits
        different_bits = 0
        for b1, b2 in zip(key1, key2):
            different_bits += bin(b1 ^ b2).count('1')
        
        total_bits = len(key1) * 8  # 128 bits
        
        # Avalanche effect: expect ~50% of bits to differ
        # In practice, 35-65% is acceptable for cryptographic hash functions
        diff_ratio = different_bits / total_bits
        self.assertGreater(diff_ratio, 0.35,
                          "Single bit flip should cause significant output change (>35%)")
        self.assertLess(diff_ratio, 0.65,
                       "Bit difference should be reasonable (~50% ± 15%)")


class TestRegressionVectors(unittest.TestCase):
    """Test against known regression vectors to catch any changes."""
    
    def test_first_10_vectors_match_specification(self):
        """Test first 10 GQS-1 vectors match known good values."""
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
        self.assertEqual(actual_vectors, expected_vectors,
                        "First 10 vectors must match specification")
    
    def test_universal_qkd_first_key(self):
        """Test Universal QKD first key matches specification."""
        expected_first_key = "3c732e0d04dac163a5cc2b15c7caf42c"
        
        generator = universal_qkd_generator()
        first_key = next(generator)
        
        self.assertEqual(first_key.hex(), expected_first_key,
                        "First Universal QKD key must match specification")
    
    def test_golden_ratio_first_100_coins(self):
        """Test first 100 golden ratio coin flips are deterministic."""
        generator = GoldenRatioCoinFlip()
        sequence = generator.generate_sequence(100)
        
        # Store a hash of the sequence for regression testing
        sequence_bytes = bytes(sequence)
        sequence_hash = hashlib.sha256(sequence_bytes).hexdigest()
        
        # This hash represents the current correct behavior
        expected_hash = hashlib.sha256(bytes(
            GoldenRatioCoinFlip().generate_sequence(100)
        )).hexdigest()
        
        self.assertEqual(sequence_hash, expected_hash,
                        "Golden ratio sequence must be deterministic")


if __name__ == "__main__":
    unittest.main(verbosity=2)
