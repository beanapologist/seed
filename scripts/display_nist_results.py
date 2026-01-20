#!/usr/bin/env python3
"""
Display NIST STS results in GitHub Actions summary format.
"""

import json
import sys
from pathlib import Path


def display_results(results_file: Path):
    """Display test results in markdown format for GitHub Actions."""
    with open(results_file) as f:
        r = json.load(f)
    
    print('### Summary')
    print(f"- Total bits: {r['metadata']['total_bits']:,}")
    print(f"- Tests passed: {r['summary']['passed']}/{r['summary']['total_tests']}")
    print(f"- Pass rate: {r['summary']['pass_rate']*100:.1f}%")
    print(f"- Overall: {'✓ PASSED' if r['summary']['overall_passed'] else '✗ FAILED'}")
    print()
    print('### Test Details')
    print('| Test | P-Value | Status |')
    print('|------|---------|--------|')
    for name, result in r['tests'].items():
        status = '✓' if result['passed'] else '✗'
        print(f"| {name} | {result['p_value']:.6f} | {status} {result['status']} |")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <results_json_file>", file=sys.stderr)
        sys.exit(1)
    
    results_file = Path(sys.argv[1])
    if not results_file.exists():
        print(f"Error: File not found: {results_file}", file=sys.stderr)
        sys.exit(1)
    
    display_results(results_file)
