"""
GoldenSeed - Deterministic PRNG (Pseudo-Random Number Generator)

⚠️ NOT FOR CRYPTOGRAPHY: This is a PRNG that generates deterministic pseudo-random
streams and must NOT be used for cryptographic purposes (passwords, keys, tokens, etc.).

This PRNG is designed for:
- Procedural content generation (games, simulations)
- Reproducible test data and fixtures
- Deterministic noise functions
- Consensus randomness in distributed systems
- Space-efficient storage of procedural content

Core Implementations:
- Deterministic PRNG based on golden ratio seed
- Test vector generation for cross-platform validation
- Golden ratio-based deterministic sequences
- Commercial licensing watermarking system

Example Usage:
    >>> from gq import GoldenStreamGenerator, GQS1
    >>>
    >>> # Generate deterministic byte streams
    >>> generator = GoldenStreamGenerator()
    >>> stream = next(generator)
    >>> print(stream.hex())
    '3c732e0d04dac163a5cc2b15c7caf42c'
    >>>
    >>> # Generate test vectors
    >>> vectors = GQS1.generate_test_vectors(10)
    >>> print(vectors[0])
    'a01611f01e8207a27c1529c3650c4838'
"""

from .stream_generator import (
    golden_stream_generator as GoldenStreamGenerator,
    generate_streams,
    HEX_SEED,
    EXPECTED_CHECKSUM,
    GOLDEN_RATIO,
    PI,
    E,
    SQRT2,
    GOLDEN_RATIO_HEX,
    PI_HEX,
    E_HEX,
    SQRT2_HEX,
)

# Backward compatibility aliases (deprecated - will be removed in future versions)
UniversalQKD = GoldenStreamGenerator
generate_universal_keys = generate_streams

from .gqs1 import (
    generate_test_vectors as generate_gqs1_vectors,
    GQS1,
)

from .golden_ratio_coin_flip import (
    GoldenRatioCoinFlip,
    EquidistributionValidator,
    CoinFlipValidator,
    QuasirandomnessValidator,
    PerformanceMetricsValidator,
    fractional_part,
    comprehensive_validation,
    PHI,
)

from .watermark import (
    WatermarkData,
    WatermarkError,
    encode_watermark,
    decode_watermark,
    embed_watermark_in_binary,
    extract_watermark_from_binary,
    check_watermark_present,
)

__all__ = [
    # Primary API (honest names)
    "GoldenStreamGenerator",
    "generate_streams",
    "GQS1",
    "generate_gqs1_vectors",
    "HEX_SEED",
    "EXPECTED_CHECKSUM",
    # Backward compatibility (deprecated)
    "UniversalQKD",
    "generate_universal_keys",
    # Mathematical constants
    "GOLDEN_RATIO",
    "PI",
    "E",
    "SQRT2",
    "GOLDEN_RATIO_HEX",
    "PI_HEX",
    "E_HEX",
    "SQRT2_HEX",
    # Golden Ratio sequences
    "GoldenRatioCoinFlip",
    "EquidistributionValidator",
    "CoinFlipValidator",
    "QuasirandomnessValidator",
    "PerformanceMetricsValidator",
    "fractional_part",
    "comprehensive_validation",
    "PHI",
    # Watermarking for commercial licensing
    "WatermarkData",
    "WatermarkError",
    "encode_watermark",
    "decode_watermark",
    "embed_watermark_in_binary",
    "extract_watermark_from_binary",
    "check_watermark_present",
]

__version__ = "4.0.0"
__author__ = "beanapologist"
