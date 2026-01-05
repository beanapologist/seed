#!/usr/bin/env python3
"""
Integration test for runtime validation and entropy testing.

This script demonstrates the full functionality of the runtime validation
and entropy testing systems.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_runtime_validation():
    """Test runtime validation script."""
    print("="*60)
    print("Testing Runtime Validation")
    print("="*60)
    
    from runtime_validation import CryptoOperationMonitor
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        monitor = CryptoOperationMonitor(output_file=tmp_path)
        
        # Test RNG monitoring
        print("\n1. Testing RNG monitoring...")
        stats = monitor.monitor_random_generation(count=5)
        assert stats['total_operations'] == 5
        assert stats['all_bias_free'] == True
        assert stats['average_entropy'] > 3.0
        print(f"   ✓ RNG monitoring works: {stats['total_operations']} operations, avg entropy {stats['average_entropy']:.2f}")
        
        # Test key exchange monitoring
        print("\n2. Testing key exchange monitoring...")
        stats = monitor.monitor_key_exchange(count=3)
        assert stats['total_exchanges'] == 3
        assert stats['average_entropy'] > 4.0
        print(f"   ✓ Key exchange monitoring works: {stats['total_exchanges']} exchanges, avg entropy {stats['average_entropy']:.2f}")
        
        # Save log
        monitor.save_log()
        
        # Verify log file
        assert os.path.exists(tmp_path)
        with open(tmp_path, 'r') as f:
            log_data = json.load(f)
        assert log_data['total_operations'] == 8  # 5 RNG + 3 KEX
        print(f"\n3. Log file verification:")
        print(f"   ✓ Log file created: {tmp_path}")
        print(f"   ✓ Total operations logged: {log_data['total_operations']}")
        
        return True
        
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_dieharder_components():
    """Test Dieharder integration components (without actual Dieharder)."""
    print("\n" + "="*60)
    print("Testing Dieharder Integration Components")
    print("="*60)
    
    from dieharder_test import parse_size, DieharderTester
    from gq import UniversalQKD, generate_hybrid_key, PQCAlgorithm
    
    # Test size parsing
    print("\n1. Testing size parsing...")
    assert parse_size("10MB") == 10 * 1024 * 1024
    assert parse_size("1GB") == 1024 * 1024 * 1024
    assert parse_size("5KB") == 5 * 1024
    print("   ✓ Size parsing works correctly")
    
    # Test DieharderTester with generate-only mode
    print("\n2. Testing DieharderTester (generate-only mode)...")
    tester = DieharderTester(verbose=False, skip_dieharder_check=True)
    data = tester.generate_random_data('universal_qkd', 1024)
    assert len(data) == 1024
    print(f"   ✓ Generated {len(data)} bytes with DieharderTester")
    
    # Test data generation - Universal QKD
    print("\n3. Testing Universal QKD data generation...")
    generator = UniversalQKD()
    crypto_data = bytearray()
    for i in range(10):
        key = next(generator)
        crypto_data.extend(key)
    assert len(crypto_data) == 160  # 10 keys * 16 bytes
    print(f"   ✓ Generated {len(crypto_data)} bytes from Universal QKD")
    
    # Test data generation - NIST PQC
    print("\n4. Testing NIST PQC data generation...")
    crypto_data = bytearray()
    for i in range(5):
        det_key, pqc_seed = generate_hybrid_key(PQCAlgorithm.KYBER768)
        crypto_data.extend(det_key)
        crypto_data.extend(pqc_seed)
    assert len(crypto_data) == 240  # 5 * (16 + 32) bytes
    print(f"   ✓ Generated {len(crypto_data)} bytes from NIST PQC")
    
    return True


def test_entropy_analysis():
    """Test entropy analysis on generated data."""
    print("\n" + "="*60)
    print("Testing Entropy Analysis")
    print("="*60)
    
    from gq import UniversalQKD
    from gq.entropy_testing import EntropyAnalyzer, validate_zero_bias
    
    # Generate some keys
    print("\n1. Generating test data...")
    generator = UniversalQKD()
    keys = [next(generator) for _ in range(50)]
    print(f"   ✓ Generated {len(keys)} keys")
    
    # Analyze individual key
    print("\n2. Analyzing individual key entropy...")
    analyzer = EntropyAnalyzer(keys[0])
    entropy = analyzer.shannon_entropy()
    assert entropy > 3.0
    print(f"   ✓ Key entropy: {entropy:.2f} bits/byte")
    
    # Check bias
    print("\n3. Checking for bias...")
    bias_result = validate_zero_bias(keys[0])
    assert bias_result['passes'] == True
    print(f"   ✓ No bias detected")
    
    # Aggregate analysis
    print("\n4. Analyzing aggregate data...")
    aggregate_data = b''.join(keys)
    aggregate_analyzer = EntropyAnalyzer(aggregate_data)
    aggregate_entropy = aggregate_analyzer.shannon_entropy()
    assert aggregate_entropy > 7.0
    print(f"   ✓ Aggregate entropy: {aggregate_entropy:.2f} bits/byte")
    
    return True


def main():
    """Run all integration tests."""
    print("\n" + "="*70)
    print("Runtime Validation & Dieharder Integration - Integration Tests")
    print("="*70)
    
    all_passed = True
    
    try:
        if not test_runtime_validation():
            all_passed = False
    except Exception as e:
        print(f"\n❌ Runtime validation test failed: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        if not test_dieharder_components():
            all_passed = False
    except Exception as e:
        print(f"\n❌ Dieharder component test failed: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        if not test_entropy_analysis():
            all_passed = False
    except Exception as e:
        print(f"\n❌ Entropy analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("✓ ALL INTEGRATION TESTS PASSED!")
        print("="*70)
        print("\nThe runtime validation and Dieharder integration systems are")
        print("working correctly. The implementation is ready for use.")
        print("\nNext steps:")
        print("  1. Install Dieharder: sudo apt-get install dieharder")
        print("  2. Run full Dieharder tests: python scripts/dieharder_test.py")
        print("  3. Check CI/CD workflow in GitHub Actions")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
