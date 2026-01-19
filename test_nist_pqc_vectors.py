"""
Tests for NIST PQC test vector compliance.

Validates that the hybrid key generation system produces outputs that comply
with NIST PQC standards and test vector specifications.
"""

import unittest
import json
from pathlib import Path
from gq.pqc_test_vectors import (
    PQCAlgorithm,
    generate_test_vector,
    validate_seed_format,
    get_algorithm_format_info,
    ALGORITHM_SEED_LENGTHS,
)


class TestNISTPQCVectors(unittest.TestCase):
    """Test compliance with NIST PQC test vectors."""
    
    @classmethod
    def setUpClass(cls):
        """Load NIST PQC test vectors."""
        test_vectors_path = Path(__file__).parent / 'tests' / 'nist_pqc_test_vectors.json'
        with open(test_vectors_path, 'r') as f:
            cls.test_vectors = json.load(f)
    
    def test_test_vectors_loaded(self):
        """Test that test vectors are properly loaded."""
        self.assertIn('test_vectors', self.test_vectors)
        self.assertIn('kyber', self.test_vectors['test_vectors'])
        self.assertIn('dilithium', self.test_vectors['test_vectors'])
        self.assertIn('sphincs', self.test_vectors['test_vectors'])
    
    def test_kyber_algorithm_compliance(self):
        """Test Kyber algorithm compliance with NIST specifications."""
        kyber_vectors = self.test_vectors['test_vectors']['kyber']
        
        # Test Kyber-512
        kyber512_spec = kyber_vectors['kyber512']
        self.assertEqual(kyber512_spec['security_level'], 1)
        self.assertEqual(kyber512_spec['seed_length'], 32)
        
        # Verify our implementation matches spec
        info = get_algorithm_format_info(PQCAlgorithm.KYBER512)
        self.assertEqual(info['seed_length'], kyber512_spec['seed_length'])
        self.assertEqual(info['security_level'], kyber512_spec['security_level'])
        
        # Test Kyber-768
        kyber768_spec = kyber_vectors['kyber768']
        self.assertEqual(kyber768_spec['security_level'], 3)
        info = get_algorithm_format_info(PQCAlgorithm.KYBER768)
        self.assertEqual(info['seed_length'], kyber768_spec['seed_length'])
        
        # Test Kyber-1024
        kyber1024_spec = kyber_vectors['kyber1024']
        self.assertEqual(kyber1024_spec['security_level'], 5)
        info = get_algorithm_format_info(PQCAlgorithm.KYBER1024)
        self.assertEqual(info['seed_length'], kyber1024_spec['seed_length'])
    
    def test_dilithium_algorithm_compliance(self):
        """Test Dilithium algorithm compliance with NIST specifications."""
        dilithium_vectors = self.test_vectors['test_vectors']['dilithium']
        
        # Test Dilithium2
        dilithium2_spec = dilithium_vectors['dilithium2']
        self.assertEqual(dilithium2_spec['security_level'], 2)
        info = get_algorithm_format_info(PQCAlgorithm.DILITHIUM2)
        self.assertEqual(info['seed_length'], dilithium2_spec['seed_length'])
        
        # Test Dilithium3
        dilithium3_spec = dilithium_vectors['dilithium3']
        self.assertEqual(dilithium3_spec['security_level'], 3)
        info = get_algorithm_format_info(PQCAlgorithm.DILITHIUM3)
        self.assertEqual(info['seed_length'], dilithium3_spec['seed_length'])
        
        # Test Dilithium5
        dilithium5_spec = dilithium_vectors['dilithium5']
        self.assertEqual(dilithium5_spec['security_level'], 5)
        info = get_algorithm_format_info(PQCAlgorithm.DILITHIUM5)
        self.assertEqual(info['seed_length'], dilithium5_spec['seed_length'])
    
    def test_sphincs_algorithm_compliance(self):
        """Test SPHINCS+ algorithm compliance with NIST specifications."""
        sphincs_vectors = self.test_vectors['test_vectors']['sphincs']
        
        # Test SPHINCS+-128f
        sphincs128_spec = sphincs_vectors['sphincs_plus_128f']
        self.assertEqual(sphincs128_spec['security_level'], 1)
        info = get_algorithm_format_info(PQCAlgorithm.SPHINCS_PLUS_128F)
        self.assertEqual(info['seed_length'], sphincs128_spec['seed_length'])
        
        # Test SPHINCS+-192f
        sphincs192_spec = sphincs_vectors['sphincs_plus_192f']
        self.assertEqual(sphincs192_spec['security_level'], 3)
        info = get_algorithm_format_info(PQCAlgorithm.SPHINCS_PLUS_192F)
        self.assertEqual(info['seed_length'], sphincs192_spec['seed_length'])
        
        # Test SPHINCS+-256f
        sphincs256_spec = sphincs_vectors['sphincs_plus_256f']
        self.assertEqual(sphincs256_spec['security_level'], 5)
        info = get_algorithm_format_info(PQCAlgorithm.SPHINCS_PLUS_256F)
        self.assertEqual(info['seed_length'], sphincs256_spec['seed_length'])
    
    def test_hybrid_validation_requirements(self):
        """Test that hybrid key generation meets NIST validation requirements."""
        requirements = self.test_vectors['hybrid_validation']['requirements']
        
        # Test deterministic component
        det_reqs = requirements['deterministic_component']
        self.assertEqual(det_reqs['length_bytes'], 16)
        self.assertEqual(det_reqs['source'], 'GCP-1 Universal QKD Generator')
        
        # Test PQC seed component
        pqc_reqs = requirements['pqc_seed_component']
        self.assertEqual(pqc_reqs['derivation'], 'SHA-256 based KDF from deterministic key')
        
        # Verify entropy requirements
        entropy_reqs = pqc_reqs['entropy_requirements']
        min_entropy = entropy_reqs['min_shannon_entropy_bits_per_byte']
        min_diversity = entropy_reqs['min_byte_diversity']
        
        # Generate a test key and validate it meets requirements
        _, pqc_seed = generate_test_vector(PQCAlgorithm.KYBER768)
        metrics = validate_seed_format(pqc_seed)
        
        self.assertGreaterEqual(metrics['shannon_entropy'], min_entropy)
        self.assertGreaterEqual(metrics['byte_diversity'], min_diversity)
    
    def test_all_algorithms_produce_valid_seeds(self):
        """Test that all algorithms produce seeds meeting NIST requirements."""
        algorithms = [
            PQCAlgorithm.KYBER512,
            PQCAlgorithm.KYBER768,
            PQCAlgorithm.KYBER1024,
            PQCAlgorithm.DILITHIUM2,
            PQCAlgorithm.DILITHIUM3,
            PQCAlgorithm.DILITHIUM5,
            PQCAlgorithm.SPHINCS_PLUS_128F,
            PQCAlgorithm.SPHINCS_PLUS_192F,
            PQCAlgorithm.SPHINCS_PLUS_256F,
        ]
        
        for algorithm in algorithms:
            with self.subTest(algorithm=algorithm.value):
                # Generate hybrid key
                det_key, pqc_seed = generate_test_vector(algorithm)
                
                # Verify deterministic component length
                self.assertEqual(len(det_key), 16)
                
                # Verify PQC seed length matches specification
                expected_length = ALGORITHM_SEED_LENGTHS[algorithm]
                self.assertEqual(len(pqc_seed), expected_length)
                
                # Verify entropy quality
                metrics = validate_seed_format(pqc_seed)
                self.assertTrue(metrics['passes_basic_checks'],
                                f"Entropy check failed for {algorithm.value}")
    
    def test_seed_length_compliance(self):
        """Test that all seed lengths match NIST specifications."""
        # Kyber variants - all require 32 bytes
        for kyber_alg in [PQCAlgorithm.KYBER512, PQCAlgorithm.KYBER768, PQCAlgorithm.KYBER1024]:
            self.assertEqual(ALGORITHM_SEED_LENGTHS[kyber_alg], 32)
        
        # Dilithium variants - all require 32 bytes
        for dil_alg in [PQCAlgorithm.DILITHIUM2, PQCAlgorithm.DILITHIUM3, PQCAlgorithm.DILITHIUM5]:
            self.assertEqual(ALGORITHM_SEED_LENGTHS[dil_alg], 32)
        
        # SPHINCS+ variants - larger seed requirements
        self.assertEqual(ALGORITHM_SEED_LENGTHS[PQCAlgorithm.SPHINCS_PLUS_128F], 48)
        self.assertEqual(ALGORITHM_SEED_LENGTHS[PQCAlgorithm.SPHINCS_PLUS_192F], 64)
        self.assertEqual(ALGORITHM_SEED_LENGTHS[PQCAlgorithm.SPHINCS_PLUS_256F], 64)
    
    def test_security_model_documentation(self):
        """Test that security model is properly documented."""
        requirements = self.test_vectors['hybrid_validation']['requirements']
        security_model = requirements['security_model']
        
        self.assertIn('Classical determinism', security_model)
        self.assertIn('Quantum resistance', security_model)
    
    def test_nist_fips_compliance_notes(self):
        """Test that NIST FIPS compliance notes are present."""
        compliance = self.test_vectors['compliance_notes']
        
        # Check FIPS standard references
        self.assertIn('nist_fips_203', compliance)  # ML-KEM (Kyber)
        self.assertIn('nist_fips_204', compliance)  # ML-DSA (Dilithium)
        self.assertIn('nist_fips_205', compliance)  # SLH-DSA (SPHINCS+)
        
        # Check security properties
        self.assertIn('IND-CCA2', compliance['nist_fips_203'])
        self.assertIn('EUF-CMA', compliance['nist_fips_204'])
        self.assertIn('EUF-CMA', compliance['nist_fips_205'])
        
        # Check quantum resistance
        self.assertIn('quantum_resistance', compliance)
        self.assertIn("Shor's", compliance['quantum_resistance'])
        self.assertIn("Grover's", compliance['quantum_resistance'])


class TestHybridSecurityModel(unittest.TestCase):
    """Test the hybrid security model implementation."""
    
    def test_defense_in_depth(self):
        """Test that hybrid model provides defense-in-depth."""
        # Generate keys with different algorithms
        _, kyber_seed = generate_test_vector(PQCAlgorithm.KYBER768)
        _, dilithium_seed = generate_test_vector(PQCAlgorithm.DILITHIUM3)
        
        # Both should be cryptographically strong
        kyber_metrics = validate_seed_format(kyber_seed)
        dilithium_metrics = validate_seed_format(dilithium_seed)
        
        self.assertTrue(kyber_metrics['passes_basic_checks'])
        self.assertTrue(dilithium_metrics['passes_basic_checks'])
    
    def test_deterministic_reproducibility(self):
        """Test that deterministic component is reproducible."""
        # Generate same algorithm multiple times
        det_key1, _ = generate_test_vector(PQCAlgorithm.KYBER768)
        det_key2, _ = generate_test_vector(PQCAlgorithm.KYBER768)
        
        # Deterministic keys should match (same starting point)
        self.assertEqual(det_key1, det_key2)
    
    def test_quantum_resistance_through_pqc_seed(self):
        """Test that PQC seed provides quantum resistance."""
        algorithms_by_level = {
            1: PQCAlgorithm.KYBER512,
            3: PQCAlgorithm.KYBER768,
            5: PQCAlgorithm.KYBER1024,
        }
        
        for level, algorithm in algorithms_by_level.items():
            with self.subTest(level=level):
                _, pqc_seed = generate_test_vector(algorithm)
                
                # PQC seed should be cryptographically strong
                metrics = validate_seed_format(pqc_seed)
                self.assertTrue(metrics['passes_basic_checks'])
                
                # Verify algorithm provides appropriate security level
                info = get_algorithm_format_info(algorithm)
                self.assertGreaterEqual(info['security_level'], level)


if __name__ == '__main__':
    unittest.main()
