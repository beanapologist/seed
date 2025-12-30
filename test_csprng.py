"""
Unit tests for the Cryptographically Secure Pseudorandom Number Generator (CSPRNG)

These tests validate:
- Secure initialization and seeding
- Deterministic seeding for reproducibility
- Random number generation (integers, floats, bytes)
- Thread safety
- Uniform distribution properties
- Error handling
"""

import unittest
import threading
from collections import Counter
from csprng import CSPRNG


class TestCSPRNGInitialization(unittest.TestCase):
    """Test CSPRNG initialization modes."""
    
    def test_default_secure_initialization(self):
        """Test that default initialization creates a secure (non-deterministic) generator."""
        rng = CSPRNG()
        self.assertFalse(rng.is_deterministic())
    
    def test_secure_generators_produce_different_outputs(self):
        """Test that two secure generators produce different outputs."""
        rng1 = CSPRNG()
        rng2 = CSPRNG()
        
        # Two secure generators should produce different random values
        value1 = rng1.random_int(0, 1000000)
        value2 = rng2.random_int(0, 1000000)
        
        # It's extremely unlikely they'll be equal
        # (probability = 1/1000001, essentially impossible)
        self.assertNotEqual(value1, value2)
    
    def test_deterministic_seed_initialization_bytes(self):
        """Test initialization with deterministic byte seed."""
        seed = b"test_seed_12345"
        rng = CSPRNG(seed=seed)
        self.assertTrue(rng.is_deterministic())
    
    def test_deterministic_seed_initialization_int(self):
        """Test initialization with deterministic integer seed."""
        seed = 12345
        rng = CSPRNG(seed=seed)
        self.assertTrue(rng.is_deterministic())
    
    def test_deterministic_generators_same_seed_same_output(self):
        """Test that two generators with same seed produce same outputs."""
        seed = b"reproducible_seed"
        rng1 = CSPRNG(seed=seed)
        rng2 = CSPRNG(seed=seed)
        
        # Same seed should produce same sequence
        values1 = [rng1.random_int(0, 1000) for _ in range(10)]
        values2 = [rng2.random_int(0, 1000) for _ in range(10)]
        
        self.assertEqual(values1, values2)
    
    def test_deterministic_generators_different_seed_different_output(self):
        """Test that two generators with different seeds produce different outputs."""
        rng1 = CSPRNG(seed=b"seed_one")
        rng2 = CSPRNG(seed=b"seed_two")
        
        values1 = [rng1.random_int(0, 1000) for _ in range(10)]
        values2 = [rng2.random_int(0, 1000) for _ in range(10)]
        
        self.assertNotEqual(values1, values2)
    
    def test_empty_seed_raises_error(self):
        """Test that empty seed raises ValueError."""
        with self.assertRaises(ValueError):
            CSPRNG(seed=b"")
    
    def test_invalid_seed_type_raises_error(self):
        """Test that invalid seed type raises ValueError."""
        with self.assertRaises(ValueError):
            CSPRNG(seed="string_seed")
        
        with self.assertRaises(ValueError):
            CSPRNG(seed=[1, 2, 3])


class TestCSPRNGRandomBytes(unittest.TestCase):
    """Test random byte generation."""
    
    def test_random_bytes_length(self):
        """Test that random_bytes generates correct length."""
        rng = CSPRNG()
        
        for length in [1, 16, 32, 64, 128, 1000]:
            random_bytes = rng.random_bytes(length)
            self.assertEqual(len(random_bytes), length)
    
    def test_random_bytes_type(self):
        """Test that random_bytes returns bytes type."""
        rng = CSPRNG()
        random_bytes = rng.random_bytes(32)
        self.assertIsInstance(random_bytes, bytes)
    
    def test_random_bytes_different_calls(self):
        """Test that successive calls produce different bytes."""
        rng = CSPRNG()
        
        bytes1 = rng.random_bytes(32)
        bytes2 = rng.random_bytes(32)
        
        # Should be different (probability of collision is negligible)
        self.assertNotEqual(bytes1, bytes2)
    
    def test_random_bytes_deterministic(self):
        """Test that deterministic mode produces reproducible bytes."""
        seed = b"deterministic_test"
        
        rng1 = CSPRNG(seed=seed)
        bytes1 = rng1.random_bytes(32)
        
        rng2 = CSPRNG(seed=seed)
        bytes2 = rng2.random_bytes(32)
        
        self.assertEqual(bytes1, bytes2)
    
    def test_random_bytes_invalid_length(self):
        """Test that invalid length raises ValueError."""
        rng = CSPRNG()
        
        with self.assertRaises(ValueError):
            rng.random_bytes(0)
        
        with self.assertRaises(ValueError):
            rng.random_bytes(-1)


class TestCSPRNGRandomInt(unittest.TestCase):
    """Test random integer generation."""
    
    def test_random_int_range(self):
        """Test that random integers are within specified range."""
        rng = CSPRNG()
        
        for _ in range(100):
            value = rng.random_int(10, 20)
            self.assertGreaterEqual(value, 10)
            self.assertLessEqual(value, 20)
    
    def test_random_int_edge_cases(self):
        """Test random integer generation with edge cases."""
        rng = CSPRNG()
        
        # Same bounds should return that value
        self.assertEqual(rng.random_int(42, 42), 42)
        
        # Minimum range
        value = rng.random_int(0, 1)
        self.assertIn(value, [0, 1])
        
        # Large range
        value = rng.random_int(0, 1000000)
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 1000000)
    
    def test_random_int_negative_range(self):
        """Test random integers in negative range."""
        rng = CSPRNG()
        
        for _ in range(100):
            value = rng.random_int(-50, -10)
            self.assertGreaterEqual(value, -50)
            self.assertLessEqual(value, -10)
    
    def test_random_int_mixed_range(self):
        """Test random integers in mixed positive/negative range."""
        rng = CSPRNG()
        
        for _ in range(100):
            value = rng.random_int(-25, 25)
            self.assertGreaterEqual(value, -25)
            self.assertLessEqual(value, 25)
    
    def test_random_int_invalid_range(self):
        """Test that invalid range raises ValueError."""
        rng = CSPRNG()
        
        with self.assertRaises(ValueError):
            rng.random_int(10, 5)
    
    def test_random_int_distribution(self):
        """Test that random integers have roughly uniform distribution."""
        rng = CSPRNG()
        
        # Generate many samples
        samples = [rng.random_int(0, 9) for _ in range(10000)]
        
        # Count occurrences
        counter = Counter(samples)
        
        # Each value (0-9) should appear roughly 1000 times
        # We'll use a generous tolerance of ±20% due to randomness
        expected = 1000
        tolerance = 200
        
        for value in range(10):
            count = counter[value]
            self.assertGreaterEqual(count, expected - tolerance,
                                   f"Value {value} appeared {count} times, expected ~{expected}")
            self.assertLessEqual(count, expected + tolerance,
                                f"Value {value} appeared {count} times, expected ~{expected}")
    
    def test_random_int_deterministic(self):
        """Test that deterministic mode produces reproducible integers."""
        seed = b"int_test_seed"
        
        rng1 = CSPRNG(seed=seed)
        values1 = [rng1.random_int(0, 100) for _ in range(20)]
        
        rng2 = CSPRNG(seed=seed)
        values2 = [rng2.random_int(0, 100) for _ in range(20)]
        
        self.assertEqual(values1, values2)


class TestCSPRNGRandomFloat(unittest.TestCase):
    """Test random float generation."""
    
    def test_random_float_range(self):
        """Test that random floats are in [0.0, 1.0) range."""
        rng = CSPRNG()
        
        for _ in range(1000):
            value = rng.random_float()
            self.assertGreaterEqual(value, 0.0)
            self.assertLess(value, 1.0)
    
    def test_random_float_type(self):
        """Test that random_float returns float type."""
        rng = CSPRNG()
        value = rng.random_float()
        self.assertIsInstance(value, float)
    
    def test_random_float_different_calls(self):
        """Test that successive calls produce different floats."""
        rng = CSPRNG()
        
        values = [rng.random_float() for _ in range(10)]
        
        # All values should be unique (probability of collision is negligible)
        self.assertEqual(len(values), len(set(values)))
    
    def test_random_float_distribution(self):
        """Test that random floats have roughly uniform distribution."""
        rng = CSPRNG()
        
        # Generate many samples
        samples = [rng.random_float() for _ in range(10000)]
        
        # Divide into 10 buckets [0.0-0.1, 0.1-0.2, ..., 0.9-1.0]
        buckets = [0] * 10
        for sample in samples:
            bucket = min(int(sample * 10), 9)  # min() handles edge case of 1.0
            buckets[bucket] += 1
        
        # Each bucket should have roughly 1000 samples
        # We'll use a generous tolerance of ±20%
        expected = 1000
        tolerance = 200
        
        for i, count in enumerate(buckets):
            self.assertGreaterEqual(count, expected - tolerance,
                                   f"Bucket {i} has {count} samples, expected ~{expected}")
            self.assertLessEqual(count, expected + tolerance,
                                f"Bucket {i} has {count} samples, expected ~{expected}")
    
    def test_random_float_deterministic(self):
        """Test that deterministic mode produces reproducible floats."""
        seed = b"float_test_seed"
        
        rng1 = CSPRNG(seed=seed)
        values1 = [rng1.random_float() for _ in range(20)]
        
        rng2 = CSPRNG(seed=seed)
        values2 = [rng2.random_float() for _ in range(20)]
        
        self.assertEqual(values1, values2)


class TestCSPRNGThreadSafety(unittest.TestCase):
    """Test thread safety of CSPRNG."""
    
    def test_concurrent_random_int(self):
        """Test that concurrent random_int calls don't cause issues."""
        rng = CSPRNG()
        results = []
        errors = []
        
        def generate_random():
            try:
                for _ in range(100):
                    value = rng.random_int(0, 1000)
                    results.append(value)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = [threading.Thread(target=generate_random) for _ in range(10)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # No errors should have occurred
        self.assertEqual(len(errors), 0)
        
        # Should have 1000 results (10 threads * 100 values each)
        self.assertEqual(len(results), 1000)
        
        # All results should be in valid range
        for value in results:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1000)
    
    def test_concurrent_random_bytes(self):
        """Test that concurrent random_bytes calls don't cause issues."""
        rng = CSPRNG()
        results = []
        errors = []
        
        def generate_random():
            try:
                for _ in range(100):
                    value = rng.random_bytes(32)
                    results.append(value)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = [threading.Thread(target=generate_random) for _ in range(10)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # No errors should have occurred
        self.assertEqual(len(errors), 0)
        
        # Should have 1000 results
        self.assertEqual(len(results), 1000)
        
        # All results should be 32 bytes
        for value in results:
            self.assertEqual(len(value), 32)


class TestCSPRNGStaticMethods(unittest.TestCase):
    """Test static convenience methods."""
    
    def test_secure_random_int(self):
        """Test static secure_random_int method."""
        value = CSPRNG.secure_random_int(0, 100)
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 100)
    
    def test_secure_random_int_different_calls(self):
        """Test that static method produces different values."""
        value1 = CSPRNG.secure_random_int(0, 1000000)
        value2 = CSPRNG.secure_random_int(0, 1000000)
        
        # Should be different (extremely high probability)
        self.assertNotEqual(value1, value2)
    
    def test_secure_random_int_invalid_range(self):
        """Test that static method validates range."""
        with self.assertRaises(ValueError):
            CSPRNG.secure_random_int(10, 5)
    
    def test_secure_random_bytes(self):
        """Test static secure_random_bytes method."""
        random_bytes = CSPRNG.secure_random_bytes(32)
        self.assertEqual(len(random_bytes), 32)
        self.assertIsInstance(random_bytes, bytes)
    
    def test_secure_random_bytes_different_calls(self):
        """Test that static method produces different bytes."""
        bytes1 = CSPRNG.secure_random_bytes(32)
        bytes2 = CSPRNG.secure_random_bytes(32)
        
        # Should be different
        self.assertNotEqual(bytes1, bytes2)
    
    def test_secure_random_bytes_invalid_length(self):
        """Test that static method validates length."""
        with self.assertRaises(ValueError):
            CSPRNG.secure_random_bytes(0)
        
        with self.assertRaises(ValueError):
            CSPRNG.secure_random_bytes(-1)


if __name__ == '__main__':
    unittest.main()
