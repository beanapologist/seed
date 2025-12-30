"""
Cryptographically Secure Pseudorandom Number Generator (CSPRNG)

This module provides a cryptographically secure pseudorandom number generator
that uses secure entropy sources and follows cryptographic best practices.

Key Features:
- Secure initialization using os.urandom or secrets module
- Thread-safe operations using threading locks
- Support for deterministic seeding (for testing only, NOT for cryptographic use)
- Uniform distribution for both integers and floats
- Compliant with cryptographic best practices

WARNING: Deterministic seeding (using custom seeds) should NEVER be used for
cryptographic purposes. Use the default secure initialization for production
cryptographic applications.
"""

import os
import secrets
import threading
import hashlib
from typing import Optional, Union


class CSPRNG:
    """
    A cryptographically secure pseudorandom number generator.
    
    This generator uses secure entropy sources (os.urandom/secrets) for
    initialization and provides thread-safe random number generation.
    
    Attributes:
        _lock: Threading lock for thread-safe operations
        _is_deterministic: Flag indicating if using deterministic seed
        _state: Internal state for the generator
    
    Example:
        # Secure initialization (recommended for cryptographic use)
        rng = CSPRNG()
        secure_random = rng.random_int(0, 100)
        
        # Deterministic initialization (for testing/reproducibility only)
        rng = CSPRNG(seed=b"test_seed_12345")
        deterministic_random = rng.random_int(0, 100)
    """
    
    def __init__(self, seed: Optional[Union[bytes, int]] = None):
        """
        Initialize the CSPRNG with secure or deterministic seeding.
        
        Args:
            seed: Optional seed value. If None, uses secure entropy source.
                  Can be bytes or int. If int, will be converted to bytes.
                  
        Raises:
            ValueError: If seed is invalid type or empty.
            
        Note:
            When seed is provided, the generator operates in deterministic mode
            which is NOT suitable for cryptographic purposes. This mode should
            only be used for testing or when reproducible output is required
            for non-security-critical applications.
        """
        self._lock = threading.Lock()
        self._is_deterministic = seed is not None
        
        if seed is None:
            # Secure initialization using cryptographically secure entropy
            self._state = self._secure_init()
        else:
            # Deterministic initialization with custom seed
            if isinstance(seed, int):
                # Convert int to bytes (big-endian)
                seed = seed.to_bytes((seed.bit_length() + 7) // 8 or 1, 'big')
            elif not isinstance(seed, bytes):
                raise ValueError("Seed must be bytes, int, or None")
            
            if len(seed) == 0:
                raise ValueError("Seed cannot be empty")
            
            self._state = self._deterministic_init(seed)
    
    def _secure_init(self) -> bytes:
        """
        Initialize the generator with cryptographically secure entropy.
        
        Uses os.urandom as the primary entropy source, which is suitable
        for cryptographic purposes on all modern platforms.
        
        Returns:
            bytes: 64 bytes of secure random state
        """
        # Use os.urandom which provides cryptographically secure random bytes
        # This is backed by the OS's secure random number generator:
        # - Linux: /dev/urandom (getrandom() syscall when available)
        # - Windows: CryptGenRandom
        # - macOS: /dev/urandom (backed by Yarrow PRNG)
        return os.urandom(64)
    
    def _deterministic_init(self, seed: bytes) -> bytes:
        """
        Initialize the generator with a deterministic seed.
        
        WARNING: This mode is NOT cryptographically secure and should only
        be used for testing or non-security-critical reproducible outputs.
        
        Args:
            seed: Seed bytes to initialize the state
            
        Returns:
            bytes: 64 bytes of deterministic state derived from seed
        """
        # Use SHA-512 to expand the seed to 64 bytes
        # This provides good avalanche properties and distributes
        # the seed bits throughout the state
        return hashlib.sha512(seed).digest()
    
    def _advance_state(self) -> None:
        """
        Advance the internal state using cryptographic hashing.
        
        This method is thread-safe and uses SHA-512 to evolve the state,
        ensuring that the state progression is non-reversible and has
        good statistical properties.
        """
        with self._lock:
            if self._is_deterministic:
                # For deterministic mode, hash the current state
                self._state = hashlib.sha512(self._state).digest()
            else:
                # For secure mode, mix new entropy with current state
                # This provides forward secrecy: even if state is compromised,
                # past outputs cannot be reconstructed
                new_entropy = os.urandom(64)
                mixed = bytes(a ^ b for a, b in zip(self._state, new_entropy))
                self._state = hashlib.sha512(mixed).digest()
    
    def random_bytes(self, length: int) -> bytes:
        """
        Generate cryptographically secure random bytes.
        
        Args:
            length: Number of random bytes to generate (must be positive)
            
        Returns:
            bytes: Random bytes of specified length
            
        Raises:
            ValueError: If length is not positive
            
        Example:
            rng = CSPRNG()
            random_data = rng.random_bytes(32)  # 32 random bytes
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        
        result = bytearray()
        
        while len(result) < length:
            self._advance_state()
            with self._lock:
                # Use current state as random bytes
                result.extend(self._state[:min(64, length - len(result))])
        
        return bytes(result)
    
    def random_int(self, a: int, b: int) -> int:
        """
        Generate a uniformly distributed random integer in range [a, b].
        
        This method ensures uniform distribution by using rejection sampling
        to avoid modulo bias.
        
        Args:
            a: Lower bound (inclusive)
            b: Upper bound (inclusive)
            
        Returns:
            int: Random integer in range [a, b]
            
        Raises:
            ValueError: If a > b
            
        Example:
            rng = CSPRNG()
            dice_roll = rng.random_int(1, 6)  # Fair dice roll
        """
        if a > b:
            raise ValueError(f"Invalid range: a={a} must be <= b={b}")
        
        # Handle edge case where a == b
        if a == b:
            return a
        
        # Calculate range size
        range_size = b - a + 1
        
        # Determine number of bytes needed to represent range_size
        num_bytes = (range_size.bit_length() + 7) // 8
        
        # Use rejection sampling to ensure uniform distribution
        # This avoids modulo bias that occurs with simple modulo operation
        max_valid = (256 ** num_bytes // range_size) * range_size
        
        while True:
            random_bytes = self.random_bytes(num_bytes)
            random_value = int.from_bytes(random_bytes, 'big')
            
            # Reject values that would cause bias
            if random_value < max_valid:
                return a + (random_value % range_size)
    
    def random_float(self) -> float:
        """
        Generate a uniformly distributed random float in range [0.0, 1.0).
        
        Uses 53 bits of randomness to achieve full double precision
        uniform distribution.
        
        Returns:
            float: Random float in range [0.0, 1.0)
            
        Example:
            rng = CSPRNG()
            probability = rng.random_float()
        """
        # Generate 8 random bytes (64 bits)
        random_bytes = self.random_bytes(8)
        
        # Convert to integer
        random_int = int.from_bytes(random_bytes, 'big')
        
        # Use 53 bits for mantissa (IEEE 754 double precision)
        # This ensures uniform distribution across the full precision
        # of a double-precision float
        mantissa_bits = 53
        mantissa_mask = (1 << mantissa_bits) - 1
        mantissa = random_int & mantissa_mask
        
        # Divide by 2^53 to get value in [0.0, 1.0)
        return mantissa / (1 << mantissa_bits)
    
    def is_deterministic(self) -> bool:
        """
        Check if the generator is operating in deterministic mode.
        
        Returns:
            bool: True if using custom seed (deterministic), False if secure
            
        Example:
            rng = CSPRNG()
            assert not rng.is_deterministic()  # Secure mode
            
            rng2 = CSPRNG(seed=b"test")
            assert rng2.is_deterministic()  # Deterministic mode
        """
        return self._is_deterministic
    
    @staticmethod
    def secure_random_int(a: int, b: int) -> int:
        """
        Static method to generate a single secure random integer.
        
        This is a convenience method that uses Python's secrets module
        directly without maintaining state. Suitable for one-off random
        number generation.
        
        Args:
            a: Lower bound (inclusive)
            b: Upper bound (inclusive)
            
        Returns:
            int: Secure random integer in range [a, b]
            
        Raises:
            ValueError: If a > b
            
        Example:
            random_port = CSPRNG.secure_random_int(49152, 65535)
        """
        if a > b:
            raise ValueError(f"Invalid range: a={a} must be <= b={b}")
        
        return secrets.randbelow(b - a + 1) + a
    
    @staticmethod
    def secure_random_bytes(length: int) -> bytes:
        """
        Static method to generate secure random bytes.
        
        This is a convenience method that uses Python's secrets module
        directly without maintaining state. Suitable for one-off random
        byte generation.
        
        Args:
            length: Number of random bytes to generate
            
        Returns:
            bytes: Secure random bytes
            
        Raises:
            ValueError: If length is not positive
            
        Example:
            token = CSPRNG.secure_random_bytes(32)
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        
        return secrets.token_bytes(length)
