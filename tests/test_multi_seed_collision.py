"""
Multi-Seed Collision Test Suite for STL (Standardized Test Library)

This test suite validates collision resistance and uniqueness guarantees
across multiple seeds, different initialization parameters, and diverse
entropy sources.

Tests validate:
- Collision detection across different seeds
- Uniqueness guarantees within and across seed spaces
- Seed diversity and entropy distribution
- Avalanche effects from seed variations
- Statistical properties of key distributions
"""

import unittest
import hashlib
import math
import sys
import os
from typing import List, Set, Dict
from collections import Counter

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gq import UniversalQKD, GQS1
from gq.universal_qkd import (
    universal_qkd_generator,
    collect_sifted_bits,
)
from gq.gqs1_core import (
    hash_drbg_ratchet,
    generate_test_vectors,
)


class TestSeedCollisionResistance(unittest.TestCase):
    """Test suite for collision resistance across different seeds."""
    
    def test_no_collisions_within_single_seed_stream(self):
        """Test that a single seed stream produces no collisions."""
        generator = universal_qkd_generator()
        
        # Generate large number of keys
        num_keys = 100000
        keys = set()
        
        for i in range(num_keys):
            key = next(generator)
            
            # Check for collision
            self.assertNotIn(key, keys, f"Collision detected at key {i}")
            keys.add(key)
        
        # Verify all unique
        self.assertEqual(len(keys), num_keys)
        print(f"\nGenerated {num_keys:,} unique keys with no collisions")
    
    def test_different_seeds_produce_different_sequences(self):
        """Test that different seeds produce different key sequences."""
        # Create multiple generators (all use same golden seed by design)
        # But test that state variations produce different outputs
        
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        
        # Generate keys starting from different state variations
        sequences = []
        for variation in range(10):
            # Vary the initial state by hashing with different context
            varied_seed = hashlib.sha256(seed + bytes([variation])).digest()
            state = hashlib.sha256(varied_seed).digest()
            counter = 0
            
            # Generate sequence
            keys = []
            for i in range(100):
                sifted, state, counter = collect_sifted_bits(state, counter)
                from gq.universal_qkd import xor_fold_hardening
                key = xor_fold_hardening(sifted)
                keys.append(key)
            
            sequences.append(keys)
        
        # All sequences should be different
        for i in range(len(sequences)):
            for j in range(i + 1, len(sequences)):
                # Sequences should differ
                self.assertNotEqual(sequences[i], sequences[j],
                                  f"Sequences {i} and {j} are identical")
                
                # But should have some differences even in first key
                self.assertNotEqual(sequences[i][0], sequences[j][0])
    
    def test_avalanche_effect_on_seed_variation(self):
        """Test that small seed variations produce large output differences."""
        base_seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        
        # Generate keys from base seed
        base_state = hashlib.sha256(base_seed).digest()
        base_result = hash_drbg_ratchet(base_state, 1)
        
        # Flip each bit of the seed and measure output difference
        bit_differences = []
        
        for byte_idx in range(min(8, len(base_seed))):  # Test first 8 bytes
            for bit_idx in range(8):
                # Create seed with single bit flipped
                modified_seed = bytearray(base_seed)
                modified_seed[byte_idx] ^= (1 << bit_idx)
                modified_seed = bytes(modified_seed)
                
                # Generate output
                modified_state = hashlib.sha256(modified_seed).digest()
                modified_result = hash_drbg_ratchet(modified_state, 1)
                
                # Count different bits
                diff_bits = sum(bin(a ^ b).count('1') 
                              for a, b in zip(base_result, modified_result))
                bit_differences.append(diff_bits)
        
        # Average bit difference should be close to 50% (128 bits out of 256)
        avg_diff = sum(bit_differences) / len(bit_differences)
        
        # Should have significant avalanche (at least 25% different, ideally ~50%)
        self.assertGreater(avg_diff, 64, 
                          f"Insufficient avalanche: only {avg_diff:.1f} bits different")
        
        print(f"\nAvalanche effect: {avg_diff:.1f} bits different on average (out of 256)")
    
    def test_counter_variation_produces_unique_outputs(self):
        """Test that different counter values produce unique outputs."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Generate outputs for many counter values
        outputs = {}
        for counter in range(1000):
            result = hash_drbg_ratchet(state, counter)
            
            # Check for collision
            self.assertNotIn(result, outputs.values(),
                            f"Collision at counter {counter}")
            outputs[counter] = result
        
        # All outputs should be unique
        unique_outputs = set(outputs.values())
        self.assertEqual(len(unique_outputs), 1000)


class TestUniquenessGuarantees(unittest.TestCase):
    """Test suite for uniqueness guarantees."""
    
    def test_uniqueness_across_key_positions(self):
        """Test that keys at different positions in stream are unique."""
        generator = universal_qkd_generator()
        
        # Sample keys at various positions
        sampled_positions = [0, 100, 1000, 10000, 50000]
        sampled_keys = []
        
        current_pos = 0
        for target_pos in sampled_positions:
            # Advance to target position
            while current_pos < target_pos:
                next(generator)
                current_pos += 1
            
            # Sample key at this position
            key = next(generator)
            current_pos += 1
            sampled_keys.append(key)
        
        # All sampled keys should be unique
        unique_keys = set(sampled_keys)
        self.assertEqual(len(unique_keys), len(sampled_positions))
    
    def test_uniqueness_with_parallel_generation(self):
        """Test uniqueness when generating keys in parallel conceptually."""
        # Note: actual parallelism not needed since generator is deterministic
        # This tests that the same sequence is always generated
        
        # Create multiple "parallel" generators
        generators = [universal_qkd_generator() for _ in range(5)]
        
        # Generate keys from each
        all_keys = []
        for gen_idx, gen in enumerate(generators):
            keys = [next(gen) for _ in range(100)]
            
            # Each generator should produce the same sequence
            if gen_idx == 0:
                reference_keys = keys
            else:
                self.assertEqual(keys, reference_keys,
                               f"Generator {gen_idx} produced different sequence")
            
            all_keys.extend(keys)
        
        # Within each generator, keys should be unique
        self.assertEqual(len(set(reference_keys)), 100)
    
    def test_gqs1_vector_uniqueness(self):
        """Test that GQS-1 test vectors are unique."""
        num_vectors = 10000
        vectors = generate_test_vectors(num_vectors)
        
        # All vectors should be unique (vectors are already hex strings)
        unique_vectors = set(vectors)
        self.assertEqual(len(unique_vectors), num_vectors)
        
        print(f"\nGenerated {num_vectors:,} unique GQS-1 test vectors")
    
    def test_no_duplicate_states_in_evolution(self):
        """Test that state evolution never produces duplicate states."""
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Track state evolution
        seen_states = {state}
        
        for i in range(10000):
            state = hash_drbg_ratchet(state, i)
            
            # Check for cycle
            self.assertNotIn(state, seen_states,
                            f"State cycle detected at iteration {i}")
            seen_states.add(state)
        
        print(f"\nNo state cycles detected in 10,000 iterations")


class TestSeedDiversityAnalysis(unittest.TestCase):
    """Test suite for seed diversity and entropy distribution."""
    
    def test_bit_distribution_uniformity(self):
        """Test that generated keys have uniform bit distribution."""
        generator = universal_qkd_generator()
        
        # Generate many keys and count bit frequencies
        num_keys = 1000
        bit_counts = [0] * 128  # 128 bits per key
        
        for _ in range(num_keys):
            key = next(generator)
            
            # Count bits in each position
            for byte_idx, byte_val in enumerate(key):
                for bit_idx in range(8):
                    bit_pos = byte_idx * 8 + bit_idx
                    if byte_val & (1 << bit_idx):
                        bit_counts[bit_pos] += 1
        
        # Each bit position should be roughly 50% ones
        for bit_pos, count in enumerate(bit_counts):
            proportion = count / num_keys
            
            # Allow 10% deviation from 50%
            self.assertGreater(proportion, 0.40,
                             f"Bit {bit_pos} too few ones: {proportion:.3f}")
            self.assertLess(proportion, 0.60,
                          f"Bit {bit_pos} too many ones: {proportion:.3f}")
    
    def test_byte_value_distribution(self):
        """Test that byte values are well-distributed."""
        generator = universal_qkd_generator()
        
        # Generate keys and collect all byte values
        num_keys = 1000
        byte_values = []
        
        for _ in range(num_keys):
            key = next(generator)
            byte_values.extend(key)
        
        # Count frequency of each byte value (0-255)
        byte_counts = Counter(byte_values)
        
        # Should see a reasonable distribution
        # With 16,000 bytes, each value should appear ~62 times on average
        expected_per_value = len(byte_values) / 256
        
        # Check that we have a good spread
        num_unique_values = len(byte_counts)
        self.assertGreater(num_unique_values, 200,
                          f"Only {num_unique_values} unique byte values seen")
        
        # Check that no value is extremely over-represented
        max_count = max(byte_counts.values())
        max_ratio = max_count / expected_per_value
        self.assertLess(max_ratio, 3.0,
                       f"Byte value over-represented by {max_ratio:.1f}x")
        
        print(f"\nByte value distribution: {num_unique_values} unique values, "
              f"max frequency {max_ratio:.2f}x expected")
    
    def test_hamming_distance_distribution(self):
        """Test distribution of Hamming distances between consecutive keys."""
        generator = universal_qkd_generator()
        
        # Generate consecutive keys and measure Hamming distances
        num_pairs = 1000
        hamming_distances = []
        
        prev_key = next(generator)
        for _ in range(num_pairs):
            curr_key = next(generator)
            
            # Calculate Hamming distance
            distance = sum(bin(a ^ b).count('1') 
                          for a, b in zip(prev_key, curr_key))
            hamming_distances.append(distance)
            
            prev_key = curr_key
        
        # Average Hamming distance should be around 64 (50% of 128 bits)
        avg_distance = sum(hamming_distances) / len(hamming_distances)
        
        # Should be roughly 50% with reasonable variance
        self.assertGreater(avg_distance, 55,
                          f"Average Hamming distance too low: {avg_distance:.1f}")
        self.assertLess(avg_distance, 73,
                       f"Average Hamming distance too high: {avg_distance:.1f}")
        
        print(f"\nAverage Hamming distance: {avg_distance:.1f} bits (out of 128)")
    
    def test_entropy_quality_across_stream(self):
        """Test that entropy quality remains high throughout key stream."""
        generator = universal_qkd_generator()
        
        # Sample keys at different positions and measure entropy
        sample_positions = [0, 1000, 10000, 50000]
        entropy_samples = []
        
        current_pos = 0
        for target_pos in sample_positions:
            # Advance to target position
            while current_pos < target_pos:
                next(generator)
                current_pos += 1
            
            # Generate sample of keys and measure entropy
            sample_keys = [next(generator) for _ in range(100)]
            current_pos += 100
            
            # Calculate Shannon entropy of concatenated bytes
            all_bytes = b''.join(sample_keys)
            byte_counts = Counter(all_bytes)
            total_bytes = len(all_bytes)
            
            # Calculate Shannon entropy in bits
            entropy_bits = 0.0
            for count in byte_counts.values():
                if count > 0:  # Only calculate for non-zero probabilities
                    p = count / total_bytes
                    entropy_bits -= p * math.log2(p)
            
            entropy_samples.append(entropy_bits)
        
        # All samples should have high entropy (> 7.0 bits per byte, max is 8)
        for pos, entropy in zip(sample_positions, entropy_samples):
            self.assertGreater(entropy, 7.0,
                             f"Low entropy at position {pos}: {entropy:.3f}")
        
        print(f"\nEntropy samples: {[f'{e:.3f}' for e in entropy_samples]} bits/byte")


class TestStatisticalProperties(unittest.TestCase):
    """Test suite for statistical properties of key distributions."""
    
    def test_runs_test(self):
        """Test runs of consecutive bits (should not have long runs)."""
        generator = universal_qkd_generator()
        
        # Generate keys and concatenate bits
        num_keys = 100
        all_bits = []
        
        for _ in range(num_keys):
            key = next(generator)
            for byte_val in key:
                for bit_idx in range(8):
                    all_bits.append((byte_val >> bit_idx) & 1)
        
        # Count runs (sequences of same bit)
        runs = []
        current_run_length = 1
        current_bit = all_bits[0]
        
        for bit in all_bits[1:]:
            if bit == current_bit:
                current_run_length += 1
            else:
                runs.append(current_run_length)
                current_run_length = 1
                current_bit = bit
        runs.append(current_run_length)
        
        # Should not have very long runs (more than 10-12 bits)
        max_run = max(runs)
        self.assertLess(max_run, 20,
                       f"Unexpectedly long run detected: {max_run} bits")
        
        # Average run length should be around 2
        avg_run = sum(runs) / len(runs)
        self.assertGreater(avg_run, 1.5)
        self.assertLess(avg_run, 2.5)
        
        print(f"\nRuns test: max run = {max_run}, avg run = {avg_run:.2f}")
    
    def test_chi_square_byte_distribution(self):
        """Test chi-square goodness of fit for byte distribution."""
        generator = universal_qkd_generator()
        
        # Generate many keys
        num_keys = 1000
        all_bytes = []
        
        for _ in range(num_keys):
            key = next(generator)
            all_bytes.extend(key)
        
        # Count byte frequencies
        byte_counts = Counter(all_bytes)
        
        # Expected frequency (uniform distribution)
        total_bytes = len(all_bytes)
        expected_freq = total_bytes / 256
        
        # Calculate chi-square statistic
        chi_square = 0.0
        for byte_val in range(256):
            observed = byte_counts.get(byte_val, 0)
            chi_square += (observed - expected_freq) ** 2 / expected_freq
        
        # For 255 degrees of freedom, chi-square should be roughly 255
        # Allow reasonable variance (between 200 and 310)
        self.assertGreater(chi_square, 200,
                          f"Chi-square too low: {chi_square:.1f}")
        self.assertLess(chi_square, 310,
                       f"Chi-square too high: {chi_square:.1f}")
        
        print(f"\nChi-square statistic: {chi_square:.1f} (df=255)")
    
    def test_serial_correlation(self):
        """Test that consecutive keys are not correlated."""
        generator = universal_qkd_generator()
        
        # Generate key pairs
        num_pairs = 1000
        correlations = []
        
        for _ in range(num_pairs):
            key1 = next(generator)
            key2 = next(generator)
            
            # Calculate correlation (should be low)
            # Use XOR distance as proxy for correlation
            xor_result = bytes(a ^ b for a, b in zip(key1, key2))
            num_diff_bits = bin(int.from_bytes(xor_result, 'big')).count('1')
            
            # Normalize to -1 to 1 range (though we expect near 0)
            correlation = (num_diff_bits - 64) / 64  # 64 is expected
            correlations.append(correlation)
        
        # Average correlation should be near zero
        avg_correlation = sum(correlations) / len(correlations)
        
        # Should be within reasonable bounds
        self.assertGreater(avg_correlation, -0.2)
        self.assertLess(avg_correlation, 0.2)
        
        print(f"\nSerial correlation: {avg_correlation:.3f}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
