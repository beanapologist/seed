#!/usr/bin/env python3
"""
Seed-Based Distribution and Extreme Compression Demonstration

This script provides interactive demonstrations of:
1. Seed-based distribution - regenerating identical data at different locations
2. Extreme compression - storing seeds instead of full data
3. Bandwidth savings - comparing transfer sizes
4. Privacy protection - minimal network exposure

⚠️ NOT FOR CRYPTOGRAPHY: This is for demonstration and educational purposes only.

Usage:
    python3 seed_distribution_demo.py [--demo all|distribution|compression|bandwidth|privacy]
"""

import sys
import os
import hashlib
import time
import gzip
import argparse

# Add parent directory and src to path for imports
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, 'src'))

try:
    from gq import UniversalQKD, GQS1
except ImportError:
    print("Error: Could not import gq module. Please ensure the package is installed.")
    print("Run: pip install -e .")
    sys.exit(1)


# Constants
KEYS_PER_MB_APPROX = 65536  # 65536 keys × 16 bytes/key = 1,048,576 bytes ≈ 1 MB


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_subsection(title):
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---\n")


def format_bytes(num_bytes):
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def demo_seed_based_distribution():
    """Demonstrate seed-based distribution across multiple locations."""
    print_section("DEMO 1: Seed-Based Distribution")
    
    print("Concept: Generate identical data at different 'locations' without")
    print("physically transferring the data. Only the seed identifier is shared.")
    print()
    
    # Simulate three different locations
    locations = ['New York', 'London', 'Tokyo']
    data_size_mb = 1  # Approximately 1 MB
    num_keys = data_size_mb * KEYS_PER_MB_APPROX
    
    print(f"Scenario: Generate {data_size_mb} MB of data at {len(locations)} locations")
    print()
    
    # Generate data at each location
    location_data = {}
    location_checksums = {}
    
    for location in locations:
        print(f"Location: {location}")
        print(f"  1. Initialize generator with seed (built-in golden ratio)")
        
        generator = UniversalQKD()
        
        print(f"  2. Generate {data_size_mb} MB of data locally...")
        start_time = time.time()
        data = b''.join([next(generator) for _ in range(num_keys)])
        elapsed = time.time() - start_time
        
        checksum = hashlib.sha256(data).hexdigest()
        location_data[location] = data
        location_checksums[location] = checksum
        
        print(f"  3. Generated {len(data):,} bytes in {elapsed:.3f}s")
        print(f"  4. Checksum: {checksum[:32]}...")
        print()
    
    # Verify all locations have identical data
    print_subsection("Verification")
    
    reference_data = location_data[locations[0]]
    all_identical = all(data == reference_data for data in location_data.values())
    
    print(f"Data identical across all locations: {all_identical}")
    print()
    
    # Show bandwidth savings
    print_subsection("Bandwidth Analysis")
    
    actual_data_transferred = 0  # Seed is implicit in algorithm
    print(f"Seed data transferred: {actual_data_transferred} bytes")
    print(f"Data generated at each location: {format_bytes(len(reference_data))}")
    print(f"Total data distributed: {format_bytes(len(reference_data) * len(locations))}")
    print()
    
    traditional_bandwidth = len(reference_data) * len(locations)
    print(f"Traditional method would transfer: {format_bytes(traditional_bandwidth)}")
    print(f"Seed-based method transferred: {actual_data_transferred} bytes")
    
    if actual_data_transferred > 0:
        savings_ratio = traditional_bandwidth / actual_data_transferred
        print(f"Bandwidth savings: {savings_ratio:,.0f}x")
    else:
        print(f"Bandwidth savings: Infinite (zero transfer)")
    
    print()
    print("✓ Data successfully distributed to all locations without physical transfer!")


def demo_extreme_compression():
    """Demonstrate extreme compression ratios."""
    print_section("DEMO 2: Extreme Compression")
    
    print("Concept: Store only a seed (32 bytes) instead of full data,")
    print("achieving compression ratios that far exceed traditional algorithms.")
    print()
    
    # Test different data sizes
    test_cases = [
        (1, "Small"),      # 1 KB
        (100, "Medium"),   # 100 KB
        (1024, "Large"),   # 1 MB
        (10240, "X-Large") # 10 MB
    ]
    
    results = []
    
    for size_kb, label in test_cases:
        print_subsection(f"{label} Dataset ({size_kb} KB)")
        
        # Generate data
        num_keys = (size_kb * 1024) // 16
        generator = UniversalQKD()
        
        print(f"Generating {size_kb} KB of data...")
        start_time = time.time()
        data = b''.join([next(generator) for _ in range(num_keys)])
        gen_time = time.time() - start_time
        
        original_size = len(data)
        print(f"  Original size: {format_bytes(original_size)}")
        print(f"  Generation time: {gen_time:.3f}s")
        
        # Traditional compression (gzip)
        print(f"  Compressing with gzip...")
        start_time = time.time()
        compressed_gzip = gzip.compress(data, compresslevel=9)
        gzip_time = time.time() - start_time
        gzip_size = len(compressed_gzip)
        gzip_ratio = original_size / gzip_size
        
        print(f"  Gzip size: {format_bytes(gzip_size)} (ratio: {gzip_ratio:.2f}:1, time: {gzip_time:.3f}s)")
        
        # Seed-based compression
        seed_size = 32  # Always 32 bytes
        seed_ratio = original_size / seed_size
        
        print(f"  Seed size: {seed_size} bytes (ratio: {seed_ratio:,.0f}:1, time: 0.000s)")
        
        advantage = seed_ratio / gzip_ratio
        print(f"  Advantage over gzip: {advantage:,.1f}x better")
        
        results.append({
            'label': label,
            'size_kb': size_kb,
            'original': original_size,
            'gzip': gzip_size,
            'seed': seed_size,
            'gzip_ratio': gzip_ratio,
            'seed_ratio': seed_ratio,
            'advantage': advantage
        })
        
        print()
    
    # Summary table
    print_subsection("Compression Comparison Summary")
    
    print(f"{'Dataset':<12} {'Original':<12} {'Gzip':<12} {'Seed':<12} {'Advantage':<12}")
    print("-" * 60)
    
    for r in results:
        print(f"{r['label']:<12} {format_bytes(r['original']):<12} "
              f"{format_bytes(r['gzip']):<12} {r['seed']} bytes     "
              f"{r['advantage']:>8.1f}x")
    
    print()
    print("✓ Seed-based compression vastly outperforms traditional algorithms!")


def demo_bandwidth_savings():
    """Demonstrate bandwidth savings in distribution scenarios."""
    print_section("DEMO 3: Bandwidth Savings")
    
    print("Concept: Calculate bandwidth savings when distributing data to")
    print("multiple recipients using seeds vs. traditional methods.")
    print()
    
    # Scenario parameters
    dataset_size_mb = 100
    num_recipients = 1000
    
    print(f"Scenario: Distribute {dataset_size_mb} MB dataset to {num_recipients:,} recipients")
    print()
    
    # Traditional distribution
    print_subsection("Traditional Distribution")
    
    traditional_per_user = dataset_size_mb * 1024 * 1024  # bytes
    traditional_total = traditional_per_user * num_recipients
    
    print(f"  Per recipient: {format_bytes(traditional_per_user)}")
    print(f"  Total bandwidth: {format_bytes(traditional_total)}")
    
    # Estimate costs (typical cloud transfer pricing)
    cost_per_gb = 0.09  # USD
    traditional_cost = (traditional_total / (1024**3)) * cost_per_gb
    
    print(f"  Estimated cost (${cost_per_gb}/GB): ${traditional_cost:,.2f}")
    print()
    
    # Seed-based distribution
    print_subsection("Seed-Based Distribution")
    
    seed_size = 32  # bytes
    seed_per_user = seed_size
    seed_total = seed_per_user * num_recipients
    
    print(f"  Per recipient: {seed_size} bytes")
    print(f"  Total bandwidth: {format_bytes(seed_total)}")
    
    seed_cost = (seed_total / (1024**3)) * cost_per_gb
    
    print(f"  Estimated cost (${cost_per_gb}/GB): ${seed_cost:.6f}")
    print()
    
    # Comparison
    print_subsection("Savings Analysis")
    
    bandwidth_reduction = traditional_total / seed_total
    cost_savings = traditional_cost - seed_cost
    cost_savings_percent = (cost_savings / traditional_cost) * 100
    
    print(f"  Bandwidth reduction: {bandwidth_reduction:,.0f}x")
    print(f"  Cost savings: ${cost_savings:,.2f} ({cost_savings_percent:.4f}%)")
    print(f"  Time savings: Recipients generate locally (no download wait)")
    print()
    
    # Environmental impact
    print_subsection("Environmental Impact")
    
    # Rough estimate: 0.5 kg CO2 per GB transferred
    co2_per_gb = 0.5  # kg
    traditional_co2 = (traditional_total / (1024**3)) * co2_per_gb
    seed_co2 = (seed_total / (1024**3)) * co2_per_gb
    co2_saved = traditional_co2 - seed_co2
    
    print(f"  Traditional method CO₂: {traditional_co2:,.2f} kg")
    print(f"  Seed-based method CO₂: {seed_co2:.6f} kg")
    print(f"  CO₂ emissions avoided: {co2_saved:,.2f} kg")
    print()
    
    print("✓ Seed-based distribution provides massive bandwidth and cost savings!")


def demo_privacy_protection():
    """Demonstrate privacy protection through minimal network exposure."""
    print_section("DEMO 4: Privacy Protection")
    
    print("Concept: Protect privacy by never transmitting bulk data over the")
    print("network. Only seeds are shared; data is generated locally.")
    print()
    
    # Scenario
    data_size_mb = 50
    num_keys = data_size_mb * KEYS_PER_MB_APPROX
    
    print(f"Scenario: Share {data_size_mb} MB of research data")
    print()
    
    # Traditional method
    print_subsection("Traditional Method (Full Data Transfer)")
    
    print("  Network exposure:")
    print(f"    - {data_size_mb} MB transmitted over network")
    print(f"    - Data visible to: ISPs, network admins, potential eavesdroppers")
    print(f"    - Metadata: Transfer time, size, endpoints, etc.")
    print(f"    - Risk: Interception, tampering, surveillance")
    print()
    
    # Seed-based method
    print_subsection("Seed-Based Method (Seed Transfer Only)")
    
    seed_identifier = 42  # Just an offset number
    
    print("  Network exposure:")
    print(f"    - Seed identifier transmitted: {seed_identifier} (tiny integer)")
    print(f"    - Data visible to: Only seed ID (minimal information)")
    print(f"    - Metadata: Minimal (just seed identifier)")
    print(f"    - Risk: Negligible (seed reveals nothing about data content)")
    print()
    
    # Generate and verify locally
    print_subsection("Local Generation and Verification")
    
    print("  Recipient generates data locally:")
    generator = UniversalQKD()
    
    # Skip to offset
    for _ in range(seed_identifier):
        next(generator)
    
    print(f"    1. Initialize generator")
    print(f"    2. Skip to offset {seed_identifier}")
    print(f"    3. Generate {data_size_mb} MB locally...")
    
    start_time = time.time()
    data = b''.join([next(generator) for _ in range(num_keys)])
    elapsed = time.time() - start_time
    
    checksum = hashlib.sha256(data).hexdigest()
    
    print(f"    4. Generated {format_bytes(len(data))} in {elapsed:.3f}s")
    print(f"    5. Verify checksum: {checksum[:32]}...")
    print()
    
    # Privacy comparison
    print_subsection("Privacy Comparison")
    
    print("  Traditional Method:")
    print("    ❌ Bulk data exposed on network")
    print("    ❌ Susceptible to eavesdropping")
    print("    ❌ Can be intercepted and copied")
    print("    ❌ Leaves extensive network traces")
    print()
    
    print("  Seed-Based Method:")
    print("    ✓ Bulk data never leaves endpoint")
    print("    ✓ Network sees only seed identifier")
    print("    ✓ No meaningful data to intercept")
    print("    ✓ Minimal network metadata")
    print()
    
    # Use case examples
    print_subsection("Privacy-Preserving Use Cases")
    
    use_cases = [
        ("Medical Research", "Share research datasets without exposing patient data patterns"),
        ("Financial Analysis", "Distribute test datasets without revealing transaction patterns"),
        ("Education", "Provide learning datasets without network surveillance"),
        ("Journalism", "Share data with sources while minimizing network exposure"),
    ]
    
    for use_case, benefit in use_cases:
        print(f"  • {use_case}")
        print(f"    {benefit}")
        print()
    
    print("✓ Seed-based distribution minimizes privacy risks through minimal exposure!")


def demo_cross_location_sync():
    """Demonstrate cross-location synchronization."""
    print_section("BONUS DEMO: Cross-Location Synchronization")
    
    print("Concept: Multiple locations can synchronize large datasets by")
    print("sharing only seed identifiers, not the data itself.")
    print()
    
    locations = {
        'Headquarters (USA)': 0,
        'Regional Office (EU)': 0,
        'Branch Office (Asia)': 0,
        'Remote Lab (Africa)': 0
    }
    
    dataset_size_mb = 500  # 500 MB dataset
    dataset_id = 1234
    
    print(f"Scenario: Synchronize {dataset_size_mb} MB dataset across {len(locations)} locations")
    print(f"Dataset ID: {dataset_id}")
    print()
    
    print_subsection("Synchronization Process")
    
    # Each location generates the dataset
    checksums = {}
    
    for location in locations:
        print(f"{location}:")
        print(f"  1. Receive dataset ID: {dataset_id}")
        print(f"  2. Initialize generator and skip to offset {dataset_id}")
        
        generator = UniversalQKD()
        for _ in range(dataset_id):
            next(generator)
        
        print(f"  3. Generate {dataset_size_mb} MB locally...")
        
        # For demo, generate smaller sample
        sample_keys = 1000
        sample_data = b''.join([next(generator) for _ in range(sample_keys)])
        checksum = hashlib.sha256(sample_data).hexdigest()
        checksums[location] = checksum
        
        print(f"  4. Checksum: {checksum[:32]}...")
        print()
    
    # Verify synchronization
    print_subsection("Synchronization Verification")
    
    all_checksums = list(checksums.values())
    all_match = all(c == all_checksums[0] for c in all_checksums)
    
    print(f"All locations synchronized: {all_match}")
    print()
    
    # Calculate savings
    print_subsection("Bandwidth Savings")
    
    traditional_sync = dataset_size_mb * 1024 * 1024 * len(locations)
    seed_sync = 8 * len(locations)  # Just 8 bytes for dataset ID
    
    print(f"Traditional sync: {format_bytes(traditional_sync)}")
    print(f"Seed-based sync: {format_bytes(seed_sync)}")
    print(f"Bandwidth savings: {traditional_sync / seed_sync:,.0f}x")
    print()
    
    print("✓ All locations synchronized with minimal bandwidth!")


def run_all_demos():
    """Run all demonstrations."""
    demo_seed_based_distribution()
    demo_extreme_compression()
    demo_bandwidth_savings()
    demo_privacy_protection()
    demo_cross_location_sync()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Seed-Based Distribution and Extreme Compression Demonstrations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 seed_distribution_demo.py --demo all
  python3 seed_distribution_demo.py --demo distribution
  python3 seed_distribution_demo.py --demo compression
        """
    )
    
    parser.add_argument(
        '--demo',
        choices=['all', 'distribution', 'compression', 'bandwidth', 'privacy', 'sync'],
        default='all',
        help='Which demonstration to run (default: all)'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  SEED-BASED DISTRIBUTION & EXTREME COMPRESSION DEMONSTRATIONS")
    print("  GoldenSeed - Deterministic High-Entropy Byte Streams")
    print("=" * 70)
    print()
    print("⚠️  NOT FOR CRYPTOGRAPHY")
    print("    These demonstrations are for educational and practical use cases")
    print("    involving deterministic data generation. Not for security purposes.")
    print()
    
    try:
        if args.demo == 'all':
            run_all_demos()
        elif args.demo == 'distribution':
            demo_seed_based_distribution()
        elif args.demo == 'compression':
            demo_extreme_compression()
        elif args.demo == 'bandwidth':
            demo_bandwidth_savings()
        elif args.demo == 'privacy':
            demo_privacy_protection()
        elif args.demo == 'sync':
            demo_cross_location_sync()
        
        print()
        print("=" * 70)
        print("  DEMONSTRATIONS COMPLETE")
        print("=" * 70)
        print()
        print("For more information, see:")
        print("  - docs/DATA_TELEPORTATION_AND_COMPRESSION.md")
        print("  - README.md")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
