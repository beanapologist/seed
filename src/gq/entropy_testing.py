"""
Comprehensive Entropy Testing Module

This module provides statistical analysis tools for validating the entropy quality
of cryptographic random number generators and key generation mechanisms.

Implements tests from:
- NIST Special Publication 800-22 (Statistical Test Suite)
- Basic Shannon entropy analysis
- Distribution uniformity tests
- Bias detection tests

These tests ensure cryptographic security standards are met for:
- Universal QKD (GCP-1) key generation
- Binary Fusion Tap algorithm
- NIST PQC hybrid key generation
- Quantum key generator service
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List, Tuple, Optional


class EntropyAnalyzer:
    """
    Statistical analyzer for cryptographic entropy validation.
    
    Provides multiple statistical tests to validate randomness quality
    and detect potential biases in cryptographic key material.
    """
    
    def __init__(self, data: bytes):
        """
        Initialize entropy analyzer with binary data.
        
        Args:
            data: Binary data to analyze (key material, seeds, etc.)
        """
        self.data = data
        self.bit_length = len(data) * 8
        
    def shannon_entropy(self) -> float:
        """
        Calculate Shannon entropy in bits per byte.
        
        Shannon entropy measures the average information content per byte.
        For cryptographic quality randomness, we expect values close to 8.0
        (maximum entropy for byte-level analysis).
        
        Returns:
            Shannon entropy value (0.0 to 8.0 bits per byte)
        """
        if len(self.data) == 0:
            return 0.0
        
        # Count byte frequencies
        byte_counts = [0] * 256
        for byte in self.data:
            byte_counts[byte] += 1
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in byte_counts:
            if count > 0:
                probability = count / len(self.data)
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def byte_distribution(self) -> Dict[str, float]:
        """
        Analyze byte distribution for uniformity.
        
        Returns:
            Dictionary with distribution metrics:
            - unique_bytes: Number of unique byte values (0-256)
            - byte_diversity: Ratio of unique bytes to possible values
            - most_common_frequency: Frequency of most common byte
            - least_common_frequency: Frequency of least common byte (non-zero)
        """
        if len(self.data) == 0:
            return {
                'unique_bytes': 0,
                'byte_diversity': 0.0,
                'most_common_frequency': 0.0,
                'least_common_frequency': 0.0
            }
        
        counter = Counter(self.data)
        frequencies = list(counter.values())
        
        return {
            'unique_bytes': len(counter),
            'byte_diversity': len(counter) / 256,
            'most_common_frequency': max(frequencies) / len(self.data),
            'least_common_frequency': min(frequencies) / len(self.data) if frequencies else 0.0
        }
    
    def monobit_frequency_test(self) -> Dict[str, float]:
        """
        NIST SP 800-22 Monobit Frequency Test.
        
        Tests the proportion of zeros and ones in the entire sequence.
        For random data, we expect roughly equal numbers of 0s and 1s.
        
        Returns:
            Dictionary with:
            - ones_count: Number of 1 bits
            - zeros_count: Number of 0 bits
            - ones_ratio: Ratio of 1s to total bits
            - balance: Absolute difference from 0.5 (lower is better)
            - passes: True if test passes (balance < 0.05)
        """
        if len(self.data) == 0:
            return {
                'ones_count': 0,
                'zeros_count': 0,
                'ones_ratio': 0.0,
                'balance': 0.0,
                'passes': False
            }
        
        # Count 1 bits
        ones_count = 0
        for byte in self.data:
            ones_count += bin(byte).count('1')
        
        zeros_count = self.bit_length - ones_count
        ones_ratio = ones_count / self.bit_length
        balance = abs(ones_ratio - 0.5)
        
        # Pass if balance is within 5% of ideal (0.5)
        passes = balance < 0.05
        
        return {
            'ones_count': ones_count,
            'zeros_count': zeros_count,
            'ones_ratio': ones_ratio,
            'balance': balance,
            'passes': passes
        }
    
    def runs_test(self) -> Dict[str, any]:
        """
        Runs test for bit independence.
        
        A "run" is a sequence of consecutive identical bits. This test checks
        if the number of runs is consistent with a random sequence.
        
        Returns:
            Dictionary with:
            - total_runs: Number of runs found
            - expected_runs: Expected number for random data
            - runs_ratio: Ratio of actual to expected
            - passes: True if within acceptable range (0.9 to 1.1)
        """
        if len(self.data) == 0 or self.bit_length < 2:
            return {
                'total_runs': 0,
                'expected_runs': 0,
                'runs_ratio': 0.0,
                'passes': False
            }
        
        # Convert to bit string
        bit_string = ''.join(format(byte, '08b') for byte in self.data)
        
        # Count runs
        runs = 1
        for i in range(1, len(bit_string)):
            if bit_string[i] != bit_string[i-1]:
                runs += 1
        
        # Expected runs for random sequence
        # E[runs] = (2 * n0 * n1 / n) + 1 where n0 = zeros, n1 = ones
        monobit = self.monobit_frequency_test()
        n0 = monobit['zeros_count']
        n1 = monobit['ones_count']
        n = self.bit_length
        
        expected_runs = (2 * n0 * n1 / n) + 1 if n > 0 else 0
        runs_ratio = runs / expected_runs if expected_runs > 0 else 0.0
        
        # Pass if ratio is between 0.9 and 1.1
        passes = 0.9 <= runs_ratio <= 1.1
        
        return {
            'total_runs': runs,
            'expected_runs': expected_runs,
            'runs_ratio': runs_ratio,
            'passes': passes
        }
    
    def serial_correlation_test(self, lag: int = 1) -> Dict[str, float]:
        """
        Test for serial correlation between bytes.
        
        Checks if byte values are correlated with previous values,
        which would indicate non-random patterns.
        
        Args:
            lag: Number of positions to check correlation (default: 1)
        
        Returns:
            Dictionary with:
            - correlation: Correlation coefficient (-1.0 to 1.0)
            - passes: True if |correlation| < 0.1 (weak correlation)
        """
        if len(self.data) < lag + 1:
            return {
                'correlation': 0.0,
                'passes': False
            }
        
        # Calculate mean
        mean_val = sum(self.data) / len(self.data)
        
        # Calculate correlation
        numerator = 0
        denominator = 0
        
        for i in range(len(self.data) - lag):
            deviation1 = self.data[i] - mean_val
            deviation2 = self.data[i + lag] - mean_val
            numerator += deviation1 * deviation2
            denominator += deviation1 * deviation1
        
        correlation = numerator / denominator if denominator > 0 else 0.0
        
        # Pass if absolute correlation is small
        passes = abs(correlation) < 0.1
        
        return {
            'correlation': correlation,
            'passes': passes
        }
    
    def chi_square_test(self) -> Dict[str, any]:
        """
        Chi-square test for uniform distribution.
        
        Tests if byte values are uniformly distributed across all possible
        values (0-255). For cryptographic randomness, we expect uniform distribution.
        
        Returns:
            Dictionary with:
            - chi_square: Chi-square statistic
            - expected_frequency: Expected count per byte value
            - degrees_of_freedom: Degrees of freedom (255)
            - passes: True if distribution appears uniform
        """
        if len(self.data) == 0:
            return {
                'chi_square': 0.0,
                'expected_frequency': 0.0,
                'degrees_of_freedom': 255,
                'passes': False
            }
        
        # Count byte frequencies
        byte_counts = [0] * 256
        for byte in self.data:
            byte_counts[byte] += 1
        
        # Expected frequency for uniform distribution
        expected = len(self.data) / 256
        
        # Calculate chi-square statistic
        chi_square = 0.0
        for observed in byte_counts:
            chi_square += ((observed - expected) ** 2) / expected if expected > 0 else 0
        
        # For 255 degrees of freedom and 95% confidence, critical value ≈ 293
        # For smaller samples, adjust threshold
        critical_value = 293 if len(self.data) >= 256 else len(self.data) * 1.2
        passes = chi_square < critical_value
        
        return {
            'chi_square': chi_square,
            'expected_frequency': expected,
            'degrees_of_freedom': 255,
            'passes': passes
        }
    
    def comprehensive_analysis(self) -> Dict[str, any]:
        """
        Perform comprehensive entropy analysis.
        
        Runs all statistical tests and provides overall assessment.
        
        Returns:
            Dictionary containing:
            - All individual test results
            - overall_quality: Quality rating (excellent/good/fair/poor)
            - passes_all_tests: True if all critical tests pass
            - recommendations: List of recommendations if any tests fail
        """
        results = {
            'data_length_bytes': len(self.data),
            'data_length_bits': self.bit_length,
            'shannon_entropy': self.shannon_entropy(),
            'byte_distribution': self.byte_distribution(),
            'monobit_test': self.monobit_frequency_test(),
            'runs_test': self.runs_test(),
            'serial_correlation': self.serial_correlation_test(),
            'chi_square_test': self.chi_square_test()
        }
        
        # Evaluate overall quality
        shannon = results['shannon_entropy']
        monobit_pass = results['monobit_test']['passes']
        runs_pass = results['runs_test']['passes']
        correlation_pass = results['serial_correlation']['passes']
        chi_square_pass = results['chi_square_test']['passes']
        
        all_pass = monobit_pass and runs_pass and correlation_pass and chi_square_pass
        
        # Quality rating based on Shannon entropy and test passes
        if shannon >= 7.5 and all_pass:
            quality = 'excellent'
        elif shannon >= 7.0 and (monobit_pass and runs_pass):
            quality = 'good'
        elif shannon >= 6.0:
            quality = 'fair'
        else:
            quality = 'poor'
        
        results['overall_quality'] = quality
        results['passes_all_tests'] = all_pass
        
        # Generate recommendations
        recommendations = []
        if shannon < 7.0:
            recommendations.append(f"Shannon entropy ({shannon:.2f}) is below recommended 7.0+ for cryptographic use")
        if not monobit_pass:
            recommendations.append("Monobit frequency test failed - bit distribution is biased")
        if not runs_pass:
            recommendations.append("Runs test failed - bits may not be independent")
        if not correlation_pass:
            recommendations.append("Serial correlation detected - data may have patterns")
        if not chi_square_pass:
            recommendations.append("Chi-square test failed - byte distribution is not uniform")
        
        results['recommendations'] = recommendations
        
        return results


def analyze_key_stream(keys: List[bytes], min_sample_size: int = 1000) -> Dict[str, any]:
    """
    Analyze entropy across a stream of generated keys.
    
    Args:
        keys: List of key material (bytes) to analyze
        min_sample_size: Minimum total bytes needed for reliable analysis
    
    Returns:
        Dictionary with aggregate entropy analysis and per-key statistics
    """
    # Concatenate all keys for aggregate analysis
    combined_data = b''.join(keys)
    
    if len(combined_data) < min_sample_size:
        return {
            'error': f'Insufficient data: {len(combined_data)} bytes (minimum: {min_sample_size})',
            'total_keys': len(keys),
            'total_bytes': len(combined_data)
        }
    
    # Analyze combined key stream
    analyzer = EntropyAnalyzer(combined_data)
    aggregate_results = analyzer.comprehensive_analysis()
    
    # Analyze individual keys
    individual_entropies = []
    for key in keys:
        if len(key) > 0:
            key_analyzer = EntropyAnalyzer(key)
            individual_entropies.append(key_analyzer.shannon_entropy())
    
    # Calculate statistics across keys
    if individual_entropies:
        avg_entropy = sum(individual_entropies) / len(individual_entropies)
        min_entropy = min(individual_entropies)
        max_entropy = max(individual_entropies)
    else:
        avg_entropy = min_entropy = max_entropy = 0.0
    
    return {
        'aggregate_analysis': aggregate_results,
        'per_key_statistics': {
            'total_keys': len(keys),
            'average_entropy': avg_entropy,
            'min_entropy': min_entropy,
            'max_entropy': max_entropy,
            'entropy_variance': sum((e - avg_entropy) ** 2 for e in individual_entropies) / len(individual_entropies) if individual_entropies else 0.0
        }
    }


def validate_zero_bias(data: bytes) -> Dict[str, any]:
    """
    Validate that random seed generation has zero bias.
    
    Specifically checks for common bias patterns:
    - Leading zeros
    - Trailing zeros  
    - Repeated patterns
    - Low byte diversity
    
    Args:
        data: Binary data to check for bias
    
    Returns:
        Dictionary with bias detection results
    """
    if len(data) == 0:
        return {
            'has_bias': True,
            'bias_types': ['empty_data'],
            'passes': False
        }
    
    bias_types = []
    
    # Check for leading zeros (first 4 bytes)
    if len(data) >= 4 and data[:4] == b'\x00\x00\x00\x00':
        bias_types.append('leading_zeros')
    
    # Check for trailing zeros (last 4 bytes)
    if len(data) >= 4 and data[-4:] == b'\x00\x00\x00\x00':
        bias_types.append('trailing_zeros')
    
    # Check for repeated patterns (same byte repeated)
    if len(set(data[:8])) == 1 and len(data) >= 8:
        bias_types.append('repeated_pattern')
    
    # Check byte diversity
    diversity = len(set(data)) / min(len(data), 256)
    if diversity < 0.3:
        bias_types.append('low_diversity')
    
    # Check for all zeros
    if all(byte == 0 for byte in data):
        bias_types.append('all_zeros')
    
    # Check for all ones (0xFF)
    if all(byte == 0xFF for byte in data):
        bias_types.append('all_ones')
    
    has_bias = len(bias_types) > 0
    
    return {
        'has_bias': has_bias,
        'bias_types': bias_types,
        'byte_diversity': diversity,
        'passes': not has_bias
    }
