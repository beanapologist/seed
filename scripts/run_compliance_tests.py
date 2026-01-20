#!/usr/bin/env python3
"""
Run Comprehensive Standards Compliance Tests

This script executes all standards compliance tests and generates a detailed report.
It validates compliance with:
- NIST SP 800-22 (Statistical Test Suite)
- NIST SP 800-90B (Entropy Source Validation)
- FIPS 203 (ML-KEM/Kyber)
- FIPS 204 (ML-DSA/Dilithium)
- FIPS 205 (SLH-DSA/SPHINCS+)
- IEEE 754 (Floating-Point Arithmetic)
- Quantum Mechanics Principles
- Cryptographic Hash Standards (FIPS 180-4)
- Information Theory

Usage:
    python run_compliance_tests.py [--verbose] [--report OUTPUT]
"""

import argparse
import sys
import unittest
import json
from datetime import datetime
from pathlib import Path

# Import compliance test modules
import test_standards_compliance


def run_compliance_suite(verbose=False):
    """
    Run complete standards compliance test suite.
    
    Args:
        verbose: If True, show detailed test output
        
    Returns:
        (result, summary) tuple where result is unittest.TestResult
        and summary is dict with test statistics
    """
    # Create test loader
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all compliance test classes
    test_classes = [
        test_standards_compliance.TestNISTSP80022Compliance,
        test_standards_compliance.TestNISTSP80090BCompliance,
        test_standards_compliance.TestFIPS203Compliance,
        test_standards_compliance.TestFIPS204Compliance,
        test_standards_compliance.TestFIPS205Compliance,
        test_standards_compliance.TestIEEE754Compliance,
        test_standards_compliance.TestQuantumMechanicsPrinciples,
        test_standards_compliance.TestCryptographicHashCompliance,
        test_standards_compliance.TestEntropyTheoryCompliance,
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Generate summary
    summary = {
        'total_tests': result.testsRun,
        'passed': result.testsRun - len(result.failures) - len(result.errors),
        'failed': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'success': result.wasSuccessful(),
        'timestamp': datetime.now().isoformat(),
    }
    
    return result, summary


def print_summary_report(summary):
    """Print summary report to console."""
    print("\n" + "="*70)
    print("STANDARDS COMPLIANCE TEST SUMMARY")
    print("="*70)
    print(f"Report Date: {summary['timestamp']}")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed:      {summary['passed']} ({summary['passed']/summary['total_tests']*100:.1f}%)")
    print(f"Failed:      {summary['failed']}")
    print(f"Errors:      {summary['errors']}")
    print(f"Skipped:     {summary['skipped']}")
    print("="*70)
    
    if summary['success']:
        print("✅ OVERALL STATUS: FULLY COMPLIANT")
        print("\nAll generators comply with applicable NIST and physics standards.")
    else:
        print("❌ OVERALL STATUS: NON-COMPLIANT")
        print("\nSome tests failed. Review failures above for details.")
    
    print("="*70)


def generate_json_report(summary, output_path):
    """Generate JSON report file."""
    # Determine compliance status based on actual test results
    overall_status = 'COMPLIANT' if summary['success'] else 'NON-COMPLIANT'
    standard_status = 'COMPLIANT' if summary['success'] else 'NON-COMPLIANT'
    
    report = {
        'compliance_report': {
            'version': '1.0',
            'repository': 'beanapologist/seed',
            'timestamp': summary['timestamp'],
            'overall_status': overall_status,
            'test_summary': summary,
            'standards_tested': [
                {
                    'standard': 'NIST SP 800-22 Rev. 1a',
                    'description': 'Statistical Test Suite for RNGs',
                    'status': standard_status
                },
                {
                    'standard': 'NIST SP 800-90B',
                    'description': 'Entropy Source Validation',
                    'status': standard_status
                },
                {
                    'standard': 'FIPS 203',
                    'description': 'ML-KEM (Kyber)',
                    'status': standard_status
                },
                {
                    'standard': 'FIPS 204',
                    'description': 'ML-DSA (Dilithium)',
                    'status': standard_status
                },
                {
                    'standard': 'FIPS 205',
                    'description': 'SLH-DSA (SPHINCS+)',
                    'status': standard_status
                },
                {
                    'standard': 'IEEE 754-2019',
                    'description': 'Floating-Point Arithmetic',
                    'status': standard_status
                },
                {
                    'standard': 'FIPS 180-4',
                    'description': 'Secure Hash Standard',
                    'status': standard_status
                },
                {
                    'standard': 'Quantum Mechanics',
                    'description': 'Unit circle, 8th roots of unity',
                    'status': standard_status
                },
                {
                    'standard': 'Information Theory',
                    'description': 'Shannon entropy, statistical independence',
                    'status': standard_status
                }
            ]
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 JSON report written to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run comprehensive standards compliance tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_compliance_tests.py
  python run_compliance_tests.py --verbose
  python run_compliance_tests.py --report compliance_report.json
  python run_compliance_tests.py -v --report results/compliance.json
        """
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed test output')
    parser.add_argument('--report', type=str, metavar='OUTPUT',
                       help='Generate JSON report to specified file')
    
    args = parser.parse_args()
    
    # Print header
    print("="*70)
    print("COMPREHENSIVE STANDARDS COMPLIANCE TEST SUITE")
    print("="*70)
    print("\nTesting compliance with:")
    print("  • NIST SP 800-22 Rev. 1a (Statistical Tests)")
    print("  • NIST SP 800-90B (Entropy Sources)")
    print("  • FIPS 203/204/205 (Post-Quantum Cryptography)")
    print("  • IEEE 754-2019 (Floating-Point Arithmetic)")
    print("  • FIPS 180-4 (Cryptographic Hashing)")
    print("  • Quantum Mechanics Principles")
    print("  • Information Theory")
    print("\nRunning tests...\n")
    
    # Run tests
    result, summary = run_compliance_suite(verbose=args.verbose)
    
    # Print summary
    print_summary_report(summary)
    
    # Generate JSON report if requested
    if args.report:
        generate_json_report(summary, args.report)
    
    # Exit with appropriate code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
