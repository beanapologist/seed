"""
Unit tests for NIST Post-Quantum Cryptography (PQC) hybrid key generation.

Tests validate:
- Hybrid key generation for all supported NIST PQC algorithms
- Deterministic reproducibility
- Correct seed lengths for each algorithm
- Entropy quality of generated seeds
- Security level mappings
- Zero-bias validation
"""

import unittest
from gq.pqc_test_vectors import (
    PQCAlgorithm,
    PQCSecurityLevel,
    generate_test_vector,
    generate_test_vector_stream,
    generate_kyber_test_seed,
    generate_dilithium_test_seed,
    generate_sphincs_test_seed,
    validate_seed_format,
    get_algorithm_format_info,
    ALGORITHM_SECURITY_LEVELS,
    ALGORITHM_SEED_LENGTHS,
)
from gq.entropy_testing import validate_zero_bias


class TestPQCAlgorithms(unittest.TestCase):
    """Test NIST PQC algorithm definitions and mappings."""
    
    def test_algorithm_enum_values(self):
        """Test that all PQC algorithms are properly defined."""
        expected_algorithms = {
            'Kyber-512', 'Kyber-768', 'Kyber-1024',
            'Dilithium2', 'Dilithium3', 'Dilithium5',
            'SPHINCS+-128f', 'SPHINCS+-192f', 'SPHINCS+-256f'
        }
        actual_algorithms = {alg.value for alg in PQCAlgorithm}
        self.assertEqual(actual_algorithms, expected_algorithms)
    
    def test_security_level_enum(self):
        """Test that security levels are properly defined."""
        levels = [level.value for level in PQCSecurityLevel]
        self.assertEqual(levels, [1, 2, 3, 4, 5])
    
    def test_all_algorithms_have_security_levels(self):
        """Test that all algorithms have assigned security levels."""
        for algorithm in PQCAlgorithm:
            self.assertIn(algorithm, ALGORITHM_SECURITY_LEVELS)
            self.assertIsInstance(ALGORITHM_SECURITY_LEVELS[algorithm], PQCSecurityLevel)
    
    def test_all_algorithms_have_seed_lengths(self):
        """Test that all algorithms have defined seed lengths."""
        for algorithm in PQCAlgorithm:
            self.assertIn(algorithm, ALGORITHM_SEED_LENGTHS)
            length = ALGORITHM_SEED_LENGTHS[algorithm]
            self.assertIsInstance(length, int)
            self.assertGreater(length, 0)
    
    def test_kyber_security_levels(self):
        """Test Kyber algorithm security level mappings."""
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.KYBER512], PQCSecurityLevel.LEVEL_1)
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.KYBER768], PQCSecurityLevel.LEVEL_3)
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.KYBER1024], PQCSecurityLevel.LEVEL_5)
    
    def test_dilithium_security_levels(self):
        """Test Dilithium algorithm security level mappings."""
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.DILITHIUM2], PQCSecurityLevel.LEVEL_2)
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.DILITHIUM3], PQCSecurityLevel.LEVEL_3)
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.DILITHIUM5], PQCSecurityLevel.LEVEL_5)
    
    def test_sphincs_security_levels(self):
        """Test SPHINCS+ algorithm security level mappings."""
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.SPHINCS_PLUS_128F], PQCSecurityLevel.LEVEL_1)
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.SPHINCS_PLUS_192F], PQCSecurityLevel.LEVEL_3)
        self.assertEqual(ALGORITHM_SECURITY_LEVELS[PQCAlgorithm.SPHINCS_PLUS_256F], PQCSecurityLevel.LEVEL_5)


class TestHybridKeyGeneration(unittest.TestCase):
    """Test hybrid key generation combining GCP-1 with PQC algorithms."""
    
    def test_generate_kyber512_seed(self):
        """Test Kyber-512 hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.KYBER512)
        self.assertEqual(len(det_key), 16)  # GCP-1 produces 16-byte keys
        self.assertEqual(len(pqc_seed), 32)  # Kyber needs 32-byte seed
        self.assertIsInstance(det_key, bytes)
        self.assertIsInstance(pqc_seed, bytes)
    
    def test_generate_kyber768_seed(self):
        """Test Kyber-768 hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.KYBER768)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
        
        # Validate zero bias
        self.assertTrue(validate_zero_bias(det_key)['passes'])
        self.assertTrue(validate_zero_bias(pqc_seed)['passes'])
    
    def test_generate_kyber1024_seed(self):
        """Test Kyber-1024 hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.KYBER1024)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
        
        # Validate zero bias
        self.assertTrue(validate_zero_bias(det_key)['passes'])
        self.assertTrue(validate_zero_bias(pqc_seed)['passes'])
    
    def test_generate_dilithium2_seed(self):
        """Test Dilithium2 hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.DILITHIUM2)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_dilithium3_seed(self):
        """Test Dilithium3 hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.DILITHIUM3)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_dilithium5_seed(self):
        """Test Dilithium5 hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.DILITHIUM5)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_sphincs_128f_seed(self):
        """Test SPHINCS+-128f hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.SPHINCS_PLUS_128F)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 48)
    
    def test_generate_sphincs_192f_seed(self):
        """Test SPHINCS+-192f hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.SPHINCS_PLUS_192F)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 64)
    
    def test_generate_sphincs_256f_seed(self):
        """Test SPHINCS+-256f hybrid key generation."""
        det_key, pqc_seed = generate_test_vector(PQCAlgorithm.SPHINCS_PLUS_256F)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 64)
    
    def test_deterministic_generation(self):
        """Test that hybrid key generation is deterministic."""
        det_key1, pqc_seed1 = generate_test_vector(PQCAlgorithm.KYBER768)
        det_key2, pqc_seed2 = generate_test_vector(PQCAlgorithm.KYBER768)
        
        # First keys should match (deterministic)
        self.assertEqual(det_key1, det_key2)
        self.assertEqual(pqc_seed1, pqc_seed2)
    
    def test_context_affects_pqc_seed(self):
        """Test that context parameter affects PQC seed derivation."""
        det_key1, pqc_seed1 = generate_test_vector(PQCAlgorithm.KYBER768, context=b"CONTEXT_A")
        det_key2, pqc_seed2 = generate_test_vector(PQCAlgorithm.KYBER768, context=b"CONTEXT_B")
        
        # Different contexts should produce different PQC seeds
        # (deterministic keys will be the same due to generator reset)
        self.assertNotEqual(pqc_seed1, pqc_seed2)
    
    def test_different_algorithms_produce_different_seeds(self):
        """Test that different algorithms produce different PQC seeds."""
        _, kyber_seed = generate_test_vector(PQCAlgorithm.KYBER768)
        _, dilithium_seed = generate_test_vector(PQCAlgorithm.DILITHIUM3)
        
        # Different algorithms should produce different seeds
        self.assertNotEqual(kyber_seed, dilithium_seed)


class TestHybridKeyStream(unittest.TestCase):
    """Test hybrid key stream generation."""
    
    def test_generate_key_stream(self):
        """Test generating multiple hybrid keys."""
        keys = generate_test_vector_stream(PQCAlgorithm.KYBER768, count=5)
        self.assertEqual(len(keys), 5)
        
        # Verify each key pair
        for det_key, pqc_seed in keys:
            self.assertEqual(len(det_key), 16)
            self.assertEqual(len(pqc_seed), 32)
    
    def test_key_stream_uniqueness(self):
        """Test that key stream produces unique keys."""
        keys = generate_test_vector_stream(PQCAlgorithm.KYBER768, count=10)
        
        # All deterministic keys should be unique
        det_keys = [k[0] for k in keys]
        self.assertEqual(len(set(det_keys)), 10)
        
        # All PQC seeds should be unique
        pqc_seeds = [k[1] for k in keys]
        self.assertEqual(len(set(pqc_seeds)), 10)
    
    def test_single_key_stream(self):
        """Test generating a single key via stream."""
        keys = generate_test_vector_stream(PQCAlgorithm.DILITHIUM3, count=1)
        self.assertEqual(len(keys), 1)
        det_key, pqc_seed = keys[0]
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_key_stream_with_context(self):
        """Test key stream generation with context."""
        keys = generate_test_vector_stream(
            PQCAlgorithm.KYBER768,
            count=3,
            context=b"TEST_CONTEXT"
        )
        self.assertEqual(len(keys), 3)
        
        # Verify all keys are properly generated
        for det_key, pqc_seed in keys:
            self.assertEqual(len(det_key), 16)
            self.assertEqual(len(pqc_seed), 32)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions for specific algorithms."""
    
    def test_generate_kyber_seed_default(self):
        """Test Kyber seed generation with default level."""
        det_key, pqc_seed = generate_kyber_test_seed()
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_kyber_seed_512(self):
        """Test Kyber-512 seed generation."""
        det_key, pqc_seed = generate_kyber_test_seed(level=512)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_kyber_seed_768(self):
        """Test Kyber-768 seed generation."""
        det_key, pqc_seed = generate_kyber_test_seed(level=768)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_kyber_seed_1024(self):
        """Test Kyber-1024 seed generation."""
        det_key, pqc_seed = generate_kyber_test_seed(level=1024)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_dilithium_seed_default(self):
        """Test Dilithium seed generation with default level."""
        det_key, pqc_seed = generate_dilithium_test_seed()
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_dilithium_seed_2(self):
        """Test Dilithium2 seed generation."""
        det_key, pqc_seed = generate_dilithium_test_seed(level=2)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_dilithium_seed_3(self):
        """Test Dilithium3 seed generation."""
        det_key, pqc_seed = generate_dilithium_test_seed(level=3)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_dilithium_seed_5(self):
        """Test Dilithium5 seed generation."""
        det_key, pqc_seed = generate_dilithium_test_seed(level=5)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32)
    
    def test_generate_sphincs_seed_default(self):
        """Test SPHINCS+ seed generation with default level."""
        det_key, pqc_seed = generate_sphincs_test_seed()
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 48)
    
    def test_generate_sphincs_seed_128(self):
        """Test SPHINCS+-128f seed generation."""
        det_key, pqc_seed = generate_sphincs_test_seed(level=128)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 48)
    
    def test_generate_sphincs_seed_192(self):
        """Test SPHINCS+-192f seed generation."""
        det_key, pqc_seed = generate_sphincs_test_seed(level=192)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 64)
    
    def test_generate_sphincs_seed_256(self):
        """Test SPHINCS+-256f seed generation."""
        det_key, pqc_seed = generate_sphincs_test_seed(level=256)
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 64)


class TestEntropyValidation(unittest.TestCase):
    """Test entropy validation for PQC seed material."""
    
    def test_validate_good_entropy(self):
        """Test validation of high-quality entropy."""
        # Generate a real PQC seed
        _, pqc_seed = generate_test_vector(PQCAlgorithm.KYBER768)
        metrics = validate_seed_format(pqc_seed)
        
        self.assertIn('shannon_entropy', metrics)
        self.assertIn('byte_diversity', metrics)
        self.assertIn('passes_basic_checks', metrics)
        
        # SHA-256 output should have reasonable entropy for the seed size
        # For 32-byte seeds, we expect at least 4 bits per byte
        self.assertGreater(metrics['shannon_entropy'], 4.0)
        self.assertTrue(metrics['passes_basic_checks'])
    
    def test_validate_empty_seed(self):
        """Test validation of empty seed."""
        metrics = validate_seed_format(b'')
        self.assertEqual(metrics['shannon_entropy'], 0.0)
        self.assertEqual(metrics['byte_diversity'], 0.0)
        self.assertFalse(metrics['passes_basic_checks'])
    
    def test_validate_low_entropy(self):
        """Test validation of low-entropy seed."""
        # Create a low-entropy seed (all zeros)
        low_entropy_seed = b'\x00' * 32
        metrics = validate_seed_format(low_entropy_seed)
        
        # All zeros should have 0 entropy
        self.assertEqual(metrics['shannon_entropy'], 0.0)
        self.assertFalse(metrics['passes_basic_checks'])
    
    def test_validate_different_lengths(self):
        """Test entropy validation with different seed lengths."""
        for algorithm in [PQCAlgorithm.KYBER768, PQCAlgorithm.SPHINCS_PLUS_128F, PQCAlgorithm.SPHINCS_PLUS_256F]:
            _, pqc_seed = generate_test_vector(algorithm)
            metrics = validate_seed_format(pqc_seed)
            
            # All generated seeds should pass quality checks
            self.assertTrue(metrics['passes_basic_checks'],
                            f"Failed for {algorithm.value}")


class TestAlgorithmInfo(unittest.TestCase):
    """Test algorithm information retrieval."""
    
    def test_get_kyber768_info(self):
        """Test getting Kyber-768 algorithm information."""
        info = get_algorithm_format_info(PQCAlgorithm.KYBER768)
        
        self.assertEqual(info['name'], 'Kyber-768')
        self.assertEqual(info['security_level'], 3)
        self.assertEqual(info['seed_length'], 32)
        self.assertEqual(info['type'], 'KEM')
    
    def test_get_dilithium3_info(self):
        """Test getting Dilithium3 algorithm information."""
        info = get_algorithm_format_info(PQCAlgorithm.DILITHIUM3)
        
        self.assertEqual(info['name'], 'Dilithium3')
        self.assertEqual(info['security_level'], 3)
        self.assertEqual(info['seed_length'], 32)
        self.assertEqual(info['type'], 'Signature')
    
    def test_get_sphincs_info(self):
        """Test getting SPHINCS+ algorithm information."""
        info = get_algorithm_format_info(PQCAlgorithm.SPHINCS_PLUS_256F)
        
        self.assertEqual(info['name'], 'SPHINCS+-256f')
        self.assertEqual(info['security_level'], 5)
        self.assertEqual(info['seed_length'], 64)
        self.assertEqual(info['type'], 'Signature')
    
    def test_all_algorithms_have_info(self):
        """Test that all algorithms can return info."""
        for algorithm in PQCAlgorithm:
            info = get_algorithm_format_info(algorithm)
            
            self.assertIn('name', info)
            self.assertIn('security_level', info)
            self.assertIn('seed_length', info)
            self.assertIn('type', info)
            
            # Verify types are correct
            self.assertIsInstance(info['name'], str)
            self.assertIsInstance(info['security_level'], int)
            self.assertIsInstance(info['seed_length'], int)
            self.assertIn(info['type'], ['KEM', 'Signature'])


class TestNISTPQCIntegration(unittest.TestCase):
    """Integration tests for NIST PQC functionality."""
    
    def test_full_kyber_workflow(self):
        """Test complete workflow for Kyber key generation."""
        # Generate hybrid key
        det_key, pqc_seed = generate_kyber_test_seed(level=768, context=b"KEYGEN")
        
        # Validate seed quality
        metrics = validate_seed_format(pqc_seed)
        self.assertTrue(metrics['passes_basic_checks'])
        
        # Get algorithm info
        info = get_algorithm_format_info(PQCAlgorithm.KYBER768)
        self.assertEqual(len(pqc_seed), info['seed_length'])
    
    def test_full_dilithium_workflow(self):
        """Test complete workflow for Dilithium signature generation."""
        # Generate hybrid key
        det_key, pqc_seed = generate_dilithium_test_seed(level=3, context=b"SIGN")
        
        # Validate seed quality
        metrics = validate_seed_format(pqc_seed)
        self.assertTrue(metrics['passes_basic_checks'])
        
        # Get algorithm info
        info = get_algorithm_format_info(PQCAlgorithm.DILITHIUM3)
        self.assertEqual(info['type'], 'Signature')
    
    def test_multiple_algorithm_generation(self):
        """Test generating seeds for multiple algorithms in sequence."""
        algorithms = [
            PQCAlgorithm.KYBER768,
            PQCAlgorithm.DILITHIUM3,
            PQCAlgorithm.SPHINCS_PLUS_128F
        ]
        
        seeds = {}
        for algorithm in algorithms:
            det_key, pqc_seed = generate_test_vector(algorithm, context=b"MULTI")
            seeds[algorithm] = (det_key, pqc_seed)
            
            # Validate each seed
            metrics = validate_seed_format(pqc_seed)
            self.assertTrue(metrics['passes_basic_checks'])
        
        # Verify all seeds are unique
        all_pqc_seeds = [s[1] for s in seeds.values()]
        self.assertEqual(len(set(all_pqc_seeds)), len(algorithms))


if __name__ == '__main__':
    unittest.main()
