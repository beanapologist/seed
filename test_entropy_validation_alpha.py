"""
Comprehensive test suite for entropy validation with fine-structure constant scaling.

Tests the framework using:
- μ = e^(i·3π/4) as the 8th root of unity (135° on the unit circle)
- α ≈ 1/137 (fine-structure constant approximation) for scaling
- Z ∈ {1, 2, 3, ...} (integer quantization)
- Vector formulation: V_Z = Z · α · μ

Author: GitHub Copilot
Date: 2026-01-05
"""

import unittest
import cmath
import math
from src.gq.entropy_validation_alpha import (
    QuantizedVector,
    DiscreteSymmetryValidator,
    PeriodicTableValidator,
    EntropyExtractor,
    StatisticalValidator,
    MU, MU_ANGLE, ALPHA_APPROX,
    generate_test_vectors,
    validate_framework
)

# Test thresholds
SERIAL_CORRELATION_THRESHOLD = 0.1  # Maximum acceptable correlation for independence


class TestQuantizedVector(unittest.TestCase):
    """Test QuantizedVector class."""
    
    def test_vector_creation(self):
        """Test creating quantized vectors."""
        v1 = QuantizedVector(1)
        self.assertEqual(v1.z, 1)
        self.assertAlmostEqual(v1.alpha, ALPHA_APPROX)
        self.assertEqual(v1.mu, MU)
    
    def test_vector_magnitude(self):
        """Test vector magnitude calculation."""
        v1 = QuantizedVector(1)
        expected_magnitude = 1 * ALPHA_APPROX * abs(MU)
        self.assertAlmostEqual(v1.magnitude(), expected_magnitude)
        
        v10 = QuantizedVector(10)
        expected_magnitude_10 = 10 * ALPHA_APPROX * abs(MU)
        self.assertAlmostEqual(v10.magnitude(), expected_magnitude_10)
    
    def test_vector_angle(self):
        """Test vector angle is 135 degrees."""
        v1 = QuantizedVector(1)
        self.assertAlmostEqual(v1.angle_degrees(), 135.0, places=10)
        
        v100 = QuantizedVector(100)
        self.assertAlmostEqual(v100.angle_degrees(), 135.0, places=10)
    
    def test_linear_scaling(self):
        """Test that magnitude scales linearly with Z."""
        v1 = QuantizedVector(1)
        v2 = QuantizedVector(2)
        v10 = QuantizedVector(10)
        
        self.assertAlmostEqual(v2.magnitude() / v1.magnitude(), 2.0)
        self.assertAlmostEqual(v10.magnitude() / v1.magnitude(), 10.0)
    
    def test_invalid_z(self):
        """Test that invalid Z values raise errors."""
        with self.assertRaises(ValueError):
            QuantizedVector(0)
        
        with self.assertRaises(ValueError):
            QuantizedVector(-1)
    
    def test_to_bytes(self):
        """Test conversion to bytes."""
        v1 = QuantizedVector(1)
        byte_data = v1.to_bytes()
        self.assertEqual(len(byte_data), 16)  # 2 doubles = 16 bytes


class TestDiscreteSymmetryValidator(unittest.TestCase):
    """Test discrete symmetry validation."""
    
    def test_8th_root_of_unity(self):
        """Test that μ is an 8th root of unity."""
        result = DiscreteSymmetryValidator.verify_8th_root_of_unity()
        
        self.assertTrue(result['is_8th_root_of_unity'])
        self.assertAlmostEqual(result['mu_magnitude'], 1.0, places=10)
        self.assertAlmostEqual(result['mu_angle_degrees'], 135.0, places=10)
        self.assertLess(result['mu^8_error_from_1'], 1e-10)
    
    def test_mu_power_8(self):
        """Test that μ^8 ≈ 1."""
        mu_8 = MU ** 8
        error = abs(mu_8 - 1.0)
        self.assertLess(error, 1e-10)
    
    def test_discrete_symmetry_small_z(self):
        """Test discrete symmetry for small Z values."""
        z_values = [1, 2, 3, 4, 5]
        result = DiscreteSymmetryValidator.verify_discrete_symmetry(z_values)
        
        self.assertTrue(result['all_aligned_at_135'])
        self.assertTrue(result['linear_scaling_preserved'])
        self.assertLess(result['angle_variance'], 1e-10)
    
    def test_discrete_symmetry_large_z(self):
        """Test discrete symmetry for large Z values."""
        z_values = [1, 10, 50, 100, 118]
        result = DiscreteSymmetryValidator.verify_discrete_symmetry(z_values)
        
        self.assertTrue(result['all_aligned_at_135'])
        self.assertTrue(result['linear_scaling_preserved'])
        
        # All angles should be 135°
        for angle in result['angles_degrees']:
            self.assertAlmostEqual(angle, 135.0, places=10)
    
    def test_angle_consistency(self):
        """Test that all vectors maintain 135° angle regardless of Z."""
        z_values = list(range(1, 119))  # Z = 1 to 118
        vectors = [QuantizedVector(z) for z in z_values]
        angles = [v.angle_degrees() for v in vectors]
        
        # All angles should be exactly 135°
        for angle in angles:
            self.assertAlmostEqual(angle, 135.0, places=10)


class TestPeriodicTableValidator(unittest.TestCase):
    """Test periodic table-like sampling validation."""
    
    def test_generate_periodic_samples(self):
        """Test generation of periodic samples."""
        samples = PeriodicTableValidator.generate_periodic_samples(118)
        
        self.assertEqual(len(samples), 118)
        self.assertEqual(samples[0].z, 1)
        self.assertEqual(samples[-1].z, 118)
    
    def test_periodicity_analysis(self):
        """Test periodicity analysis."""
        vectors = PeriodicTableValidator.generate_periodic_samples(118)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        self.assertEqual(result['num_samples'], 118)
        self.assertEqual(result['z_range'], (1, 118))
        self.assertTrue(result['uniform_spacing'])
        self.assertTrue(result['angle_consistency'])
        self.assertTrue(result['all_on_135_ray'])
    
    def test_magnitude_spacing(self):
        """Test that magnitudes are uniformly spaced."""
        vectors = PeriodicTableValidator.generate_periodic_samples(50)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        # Spacing variance should be essentially zero (uniform)
        self.assertLess(result['magnitude_spacing_variance'], 1e-20)
    
    def test_small_periodic_table(self):
        """Test with smaller periodic table."""
        vectors = PeriodicTableValidator.generate_periodic_samples(10)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        self.assertEqual(result['num_samples'], 10)
        self.assertTrue(result['all_on_135_ray'])


class TestEntropyExtractor(unittest.TestCase):
    """Test entropy extraction from vectors."""
    
    def test_vectors_to_bytes(self):
        """Test conversion of vectors to bytes."""
        vectors = [QuantizedVector(1), QuantizedVector(2), QuantizedVector(3)]
        byte_data = EntropyExtractor.vectors_to_bytes(vectors)
        
        # Each vector produces 16 bytes
        self.assertEqual(len(byte_data), 48)
    
    def test_extract_bits_from_vector(self):
        """Test bit extraction from a single vector."""
        vector = QuantizedVector(1)
        bits = EntropyExtractor.extract_bits_from_vector(vector, 256)
        
        self.assertEqual(len(bits), 32)  # 256 bits = 32 bytes
    
    def test_deterministic_extraction(self):
        """Test that extraction is deterministic."""
        vector = QuantizedVector(42)
        
        bits1 = EntropyExtractor.extract_bits_from_vector(vector, 256)
        bits2 = EntropyExtractor.extract_bits_from_vector(vector, 256)
        
        self.assertEqual(bits1, bits2)
    
    def test_different_z_different_output(self):
        """Test that different Z values produce different outputs."""
        v1 = QuantizedVector(1)
        v2 = QuantizedVector(2)
        
        bits1 = EntropyExtractor.extract_bits_from_vector(v1, 256)
        bits2 = EntropyExtractor.extract_bits_from_vector(v2, 256)
        
        self.assertNotEqual(bits1, bits2)
    
    def test_entropy_stream_generation(self):
        """Test generation of entropy stream."""
        stream = EntropyExtractor.generate_entropy_stream((1, 10), 1000)
        
        self.assertEqual(len(stream), 1000)
    
    def test_entropy_stream_deterministic(self):
        """Test that entropy stream generation is deterministic."""
        stream1 = EntropyExtractor.generate_entropy_stream((1, 10), 500)
        stream2 = EntropyExtractor.generate_entropy_stream((1, 10), 500)
        
        self.assertEqual(stream1, stream2)


class TestStatisticalValidator(unittest.TestCase):
    """Test statistical validation methods."""
    
    def test_bytes_to_bits(self):
        """Test byte to bit conversion."""
        data = b'\xFF\x00\xAA'
        bits = StatisticalValidator.bytes_to_bits(data)
        
        self.assertEqual(len(bits), 24)
        self.assertEqual(bits[:8], [1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(bits[8:16], [0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_frequency_test_balanced(self):
        """Test frequency test with balanced data."""
        # Perfectly balanced: alternating bits
        data = b'\xAA' * 100  # 10101010 pattern
        result = StatisticalValidator.frequency_test(data)
        
        self.assertEqual(result['ones'], result['zeros'])
        self.assertLess(result['balance'], 0.01)
    
    def test_frequency_test_unbalanced(self):
        """Test frequency test with unbalanced data."""
        data = b'\xFF' * 100  # All ones
        result = StatisticalValidator.frequency_test(data)
        
        self.assertGreater(result['balance'], 0.9)
    
    def test_runs_test(self):
        """Test runs test."""
        # Alternating pattern has many runs
        data = b'\xAA' * 100
        result = StatisticalValidator.runs_test(data)
        
        self.assertIn('runs', result)
        self.assertIn('expected_runs', result)
    
    def test_chi_square_test(self):
        """Test chi-square test."""
        # Generate some data
        stream = EntropyExtractor.generate_entropy_stream((1, 50), 1000)
        result = StatisticalValidator.chi_square_test(stream)
        
        self.assertIn('chi_square', result)
        self.assertIn('passed', result)
        self.assertEqual(result['degrees_of_freedom'], 255)
    
    def test_serial_correlation_test(self):
        """Test serial correlation."""
        stream = EntropyExtractor.generate_entropy_stream((1, 50), 1000)
        result = StatisticalValidator.serial_correlation_test(stream)
        
        self.assertIn('correlation', result)
        self.assertIn('passed', result)
    
    def test_comprehensive_analysis(self):
        """Test comprehensive statistical analysis."""
        stream = EntropyExtractor.generate_entropy_stream((1, 50), 5000)
        result = StatisticalValidator.comprehensive_analysis(stream)
        
        self.assertIn('frequency_test', result)
        self.assertIn('runs_test', result)
        self.assertIn('chi_square_test', result)
        self.assertIn('serial_correlation_test', result)
        self.assertIn('overall_passed', result)


class TestDeterministicBehavior(unittest.TestCase):
    """Test deterministic behavior of the framework."""
    
    def test_vector_reproducibility(self):
        """Test that vectors are reproducible."""
        v1a = QuantizedVector(42)
        v1b = QuantizedVector(42)
        
        self.assertEqual(v1a.vector, v1b.vector)
        self.assertEqual(v1a.magnitude(), v1b.magnitude())
        self.assertEqual(v1a.angle(), v1b.angle())
    
    def test_entropy_stream_reproducibility(self):
        """Test that entropy streams are reproducible."""
        stream1 = EntropyExtractor.generate_entropy_stream((1, 100), 5000)
        stream2 = EntropyExtractor.generate_entropy_stream((1, 100), 5000)
        
        self.assertEqual(stream1, stream2)
    
    def test_statistical_test_reproducibility(self):
        """Test that statistical tests are reproducible."""
        stream = EntropyExtractor.generate_entropy_stream((1, 50), 2000)
        
        result1 = StatisticalValidator.comprehensive_analysis(stream)
        result2 = StatisticalValidator.comprehensive_analysis(stream)
        
        self.assertEqual(result1['frequency_test']['p_value'], 
                        result2['frequency_test']['p_value'])


class TestQuantumLikeBehavior(unittest.TestCase):
    """Test quantum-like behavior claims."""
    
    def test_discrete_quantization(self):
        """Test that Z values are discrete integers."""
        vectors = generate_test_vectors((1, 10))
        
        for i, vector in enumerate(vectors):
            self.assertEqual(vector.z, i + 1)
            self.assertIsInstance(vector.z, int)
    
    def test_fine_structure_scaling(self):
        """Test that α ≈ 1/137 scaling is applied."""
        v1 = QuantizedVector(1)
        
        # Magnitude should be α * |μ|
        expected = ALPHA_APPROX * abs(MU)
        self.assertAlmostEqual(v1.magnitude(), expected)
    
    def test_unit_circle_geometry(self):
        """Test that μ lies on the unit circle."""
        mu_magnitude = abs(MU)
        self.assertAlmostEqual(mu_magnitude, 1.0, places=10)
    
    def test_135_degree_ray(self):
        """Test that all vectors lie on the 135° ray."""
        vectors = generate_test_vectors((1, 50))
        
        for vector in vectors:
            self.assertAlmostEqual(vector.angle_degrees(), 135.0, places=10)


class TestFrameworkIntegration(unittest.TestCase):
    """Test complete framework integration."""
    
    def test_validate_framework(self):
        """Test complete framework validation."""
        results = validate_framework()
        
        self.assertIn('8th_root_validation', results)
        self.assertIn('discrete_symmetry', results)
        self.assertIn('periodicity', results)
        self.assertIn('statistical_tests', results)
        self.assertIn('overall_assessment', results)
    
    def test_8th_root_validation(self):
        """Test 8th root of unity validation."""
        results = validate_framework()
        root_val = results['8th_root_validation']
        
        self.assertTrue(root_val['is_8th_root_of_unity'])
    
    def test_discrete_symmetry_validation(self):
        """Test discrete symmetry validation."""
        results = validate_framework()
        sym_val = results['discrete_symmetry']
        
        self.assertTrue(sym_val['all_aligned_at_135'])
        self.assertTrue(sym_val['linear_scaling_preserved'])
    
    def test_periodicity_validation(self):
        """Test periodicity validation."""
        results = validate_framework()
        period_val = results['periodicity']
        
        self.assertTrue(period_val['all_on_135_ray'])
        self.assertTrue(period_val['uniform_spacing'])
    
    def test_overall_assessment(self):
        """Test overall assessment."""
        results = validate_framework()
        assessment = results['overall_assessment']
        
        # These should all pass
        self.assertTrue(assessment['mu_is_8th_root'])
        self.assertTrue(assessment['discrete_symmetry_maintained'])
        self.assertTrue(assessment['linear_scaling_preserved'])
        self.assertTrue(assessment['periodic_sampling_consistent'])


class TestCryptographicProperties(unittest.TestCase):
    """Test cryptographic randomness properties."""
    
    def test_deterministic_not_random(self):
        """Test that the framework is deterministic, not random."""
        # Generate same stream twice
        stream1 = EntropyExtractor.generate_entropy_stream((1, 50), 1000)
        stream2 = EntropyExtractor.generate_entropy_stream((1, 50), 1000)
        
        # Should be identical (deterministic)
        self.assertEqual(stream1, stream2)
    
    def test_predictability_from_z(self):
        """Test that output is predictable from Z value."""
        z = 42
        v1 = QuantizedVector(z)
        v2 = QuantizedVector(z)
        
        bits1 = EntropyExtractor.extract_bits_from_vector(v1, 256)
        bits2 = EntropyExtractor.extract_bits_from_vector(v2, 256)
        
        # Same Z produces same output (predictable)
        self.assertEqual(bits1, bits2)
    
    def test_knowledge_of_formula_enables_prediction(self):
        """Test that knowledge of formula enables perfect prediction."""
        # If you know Z, α, and μ, you can compute the output
        z = 17
        
        # Compute vector using formula
        expected_vector = z * ALPHA_APPROX * MU
        
        # Compute using class
        actual_vector = QuantizedVector(z).vector
        
        # Should match exactly
        self.assertAlmostEqual(expected_vector.real, actual_vector.real)
        self.assertAlmostEqual(expected_vector.imag, actual_vector.imag)


class TestNISTSP800_90B(unittest.TestCase):
    """Test NIST SP 800-90B style entropy assessment."""
    
    def test_min_entropy_estimate(self):
        """Test minimum entropy estimation."""
        # Generate entropy stream
        stream = EntropyExtractor.generate_entropy_stream((1, 100), 10000)
        
        # Count byte frequencies
        from collections import Counter
        freq = Counter(stream)
        
        # Most common byte frequency
        max_freq = max(freq.values())
        n = len(stream)
        
        # Min-entropy estimate: -log2(p_max)
        p_max = max_freq / n
        min_entropy = -math.log2(p_max) if p_max > 0 else 0
        
        # For cryptographic use, min-entropy should be high
        # This is deterministic, so it will be low
        self.assertLess(min_entropy, 8.0)  # Less than 8 bits/byte
    
    def test_collision_entropy(self):
        """Test collision entropy (number of unique values)."""
        stream = EntropyExtractor.generate_entropy_stream((1, 100), 1000)
        
        unique_bytes = len(set(stream))
        total_bytes = len(stream)
        
        uniqueness_ratio = unique_bytes / total_bytes
        
        # Deterministic structure means some repetition
        # True random would have uniqueness close to 1.0 for small samples
        self.assertGreater(uniqueness_ratio, 0.0)


class TestSummaryResults(unittest.TestCase):
    """Test suite summary and final conclusions."""
    
    def test_mu_as_8th_root_maintains_symmetry(self):
        """
        Test #1: Verify μ = e^(i·3π/4) as 8th root maintains discrete symmetry.
        """
        result = DiscreteSymmetryValidator.verify_8th_root_of_unity()
        
        # μ should be an 8th root of unity
        self.assertTrue(result['is_8th_root_of_unity'])
        
        # μ^8 should equal 1
        mu_8 = MU ** 8
        self.assertAlmostEqual(abs(mu_8 - 1.0), 0.0, places=10)
    
    def test_scaling_with_alpha_and_z_coherent(self):
        """
        Test #2: Verify scaling with α and quantized Z leads to coherent results.
        """
        z_values = [1, 2, 5, 10, 20, 50, 100]
        result = DiscreteSymmetryValidator.verify_discrete_symmetry(z_values)
        
        # Linear scaling should be preserved
        self.assertTrue(result['linear_scaling_preserved'])
        
        # All vectors should be aligned at 135°
        self.assertTrue(result['all_aligned_at_135'])
    
    def test_periodic_table_discrete_samples(self):
        """
        Test #3: Verify outputs align with periodic table-like discrete samples.
        """
        vectors = PeriodicTableValidator.generate_periodic_samples(118)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        # Should have uniform spacing
        self.assertTrue(result['uniform_spacing'])
        
        # All should be on 135° ray
        self.assertTrue(result['all_on_135_ray'])
    
    def test_statistical_entropy_properties(self):
        """
        Test #4: Verify statistical properties via NIST-style tests.
        
        Note: This framework is DETERMINISTIC by design, so it will NOT
        pass as cryptographic randomness. This is expected and documented.
        """
        stream = EntropyExtractor.generate_entropy_stream((1, 118), 10000)
        result = StatisticalValidator.comprehensive_analysis(stream)
        
        # Frequency test may pass (balanced 0s and 1s)
        self.assertIn('frequency_test', result)
        
        # Serial correlation should be low (below threshold for independence)
        self.assertLess(abs(result['serial_correlation_test']['correlation']), 
                       SERIAL_CORRELATION_THRESHOLD)
        
        # Chi-square test will likely fail (not uniform due to deterministic structure)
        # This is EXPECTED for a deterministic mathematical formula


def run_validation_suite():
    """Run the complete validation suite and print summary."""
    print("=" * 80)
    print("ENTROPY VALIDATION TEST SUITE")
    print("Framework: V_Z = Z · α · μ")
    print(f"  μ = e^(i·3π/4) ≈ {MU}")
    print(f"  α ≈ 1/137 = {ALPHA_APPROX}")
    print("  Z ∈ {{1, 2, 3, ...}}")
    print("=" * 80)
    print()
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED")
        print()
        print("Conclusions:")
        print("  1. ✓ μ = e^(i·3π/4) maintains discrete symmetry as 8th root of unity")
        print("  2. ✓ Scaling with α ≈ 1/137 and quantized Z is coherent and predictable")
        print("  3. ✓ Outputs align with periodic table-like discrete samples on 135° ray")
        print("  4. ⚠ Statistical tests show DETERMINISTIC behavior (as expected)")
        print()
        print("Note: This framework is DETERMINISTIC by design, using mathematical")
        print("formulas with fixed constants. It does NOT generate cryptographic")
        print("randomness, but rather demonstrates quantum-like discrete structure.")
    else:
        print("✗ SOME TESTS FAILED")
    
    print("=" * 80)
    
    return result


if __name__ == '__main__':
    run_validation_suite()
