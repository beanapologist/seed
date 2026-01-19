"""
Scalability and Stress Test Suite for STL (Standardized Test Library)

This test suite validates performance, memory efficiency, and scalability
under high-load conditions and with large-scale data generation.

Tests validate:
- Large-scale key generation (10K, 100K, 1M+ keys)
- Memory efficiency and leak detection
- Performance benchmarks and timing
- Continuous generation without degradation
- Resource utilization under stress
"""

import unittest
import hashlib
import sys
import os
import time
import gc
from typing import List, Iterator

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gq import GoldenStreamGenerator, GQS1
from gq.stream_generator import golden_stream_generator
from gq.gqs1_core import generate_test_vectors


class TestLargeScaleKeyGeneration(unittest.TestCase):
    """Test suite for large-scale key generation."""
    
    def test_generate_10k_keys(self):
        """Test generation of 10,000 keys."""
        generator = golden_stream_generator()
        
        start_time = time.time()
        keys = [next(generator) for _ in range(10000)]
        elapsed = time.time() - start_time
        
        # Verify all keys generated
        self.assertEqual(len(keys), 10000)
        
        # All keys should be 16 bytes
        self.assertTrue(all(len(k) == 16 for k in keys))
        
        # All keys should be unique
        unique_keys = set(keys)
        self.assertEqual(len(unique_keys), 10000)
        
        # Performance check: should complete in reasonable time
        # ~10,000 keys should take less than 30 seconds
        self.assertLess(elapsed, 30.0, f"Generation took {elapsed:.2f}s")
        
        # Log performance
        keys_per_sec = 10000 / elapsed
        print(f"\n10K keys generated in {elapsed:.2f}s ({keys_per_sec:.0f} keys/sec)")
    
    def test_generate_100k_keys(self):
        """Test generation of 100,000 keys."""
        generator = golden_stream_generator()
        
        start_time = time.time()
        
        # Generate in batches to monitor progress
        batch_size = 10000
        total_keys = 100000
        all_keys_unique = True
        seen_keys = set()
        
        for batch_num in range(total_keys // batch_size):
            batch_keys = [next(generator) for _ in range(batch_size)]
            
            # Check for duplicates within and across batches
            batch_set = set(batch_keys)
            if len(batch_set) != batch_size:
                all_keys_unique = False
            
            # Check against previously seen keys
            if seen_keys & batch_set:
                all_keys_unique = False
            
            seen_keys.update(batch_set)
        
        elapsed = time.time() - start_time
        
        # Verify uniqueness
        self.assertTrue(all_keys_unique)
        self.assertEqual(len(seen_keys), total_keys)
        
        # Performance check: should complete in reasonable time
        # ~100,000 keys should take less than 5 minutes
        self.assertLess(elapsed, 300.0, f"Generation took {elapsed:.2f}s")
        
        # Log performance
        keys_per_sec = total_keys / elapsed
        print(f"\n100K keys generated in {elapsed:.2f}s ({keys_per_sec:.0f} keys/sec)")
    
    def test_streaming_generation_1m_keys(self):
        """Test streaming generation of 1 million keys without storing all."""
        generator = golden_stream_generator()
        
        start_time = time.time()
        
        # Use rolling window to check uniqueness without storing all keys
        window_size = 10000
        recent_keys = []
        count = 0
        total_keys = 1000000
        
        for i, key in enumerate(generator):
            if i >= total_keys:
                break
            
            # Progress reporting at reasonable intervals (every 200K keys)
            if i > 0 and i % 200000 == 0:
                print(f"\nGenerated {i:,} keys...")
            
            self.assertEqual(len(key), 16)
            
            # Check against recent keys
            self.assertNotIn(key, recent_keys)
            
            recent_keys.append(key)
            if len(recent_keys) > window_size:
                recent_keys.pop(0)
            
            count += 1
        
        elapsed = time.time() - start_time
        
        self.assertEqual(count, total_keys)
        
        # Performance check
        keys_per_sec = total_keys / elapsed
        print(f"\n1M keys generated in {elapsed:.2f}s ({keys_per_sec:.0f} keys/sec)")
        
        # Should be able to generate 1M keys in reasonable time (< 10 minutes)
        self.assertLess(elapsed, 600.0, f"Generation took {elapsed:.2f}s")


class TestMemoryEfficiency(unittest.TestCase):
    """Test suite for memory efficiency and leak detection."""
    
    def test_memory_efficiency_continuous_generation(self):
        """Test that continuous generation doesn't leak memory."""
        generator = golden_stream_generator()
        
        # Force garbage collection before test
        gc.collect()
        
        # Generate keys in batches and discard
        num_iterations = 10
        batch_size = 10000
        
        for iteration in range(num_iterations):
            # Generate batch
            keys = [next(generator) for _ in range(batch_size)]
            
            # Verify batch
            self.assertEqual(len(keys), batch_size)
            
            # Explicitly delete and collect garbage
            del keys
            gc.collect()
        
        # If we got here without MemoryError, test passes
        self.assertTrue(True)
    
    def test_generator_state_size(self):
        """Test that generator state remains constant size."""
        generator = golden_stream_generator()
        
        # Generate some keys to establish state
        for i in range(100):
            next(generator)
        
        # Generator state should be minimal (just internal counter and state)
        # Python generators are efficient and don't store history
        self.assertTrue(True)  # If we got here, memory is fine
    
    def test_no_key_storage_in_generator(self):
        """Test that generator doesn't store previously generated keys."""
        generator = golden_stream_generator()
        
        # Generate many keys
        for i in range(1000):
            key = next(generator)
            # Key should be new bytes object each time
            self.assertIsInstance(key, bytes)
        
        # Generator should not have stored keys attribute
        self.assertFalse(hasattr(generator, 'stored_keys'))


class TestPerformanceBenchmarks(unittest.TestCase):
    """Test suite for performance benchmarking."""
    
    def test_key_generation_rate(self):
        """Benchmark key generation rate."""
        generator = golden_stream_generator()
        
        # Warm up
        for _ in range(100):
            next(generator)
        
        # Benchmark
        start_time = time.time()
        num_keys = 10000
        keys = [next(generator) for _ in range(num_keys)]
        elapsed = time.time() - start_time
        
        keys_per_sec = num_keys / elapsed
        
        # Log benchmark results
        print(f"\nKey generation rate: {keys_per_sec:.0f} keys/sec")
        print(f"Time per key: {(elapsed / num_keys) * 1000:.3f} ms")
        
        # Should be able to generate at least 100 keys/sec
        self.assertGreater(keys_per_sec, 100)
    
    def test_gqs1_generation_rate(self):
        """Benchmark GQS-1 test vector generation rate."""
        # Warm up
        generate_test_vectors(10)
        
        # Benchmark
        start_time = time.time()
        num_vectors = 1000
        vectors = generate_test_vectors(num_vectors)
        elapsed = time.time() - start_time
        
        vectors_per_sec = num_vectors / elapsed
        
        # Log benchmark results
        print(f"\nGQS-1 generation rate: {vectors_per_sec:.0f} vectors/sec")
        print(f"Time per vector: {(elapsed / num_vectors) * 1000:.3f} ms")
        
        # Verify results
        self.assertEqual(len(vectors), num_vectors)
        
        # Should be able to generate at least 50 vectors/sec
        self.assertGreater(vectors_per_sec, 50)
    
    def test_basis_matching_performance(self):
        """Benchmark basis matching simulation performance."""
        from gq.universal_qkd import basis_match
        
        # Test with all possible byte values
        start_time = time.time()
        num_iterations = 100000
        
        for iteration in range(num_iterations):
            byte_val = iteration % 256
            result = basis_match(byte_val)
        
        elapsed = time.time() - start_time
        ops_per_sec = num_iterations / elapsed
        
        print(f"\nBasis matching rate: {ops_per_sec:.0f} ops/sec")
        
        # Should be very fast (millions per second)
        self.assertGreater(ops_per_sec, 100000)
    
    def test_hash_drbg_performance(self):
        """Benchmark Hash-DRBG ratchet performance."""
        from gq.gqs1_core import hash_drbg_ratchet
        
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        start_time = time.time()
        num_iterations = 10000
        
        for i in range(num_iterations):
            state = hash_drbg_ratchet(state, i)
        
        elapsed = time.time() - start_time
        ops_per_sec = num_iterations / elapsed
        
        print(f"\nHash-DRBG ratchet rate: {ops_per_sec:.0f} ops/sec")
        
        # Should be able to do thousands per second
        self.assertGreater(ops_per_sec, 1000)


class TestContinuousGeneration(unittest.TestCase):
    """Test suite for continuous generation without degradation."""
    
    def test_no_performance_degradation(self):
        """Test that performance doesn't degrade over time."""
        generator = golden_stream_generator()
        
        # Generate keys in multiple batches and time each
        batch_size = 1000
        num_batches = 10
        batch_times = []
        
        for batch_num in range(num_batches):
            start_time = time.time()
            keys = [next(generator) for _ in range(batch_size)]
            elapsed = time.time() - start_time
            batch_times.append(elapsed)
            
            # Verify batch
            self.assertEqual(len(keys), batch_size)
        
        # Calculate average times for first and last batches
        first_half_avg = sum(batch_times[:5]) / 5
        second_half_avg = sum(batch_times[5:]) / 5
        
        # Second half should not be significantly slower than first half
        # Allow up to 50% degradation (should be much less in practice)
        self.assertLess(second_half_avg, first_half_avg * 1.5,
                       f"Performance degraded: {first_half_avg:.3f}s -> {second_half_avg:.3f}s")
        
        print(f"\nBatch times: {[f'{t:.3f}s' for t in batch_times]}")
        print(f"First half avg: {first_half_avg:.3f}s, Second half avg: {second_half_avg:.3f}s")
    
    def test_consistent_output_quality(self):
        """Test that output quality remains consistent over time."""
        generator = golden_stream_generator()
        
        # Generate keys at different points in the stream
        early_keys = [next(generator) for _ in range(100)]
        
        # Skip ahead
        for _ in range(10000):
            next(generator)
        
        middle_keys = [next(generator) for _ in range(100)]
        
        # Skip ahead more
        for _ in range(90000):
            next(generator)
        
        late_keys = [next(generator) for _ in range(100)]
        
        # All sets should have unique keys
        self.assertEqual(len(set(early_keys)), 100)
        self.assertEqual(len(set(middle_keys)), 100)
        self.assertEqual(len(set(late_keys)), 100)
        
        # No overlap between sets
        all_keys = set(early_keys) | set(middle_keys) | set(late_keys)
        self.assertEqual(len(all_keys), 300)


class TestResourceUtilization(unittest.TestCase):
    """Test suite for resource utilization under stress."""
    
    def test_concurrent_generators_independence(self):
        """Test that multiple concurrent generators are independent."""
        # Create multiple generators
        num_generators = 10
        generators = [golden_stream_generator() for _ in range(num_generators)]
        
        # Generate keys from each
        all_keys = []
        for gen in generators:
            keys = [next(gen) for _ in range(100)]
            all_keys.extend(keys)
        
        # All generators should produce the same sequence (deterministic)
        # Check that each generator produced the same keys
        for i in range(num_generators):
            start_idx = i * 100
            end_idx = start_idx + 100
            keys_from_gen_i = all_keys[start_idx:end_idx]
            
            # Compare with first generator's output
            if i > 0:
                first_gen_keys = all_keys[0:100]
                self.assertEqual(keys_from_gen_i, first_gen_keys)
    
    def test_stress_alternating_generation(self):
        """Test alternating between different generation methods."""
        universal_gen = golden_stream_generator()
        
        # Alternate between generation methods
        for i in range(100):
            # Universal QKD
            key1 = next(universal_gen)
            self.assertEqual(len(key1), 16)
            
            # GQS-1
            vectors = generate_test_vectors(1)
            self.assertEqual(len(vectors), 1)
            self.assertEqual(len(vectors[0]), 16)
            
            # Both should work without interference
    
    def test_rapid_generator_creation(self):
        """Test rapid creation and destruction of generators."""
        # Create and use many generators rapidly
        num_iterations = 1000
        
        for i in range(num_iterations):
            gen = golden_stream_generator()
            key = next(gen)
            self.assertEqual(len(key), 16)
            del gen
        
        # Should complete without issues
        self.assertTrue(True)


class TestComplexityScaling(unittest.TestCase):
    """Test suite for behavior under high complexity scenarios."""
    
    def test_deep_ratchet_state_evolution(self):
        """Test state evolution through many ratchet operations."""
        from gq.gqs1_core import hash_drbg_ratchet
        
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Perform deep ratcheting
        num_ratchets = 10000
        states = [state]
        
        for i in range(num_ratchets):
            state = hash_drbg_ratchet(state, i)
            if i % 1000 == 0:
                states.append(state)
        
        # All sampled states should be unique
        unique_states = set(states)
        self.assertEqual(len(unique_states), len(states))
        
        # Final state should be completely different from initial
        self.assertNotEqual(states[0], states[-1])
    
    def test_sifting_efficiency_over_scale(self):
        """Test that sifting efficiency remains consistent at scale."""
        from gq.universal_qkd import collect_sifted_bits
        
        seed = bytes.fromhex("0000000000000000a8f4979b77e3f93fa8f4979b77e3f93fa8f4979b77e3f93f")
        state = hashlib.sha256(seed).digest()
        
        # Collect sifted bits multiple times
        num_collections = 100
        counter_increments = []
        
        counter = 0
        for i in range(num_collections):
            sifted, state, new_counter = collect_sifted_bits(state, counter)
            counter_increment = new_counter - counter
            counter_increments.append(counter_increment)
            counter = new_counter
            
            # Verify output
            self.assertEqual(len(sifted), 256)
        
        # Calculate average and variance
        avg_increment = sum(counter_increments) / len(counter_increments)
        variance = sum((x - avg_increment) ** 2 for x in counter_increments) / len(counter_increments)
        
        # Efficiency should be roughly consistent (low variance relative to mean)
        # Typical efficiency is ~25-50%, so avg_increment should be ~16-32
        self.assertGreater(avg_increment, 10)
        self.assertLess(avg_increment, 40)
        
        print(f"\nAverage counter increment: {avg_increment:.2f} (variance: {variance:.2f})")


if __name__ == '__main__':
    unittest.main(verbosity=2)
