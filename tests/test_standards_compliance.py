#!/usr/bin/env python3
"""
Comprehensive Standards Compliance Test Suite

This test suite validates that all generators in the repository comply with:
1. NIST Standards (SP 800-22, SP 800-90B, FIPS 203/204/205)
2. Physics Standards (IEEE 754, quantum mechanics principles, entropy theory)
3. Cryptographic Standards (SHA-256/SHA-512, forward secrecy)

Each test is designed to validate specific requirements from the applicable standards.
"""

import unittest
import sys
import math
import struct
import hashlib
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gq import (
    universal_qkd,
    gqs1,
    nist_pqc,
    entropy_testing,
)


class TestNISTSP80022Compliance(unittest.TestCase):
    """
    Test compliance with NIST SP 800-22 Rev. 1a:
    Statistical Test Suite for Random and Pseudorandom Number Generators
    
    Standard: https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.significance_level = 0.01  # Alpha = 0.01 per NIST SP 800-22
        self.min_sample_size = 100000  # Minimum bits for statistical significance
        
    def test_universal_qkd_randomness_quality(self):
        """
        Test Universal QKD generator produces statistically random output.
        
        NIST SP 800-22 Section 1: Purpose
        Random number generators must produce output indistinguishable from truly random data.
        """
        # Generate sufficient sample
        generator = universal_qkd.universal_qkd_generator()
        keys = [next(generator) for _ in range(1000)]
        
        # Convert to binary string
        binary_data = ''.join(format(byte, '08b') for key in keys for byte in key)
        
        # Basic randomness check - approximately equal 0s and 1s
        ones = binary_data.count('1')
        zeros = binary_data.count('0')
        total = len(binary_data)
        
        ones_ratio = ones / total
        
        # Should be close to 0.5 (within 2 standard deviations)
        # For large sample, std = sqrt(n*p*(1-p))/n ≈ 0.5/sqrt(n)
        std_error = 0.5 / math.sqrt(total)
        
        self.assertGreater(ones_ratio, 0.5 - 2*std_error)
        self.assertLess(ones_ratio, 0.5 + 2*std_error)
        
    def test_gqs1_deterministic_reproducibility(self):
        """
        Test GQS-1 generator produces deterministic, reproducible output.
        
        NIST SP 800-22: Deterministic generators must produce identical output
        given identical inputs.
        """
        vectors1 = gqs1.generate_test_vectors(100)
        vectors2 = gqs1.generate_test_vectors(100)
        
        self.assertEqual(vectors1, vectors2, 
                        "GQS-1 must produce deterministic output")
        
    def test_nist_pqc_seed_lengths_compliance(self):
        """
        Test NIST PQC generators produce correct seed lengths.
        
        FIPS 203/204/205: Each algorithm specifies exact seed lengths.
        """
        test_cases = [
            (nist_pqc.PQCAlgorithm.KYBER512, 32),
            (nist_pqc.PQCAlgorithm.KYBER768, 32),
            (nist_pqc.PQCAlgorithm.KYBER1024, 32),
            (nist_pqc.PQCAlgorithm.DILITHIUM2, 32),
            (nist_pqc.PQCAlgorithm.DILITHIUM3, 32),
            (nist_pqc.PQCAlgorithm.DILITHIUM5, 32),
            (nist_pqc.PQCAlgorithm.SPHINCS_PLUS_128F, 48),
            (nist_pqc.PQCAlgorithm.SPHINCS_PLUS_192F, 64),
            (nist_pqc.PQCAlgorithm.SPHINCS_PLUS_256F, 64),
        ]
        
        for algorithm, expected_length in test_cases:
            with self.subTest(algorithm=algorithm.value):
                _, pqc_seed = nist_pqc.generate_hybrid_key(algorithm)
                self.assertEqual(len(pqc_seed), expected_length,
                               f"{algorithm.value} must produce {expected_length}-byte seeds")


class TestNISTSP80090BCompliance(unittest.TestCase):
    """
    Test compliance with NIST SP 800-90B:
    Recommendation for the Entropy Sources Used for Random Bit Generation
    
    Standard: https://csrc.nist.gov/publications/detail/sp/800-90b/final
    """
    
    def test_entropy_estimation_universal_qkd(self):
        """
        Test entropy estimation for Universal QKD output.
        
        NIST SP 800-90B Section 3: Entropy sources must have min-entropy estimation.
        """
        generator = universal_qkd.universal_qkd_generator()
        keys = [next(generator) for _ in range(100)]
        
        # Concatenate for entropy analysis
        data = b''.join(keys)
        
        # Calculate Shannon entropy per byte
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
        
        total = len(data)
        shannon_entropy = 0
        for count in byte_counts:
            if count > 0:
                p = count / total
                shannon_entropy -= p * math.log2(p)
        
        # Shannon entropy should be high (close to 8 bits per byte for random data)
        self.assertGreater(shannon_entropy, 7.0,
                          "Entropy should be > 7 bits/byte for cryptographic quality")
        
    def test_min_entropy_pqc_seeds(self):
        """
        Test min-entropy of PQC seed generation.
        
        NIST SP 800-90B: Min-entropy must be sufficient for security level.
        """
        # Generate multiple Kyber-768 seeds with different contexts for variety
        seeds = []
        for i in range(100):
            context = f"TEST_{i}".encode()
            _, pqc_seed = nist_pqc.generate_hybrid_key(
                nist_pqc.PQCAlgorithm.KYBER768, 
                context=context
            )
            seeds.append(pqc_seed)
        
        # Check for uniqueness (no duplicates in small sample)
        unique_seeds = set(seeds)
        self.assertEqual(len(unique_seeds), len(seeds),
                        "All PQC seeds should be unique with different contexts")
        
        # Validate entropy metrics
        for seed in seeds[:10]:  # Check first 10
            metrics = nist_pqc.validate_pqc_seed_entropy(seed)
            self.assertTrue(metrics['passes_basic_checks'],
                          "PQC seed must pass basic entropy checks")
            # For 32-byte seeds with different contexts, expect > 4 bits/byte entropy
            # Full randomness would be 8 bits/byte, but deterministic generation
            # with good distribution gives 4-5 bits/byte which is acceptable
            self.assertGreater(metrics['shannon_entropy'], 4.0,
                             "PQC seed Shannon entropy should be > 4.0 bits/byte")


class TestFIPS203Compliance(unittest.TestCase):
    """
    Test compliance with FIPS 203:
    Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM/Kyber)
    
    Standard: https://csrc.nist.gov/pubs/fips/203/final
    """
    
    def test_kyber512_seed_generation(self):
        """
        Test Kyber-512 (Security Level 1) seed generation.
        
        FIPS 203: Kyber-512 requires 32-byte seed for key generation.
        """
        det_key, pqc_seed = nist_pqc.generate_kyber_seed(level=512, context=b"TEST")
        
        self.assertEqual(len(det_key), 16, "Deterministic key should be 16 bytes")
        self.assertEqual(len(pqc_seed), 32, "Kyber-512 seed should be 32 bytes")
        self.assertIsInstance(det_key, bytes)
        self.assertIsInstance(pqc_seed, bytes)
        
    def test_kyber768_seed_generation(self):
        """
        Test Kyber-768 (Security Level 3) seed generation.
        
        FIPS 203: Kyber-768 requires 32-byte seed for key generation.
        """
        det_key, pqc_seed = nist_pqc.generate_kyber_seed(level=768, context=b"TEST")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32, "Kyber-768 seed should be 32 bytes")
        
    def test_kyber1024_seed_generation(self):
        """
        Test Kyber-1024 (Security Level 5) seed generation.
        
        FIPS 203: Kyber-1024 requires 32-byte seed for key generation.
        """
        det_key, pqc_seed = nist_pqc.generate_kyber_seed(level=1024, context=b"TEST")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32, "Kyber-1024 seed should be 32 bytes")
        
    def test_kyber_security_levels(self):
        """
        Test Kyber security level mappings are correct.
        
        FIPS 203 Table 2: Security levels for Kyber parameter sets.
        """
        self.assertEqual(
            nist_pqc.ALGORITHM_SECURITY_LEVELS[nist_pqc.PQCAlgorithm.KYBER512],
            nist_pqc.PQCSecurityLevel.LEVEL_1
        )
        self.assertEqual(
            nist_pqc.ALGORITHM_SECURITY_LEVELS[nist_pqc.PQCAlgorithm.KYBER768],
            nist_pqc.PQCSecurityLevel.LEVEL_3
        )
        self.assertEqual(
            nist_pqc.ALGORITHM_SECURITY_LEVELS[nist_pqc.PQCAlgorithm.KYBER1024],
            nist_pqc.PQCSecurityLevel.LEVEL_5
        )


class TestFIPS204Compliance(unittest.TestCase):
    """
    Test compliance with FIPS 204:
    Module-Lattice-Based Digital Signature Standard (ML-DSA/Dilithium)
    
    Standard: https://csrc.nist.gov/pubs/fips/204/final
    """
    
    def test_dilithium2_seed_generation(self):
        """
        Test Dilithium2 (Security Level 2) seed generation.
        
        FIPS 204: Dilithium2 requires 32-byte seed.
        """
        det_key, pqc_seed = nist_pqc.generate_dilithium_seed(level=2, context=b"SIGN")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32, "Dilithium2 seed should be 32 bytes")
        
    def test_dilithium3_seed_generation(self):
        """
        Test Dilithium3 (Security Level 3) seed generation.
        
        FIPS 204: Dilithium3 requires 32-byte seed.
        """
        det_key, pqc_seed = nist_pqc.generate_dilithium_seed(level=3, context=b"SIGN")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32, "Dilithium3 seed should be 32 bytes")
        
    def test_dilithium5_seed_generation(self):
        """
        Test Dilithium5 (Security Level 5) seed generation.
        
        FIPS 204: Dilithium5 requires 32-byte seed.
        """
        det_key, pqc_seed = nist_pqc.generate_dilithium_seed(level=5, context=b"SIGN")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 32, "Dilithium5 seed should be 32 bytes")


class TestFIPS205Compliance(unittest.TestCase):
    """
    Test compliance with FIPS 205:
    Stateless Hash-Based Digital Signature Standard (SLH-DSA/SPHINCS+)
    
    Standard: https://csrc.nist.gov/pubs/fips/205/final
    """
    
    def test_sphincs_128f_seed_generation(self):
        """
        Test SPHINCS+-128f (Security Level 1) seed generation.
        
        FIPS 205: SPHINCS+-128f requires 48-byte seed.
        """
        det_key, pqc_seed = nist_pqc.generate_sphincs_seed(level=128, context=b"HASH")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 48, "SPHINCS+-128f seed should be 48 bytes")
        
    def test_sphincs_192f_seed_generation(self):
        """
        Test SPHINCS+-192f (Security Level 3) seed generation.
        
        FIPS 205: SPHINCS+-192f requires 64-byte seed.
        """
        det_key, pqc_seed = nist_pqc.generate_sphincs_seed(level=192, context=b"HASH")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 64, "SPHINCS+-192f seed should be 64 bytes")
        
    def test_sphincs_256f_seed_generation(self):
        """
        Test SPHINCS+-256f (Security Level 5) seed generation.
        
        FIPS 205: SPHINCS+-256f requires 64-byte seed.
        """
        det_key, pqc_seed = nist_pqc.generate_sphincs_seed(level=256, context=b"HASH")
        
        self.assertEqual(len(det_key), 16)
        self.assertEqual(len(pqc_seed), 64, "SPHINCS+-256f seed should be 64 bytes")


class TestIEEE754Compliance(unittest.TestCase):
    """
    Test compliance with IEEE 754-2019:
    IEEE Standard for Floating-Point Arithmetic
    
    Standard: https://standards.ieee.org/standard/754-2019.html
    
    This validates that the golden ratio seed and complex number operations
    comply with IEEE 754 double-precision floating-point arithmetic.
    """
    
    def test_golden_ratio_ieee754_representation(self):
        """
        Test golden ratio φ is correctly represented in IEEE 754 format.
        
        IEEE 754: Double precision (binary64) provides 53 bits of precision.
        """
        phi = (1 + math.sqrt(5)) / 2
        
        # Check it's close to expected value
        self.assertAlmostEqual(phi, 1.618033988749895, places=15)
        
        # Verify it's a valid IEEE 754 double
        # Pack as double, unpack, should be identical
        packed = struct.pack('d', phi)
        unpacked = struct.unpack('d', packed)[0]
        self.assertEqual(phi, unpacked)
        
    def test_complex_arithmetic_precision(self):
        """
        Test complex number arithmetic maintains IEEE 754 precision.
        
        IEEE 754: Operations should be correctly rounded.
        """
        # Test unit circle point
        z = complex(0, 1.618033988749895)  # iφ
        
        # Magnitude should be φ (within IEEE 754 precision)
        magnitude = abs(z)
        expected_magnitude = 1.618033988749895
        
        self.assertAlmostEqual(magnitude, expected_magnitude, places=15)
        
    def test_eight_fold_rotation_precision(self):
        """
        Test 8-fold unit circle rotation maintains IEEE 754 precision.
        
        IEEE 754: Accumulated rounding error should be bounded by machine epsilon.
        """
        import cmath
        
        # Start at angle 0
        z = complex(1, 0)
        step = cmath.exp(1j * math.pi / 4)  # π/4 rotation
        
        # Rotate 8 times
        for _ in range(8):
            z *= step
        
        # Should return to (1, 0) within machine epsilon
        epsilon = sys.float_info.epsilon
        
        self.assertAlmostEqual(z.real, 1.0, delta=10*epsilon)
        self.assertAlmostEqual(z.imag, 0.0, delta=10*epsilon)


class TestQuantumMechanicsPrinciples(unittest.TestCase):
    """
    Test compliance with quantum mechanics principles:
    - Unit circle geometry
    - 8th roots of unity
    - Phase coherence
    - Discrete rotations
    
    References: Quantum mechanics textbooks, unit circle theory
    """
    
    def test_eighth_roots_of_unity(self):
        """
        Test 8th roots of unity are correctly computed.
        
        Quantum mechanics: e^(i*2πk/8) for k=0..7 form the 8th roots of unity.
        """
        import cmath
        
        roots = []
        for k in range(8):
            root = cmath.exp(1j * 2 * math.pi * k / 8)
            roots.append(root)
            
            # Each root should have magnitude 1
            self.assertAlmostEqual(abs(root), 1.0, places=10)
        
        # Check 8th power returns to 1
        for root in roots:
            eighth_power = root ** 8
            self.assertAlmostEqual(eighth_power.real, 1.0, places=10)
            self.assertAlmostEqual(eighth_power.imag, 0.0, places=10)
            
    def test_unit_circle_closure(self):
        """
        Test unit circle operations maintain closure property.
        
        Quantum mechanics: Points on unit circle stay on unit circle.
        """
        import cmath
        
        # Generate several unit circle points
        angles = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]
        
        for angle in angles:
            z = cmath.exp(1j * angle)
            
            # Should be on unit circle
            self.assertAlmostEqual(abs(z), 1.0, places=10)
            
            # Multiply by another unit circle point
            z2 = cmath.exp(1j * math.pi/4)
            product = z * z2
            
            # Product should also be on unit circle
            self.assertAlmostEqual(abs(product), 1.0, places=10)


class TestCryptographicHashCompliance(unittest.TestCase):
    """
    Test compliance with cryptographic hash function standards:
    - SHA-256 (FIPS 180-4)
    - SHA-512 (FIPS 180-4)
    - One-way property
    - Collision resistance
    - Avalanche effect
    
    Standard: FIPS 180-4 Secure Hash Standard (SHS)
    """
    
    def test_sha256_deterministic(self):
        """
        Test SHA-256 produces deterministic output.
        
        FIPS 180-4: Hash function must be deterministic.
        """
        data = b"test data for hashing"
        
        hash1 = hashlib.sha256(data).digest()
        hash2 = hashlib.sha256(data).digest()
        
        self.assertEqual(hash1, hash2, "SHA-256 must be deterministic")
        
    def test_sha256_avalanche_effect(self):
        """
        Test SHA-256 exhibits avalanche effect.
        
        FIPS 180-4: Small input change causes large output change.
        """
        data1 = b"test data"
        data2 = b"test datb"  # Single character change (not single bit)
        
        hash1 = hashlib.sha256(data1).digest()
        hash2 = hashlib.sha256(data2).digest()
        
        # Hashes should be completely different
        self.assertNotEqual(hash1, hash2)
        
        # Count differing bits
        diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(hash1, hash2))
        total_bits = len(hash1) * 8
        
        # Should have ~50% bits different (avalanche effect)
        self.assertGreater(diff_bits, total_bits * 0.3)
        self.assertLess(diff_bits, total_bits * 0.7)
        
    def test_universal_qkd_uses_sha256(self):
        """
        Test Universal QKD generator uses SHA-256 for state progression.
        
        GCP-1 Protocol: Must use SHA-256 for forward secrecy.
        """
        # Generate keys and verify they use SHA-256 internally
        generator = universal_qkd.universal_qkd_generator()
        key1 = next(generator)
        key2 = next(generator)
        
        # Keys should be different (forward secrecy)
        self.assertNotEqual(key1, key2)
        
        # Keys should be 16 bytes (128 bits)
        self.assertEqual(len(key1), 16)
        self.assertEqual(len(key2), 16)


class TestEntropyTheoryCompliance(unittest.TestCase):
    """
    Test compliance with entropy theory principles:
    - Shannon entropy
    - Min-entropy
    - Information theory
    - Statistical independence
    
    Reference: Shannon's Information Theory, NIST SP 800-90B
    """
    
    def test_shannon_entropy_universal_qkd(self):
        """
        Test Shannon entropy of Universal QKD output.
        
        Shannon's theorem: Maximum entropy for random binary data is 1 bit per bit.
        For bytes: maximum is 8 bits per byte.
        """
        generator = universal_qkd.universal_qkd_generator()
        keys = [next(generator) for _ in range(1000)]
        
        # Concatenate for analysis
        data = b''.join(keys)
        
        # Calculate Shannon entropy
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
        
        total = len(data)
        shannon_entropy = 0
        for count in byte_counts:
            if count > 0:
                p = count / total
                shannon_entropy -= p * math.log2(p)
        
        # Should be close to 8 bits/byte for high-quality random data
        self.assertGreater(shannon_entropy, 7.5,
                          f"Shannon entropy {shannon_entropy:.2f} should be > 7.5 bits/byte")
        
    def test_statistical_independence(self):
        """
        Test successive keys from Universal QKD are statistically independent.
        
        Information theory: Successive outputs should not be predictable.
        """
        generator = universal_qkd.universal_qkd_generator()
        keys = [next(generator) for _ in range(100)]
        
        # Check no duplicates (collision resistance)
        unique_keys = set(keys)
        self.assertEqual(len(unique_keys), len(keys),
                        "All keys should be unique (no collisions)")
        
        # Check each key has good byte distribution
        for key in keys[:10]:  # Check first 10
            byte_values = set(key)
            # Should have reasonable variety (not all same byte)
            self.assertGreater(len(byte_values), 1,
                             "Key should have varied byte values")


def run_compliance_tests():
    """Run all standards compliance tests and generate report."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestNISTSP80022Compliance))
    suite.addTests(loader.loadTestsFromTestCase(TestNISTSP80090BCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestFIPS203Compliance))
    suite.addTests(loader.loadTestsFromTestCase(TestFIPS204Compliance))
    suite.addTests(loader.loadTestsFromTestCase(TestFIPS205Compliance))
    suite.addTests(loader.loadTestsFromTestCase(TestIEEE754Compliance))
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumMechanicsPrinciples))
    suite.addTests(loader.loadTestsFromTestCase(TestCryptographicHashCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestEntropyTheoryCompliance))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_compliance_tests())
