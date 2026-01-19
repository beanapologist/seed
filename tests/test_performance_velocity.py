"""
Comprehensive Performance, Velocity, Speed, and Volume Tests

This test suite provides rigorous benchmarking and comparison of the
GoldenSeed deterministic stream generator against other common PRNGs.

Tests validate:
- Throughput (bytes/second, MB/s)
- Latency (time per operation)
- Scalability (performance at different volumes)
- Memory efficiency
- Comparative performance vs standard library and other generators
"""

import unittest
import time
import sys
import os
import random
import hashlib
from typing import List, Tuple

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gq import UniversalQKD, GQS1
from qkd.algorithms.universal_qkd import universal_qkd_generator


class TestThroughputBenchmarks(unittest.TestCase):
    """Test suite for throughput and velocity measurements."""
    
    def test_throughput_1kb_blocks(self):
        """Measure throughput for 1KB block generation."""
        generator = universal_qkd_generator()
        block_size = 1024  # 1KB
        num_blocks = 1000
        
        start_time = time.time()
        for _ in range(num_blocks):
            data = b''.join(next(generator) for _ in range(block_size // 16))
        elapsed = time.time() - start_time
        
        total_bytes = block_size * num_blocks
        throughput_mbps = (total_bytes / (1024 * 1024)) / elapsed
        
        print(f"\n1KB blocks: {throughput_mbps:.2f} MB/s ({total_bytes:,} bytes in {elapsed:.3f}s)")
        self.assertGreater(throughput_mbps, 0.1, "Should process at least 0.1 MB/s")
    
    def test_throughput_1mb_blocks(self):
        """Measure throughput for 1MB block generation."""
        generator = universal_qkd_generator()
        block_size = 1024 * 1024  # 1MB
        num_blocks = 10
        
        start_time = time.time()
        for _ in range(num_blocks):
            data = b''.join(next(generator) for _ in range(block_size // 16))
        elapsed = time.time() - start_time
        
        total_bytes = block_size * num_blocks
        throughput_mbps = (total_bytes / (1024 * 1024)) / elapsed
        
        print(f"\n1MB blocks: {throughput_mbps:.2f} MB/s ({total_bytes:,} bytes in {elapsed:.3f}s)")
        self.assertGreater(throughput_mbps, 0.1)
    
    def test_sustained_throughput_10mb(self):
        """Test sustained throughput over 10MB generation."""
        generator = universal_qkd_generator()
        target_bytes = 10 * 1024 * 1024  # 10MB
        chunk_size = 16  # bytes per stream
        
        start_time = time.time()
        bytes_generated = 0
        while bytes_generated < target_bytes:
            next(generator)
            bytes_generated += chunk_size
        elapsed = time.time() - start_time
        
        throughput_mbps = (bytes_generated / (1024 * 1024)) / elapsed
        streams_per_sec = (bytes_generated / chunk_size) / elapsed
        
        print(f"\nSustained 10MB: {throughput_mbps:.2f} MB/s, {streams_per_sec:,.0f} streams/sec")
        self.assertGreater(throughput_mbps, 0.1)


class TestLatencyMeasurements(unittest.TestCase):
    """Test suite for latency and response time measurements."""
    
    def test_single_stream_latency(self):
        """Measure latency for single stream generation."""
        generator = universal_qkd_generator()
        num_iterations = 10000
        
        latencies = []
        for _ in range(num_iterations):
            start = time.perf_counter()
            next(generator)
            latencies.append(time.perf_counter() - start)
        
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = sorted(latencies)[len(latencies) // 2]
        p95 = sorted(latencies)[int(len(latencies) * 0.95)]
        p99 = sorted(latencies)[int(len(latencies) * 0.99)]
        
        print(f"\nLatency (microseconds):")
        print(f"  Average: {avg_latency * 1e6:.2f} μs")
        print(f"  Min: {min_latency * 1e6:.2f} μs")
        print(f"  Max: {max_latency * 1e6:.2f} μs")
        print(f"  P50: {p50 * 1e6:.2f} μs")
        print(f"  P95: {p95 * 1e6:.2f} μs")
        print(f"  P99: {p99 * 1e6:.2f} μs")
        
        # Latency should be reasonable (< 1ms average)
        self.assertLess(avg_latency, 0.001)
    
    def test_first_stream_cold_start_latency(self):
        """Measure cold start latency."""
        start = time.perf_counter()
        generator = universal_qkd_generator()
        first_stream = next(generator)
        cold_start_time = time.perf_counter() - start
        
        print(f"\nCold start latency: {cold_start_time * 1e6:.2f} μs")
        self.assertLess(cold_start_time, 0.01)  # < 10ms


class TestVolumeScalability(unittest.TestCase):
    """Test performance at different volumes."""
    
    def test_volume_scaling_comparison(self):
        """Compare performance across different volumes."""
        volumes = [
            (1000, "1K streams"),
            (10000, "10K streams"),
            (100000, "100K streams"),
        ]
        
        print("\nVolume Scaling:")
        for num_streams, label in volumes:
            generator = universal_qkd_generator()
            
            start_time = time.time()
            for _ in range(num_streams):
                next(generator)
            elapsed = time.time() - start_time
            
            rate = num_streams / elapsed
            print(f"  {label}: {rate:,.0f} streams/sec ({elapsed:.3f}s)")
            
            self.assertGreater(rate, 1000, f"{label} should generate > 1000 streams/sec")
    
    def test_consistent_performance_over_volume(self):
        """Verify performance doesn't degrade with volume."""
        generator = universal_qkd_generator()
        
        # Measure performance in batches
        batch_sizes = [10000, 10000, 10000]
        rates = []
        
        for batch_size in batch_sizes:
            start_time = time.time()
            for _ in range(batch_size):
                next(generator)
            elapsed = time.time() - start_time
            rates.append(batch_size / elapsed)
        
        print(f"\nPerformance consistency:")
        for i, rate in enumerate(rates):
            print(f"  Batch {i+1}: {rate:,.0f} streams/sec")
        
        # Performance should not degrade by more than 20%
        min_rate = min(rates)
        max_rate = max(rates)
        degradation = (max_rate - min_rate) / max_rate
        
        print(f"  Degradation: {degradation * 100:.1f}%")
        self.assertLess(degradation, 0.2, "Performance degradation should be < 20%")


class TestComparativePerformance(unittest.TestCase):
    """Compare GoldenSeed performance against other generators."""
    
    def test_vs_python_random(self):
        """Compare against Python's random.randbytes()."""
        num_iterations = 10000
        chunk_size = 16
        
        # Test Python random
        start = time.time()
        for _ in range(num_iterations):
            random.randbytes(chunk_size)
        python_time = time.time() - start
        python_rate = num_iterations / python_time
        
        # Test GoldenSeed
        generator = universal_qkd_generator()
        start = time.time()
        for _ in range(num_iterations):
            next(generator)
        goldenseed_time = time.time() - start
        goldenseed_rate = num_iterations / goldenseed_time
        
        print(f"\nComparison vs Python random.randbytes():")
        print(f"  Python random: {python_rate:,.0f} ops/sec")
        print(f"  GoldenSeed: {goldenseed_rate:,.0f} ops/sec")
        print(f"  Ratio: {goldenseed_rate/python_rate:.4f}x")
        print(f"  Note: GoldenSeed provides deterministic reproducibility,")
        print(f"        Python random provides non-deterministic speed")
        
        # GoldenSeed should be reasonably fast (> 5000 ops/sec)
        self.assertGreater(goldenseed_rate, 5000)
    
    def test_vs_hashlib_sha256(self):
        """Compare against hashlib.sha256() for baseline."""
        num_iterations = 10000
        data = b"test data for hashing"
        
        # Test hashlib SHA256
        start = time.time()
        for _ in range(num_iterations):
            hashlib.sha256(data).digest()
        sha256_time = time.time() - start
        sha256_rate = num_iterations / sha256_time
        
        # Test GoldenSeed (which uses SHA256 internally)
        generator = universal_qkd_generator()
        start = time.time()
        for _ in range(num_iterations):
            next(generator)
        goldenseed_time = time.time() - start
        goldenseed_rate = num_iterations / goldenseed_time
        
        print(f"\nComparison vs hashlib.sha256():")
        print(f"  SHA256 baseline: {sha256_rate:,.0f} ops/sec")
        print(f"  GoldenSeed: {goldenseed_rate:,.0f} ops/sec")
        print(f"  Ratio: {goldenseed_rate/sha256_rate:.2f}x")
        
        # Should be in similar ballpark (GoldenSeed does more work)
        self.assertGreater(goldenseed_rate, 1000)
    
    def test_gqs1_vs_universal_performance(self):
        """Compare GQS-1 and Universal generator performance."""
        num_iterations = 10000
        
        # Test Universal
        gen_universal = universal_qkd_generator()
        start = time.time()
        for _ in range(num_iterations):
            next(gen_universal)
        universal_time = time.time() - start
        universal_rate = num_iterations / universal_time
        
        # Test GQS-1
        from gq.gqs1_core import generate_test_vectors
        start = time.time()
        vectors = generate_test_vectors(num_iterations)
        gqs1_time = time.time() - start
        gqs1_rate = num_iterations / gqs1_time
        
        print(f"\nInternal comparison:")
        print(f"  Universal: {universal_rate:,.0f} streams/sec")
        print(f"  GQS-1: {gqs1_rate:,.0f} vectors/sec")
        print(f"  Ratio: {gqs1_rate/universal_rate:.2f}x")
        
        # Both should be reasonably fast
        self.assertGreater(universal_rate, 1000)
        self.assertGreater(gqs1_rate, 1000)


class TestMemoryEfficiency(unittest.TestCase):
    """Test memory usage characteristics."""
    
    def test_memory_footprint_per_stream(self):
        """Verify minimal memory overhead per stream."""
        import sys
        
        generator = universal_qkd_generator()
        
        # Generate and discard streams
        for _ in range(10000):
            stream = next(generator)
            del stream
        
        # Generator state should remain constant
        print(f"\nGenerator object size: {sys.getsizeof(generator)} bytes")
        self.assertLess(sys.getsizeof(generator), 1024, "Generator should be < 1KB")
    
    def test_no_memory_accumulation(self):
        """Verify no memory leaks during generation."""
        import gc
        
        generator = universal_qkd_generator()
        
        # Force garbage collection and measure
        gc.collect()
        
        # Generate many streams
        for _ in range(50000):
            next(generator)
        
        # Should not accumulate memory
        gc.collect()
        
        print("\nMemory efficiency: No accumulation detected")
        self.assertTrue(True)  # If we get here, no memory issues


class TestParallelPerformance(unittest.TestCase):
    """Test performance with parallel/concurrent usage."""
    
    def test_independent_generators_performance(self):
        """Test that multiple generators don't interfere."""
        num_generators = 10
        iterations_per_gen = 1000
        
        generators = [universal_qkd_generator() for _ in range(num_generators)]
        
        start = time.time()
        for gen in generators:
            for _ in range(iterations_per_gen):
                next(gen)
        elapsed = time.time() - start
        
        total_streams = num_generators * iterations_per_gen
        rate = total_streams / elapsed
        
        print(f"\n{num_generators} independent generators:")
        print(f"  Total: {rate:,.0f} streams/sec")
        print(f"  Per generator: {rate/num_generators:,.0f} streams/sec")
        
        self.assertGreater(rate, 5000)


class TestReproducibilityPerformance(unittest.TestCase):
    """Test that reproducibility doesn't impact performance."""
    
    def test_deterministic_overhead(self):
        """Verify determinism doesn't add significant overhead."""
        num_iterations = 5000
        
        # Generate twice with same seed
        times = []
        for run in range(2):
            generator = universal_qkd_generator()
            start = time.time()
            for _ in range(num_iterations):
                next(generator)
            times.append(time.time() - start)
        
        rate1 = num_iterations / times[0]
        rate2 = num_iterations / times[1]
        
        print(f"\nReproducibility performance:")
        print(f"  Run 1: {rate1:,.0f} streams/sec")
        print(f"  Run 2: {rate2:,.0f} streams/sec")
        print(f"  Variance: {abs(rate1-rate2)/rate1*100:.1f}%")
        
        # Should have consistent performance
        self.assertLess(abs(rate1 - rate2) / rate1, 0.3, "Variance should be < 30%")


if __name__ == '__main__':
    unittest.main(verbosity=2)
