"""
Comprehensive test suite for entropy testing module.

Tests validate the statistical analysis tools and their application to
cryptographic key generation mechanisms.
"""

import unittest
import secrets
from gq.entropy_testing import (
    EntropyAnalyzer,
    analyze_key_stream,
    validate_zero_bias
)
from gq.universal_qkd import universal_qkd_generator
from gq.nist_pqc import (
    generate_hybrid_key,
    generate_hybrid_key_stream,
    PQCAlgorithm
)

# Entropy thresholds for testing
MIN_DETERMINISTIC_KEY_ENTROPY = 3.0  # bits/byte for small deterministic keys
MIN_AGGREGATE_ENTROPY = 7.0  # bits/byte for large aggregate samples
MIN_PQC_SEED_ENTROPY = 4.5  # bits/byte for derived PQC seeds


class TestEntropyAnalyzer(unittest.TestCase):
    """Test EntropyAnalyzer statistical methods."""
    
    def test_shannon_entropy_random_data(self):
        """Test Shannon entropy calculation on high-quality random data."""
        # Generate high-quality random data
        random_data = secrets.token_bytes(1024)
        analyzer = EntropyAnalyzer(random_data)
        
        entropy = analyzer.shannon_entropy()
        
        # High-quality random data should have entropy close to 8.0
        self.assertGreater(entropy, 7.0)
        self.assertLessEqual(entropy, 8.0)
    
    def test_shannon_entropy_low_entropy(self):
        """Test Shannon entropy calculation on low-entropy data."""
        # Low entropy data (repeated pattern)
        low_entropy_data = b'\x00' * 100 + b'\xFF' * 100
        analyzer = EntropyAnalyzer(low_entropy_data)
        
        entropy = analyzer.shannon_entropy()
        
        # Should detect low entropy
        self.assertLess(entropy, 3.0)
    
    def test_shannon_entropy_empty_data(self):
        """Test Shannon entropy on empty data."""
        analyzer = EntropyAnalyzer(b'')
        entropy = analyzer.shannon_entropy()
        self.assertEqual(entropy, 0.0)
    
    def test_byte_distribution_uniform(self):
        """Test byte distribution analysis on uniform data."""
        # Generate data that covers many byte values
        random_data = secrets.token_bytes(2048)
        analyzer = EntropyAnalyzer(random_data)
        
        dist = analyzer.byte_distribution()
        
        # Should have good diversity
        self.assertGreater(dist['unique_bytes'], 200)
        self.assertGreater(dist['byte_diversity'], 0.7)
    
    def test_byte_distribution_biased(self):
        """Test byte distribution on biased data."""
        biased_data = b'\x42' * 1000
        analyzer = EntropyAnalyzer(biased_data)
        
        dist = analyzer.byte_distribution()
        
        self.assertEqual(dist['unique_bytes'], 1)
        self.assertLess(dist['byte_diversity'], 0.01)
        self.assertEqual(dist['most_common_frequency'], 1.0)
    
    def test_monobit_frequency_test_balanced(self):
        """Test monobit frequency on balanced random data."""
        random_data = secrets.token_bytes(1024)
        analyzer = EntropyAnalyzer(random_data)
        
        result = analyzer.monobit_frequency_test()
        
        # Should be roughly balanced
        self.assertLess(result['balance'], 0.1)
        self.assertGreater(result['ones_ratio'], 0.4)
        self.assertLess(result['ones_ratio'], 0.6)
    
    def test_monobit_frequency_test_biased(self):
        """Test monobit frequency on biased data."""
        # All zeros - very biased
        biased_data = b'\x00' * 100
        analyzer = EntropyAnalyzer(biased_data)
        
        result = analyzer.monobit_frequency_test()
        
        self.assertEqual(result['ones_count'], 0)
        self.assertEqual(result['ones_ratio'], 0.0)
        self.assertFalse(result['passes'])
    
    def test_runs_test_random(self):
        """Test runs test on random data."""
        random_data = secrets.token_bytes(1024)
        analyzer = EntropyAnalyzer(random_data)
        
        result = analyzer.runs_test()
        
        # Runs ratio should be close to 1.0 for random data
        self.assertGreater(result['runs_ratio'], 0.8)
        self.assertLess(result['runs_ratio'], 1.2)
    
    def test_runs_test_alternating(self):
        """Test runs test on alternating pattern."""
        # Alternating pattern: 0x55 = 01010101 in binary
        alternating_data = b'\x55' * 100
        analyzer = EntropyAnalyzer(alternating_data)
        
        result = analyzer.runs_test()
        
        # Alternating pattern has many runs
        self.assertGreater(result['total_runs'], result['expected_runs'] * 0.5)
    
    def test_serial_correlation_random(self):
        """Test serial correlation on random data."""
        random_data = secrets.token_bytes(1024)
        analyzer = EntropyAnalyzer(random_data)
        
        result = analyzer.serial_correlation_test()
        
        # Random data should have low correlation
        self.assertLess(abs(result['correlation']), 0.2)
    
    def test_serial_correlation_correlated(self):
        """Test serial correlation on correlated data."""
        # Create correlated data (incrementing sequence)
        correlated_data = bytes(i % 256 for i in range(1000))
        analyzer = EntropyAnalyzer(correlated_data)
        
        result = analyzer.serial_correlation_test()
        
        # Should detect correlation
        self.assertGreater(abs(result['correlation']), 0.5)
        self.assertFalse(result['passes'])
    
    def test_chi_square_test_uniform(self):
        """Test chi-square on uniformly distributed data."""
        # Generate large sample for better uniformity
        random_data = secrets.token_bytes(10000)
        analyzer = EntropyAnalyzer(random_data)
        
        result = analyzer.chi_square_test()
        
        # Should pass uniformity test
        self.assertLess(result['chi_square'], 400)  # Reasonable threshold
    
    def test_chi_square_test_non_uniform(self):
        """Test chi-square on non-uniform data."""
        # Biased distribution (mostly zeros and ones)
        biased_data = b'\x00' * 500 + b'\x01' * 500
        analyzer = EntropyAnalyzer(biased_data)
        
        result = analyzer.chi_square_test()
        
        # Should fail uniformity test
        self.assertFalse(result['passes'])
    
    def test_comprehensive_analysis_high_quality(self):
        """Test comprehensive analysis on high-quality random data."""
        random_data = secrets.token_bytes(2048)
        analyzer = EntropyAnalyzer(random_data)
        
        results = analyzer.comprehensive_analysis()
        
        # Should pass all tests
        self.assertIn(results['overall_quality'], ['excellent', 'good'])
        self.assertGreater(results['shannon_entropy'], 7.0)
        self.assertEqual(len(results['recommendations']), 0)
    
    def test_comprehensive_analysis_low_quality(self):
        """Test comprehensive analysis on low-quality data."""
        poor_data = b'\x00' * 1000
        analyzer = EntropyAnalyzer(poor_data)
        
        results = analyzer.comprehensive_analysis()
        
        # Should detect poor quality
        self.assertEqual(results['overall_quality'], 'poor')
        self.assertFalse(results['passes_all_tests'])
        self.assertGreater(len(results['recommendations']), 0)


class TestKeyStreamAnalysis(unittest.TestCase):
    """Test entropy analysis on key streams."""
    
    def test_analyze_key_stream_random(self):
        """Test key stream analysis on random keys."""
        keys = [secrets.token_bytes(32) for _ in range(50)]
        
        results = analyze_key_stream(keys)
        
        self.assertIn('aggregate_analysis', results)
        self.assertIn('per_key_statistics', results)
        self.assertEqual(results['per_key_statistics']['total_keys'], 50)
        # Per-key entropy for 32-byte keys should be reasonable
        self.assertGreater(results['per_key_statistics']['average_entropy'], 4.5)
    
    def test_analyze_key_stream_insufficient_data(self):
        """Test key stream analysis with insufficient data."""
        keys = [b'\x00\x01\x02']
        
        results = analyze_key_stream(keys, min_sample_size=1000)
        
        self.assertIn('error', results)
    
    def test_analyze_key_stream_empty(self):
        """Test key stream analysis with empty keys."""
        keys = []
        
        results = analyze_key_stream(keys, min_sample_size=100)
        
        self.assertIn('error', results)


class TestZeroBiasValidation(unittest.TestCase):
    """Test zero-bias validation."""
    
    def test_no_bias_random_data(self):
        """Test bias detection on unbiased random data."""
        random_data = secrets.token_bytes(64)
        
        result = validate_zero_bias(random_data)
        
        # Random data should have no bias
        self.assertFalse(result['has_bias'])
        self.assertEqual(len(result['bias_types']), 0)
        self.assertTrue(result['passes'])
    
    def test_leading_zeros_bias(self):
        """Test detection of leading zeros bias."""
        biased_data = b'\x00\x00\x00\x00' + secrets.token_bytes(60)
        
        result = validate_zero_bias(biased_data)
        
        self.assertTrue(result['has_bias'])
        self.assertIn('leading_zeros', result['bias_types'])
        self.assertFalse(result['passes'])
    
    def test_trailing_zeros_bias(self):
        """Test detection of trailing zeros bias."""
        biased_data = secrets.token_bytes(60) + b'\x00\x00\x00\x00'
        
        result = validate_zero_bias(biased_data)
        
        self.assertTrue(result['has_bias'])
        self.assertIn('trailing_zeros', result['bias_types'])
    
    def test_all_zeros_bias(self):
        """Test detection of all-zeros bias."""
        biased_data = b'\x00' * 64
        
        result = validate_zero_bias(biased_data)
        
        self.assertTrue(result['has_bias'])
        self.assertIn('all_zeros', result['bias_types'])
    
    def test_low_diversity_bias(self):
        """Test detection of low diversity bias."""
        biased_data = b'\x42' * 64
        
        result = validate_zero_bias(biased_data)
        
        self.assertTrue(result['has_bias'])
        self.assertIn('low_diversity', result['bias_types'])
    
    def test_empty_data_bias(self):
        """Test bias detection on empty data."""
        result = validate_zero_bias(b'')
        
        self.assertTrue(result['has_bias'])
        self.assertIn('empty_data', result['bias_types'])


class TestUniversalQKDEntropy(unittest.TestCase):
    """Test entropy of Universal QKD key generation."""
    
    def test_universal_qkd_single_key_entropy(self):
        """Test entropy of a single Universal QKD key."""
        generator = universal_qkd_generator()
        key = next(generator)
        
        analyzer = EntropyAnalyzer(key)
        entropy = analyzer.shannon_entropy()
        
        # Single deterministic key may have lower entropy than random data
        # but should still have reasonable diversity
        self.assertGreater(entropy, MIN_DETERMINISTIC_KEY_ENTROPY)
        self.assertEqual(len(key), 16)
    
    def test_universal_qkd_key_stream_entropy(self):
        """Test entropy across multiple Universal QKD keys."""
        generator = universal_qkd_generator()
        keys = [next(generator) for _ in range(100)]
        
        results = analyze_key_stream(keys)
        
        # Aggregate should show high entropy
        self.assertGreater(results['aggregate_analysis']['shannon_entropy'], 7.0)
        self.assertIn(results['aggregate_analysis']['overall_quality'], ['excellent', 'good'])
    
    def test_universal_qkd_zero_bias(self):
        """Test Universal QKD keys for zero bias."""
        generator = universal_qkd_generator()
        
        # Test multiple keys
        for _ in range(10):
            key = next(generator)
            result = validate_zero_bias(key)
            self.assertTrue(result['passes'], 
                          f"Key failed bias test: {result['bias_types']}")


class TestNISTPQCEntropy(unittest.TestCase):
    """Test entropy of NIST PQC hybrid key generation."""
    
    def test_kyber_seed_entropy(self):
        """Test entropy of Kyber seed generation."""
        det_key, pqc_seed = generate_hybrid_key(PQCAlgorithm.KYBER768)
        
        # Test deterministic key - deterministic keys have lower per-key entropy
        det_analyzer = EntropyAnalyzer(det_key)
        det_entropy = det_analyzer.shannon_entropy()
        self.assertGreater(det_entropy, MIN_DETERMINISTIC_KEY_ENTROPY)
        
        # Test PQC seed - derived seeds should have reasonable entropy
        # Note: 32-byte seeds will have lower per-byte entropy than larger samples
        pqc_analyzer = EntropyAnalyzer(pqc_seed)
        pqc_entropy = pqc_analyzer.shannon_entropy()
        self.assertGreater(pqc_entropy, MIN_PQC_SEED_ENTROPY)
    
    def test_dilithium_seed_entropy(self):
        """Test entropy of Dilithium seed generation."""
        det_key, pqc_seed = generate_hybrid_key(PQCAlgorithm.DILITHIUM3)
        
        combined = det_key + pqc_seed
        analyzer = EntropyAnalyzer(combined)
        
        results = analyzer.comprehensive_analysis()
        # Combined key should have reasonable entropy
        self.assertGreater(results['shannon_entropy'], 5.0)
    
    def test_sphincs_seed_entropy(self):
        """Test entropy of SPHINCS+ seed generation."""
        det_key, pqc_seed = generate_hybrid_key(PQCAlgorithm.SPHINCS_PLUS_128F)
        
        # SPHINCS+ uses 48-byte seeds
        self.assertEqual(len(pqc_seed), 48)
        
        analyzer = EntropyAnalyzer(pqc_seed)
        entropy = analyzer.shannon_entropy()
        # Larger seed size helps improve entropy
        self.assertGreater(entropy, 5.0)
    
    def test_hybrid_key_stream_entropy(self):
        """Test entropy across stream of hybrid keys."""
        keys = generate_hybrid_key_stream(PQCAlgorithm.KYBER768, count=50)
        
        # Extract all deterministic keys and PQC seeds
        det_keys = [det_key for det_key, _ in keys]
        pqc_seeds = [pqc_seed for _, pqc_seed in keys]
        
        # Test deterministic key stream - aggregate entropy should be good
        det_results = analyze_key_stream(det_keys)
        if 'aggregate_analysis' in det_results:
            self.assertGreater(det_results['aggregate_analysis']['shannon_entropy'], 6.5)
        
        # Test PQC seed stream - aggregate entropy should be good
        pqc_results = analyze_key_stream(pqc_seeds)
        if 'aggregate_analysis' in pqc_results:
            self.assertGreater(pqc_results['aggregate_analysis']['shannon_entropy'], 6.5)
    
    def test_pqc_seed_zero_bias(self):
        """Test PQC seeds for zero bias."""
        # Test multiple algorithms
        algorithms = [
            PQCAlgorithm.KYBER768,
            PQCAlgorithm.DILITHIUM3,
            PQCAlgorithm.SPHINCS_PLUS_128F
        ]
        
        for algorithm in algorithms:
            det_key, pqc_seed = generate_hybrid_key(algorithm)
            
            # Check both components
            det_result = validate_zero_bias(det_key)
            pqc_result = validate_zero_bias(pqc_seed)
            
            self.assertTrue(det_result['passes'],
                          f"{algorithm.value} det_key failed bias test")
            self.assertTrue(pqc_result['passes'],
                          f"{algorithm.value} pqc_seed failed bias test")


class TestIntegrationEntropy(unittest.TestCase):
    """Integration tests for entropy across the entire system."""
    
    def test_large_key_batch_entropy(self):
        """Test entropy on large batch of keys."""
        generator = universal_qkd_generator()
        keys = [next(generator) for _ in range(1000)]
        
        results = analyze_key_stream(keys)
        
        # Large batch should show excellent entropy
        self.assertEqual(results['aggregate_analysis']['overall_quality'], 'excellent')
        self.assertTrue(results['aggregate_analysis']['passes_all_tests'])
    
    def test_cross_algorithm_entropy_consistency(self):
        """Test that all algorithms produce consistent high entropy."""
        algorithms = [
            PQCAlgorithm.KYBER512,
            PQCAlgorithm.KYBER768,
            PQCAlgorithm.KYBER1024,
            PQCAlgorithm.DILITHIUM2,
            PQCAlgorithm.DILITHIUM3,
            PQCAlgorithm.DILITHIUM5,
            PQCAlgorithm.SPHINCS_PLUS_128F,
        ]
        
        for algorithm in algorithms:
            keys = generate_hybrid_key_stream(algorithm, count=50)
            pqc_seeds = [pqc_seed for _, pqc_seed in keys]
            
            results = analyze_key_stream(pqc_seeds)
            
            # All algorithms should produce high-entropy seeds
            self.assertGreater(
                results['aggregate_analysis']['shannon_entropy'],
                7.0,
                f"{algorithm.value} failed entropy requirement"
            )


if __name__ == '__main__':
    unittest.main()
