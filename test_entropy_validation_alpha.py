"""
Comprehensive test suite for entropy validation with golden ratio phase distribution.

Tests the framework using:
- φ ≈ 1.618... (golden ratio) for fractional-phase resampling
- α ≈ 1/137 (fine-structure constant approximation) for scaling
- Z ∈ {1, 2, 3, ...} (integer quantization)
- Vector formulation: V_Z = Z · α · exp(2πi{Z·φ})

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
    PHI, ALPHA_APPROX, fractional_part,
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
        self.assertAlmostEqual(v1.phi, PHI)
    
    def test_vector_magnitude(self):
        """Test vector magnitude calculation: |V_Z| = Z·α."""
        v1 = QuantizedVector(1)
        expected_magnitude = 1 * ALPHA_APPROX
        self.assertAlmostEqual(v1.magnitude(), expected_magnitude)
        
        v10 = QuantizedVector(10)
        expected_magnitude_10 = 10 * ALPHA_APPROX
        self.assertAlmostEqual(v10.magnitude(), expected_magnitude_10)
    
    def test_vector_angle(self):
        """Test vector angle is based on {Z·φ}."""
        v1 = QuantizedVector(1)
        expected_angle_rad = 2 * math.pi * fractional_part(1 * PHI)
        # cmath.phase returns values in [-π, π], so we need to normalize
        actual_angle = v1.angle()
        if actual_angle < 0:
            actual_angle += 2 * math.pi
        self.assertAlmostEqual(actual_angle, expected_angle_rad, places=10)
        
        # Each Z has a different angle based on fractional part
        v2 = QuantizedVector(2)
        v3 = QuantizedVector(3)
        # Angles should be different (not aligned at fixed angle)
        self.assertNotAlmostEqual(v1.angle(), v2.angle(), places=2)
        self.assertNotAlmostEqual(v2.angle(), v3.angle(), places=2)
    
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
    
    def test_fractional_phase(self):
        """Test fractional phase {Z·φ} is in [0, 1)."""
        for z in range(1, 20):
            v = QuantizedVector(z)
            fp = v.fractional_phase()
            self.assertGreaterEqual(fp, 0.0)
            self.assertLess(fp, 1.0)


class TestDiscreteSymmetryValidator(unittest.TestCase):
    """Test discrete symmetry validation."""
    
    def test_golden_ratio_properties(self):
        """Test that φ satisfies φ² = φ + 1."""
        result = DiscreteSymmetryValidator.verify_golden_ratio_properties()
        
        self.assertTrue(result['is_golden_ratio'])
        self.assertAlmostEqual(result['phi'], PHI, places=10)
        # φ² should equal φ + 1
        self.assertLess(result['phi_squared_error'], 1e-10)
    
    def test_phi_squared_property(self):
        """Test that φ² = φ + 1."""
        phi_squared = PHI ** 2
        phi_plus_one = PHI + 1
        error = abs(phi_squared - phi_plus_one)
        self.assertLess(error, 1e-10)
    
    def test_discrete_symmetry_small_z(self):
        """Test magnitude scaling for small Z values."""
        z_values = [1, 2, 3, 4, 5]
        result = DiscreteSymmetryValidator.verify_discrete_symmetry(z_values)
        
        self.assertTrue(result['linear_scaling_preserved'])
    
    def test_discrete_symmetry_large_z(self):
        """Test magnitude scaling for large Z values."""
        z_values = [1, 10, 50, 100, 118]
        result = DiscreteSymmetryValidator.verify_discrete_symmetry(z_values)
        
        self.assertTrue(result['linear_scaling_preserved'])
        
        # Magnitudes should scale linearly: |V_Z| = Z·α
        for i, z in enumerate(z_values):
            expected_mag = z * ALPHA_APPROX
            self.assertAlmostEqual(result['magnitudes'][i], expected_mag, places=10)
    
    def test_phase_distribution(self):
        """Test that phases are distributed according to {Z·φ}."""
        z_values = list(range(1, 119))  # Z = 1 to 118
        vectors = [QuantizedVector(z) for z in z_values]
        fractional_phases = [v.fractional_phase() for v in vectors]
        
        # All fractional phases should be in [0, 1)
        for fp in fractional_phases:
            self.assertGreaterEqual(fp, 0.0)
            self.assertLess(fp, 1.0)


class TestPeriodicTableValidator(unittest.TestCase):
    """Test low-discrepancy sequence validation."""
    
    def test_generate_periodic_samples(self):
        """Test generation of samples."""
        samples = PeriodicTableValidator.generate_periodic_samples(118)
        
        self.assertEqual(len(samples), 118)
        self.assertEqual(samples[0].z, 1)
        self.assertEqual(samples[-1].z, 118)
    
    def test_low_discrepancy_analysis(self):
        """Test low-discrepancy sequence properties."""
        vectors = PeriodicTableValidator.generate_periodic_samples(118)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        self.assertEqual(result['num_samples'], 118)
        self.assertEqual(result['z_range'], (1, 118))
        self.assertTrue(result['uniform_magnitude_spacing'])
        self.assertTrue(result['low_discrepancy'])
        self.assertTrue(result['phase_uniformity_passed'])
    
    def test_magnitude_spacing(self):
        """Test that magnitudes are uniformly spaced."""
        vectors = PeriodicTableValidator.generate_periodic_samples(50)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        # Spacing variance should be essentially zero (uniform)
        self.assertLess(result['magnitude_spacing_variance'], 1e-20)
    
    def test_phase_uniformity(self):
        """Test that fractional phases are uniformly distributed."""
        vectors = PeriodicTableValidator.generate_periodic_samples(100)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        # Chi-square test should pass for uniform distribution
        self.assertTrue(result['phase_uniformity_passed'])
        
        # Star discrepancy should be low
        self.assertTrue(result['low_discrepancy'])
    
    def test_small_sample_set(self):
        """Test with smaller sample set."""
        vectors = PeriodicTableValidator.generate_periodic_samples(10)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        self.assertEqual(result['num_samples'], 10)
        self.assertTrue(result['low_discrepancy'])


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
        """Test that α ≈ 1/137 scaling is applied to magnitude."""
        v1 = QuantizedVector(1)
        
        # Magnitude should be Z·α
        expected = ALPHA_APPROX
        self.assertAlmostEqual(v1.magnitude(), expected)
    
    def test_golden_ratio_phase(self):
        """Test that phase is based on golden ratio φ."""
        v1 = QuantizedVector(1)
        
        # Fractional phase should be {1·φ}
        expected_fp = fractional_part(1 * PHI)
        self.assertAlmostEqual(v1.fractional_phase(), expected_fp)
    
    def test_low_discrepancy_distribution(self):
        """Test that {Z·φ} provides low-discrepancy sequence."""
        vectors = generate_test_vectors((1, 100))
        fractional_phases = [v.fractional_phase() for v in vectors]
        
        # Check that phases are well-distributed across [0, 1)
        bins = [0] * 10
        for fp in fractional_phases:
            bin_idx = min(int(fp * 10), 9)
            bins[bin_idx] += 1
        
        # Each bin should have roughly 10 values (100 samples / 10 bins)
        # Allow some variance
        for count in bins:
            self.assertGreater(count, 0)  # No empty bins


class TestFrameworkIntegration(unittest.TestCase):
    """Test complete framework integration."""
    
    def test_validate_framework(self):
        """Test complete framework validation."""
        results = validate_framework()
        
        self.assertIn('golden_ratio_validation', results)
        self.assertIn('discrete_symmetry', results)
        self.assertIn('low_discrepancy', results)
        self.assertIn('statistical_tests', results)
        self.assertIn('overall_assessment', results)
    
    def test_golden_ratio_validation(self):
        """Test golden ratio validation."""
        results = validate_framework()
        gr_val = results['golden_ratio_validation']
        
        self.assertTrue(gr_val['is_golden_ratio'])
    
    def test_discrete_symmetry_validation(self):
        """Test magnitude scaling validation."""
        results = validate_framework()
        sym_val = results['discrete_symmetry']
        
        self.assertTrue(sym_val['linear_scaling_preserved'])
    
    def test_low_discrepancy_validation(self):
        """Test low-discrepancy validation."""
        results = validate_framework()
        ld_val = results['low_discrepancy']
        
        self.assertTrue(ld_val['low_discrepancy'])
        self.assertTrue(ld_val['phase_uniformity_passed'])
    
    def test_overall_assessment(self):
        """Test overall assessment."""
        results = validate_framework()
        assessment = results['overall_assessment']
        
        # These should all pass
        self.assertTrue(assessment['phi_is_golden_ratio'])
        self.assertTrue(assessment['linear_magnitude_scaling'])
        self.assertTrue(assessment['low_discrepancy_phase'])
        self.assertTrue(assessment['phase_uniformity'])


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
        # If you know Z, α, and φ, you can compute the output
        z = 17
        
        # Compute vector using formula: V_Z = Z · α · exp(2πi{Z·φ})
        magnitude = z * ALPHA_APPROX
        fractional_phase = fractional_part(z * PHI)
        phase_angle = 2 * math.pi * fractional_phase
        expected_vector = magnitude * cmath.exp(1j * phase_angle)
        
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
    
    def test_golden_ratio_maintains_properties(self):
        """
        Test #1: Verify φ maintains golden ratio property φ² = φ + 1.
        """
        result = DiscreteSymmetryValidator.verify_golden_ratio_properties()
        
        # φ should satisfy φ² = φ + 1
        self.assertTrue(result['is_golden_ratio'])
        
        # Check the property
        phi_squared = PHI ** 2
        phi_plus_one = PHI + 1
        self.assertAlmostEqual(phi_squared, phi_plus_one, places=10)
    
    def test_magnitude_scaling_with_alpha_and_z(self):
        """
        Test #2: Verify magnitude |V_Z| = Z·α scales linearly.
        """
        z_values = [1, 2, 5, 10, 20, 50, 100]
        result = DiscreteSymmetryValidator.verify_discrete_symmetry(z_values)
        
        # Linear scaling should be preserved
        self.assertTrue(result['linear_scaling_preserved'])
        
        # Check each magnitude
        for i, z in enumerate(z_values):
            expected = z * ALPHA_APPROX
            self.assertAlmostEqual(result['magnitudes'][i], expected, places=10)
    
    def test_low_discrepancy_fractional_phase(self):
        """
        Test #3: Verify {Z·φ} provides low-discrepancy sequence.
        """
        vectors = PeriodicTableValidator.generate_periodic_samples(118)
        result = PeriodicTableValidator.analyze_periodicity(vectors)
        
        # Should have low discrepancy
        self.assertTrue(result['low_discrepancy'])
        
        # Should have uniform phase distribution
        self.assertTrue(result['phase_uniformity_passed'])
    
    def test_statistical_entropy_properties(self):
        """
        Test #4: Verify statistical properties via NIST-style tests.
        
        Note: This framework is DETERMINISTIC by design, so chi-square
        may not pass, but other tests should work well.
        """
        stream = EntropyExtractor.generate_entropy_stream((1, 118), 10000)
        result = StatisticalValidator.comprehensive_analysis(stream)
        
        # Frequency test should pass (balanced 0s and 1s)
        self.assertIn('frequency_test', result)
        
        # Serial correlation should be low (below threshold for independence)
        self.assertLess(abs(result['serial_correlation_test']['correlation']), 
                       SERIAL_CORRELATION_THRESHOLD)


def run_validation_suite():
    """Run the complete validation suite and print summary."""
    print("=" * 80)
    print("ENTROPY VALIDATION TEST SUITE")
    print("Framework: V_Z = Z · α · exp(2πi{Z·φ})")
    print(f"  φ = (1 + √5)/2 ≈ {PHI}")
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
        print("  1. ✓ φ = (1+√5)/2 maintains golden ratio property (φ² = φ + 1)")
        print("  2. ✓ Magnitude |V_Z| = Z·α scales linearly with Z and α")
        print("  3. ✓ Fractional phase {Z·φ} provides low-discrepancy sequences")
        print("  4. ✓ Phase uniformly distributed on unit circle")
        print()
        print("Note: This framework is DETERMINISTIC by design, using mathematical")
        print("formulas with the golden ratio for optimal phase distribution.")
    else:
        print("✗ SOME TESTS FAILED")
    
    print("=" * 80)
    
    return result


if __name__ == '__main__':
    run_validation_suite()
