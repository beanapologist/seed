#!/usr/bin/env python3
"""
Runtime Validation Script for Cryptographic Operations

This script instruments and monitors cryptographic operations during live deployments,
providing real-time logging and validation of:
- Random number generation
- Cryptographic key exchanges
- Entropy quality metrics
- Security compliance checks

Usage:
    python scripts/runtime_validation.py --monitor-duration 60
    python scripts/runtime_validation.py --output validation_log.json
    python scripts/runtime_validation.py --continuous
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gq import UniversalQKD, generate_hybrid_key, PQCAlgorithm
from gq.entropy_testing import EntropyAnalyzer, validate_zero_bias


class CryptoOperationMonitor:
    """Monitor and log cryptographic operations in real-time."""
    
    def __init__(self, output_file: str = None):
        """
        Initialize the crypto operation monitor.
        
        Args:
            output_file: Optional file path to write logs to
        """
        self.output_file = output_file
        self.operations: List[Dict[str, Any]] = []
        self.start_time = datetime.now(timezone.utc)
        
    def log_operation(self, operation_type: str, details: Dict[str, Any]):
        """
        Log a cryptographic operation with timestamp and details.
        
        Args:
            operation_type: Type of operation (e.g., 'key_generation', 'key_exchange')
            details: Dictionary of operation details
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        operation = {
            'timestamp': timestamp,
            'type': operation_type,
            'details': details
        }
        self.operations.append(operation)
        
        # Print to console
        print(f"[{timestamp}] {operation_type}: {json.dumps(details, indent=2)}")
        
    def monitor_random_generation(self, count: int = 10) -> Dict[str, Any]:
        """
        Monitor random number generation operations.
        
        Args:
            count: Number of random numbers to generate and monitor
            
        Returns:
            Statistics about the monitored operations
        """
        print(f"\n{'='*60}")
        print(f"Monitoring Random Number Generation ({count} operations)")
        print(f"{'='*60}\n")
        
        generator = UniversalQKD()
        keys = []
        entropy_scores = []
        
        for i in range(count):
            start = time.time()
            key = next(generator)
            duration = time.time() - start
            
            # Analyze entropy
            analyzer = EntropyAnalyzer(key)
            entropy = analyzer.shannon_entropy()
            entropy_scores.append(entropy)
            
            # Validate zero bias
            bias_check = validate_zero_bias(key)
            
            # Calculate checksum
            checksum = hashlib.sha256(key).hexdigest()
            
            details = {
                'operation_id': i + 1,
                'key_hex': key.hex(),
                'key_length_bytes': len(key),
                'entropy_bits_per_byte': round(entropy, 4),
                'has_bias': bias_check['has_bias'],
                'sha256_checksum': checksum,
                'duration_seconds': round(duration, 6)
            }
            
            self.log_operation('random_number_generation', details)
            keys.append(key)
            
        # Aggregate statistics
        stats = {
            'total_operations': count,
            'average_entropy': round(sum(entropy_scores) / len(entropy_scores), 4),
            'min_entropy': round(min(entropy_scores), 4),
            'max_entropy': round(max(entropy_scores), 4),
            'all_bias_free': all(not validate_zero_bias(k)['has_bias'] for k in keys)
        }
        
        print(f"\n{'='*60}")
        print("Random Number Generation Statistics:")
        print(json.dumps(stats, indent=2))
        print(f"{'='*60}\n")
        
        return stats
        
    def monitor_key_exchange(self, count: int = 5) -> Dict[str, Any]:
        """
        Monitor cryptographic key exchange operations.
        
        Args:
            count: Number of key exchanges to monitor
            
        Returns:
            Statistics about the monitored operations
        """
        print(f"\n{'='*60}")
        print(f"Monitoring Cryptographic Key Exchanges ({count} operations)")
        print(f"{'='*60}\n")
        
        algorithms = [
            PQCAlgorithm.KYBER768,
            PQCAlgorithm.DILITHIUM3,
            PQCAlgorithm.SPHINCS_PLUS_128F
        ]
        
        all_entropy_scores = []
        
        for i in range(count):
            algorithm = algorithms[i % len(algorithms)]
            
            start = time.time()
            det_key, pqc_seed = generate_hybrid_key(algorithm, context=f"EXCHANGE_{i}".encode())
            duration = time.time() - start
            
            # Analyze entropy of both components
            det_analyzer = EntropyAnalyzer(det_key)
            pqc_analyzer = EntropyAnalyzer(pqc_seed)
            
            det_entropy = det_analyzer.shannon_entropy()
            pqc_entropy = pqc_analyzer.shannon_entropy()
            all_entropy_scores.extend([det_entropy, pqc_entropy])
            
            # Validate bias
            det_bias = validate_zero_bias(det_key)
            pqc_bias = validate_zero_bias(pqc_seed)
            
            details = {
                'operation_id': i + 1,
                'algorithm': algorithm.value,
                'deterministic_key': {
                    'hex': det_key.hex(),
                    'length_bytes': len(det_key),
                    'entropy_bits_per_byte': round(det_entropy, 4),
                    'has_bias': det_bias['has_bias'],
                    'sha256': hashlib.sha256(det_key).hexdigest()
                },
                'pqc_seed': {
                    'length_bytes': len(pqc_seed),
                    'entropy_bits_per_byte': round(pqc_entropy, 4),
                    'has_bias': pqc_bias['has_bias'],
                    'sha256': hashlib.sha256(pqc_seed).hexdigest()
                },
                'duration_seconds': round(duration, 6)
            }
            
            self.log_operation('key_exchange', details)
            
        # Aggregate statistics
        stats = {
            'total_exchanges': count,
            'average_entropy': round(sum(all_entropy_scores) / len(all_entropy_scores), 4),
            'algorithms_tested': [alg.value for alg in algorithms[:min(count, len(algorithms))]]
        }
        
        print(f"\n{'='*60}")
        print("Key Exchange Statistics:")
        print(json.dumps(stats, indent=2))
        print(f"{'='*60}\n")
        
        return stats
        
    def save_log(self):
        """Save the operation log to file if output_file is specified."""
        if self.output_file:
            report = {
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now(timezone.utc).isoformat(),
                'total_operations': len(self.operations),
                'operations': self.operations
            }
            
            with open(self.output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\nValidation log saved to: {self.output_file}")


def main():
    """Main entry point for runtime validation."""
    parser = argparse.ArgumentParser(
        description="Runtime validation for cryptographic operations"
    )
    parser.add_argument(
        '--monitor-duration',
        type=int,
        default=None,
        help='Duration in seconds to monitor operations (default: run once)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='runtime_validation_log.json',
        help='Output file for validation logs'
    )
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run in continuous monitoring mode'
    )
    parser.add_argument(
        '--rng-count',
        type=int,
        default=10,
        help='Number of random number generations to monitor per cycle'
    )
    parser.add_argument(
        '--kex-count',
        type=int,
        default=5,
        help='Number of key exchanges to monitor per cycle'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("Cryptographic Runtime Validation Monitor")
    print("="*60)
    print(f"Start Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Output File: {args.output}")
    print("="*60)
    
    monitor = CryptoOperationMonitor(output_file=args.output)
    
    try:
        if args.continuous:
            print("\nRunning in continuous mode (Ctrl+C to stop)...")
            while True:
                monitor.monitor_random_generation(args.rng_count)
                monitor.monitor_key_exchange(args.kex_count)
                time.sleep(5)  # 5 second pause between cycles
        elif args.monitor_duration:
            print(f"\nMonitoring for {args.monitor_duration} seconds...")
            end_time = time.time() + args.monitor_duration
            while time.time() < end_time:
                monitor.monitor_random_generation(args.rng_count)
                monitor.monitor_key_exchange(args.kex_count)
                if time.time() < end_time:
                    time.sleep(min(5, end_time - time.time()))
        else:
            # Single run
            monitor.monitor_random_generation(args.rng_count)
            monitor.monitor_key_exchange(args.kex_count)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    finally:
        monitor.save_log()
        print("\nValidation complete.")
        
    return 0


if __name__ == '__main__':
    sys.exit(main())
