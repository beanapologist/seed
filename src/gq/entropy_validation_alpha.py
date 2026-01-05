"""
Entropy Validation Framework with Fine-Structure Constant Scaling

This module implements a comprehensive entropy validation framework using:
- μ = e^(i·3π/4) as the 8th root of unity (135° on the unit circle)
- α ≈ 1/137 (fine-structure constant approximation) for scaling
- Z ∈ {1, 2, 3, ...} (integer quantization)
- Vector formulation: V_Z = Z · α · μ

The framework tests whether this approach supports claims about:
1. Discrete symmetry by geometry using μ as 8th root of unity
2. Coherent and predictable results with α scaling and quantized Z-values
3. Periodic table-like discrete samples along the 135° ray
4. Cryptographic randomness properties via statistical tests

Author: GitHub Copilot
Date: 2026-01-05
"""

import cmath
import math
import struct
import hashlib
from typing import List, Tuple, Dict, Any, Optional
from collections import Counter
import sys


# Mathematical constants
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
ALPHA = 1.0 / 137.035999084  # Fine-structure constant (CODATA 2018) - precise value
ALPHA_APPROX = 1.0 / 137  # Approximation as specified in problem statement
# Note: ALPHA_APPROX is used throughout the framework as specified in the requirements

# μ = e^(i·3π/4) - The 8th root of unity at 135°
MU_ANGLE = 3 * math.pi / 4  # 135 degrees in radians
MU = cmath.exp(1j * MU_ANGLE)

# IEEE 754 constants
EPSILON_64 = sys.float_info.epsilon  # Machine epsilon for double precision


class QuantizedVector:
    """
    Represents a quantized vector V_Z = Z · α · μ
    
    Attributes:
        z: Integer quantum number (Z ∈ {1, 2, 3, ...})
        alpha: Fine-structure constant scaling factor
        mu: Complex number μ = e^(i·3π/4)
        vector: The computed vector V_Z
    """
    
    def __init__(self, z: int, alpha: float = ALPHA_APPROX, mu: complex = MU):
        """
        Initialize a quantized vector.
        
        Args:
            z: Integer quantum number (must be positive)
            alpha: Fine-structure constant (default: 1/137)
            mu: Complex rotation center (default: e^(i·3π/4))
        """
        if z < 1:
            raise ValueError("Z must be a positive integer (Z ∈ {1, 2, 3, ...})")
        
        self.z = z
        self.alpha = alpha
        self.mu = mu
        self.vector = z * alpha * mu
    
    def magnitude(self) -> float:
        """Get the magnitude of the vector."""
        return abs(self.vector)
    
    def angle(self) -> float:
        """Get the angle of the vector in radians."""
        return cmath.phase(self.vector)
    
    def angle_degrees(self) -> float:
        """Get the angle of the vector in degrees."""
        return math.degrees(self.angle())
    
    def to_bytes(self) -> bytes:
        """
        Convert the vector to bytes representation.
        Returns real and imaginary parts as double-precision floats.
        """
        real_bytes = struct.pack('d', self.vector.real)
        imag_bytes = struct.pack('d', self.vector.imag)
        return real_bytes + imag_bytes
    
    def __repr__(self) -> str:
        return f"V_{self.z} = {self.z} × α × μ = {self.vector}"


class DiscreteSymmetryValidator:
    """
    Validates discrete symmetry properties of quantized vectors.
    
    Tests whether μ = e^(i·3π/4) as the 8th root of unity maintains
    discrete symmetry by geometry.
    """
    
    @staticmethod
    def verify_8th_root_of_unity() -> Dict[str, Any]:
        """
        Verify that μ is indeed an 8th root of unity.
        
        For μ to be an 8th root of unity, μ^8 should equal 1.
        """
        mu_8 = MU ** 8
        
        # Check if μ^8 ≈ 1
        error = abs(mu_8 - 1.0)
        is_valid = error < 1e-10
        
        return {
            'mu': MU,
            'mu_angle_degrees': math.degrees(MU_ANGLE),
            'mu_magnitude': abs(MU),
            'mu^8': mu_8,
            'mu^8_error_from_1': error,
            'is_8th_root_of_unity': is_valid,
            'tolerance': 1e-10
        }
    
    @staticmethod
    def verify_discrete_symmetry(z_values: List[int]) -> Dict[str, Any]:
        """
        Verify discrete symmetry of vectors for given Z values.
        
        Args:
            z_values: List of integer quantum numbers
            
        Returns:
            Dictionary with symmetry analysis
        """
        vectors = [QuantizedVector(z) for z in z_values]
        
        # All vectors should have the same angle (135°)
        angles = [v.angle_degrees() for v in vectors]
        angle_variance = max(angles) - min(angles)
        
        # Magnitudes should scale linearly with Z
        magnitudes = [v.magnitude() for v in vectors]
        expected_scaling = [(z * ALPHA_APPROX * abs(MU)) for z in z_values]
        scaling_errors = [abs(m - e) for m, e in zip(magnitudes, expected_scaling)]
        max_scaling_error = max(scaling_errors)
        
        return {
            'z_values': z_values,
            'angles_degrees': angles,
            'angle_variance': angle_variance,
            'all_aligned_at_135': angle_variance < 1e-10,
            'magnitudes': magnitudes,
            'expected_magnitudes': expected_scaling,
            'max_scaling_error': max_scaling_error,
            'linear_scaling_preserved': max_scaling_error < 1e-10
        }


class PeriodicTableValidator:
    """
    Validates periodic table-like discrete sampling along the 135° ray.
    
    Tests whether outputs align with periodic table-like discrete samples
    with precision and consistency.
    """
    
    @staticmethod
    def generate_periodic_samples(max_z: int = 118) -> List[QuantizedVector]:
        """
        Generate periodic table-like samples (similar to element count).
        
        Args:
            max_z: Maximum Z value (default: 118, similar to periodic table)
            
        Returns:
            List of quantized vectors for Z = 1 to max_z
        """
        return [QuantizedVector(z) for z in range(1, max_z + 1)]
    
    @staticmethod
    def analyze_periodicity(vectors: List[QuantizedVector]) -> Dict[str, Any]:
        """
        Analyze periodicity and consistency of sampled vectors.
        
        Args:
            vectors: List of quantized vectors
            
        Returns:
            Dictionary with periodicity analysis
        """
        z_values = [v.z for v in vectors]
        magnitudes = [v.magnitude() for v in vectors]
        angles = [v.angle_degrees() for v in vectors]
        
        # Check linear spacing of magnitudes
        magnitude_diffs = [magnitudes[i+1] - magnitudes[i] 
                          for i in range(len(magnitudes) - 1)]
        mean_diff = sum(magnitude_diffs) / len(magnitude_diffs)
        diff_variance = sum((d - mean_diff)**2 for d in magnitude_diffs) / len(magnitude_diffs)
        
        # Check angle consistency (all should be 135°)
        angle_mean = sum(angles) / len(angles)
        angle_std = math.sqrt(sum((a - angle_mean)**2 for a in angles) / len(angles))
        
        return {
            'num_samples': len(vectors),
            'z_range': (min(z_values), max(z_values)),
            'magnitude_range': (min(magnitudes), max(magnitudes)),
            'mean_magnitude_spacing': mean_diff,
            'magnitude_spacing_variance': diff_variance,
            'uniform_spacing': diff_variance < 1e-20,
            'angle_mean_degrees': angle_mean,
            'angle_std_degrees': angle_std,
            'angle_consistency': angle_std < 1e-10,
            'all_on_135_ray': all(abs(a - 135.0) < 1e-10 for a in angles)
        }


class EntropyExtractor:
    """
    Extracts entropy from quantized vectors for cryptographic testing.
    
    Converts V_Z vectors into byte sequences for statistical analysis.
    """
    
    @staticmethod
    def vectors_to_bytes(vectors: List[QuantizedVector]) -> bytes:
        """
        Convert a list of vectors to a byte sequence.
        
        Args:
            vectors: List of quantized vectors
            
        Returns:
            Concatenated byte representation
        """
        return b''.join(v.to_bytes() for v in vectors)
    
    @staticmethod
    def extract_bits_from_vector(vector: QuantizedVector, num_bits: int = 256) -> bytes:
        """
        Extract bits from a single vector using cryptographic hashing.
        
        Args:
            vector: Quantized vector
            num_bits: Number of bits to extract (default: 256)
            
        Returns:
            Extracted bits as bytes
        """
        vector_bytes = vector.to_bytes()
        num_bytes = (num_bits + 7) // 8
        
        # Use SHA-256 to extract deterministic bits
        # Note: This is for testing/demonstration purposes only.
        # For production cryptographic applications, use a proper KDF (e.g., HKDF).
        hash_obj = hashlib.sha256(vector_bytes)
        result = hash_obj.digest()
        
        # If we need more bits, chain the hash (simple expansion for testing)
        # WARNING: This hash chaining is NOT cryptographically secure for key derivation.
        # Use HKDF or similar for production applications requiring secure bit expansion.
        while len(result) < num_bytes:
            hash_obj = hashlib.sha256(result)
            result += hash_obj.digest()
        
        return result[:num_bytes]
    
    @staticmethod
    def generate_entropy_stream(z_range: Tuple[int, int], 
                               stream_length: int = 10000) -> bytes:
        """
        Generate an entropy stream from a range of Z values.
        
        Args:
            z_range: Tuple of (min_z, max_z)
            stream_length: Number of bytes to generate
            
        Returns:
            Entropy stream as bytes
        """
        min_z, max_z = z_range
        result = b''
        z = min_z
        
        while len(result) < stream_length:
            vector = QuantizedVector(z)
            extracted = EntropyExtractor.extract_bits_from_vector(vector, 256)
            result += extracted
            
            # Cycle through Z values
            z += 1
            if z > max_z:
                z = min_z
        
        return result[:stream_length]


class StatisticalValidator:
    """
    Performs statistical validation of entropy using NIST-style tests.
    
    Implements basic versions of:
    - Frequency (monobit) test
    - Runs test
    - Serial correlation test
    - Chi-square test
    """
    
    @staticmethod
    def bytes_to_bits(data: bytes) -> List[int]:
        """Convert bytes to list of bits."""
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits
    
    @staticmethod
    def frequency_test(data: bytes) -> Dict[str, Any]:
        """
        NIST Frequency (Monobit) Test.
        
        Tests whether the number of ones and zeros are approximately equal.
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Test results including p-value
        """
        bits = StatisticalValidator.bytes_to_bits(data)
        n = len(bits)
        
        # Count ones and zeros
        ones = sum(bits)
        zeros = n - ones
        
        # Compute test statistic
        s = sum(1 if b == 1 else -1 for b in bits)
        s_obs = abs(s) / math.sqrt(n)
        
        # Compute p-value using complementary error function approximation
        p_value = math.erfc(s_obs / math.sqrt(2))
        
        return {
            'test': 'frequency_monobit',
            'n_bits': n,
            'ones': ones,
            'zeros': zeros,
            'balance': abs(ones - zeros) / n,
            's_obs': s_obs,
            'p_value': p_value,
            'passed': p_value >= 0.01
        }
    
    @staticmethod
    def runs_test(data: bytes) -> Dict[str, Any]:
        """
        NIST Runs Test.
        
        Tests for oscillation in the bit sequence.
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Test results
        """
        bits = StatisticalValidator.bytes_to_bits(data)
        n = len(bits)
        
        # Pre-requisite: frequency test proportion must be in range
        ones = sum(bits)
        pi = ones / n
        
        if abs(pi - 0.5) >= 2 / math.sqrt(n):
            return {
                'test': 'runs',
                'n_bits': n,
                'passed': False,
                'reason': 'frequency_prerequisite_failed'
            }
        
        # Count runs
        runs = 1
        for i in range(1, n):
            if bits[i] != bits[i-1]:
                runs += 1
        
        # Expected number of runs
        expected_runs = (2 * n * pi * (1 - pi))
        
        # Test statistic
        numerator = abs(runs - expected_runs)
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        
        if denominator > 0:
            test_stat = numerator / denominator
            p_value = math.erfc(test_stat / math.sqrt(2))
        else:
            test_stat = 0
            p_value = 0
        
        return {
            'test': 'runs',
            'n_bits': n,
            'runs': runs,
            'expected_runs': expected_runs,
            'test_statistic': test_stat,
            'p_value': p_value,
            'passed': p_value >= 0.01
        }
    
    @staticmethod
    def chi_square_test(data: bytes) -> Dict[str, Any]:
        """
        Chi-square test for byte distribution uniformity.
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Test results
        """
        # Count byte frequencies
        freq = Counter(data)
        n = len(data)
        expected = n / 256
        
        # Compute chi-square statistic
        chi_square = sum((freq.get(i, 0) - expected) ** 2 / expected 
                        for i in range(256))
        
        # Degrees of freedom = 255 (256 possible byte values - 1)
        # Critical value for significance level α=0.01 and df=255 is approximately 310
        # Reference: Chi-square distribution table, 99th percentile for df=255
        # For uniform distribution, we expect χ² ≈ 255; values > 310 indicate non-uniformity
        critical_value = 310
        
        return {
            'test': 'chi_square',
            'n_bytes': n,
            'chi_square': chi_square,
            'degrees_of_freedom': 255,
            'critical_value': critical_value,
            'passed': chi_square < critical_value,
            'uniformity_score': 1.0 - min(1.0, chi_square / (2 * critical_value))
        }
    
    @staticmethod
    def serial_correlation_test(data: bytes, lag: int = 1) -> Dict[str, Any]:
        """
        Serial correlation test.
        
        Tests for correlation between bits at different positions.
        
        Args:
            data: Byte sequence to test
            lag: Lag for correlation (default: 1)
            
        Returns:
            Test results
        """
        bits = StatisticalValidator.bytes_to_bits(data)
        n = len(bits)
        
        if n <= lag:
            return {
                'test': 'serial_correlation',
                'error': 'insufficient_data'
            }
        
        # Compute correlation
        mean = sum(bits) / n
        
        numerator = sum((bits[i] - mean) * (bits[i + lag] - mean) 
                       for i in range(n - lag))
        denominator = sum((bits[i] - mean) ** 2 for i in range(n))
        
        if denominator > 0:
            correlation = numerator / denominator
        else:
            correlation = 0
        
        return {
            'test': 'serial_correlation',
            'n_bits': n,
            'lag': lag,
            'correlation': correlation,
            'passed': abs(correlation) < 0.1,  # Threshold for independence
            'independence_score': 1.0 - min(1.0, abs(correlation) * 10)
        }
    
    @staticmethod
    def comprehensive_analysis(data: bytes) -> Dict[str, Any]:
        """
        Run comprehensive statistical analysis.
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Dictionary with all test results
        """
        return {
            'data_length': len(data),
            'frequency_test': StatisticalValidator.frequency_test(data),
            'runs_test': StatisticalValidator.runs_test(data),
            'chi_square_test': StatisticalValidator.chi_square_test(data),
            'serial_correlation_test': StatisticalValidator.serial_correlation_test(data),
            'overall_passed': all([
                StatisticalValidator.frequency_test(data)['passed'],
                StatisticalValidator.runs_test(data)['passed'],
                StatisticalValidator.chi_square_test(data)['passed'],
                StatisticalValidator.serial_correlation_test(data)['passed']
            ])
        }


def generate_test_vectors(z_range: Tuple[int, int] = (1, 118)) -> List[QuantizedVector]:
    """
    Generate test vectors for a range of Z values.
    
    Args:
        z_range: Tuple of (min_z, max_z), default (1, 118) like periodic table
        
    Returns:
        List of quantized vectors
    """
    min_z, max_z = z_range
    return [QuantizedVector(z) for z in range(min_z, max_z + 1)]


def validate_framework() -> Dict[str, Any]:
    """
    Run complete validation of the entropy framework.
    
    Returns:
        Dictionary with comprehensive validation results
    """
    results = {}
    
    # 1. Verify μ as 8th root of unity
    results['8th_root_validation'] = DiscreteSymmetryValidator.verify_8th_root_of_unity()
    
    # 2. Verify discrete symmetry
    test_z_values = [1, 2, 5, 10, 20, 50, 100, 118]
    results['discrete_symmetry'] = DiscreteSymmetryValidator.verify_discrete_symmetry(test_z_values)
    
    # 3. Validate periodicity
    periodic_samples = PeriodicTableValidator.generate_periodic_samples(118)
    results['periodicity'] = PeriodicTableValidator.analyze_periodicity(periodic_samples)
    
    # 4. Generate entropy stream and test
    entropy_stream = EntropyExtractor.generate_entropy_stream((1, 118), 10000)
    results['statistical_tests'] = StatisticalValidator.comprehensive_analysis(entropy_stream)
    
    # 5. Overall assessment
    results['overall_assessment'] = {
        'mu_is_8th_root': results['8th_root_validation']['is_8th_root_of_unity'],
        'discrete_symmetry_maintained': results['discrete_symmetry']['all_aligned_at_135'],
        'linear_scaling_preserved': results['discrete_symmetry']['linear_scaling_preserved'],
        'periodic_sampling_consistent': results['periodicity']['all_on_135_ray'],
        'statistical_tests_passed': results['statistical_tests']['overall_passed']
    }
    
    return results


if __name__ == '__main__':
    """Run validation when module is executed directly."""
    print("=" * 80)
    print("Entropy Validation Framework with Fine-Structure Constant Scaling")
    print("=" * 80)
    print()
    print(f"Configuration:")
    print(f"  μ = e^(i·3π/4) = {MU}")
    print(f"  |μ| = {abs(MU):.10f}")
    print(f"  ∠μ = {math.degrees(MU_ANGLE):.1f}°")
    print(f"  α = 1/137 ≈ {ALPHA_APPROX:.10f}")
    print()
    
    print("Running comprehensive validation...")
    results = validate_framework()
    
    print("\n" + "=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    
    print("\n1. 8th Root of Unity Verification:")
    root_results = results['8th_root_validation']
    print(f"   μ^8 = {root_results['mu^8']}")
    print(f"   |μ^8 - 1| = {root_results['mu^8_error_from_1']:.2e}")
    print(f"   ✓ PASS" if root_results['is_8th_root_of_unity'] else "   ✗ FAIL")
    
    print("\n2. Discrete Symmetry:")
    sym_results = results['discrete_symmetry']
    print(f"   Angle variance: {sym_results['angle_variance']:.2e}°")
    print(f"   Max scaling error: {sym_results['max_scaling_error']:.2e}")
    print(f"   All aligned at 135°: {sym_results['all_aligned_at_135']}")
    print(f"   ✓ PASS" if sym_results['all_aligned_at_135'] and sym_results['linear_scaling_preserved'] else "   ✗ FAIL")
    
    print("\n3. Periodic Table-like Sampling:")
    period_results = results['periodicity']
    print(f"   Samples: {period_results['num_samples']}")
    print(f"   Z range: {period_results['z_range']}")
    print(f"   Magnitude range: ({period_results['magnitude_range'][0]:.6e}, {period_results['magnitude_range'][1]:.6e})")
    print(f"   Uniform spacing: {period_results['uniform_spacing']}")
    print(f"   All on 135° ray: {period_results['all_on_135_ray']}")
    print(f"   ✓ PASS" if period_results['all_on_135_ray'] and period_results['uniform_spacing'] else "   ✗ FAIL")
    
    print("\n4. Statistical Tests (NIST-style):")
    stat_results = results['statistical_tests']
    print(f"   Data length: {stat_results['data_length']} bytes")
    print(f"   Frequency test: {'PASS' if stat_results['frequency_test']['passed'] else 'FAIL'} (p={stat_results['frequency_test']['p_value']:.4f})")
    print(f"   Runs test: {'PASS' if stat_results['runs_test']['passed'] else 'FAIL'} (p={stat_results['runs_test']['p_value']:.4f})")
    print(f"   Chi-square test: {'PASS' if stat_results['chi_square_test']['passed'] else 'FAIL'} (χ²={stat_results['chi_square_test']['chi_square']:.2f})")
    print(f"   Serial correlation: {'PASS' if stat_results['serial_correlation_test']['passed'] else 'FAIL'} (r={stat_results['serial_correlation_test']['correlation']:.4f})")
    print(f"   Overall: {'✓ PASS' if stat_results['overall_passed'] else '✗ FAIL'}")
    
    print("\n" + "=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)
    assessment = results['overall_assessment']
    print(f"✓ μ is 8th root of unity: {assessment['mu_is_8th_root']}")
    print(f"✓ Discrete symmetry maintained: {assessment['discrete_symmetry_maintained']}")
    print(f"✓ Linear scaling preserved: {assessment['linear_scaling_preserved']}")
    print(f"✓ Periodic sampling consistent: {assessment['periodic_sampling_consistent']}")
    print(f"✓ Statistical tests passed: {assessment['statistical_tests_passed']}")
    
    all_passed = all(assessment.values())
    print()
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print()
        print("The framework demonstrates:")
        print("  • Discrete symmetry by geometry using μ as 8th root of unity")
        print("  • Coherent and predictable results with α scaling and quantized Z")
        print("  • Periodic table-like discrete samples along the 135° ray")
        print("  • Statistical properties compatible with deterministic structure")
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print()
        print("Failed validations:")
        for key, value in assessment.items():
            if not value:
                print(f"  • {key}")
    
    print("=" * 80)
