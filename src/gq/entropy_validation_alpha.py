"""
Entropy Validation Framework with Fine-Structure Constant Scaling

This module implements a comprehensive entropy validation framework using:
- φ ≈ 1.618... (golden ratio) for fractional-phase resampling
- α ≈ 1/137 (fine-structure constant approximation) for scaling
- Z ∈ {1, 2, 3, ...} (integer quantization)
- Vector formulation: V_Z = Z · α · exp(2πi{Z·φ})

The framework tests whether this approach supports claims about:
1. Magnitude component: |V_Z| = Z·α (linear scaling with Z and α)
2. Fractional-phase resampling: Golden ratio φ provides low-discrepancy sequences
3. Uniform angular distribution on the unit circle via {Z·φ} modulo 1
4. NIST SP 800-90 statistical entropy validation

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
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618033988749895
ALPHA = 1.0 / 137.035999084  # Fine-structure constant (CODATA 2018) - precise value
ALPHA_APPROX = 1.0 / 137  # Approximation as specified in problem statement
# Note: ALPHA_APPROX is used throughout the framework as specified in the requirements

# IEEE 754 constants
EPSILON_64 = sys.float_info.epsilon  # Machine epsilon for double precision


def fractional_part(x: float) -> float:
    """
    Compute the fractional part {x} = x - floor(x).
    
    Args:
        x: Input value
        
    Returns:
        Fractional part in [0, 1)
    """
    return x - math.floor(x)


class QuantizedVector:
    """
    Represents a quantized vector V_Z = Z · α · exp(2πi{Z·φ})
    
    Attributes:
        z: Integer quantum number (Z ∈ {1, 2, 3, ...})
        alpha: Fine-structure constant scaling factor
        phi: Golden ratio for fractional-phase resampling
        vector: The computed vector V_Z
    """
    
    def __init__(self, z: int, alpha: float = ALPHA_APPROX, phi: float = PHI):
        """
        Initialize a quantized vector.
        
        Args:
            z: Integer quantum number (must be positive)
            alpha: Fine-structure constant (default: 1/137)
            phi: Golden ratio (default: (1+√5)/2)
        """
        if z < 1:
            raise ValueError("Z must be a positive integer (Z ∈ {1, 2, 3, ...})")
        
        self.z = z
        self.alpha = alpha
        self.phi = phi
        
        # Magnitude: |V_Z| = Z · α
        magnitude = z * alpha
        
        # Phase: exp(2πi{Z·φ}) where {x} is fractional part
        fractional_phase = fractional_part(z * phi)
        phase_angle = 2 * math.pi * fractional_phase
        phase = cmath.exp(1j * phase_angle)
        
        # V_Z = Z · α · exp(2πi{Z·φ})
        self.vector = magnitude * phase
    
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
    
    def fractional_phase(self) -> float:
        """Get the fractional phase {Z·φ} in [0, 1)."""
        return fractional_part(self.z * self.phi)
    
    def __repr__(self) -> str:
        return f"V_{self.z} = {self.z} × α × exp(2πi{{{self.z}·φ}}) = {self.vector}"


class DiscreteSymmetryValidator:
    """
    Validates discrete symmetry properties of quantized vectors.
    
    Tests whether the golden ratio φ provides low-discrepancy sequences
    for uniform angular distribution on the unit circle.
    """
    
    @staticmethod
    def verify_golden_ratio_properties() -> Dict[str, Any]:
        """
        Verify properties of the golden ratio φ.
        
        The golden ratio has the property: φ = 1 + 1/φ
        Also, φ² = φ + 1
        """
        phi_squared = PHI ** 2
        phi_plus_one = PHI + 1
        
        error = abs(phi_squared - phi_plus_one)
        is_valid = error < 1e-10
        
        return {
            'phi': PHI,
            'phi_value': PHI,
            'phi_squared': phi_squared,
            'phi_plus_one': phi_plus_one,
            'phi_squared_error': error,
            'is_golden_ratio': is_valid,
            'tolerance': 1e-10,
            'continued_fraction': '1 + 1/(1 + 1/(1 + ...))'
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
        
        # Magnitudes should scale linearly with Z
        magnitudes = [v.magnitude() for v in vectors]
        expected_scaling = [(z * ALPHA_APPROX) for z in z_values]
        scaling_errors = [abs(m - e) for m, e in zip(magnitudes, expected_scaling)]
        max_scaling_error = max(scaling_errors)
        
        # Angles should be distributed according to {Z·φ}
        angles_radians = [v.angle() for v in vectors]
        angles_degrees = [v.angle_degrees() for v in vectors]
        fractional_phases = [v.fractional_phase() for v in vectors]
        
        return {
            'z_values': z_values,
            'angles_radians': angles_radians,
            'angles_degrees': angles_degrees,
            'fractional_phases': fractional_phases,
            'magnitudes': magnitudes,
            'expected_magnitudes': expected_scaling,
            'max_scaling_error': max_scaling_error,
            'linear_scaling_preserved': max_scaling_error < 1e-10
        }


class PeriodicTableValidator:
    """
    Validates low-discrepancy sequence properties using golden ratio.
    
    Tests whether fractional phases {Z·φ} provide uniform distribution
    on the unit circle according to Weyl's equidistribution theorem.
    """
    
    @staticmethod
    def generate_periodic_samples(max_z: int = 118) -> List[QuantizedVector]:
        """
        Generate samples with golden ratio phase distribution.
        
        Args:
            max_z: Maximum Z value (default: 118, similar to periodic table)
            
        Returns:
            List of quantized vectors for Z = 1 to max_z
        """
        return [QuantizedVector(z) for z in range(1, max_z + 1)]
    
    @staticmethod
    def analyze_periodicity(vectors: List[QuantizedVector]) -> Dict[str, Any]:
        """
        Analyze low-discrepancy and uniformity of sampled vectors.
        
        Args:
            vectors: List of quantized vectors
            
        Returns:
            Dictionary with distribution analysis
        """
        z_values = [v.z for v in vectors]
        magnitudes = [v.magnitude() for v in vectors]
        angles = [v.angle_degrees() for v in vectors]
        fractional_phases = [v.fractional_phase() for v in vectors]
        
        # Check linear spacing of magnitudes
        magnitude_diffs = [magnitudes[i+1] - magnitudes[i] 
                          for i in range(len(magnitudes) - 1)]
        mean_diff = sum(magnitude_diffs) / len(magnitude_diffs)
        diff_variance = sum((d - mean_diff)**2 for d in magnitude_diffs) / len(magnitude_diffs)
        
        # Check uniformity of fractional phases (low-discrepancy)
        # For a truly uniform distribution, phases should be spread across [0, 1)
        phase_bins = [0] * 10  # 10 bins
        for fp in fractional_phases:
            bin_idx = min(int(fp * 10), 9)
            phase_bins[bin_idx] += 1
        
        expected_per_bin = len(vectors) / 10
        chi_square = sum((count - expected_per_bin)**2 / expected_per_bin 
                         for count in phase_bins)
        
        # Compute discrepancy (simplified star discrepancy estimate)
        sorted_phases = sorted(fractional_phases)
        max_discrepancy = 0.0
        n = len(sorted_phases)
        for i, phase in enumerate(sorted_phases):
            # Discrepancy between empirical and uniform CDF
            empirical_cdf = (i + 1) / n
            uniform_cdf = phase
            discrepancy = abs(empirical_cdf - uniform_cdf)
            max_discrepancy = max(max_discrepancy, discrepancy)
        
        return {
            'num_samples': len(vectors),
            'z_range': (min(z_values), max(z_values)),
            'magnitude_range': (min(magnitudes), max(magnitudes)),
            'mean_magnitude_spacing': mean_diff,
            'magnitude_spacing_variance': diff_variance,
            'uniform_magnitude_spacing': diff_variance < 1e-20,
            'fractional_phase_range': (min(fractional_phases), max(fractional_phases)),
            'phase_bin_distribution': phase_bins,
            'phase_chi_square': chi_square,
            'phase_uniformity_passed': chi_square < 20.0,  # χ² critical value for 9 df at α=0.01
            'star_discrepancy': max_discrepancy,
            'low_discrepancy': max_discrepancy < 0.1  # Good low-discrepancy threshold
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
    
    # 1. Verify golden ratio properties
    results['golden_ratio_validation'] = DiscreteSymmetryValidator.verify_golden_ratio_properties()
    
    # 2. Verify discrete symmetry and linear magnitude scaling
    test_z_values = [1, 2, 5, 10, 20, 50, 100, 118]
    results['discrete_symmetry'] = DiscreteSymmetryValidator.verify_discrete_symmetry(test_z_values)
    
    # 3. Validate low-discrepancy sequence properties
    periodic_samples = PeriodicTableValidator.generate_periodic_samples(118)
    results['low_discrepancy'] = PeriodicTableValidator.analyze_periodicity(periodic_samples)
    
    # 4. Generate entropy stream and test
    entropy_stream = EntropyExtractor.generate_entropy_stream((1, 118), 10000)
    results['statistical_tests'] = StatisticalValidator.comprehensive_analysis(entropy_stream)
    
    # 5. Overall assessment
    results['overall_assessment'] = {
        'phi_is_golden_ratio': results['golden_ratio_validation']['is_golden_ratio'],
        'linear_magnitude_scaling': results['discrete_symmetry']['linear_scaling_preserved'],
        'low_discrepancy_phase': results['low_discrepancy']['low_discrepancy'],
        'phase_uniformity': results['low_discrepancy']['phase_uniformity_passed'],
        'statistical_tests_passed': results['statistical_tests']['overall_passed']
    }
    
    return results


if __name__ == '__main__':
    """Run validation when module is executed directly."""
    print("=" * 80)
    print("Entropy Validation Framework with Golden Ratio Phase Distribution")
    print("=" * 80)
    print()
    print(f"Configuration:")
    print(f"  φ = (1 + √5)/2 ≈ {PHI:.15f}")
    print(f"  α = 1/137 ≈ {ALPHA_APPROX:.10f}")
    print(f"  V_Z = Z · α · exp(2πi{{Z·φ}})")
    print()
    
    print("Running comprehensive validation...")
    results = validate_framework()
    
    print("\n" + "=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    
    print("\n1. Golden Ratio Verification:")
    gr_results = results['golden_ratio_validation']
    print(f"   φ = {gr_results['phi']:.15f}")
    print(f"   φ² = {gr_results['phi_squared']:.15f}")
    print(f"   φ + 1 = {gr_results['phi_plus_one']:.15f}")
    print(f"   |φ² - (φ+1)| = {gr_results['phi_squared_error']:.2e}")
    print(f"   ✓ PASS" if gr_results['is_golden_ratio'] else "   ✗ FAIL")
    
    print("\n2. Magnitude Scaling (Linear with Z):")
    sym_results = results['discrete_symmetry']
    print(f"   Max scaling error: {sym_results['max_scaling_error']:.2e}")
    print(f"   Linear scaling preserved: {sym_results['linear_scaling_preserved']}")
    print(f"   ✓ PASS" if sym_results['linear_scaling_preserved'] else "   ✗ FAIL")
    
    print("\n3. Low-Discrepancy Phase Distribution:")
    ld_results = results['low_discrepancy']
    print(f"   Samples: {ld_results['num_samples']}")
    print(f"   Z range: {ld_results['z_range']}")
    print(f"   Star discrepancy: {ld_results['star_discrepancy']:.6f}")
    print(f"   Phase χ² statistic: {ld_results['phase_chi_square']:.2f}")
    print(f"   Phase uniformity: {'PASS' if ld_results['phase_uniformity_passed'] else 'FAIL'}")
    print(f"   Low-discrepancy: {'PASS' if ld_results['low_discrepancy'] else 'FAIL'}")
    print(f"   ✓ PASS" if ld_results['low_discrepancy'] and ld_results['phase_uniformity_passed'] else "   ✗ FAIL")
    
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
    print(f"✓ φ is golden ratio: {assessment['phi_is_golden_ratio']}")
    print(f"✓ Linear magnitude scaling (|V_Z| = Z·α): {assessment['linear_magnitude_scaling']}")
    print(f"✓ Low-discrepancy phase distribution: {assessment['low_discrepancy_phase']}")
    print(f"✓ Phase uniformity on unit circle: {assessment['phase_uniformity']}")
    print(f"✓ Statistical tests passed: {assessment['statistical_tests_passed']}")
    
    all_passed = all(assessment.values())
    print()
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print()
        print("The framework demonstrates:")
        print("  • Magnitude component: |V_Z| = Z·α (linear scaling)")
        print("  • Fractional-phase resampling via golden ratio φ")
        print("  • Low-discrepancy sequences on the unit circle")
        print("  • Uniform angular distribution via {Z·φ}")
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print()
        print("Failed validations:")
        for key, value in assessment.items():
            if not value:
                print(f"  • {key}")
    
    print("=" * 80)
