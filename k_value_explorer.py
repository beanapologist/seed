#!/usr/bin/env python3
"""
K-Value Explorer for Binary Fusion Tap

Explore and visualize the Binary Fusion Tap algorithm across different k values.
Shows how seed generation, tap states, and ZPE overflow evolve with k.
"""

import argparse
import json
import sys
import os
# Add current directory (repository root) to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from typing import List, Dict
from checksum.verify_binary_representation import binary_fusion_tap, calculate_checksum


def explore_k_range(start: int, end: int, show_details: bool = False) -> List[Dict]:
    """
    Explore binary fusion tap across a range of k values.

    Args:
        start: Starting k value
        end: Ending k value (inclusive)
        show_details: Show detailed output for each k

    Returns:
        List of results for each k value
    """
    results = []

    for k in range(start, end + 1):
        tap = binary_fusion_tap(k)

        result = {
            'k': k,
            'seed_value': tap['seed_value'],
            'seed_length': len(str(tap['seed_value'])),
            'bit_length': len(tap['binary_seed']) - 2,  # Subtract '0b'
            'tap_state': tap['tap_state'],
            'tap_bit_length': len(tap['tap_state']) - 2,
            'zpe_overflow': tap['zpe_overflow'],
            'zpe_overflow_decimal': tap['zpe_overflow_decimal'],
            'has_zpe': k >= 10,
        }

        results.append(result)

    return results


def print_summary_table(results: List[Dict]) -> None:
    """Print a summary table of k-value exploration."""
    print("\n" + "=" * 100)
    print("BINARY FUSION TAP - K-VALUE EXPLORER")
    print("=" * 100)
    print(f"\n{'K':<4} {'Seed Value':<18} {'Seed Len':<10} {'Bits':<6} {'Tap Bits':<9} {'ZPE Overflow':<15}")
    print("-" * 100)

    for r in results:
        zpe_display = f"{r['zpe_overflow_decimal']}" if r['has_zpe'] else "N/A"
        print(f"{r['k']:<4} {r['seed_value']:<18} {r['seed_length']:<10} {r['bit_length']:<6} "
              f"{r['tap_bit_length']:<9} {zpe_display:<15}")

    print("-" * 100)
    print(f"Total k values explored: {len(results)}")
    print("=" * 100)


def print_detailed_output(results: List[Dict]) -> None:
    """Print detailed output for each k value."""
    for r in results:
        print("\n" + "=" * 80)
        print(f"K = {r['k']}")
        print("=" * 80)
        print(f"Seed Value: {r['seed_value']}")
        print(f"Seed String: {''.join(map(str, range(1, r['k'] + 1)))}")
        print(f"Binary Seed: {r['tap_state']}")
        print(f"Bit Length: {r['bit_length']} → {r['tap_bit_length']} (after 8-fold heartbeat)")

        if r['has_zpe']:
            print(f"ZPE Overflow: {r['zpe_overflow']} (decimal: {r['zpe_overflow_decimal']})")
        else:
            print("ZPE Overflow: N/A (k < 10)")

        print("=" * 80)


def generate_comparison_chart(results: List[Dict]) -> None:
    """Generate a visual comparison chart."""
    print("\n" + "=" * 100)
    print("BIT LENGTH GROWTH CHART")
    print("=" * 100)

    max_bits = max(r['tap_bit_length'] for r in results)
    scale = 100 / max_bits if max_bits > 0 else 1

    for r in results:
        bar_length = int(r['tap_bit_length'] * scale)
        bar = '█' * bar_length
        print(f"k={r['k']:2d} [{r['tap_bit_length']:3d} bits] {bar}")

    print("=" * 100)


def find_special_k_values(results: List[Dict]) -> Dict:
    """Find interesting k values."""
    special = {
        'first_zpe': None,
        'max_zpe': None,
        'power_of_2_bits': [],
        'fibonacci_k': [],
    }

    # Fibonacci numbers
    fib = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    for r in results:
        # First ZPE overflow
        if r['has_zpe'] and special['first_zpe'] is None:
            special['first_zpe'] = r

        # Maximum ZPE overflow
        if r['has_zpe']:
            if special['max_zpe'] is None or r['zpe_overflow_decimal'] > special['max_zpe']['zpe_overflow_decimal']:
                special['max_zpe'] = r

        # Power of 2 bit lengths
        if r['tap_bit_length'] in [8, 16, 32, 64, 128, 256]:
            special['power_of_2_bits'].append(r)

        # Fibonacci k values
        if r['k'] in fib:
            special['fibonacci_k'].append(r)

    return special


def print_special_values(special: Dict) -> None:
    """Print special/interesting k values."""
    print("\n" + "=" * 100)
    print("SPECIAL K VALUES")
    print("=" * 100)

    if special['first_zpe']:
        print(f"\nFirst ZPE Overflow (k={special['first_zpe']['k']}):")
        print(f"  Decimal: {special['first_zpe']['zpe_overflow_decimal']}")
        print(f"  Binary:  {special['first_zpe']['zpe_overflow']}")

    if special['max_zpe']:
        print(f"\nMaximum ZPE Overflow (k={special['max_zpe']['k']}):")
        print(f"  Decimal: {special['max_zpe']['zpe_overflow_decimal']}")
        print(f"  Binary:  {special['max_zpe']['zpe_overflow']}")

    if special['fibonacci_k']:
        print(f"\nFibonacci K Values:")
        for r in special['fibonacci_k']:
            print(f"  k={r['k']:2d}: {r['tap_bit_length']} bits, ZPE={r['zpe_overflow_decimal'] if r['has_zpe'] else 'N/A'}")

    if special['power_of_2_bits']:
        print(f"\nPower-of-2 Bit Lengths:")
        for r in special['power_of_2_bits']:
            print(f"  k={r['k']:2d}: {r['tap_bit_length']} bits")

    print("=" * 100)


def main():
    """CLI for k-value explorer."""
    parser = argparse.ArgumentParser(
        description='K-Value Explorer for Binary Fusion Tap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Explore k values 1-20
  python k_value_explorer.py --start 1 --end 20

  # Show detailed output for k=10-15
  python k_value_explorer.py --start 10 --end 15 --detailed

  # Find special values in range 1-30
  python k_value_explorer.py --start 1 --end 30 --special

  # Export to JSON
  python k_value_explorer.py --start 1 --end 20 --json -o k_values.json

  # Show visual chart
  python k_value_explorer.py --start 1 --end 25 --chart
        '''
    )

    parser.add_argument(
        '-s', '--start',
        type=int,
        default=1,
        help='Starting k value (default: 1)'
    )

    parser.add_argument(
        '-e', '--end',
        type=int,
        default=20,
        help='Ending k value (default: 20)'
    )

    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Show detailed output for each k'
    )

    parser.add_argument(
        '-c', '--chart',
        action='store_true',
        help='Show visual bit length growth chart'
    )

    parser.add_argument(
        '--special',
        action='store_true',
        help='Show special/interesting k values'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (optional)'
    )

    args = parser.parse_args()

    # Validate range
    if args.start < 1:
        parser.error("Start value must be >= 1")
    if args.end < args.start:
        parser.error("End value must be >= start value")

    # Explore k values
    results = explore_k_range(args.start, args.end)

    # Output results
    if args.json:
        output = json.dumps(results, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Results written to {args.output}")
        else:
            print(output)
    else:
        # Show summary table
        print_summary_table(results)

        # Show detailed output if requested
        if args.detailed:
            print_detailed_output(results)

        # Show chart if requested
        if args.chart:
            generate_comparison_chart(results)

        # Show special values if requested
        if args.special:
            special = find_special_k_values(results)
            print_special_values(special)


if __name__ == "__main__":
    main()
