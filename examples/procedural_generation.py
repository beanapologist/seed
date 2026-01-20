"""
Procedural Generation Example for GoldenSeed

This example demonstrates how to use GoldenSeed for procedural content generation
in games, simulations, and other applications requiring deterministic randomness.

⚠️ NOT FOR CRYPTOGRAPHY: This is for procedural generation only.

Usage in Game Engines:
- Unity: Adapt this to C# using the C# examples in releases/
- Godot: Use the Python or GDScript equivalent
- Unreal: Adapt to C++ using the C++ examples in releases/
"""

from gq import UniversalQKD


class ProceduralWorldGenerator:
    """
    Generate infinite, deterministic world content.
    
    Same seed always produces the same world, perfect for:
    - Multiplayer synchronization
    - Reproducible testing
    - Space-efficient world storage
    """
    
    def __init__(self, world_seed_offset=0):
        """
        Initialize with a specific world seed.
        
        Args:
            world_seed_offset: Unique identifier for this world (0-n)
        """
        self.generator = UniversalQKD()
        
        # Skip to world-specific position
        for _ in range(world_seed_offset):
            next(self.generator)
    
    def generate_chunk(self, chunk_x, chunk_z):
        """
        Generate terrain for a world chunk at coordinates (x, z).
        
        Returns:
            Dictionary with terrain properties
        """
        # Get deterministic bytes for this chunk
        chunk_bytes = next(self.generator)
        
        # Convert bytes to terrain properties
        terrain = {
            'biome': int.from_bytes(chunk_bytes[0:1], 'big') % 10,
            'base_elevation': int.from_bytes(chunk_bytes[1:3], 'big') % 256,
            'variation': int.from_bytes(chunk_bytes[3:4], 'big') % 100,
            'vegetation_density': int.from_bytes(chunk_bytes[4:5], 'big') % 100,
            'temperature': int.from_bytes(chunk_bytes[5:6], 'big') % 100,
            'moisture': int.from_bytes(chunk_bytes[6:7], 'big') % 100,
            'ore_density': int.from_bytes(chunk_bytes[7:8], 'big') % 100,
        }
        
        return terrain
    
    def generate_entity(self, entity_type, spawn_id):
        """
        Generate deterministic entity properties.
        
        Args:
            entity_type: Type of entity (e.g., "monster", "npc", "item")
            spawn_id: Unique spawn identifier
            
        Returns:
            Dictionary with entity properties
        """
        # Skip to entity-specific position
        for _ in range(spawn_id):
            next(self.generator)
        
        entity_bytes = next(self.generator)
        
        entity = {
            'type': entity_type,
            'spawn_id': spawn_id,
            'health': int.from_bytes(entity_bytes[0:2], 'big') % 1000 + 1,
            'speed': int.from_bytes(entity_bytes[2:3], 'big') % 100 + 1,
            'strength': int.from_bytes(entity_bytes[3:4], 'big') % 100 + 1,
            'defense': int.from_bytes(entity_bytes[4:5], 'big') % 100 + 1,
            'rarity': int.from_bytes(entity_bytes[5:6], 'big') % 5,  # 0-4
            'color_seed': int.from_bytes(entity_bytes[6:10], 'big'),
        }
        
        return entity


class ProceduralLevelGenerator:
    """Generate infinite procedural game levels."""
    
    def __init__(self):
        self.generator = UniversalQKD()
    
    def generate_level(self, level_number):
        """
        Generate complete level data.
        
        Args:
            level_number: Level index (1, 2, 3, ...)
            
        Returns:
            Dictionary with level configuration
        """
        # Skip to level-specific position
        for _ in range((level_number - 1) * 100):
            next(self.generator)
        
        # Generate multiple bytes for level properties
        level_bytes = [next(self.generator) for _ in range(5)]
        
        level = {
            'number': level_number,
            'difficulty': sum(level_bytes[0]) % 10,
            'enemy_count': sum(level_bytes[1]) % 50 + 5,
            'treasure_count': sum(level_bytes[2]) % 20 + 1,
            'trap_count': sum(level_bytes[3]) % 30,
            'boss_health': sum(level_bytes[4]) * 100,
            'layout_seed': int.from_bytes(level_bytes[0][:8], 'big'),
        }
        
        return level


def example_world_generation():
    """Demonstrate world generation."""
    print("=" * 60)
    print("World Generation Example")
    print("=" * 60)
    print()
    
    # Create world with seed offset 42
    world = ProceduralWorldGenerator(world_seed_offset=42)
    
    print("Generating 3x3 chunk grid:")
    print("-" * 60)
    
    for x in range(-1, 2):
        for z in range(-1, 2):
            chunk = world.generate_chunk(x, z)
            print(f"Chunk ({x:+2d}, {z:+2d}): biome={chunk['biome']}, "
                  f"elevation={chunk['base_elevation']}, "
                  f"vegetation={chunk['vegetation_density']}%")
    
    print()
    print("Generating entities:")
    print("-" * 60)
    
    # Reset generator for entity spawning
    world = ProceduralWorldGenerator(world_seed_offset=42)
    
    for i in range(5):
        entity = world.generate_entity("monster", spawn_id=i)
        print(f"Monster {i}: HP={entity['health']}, "
              f"Str={entity['strength']}, "
              f"Def={entity['defense']}, "
              f"Rarity={entity['rarity']}")


def example_level_generation():
    """Demonstrate level generation."""
    print()
    print("=" * 60)
    print("Level Generation Example")
    print("=" * 60)
    print()
    
    level_gen = ProceduralLevelGenerator()
    
    for level_num in [1, 5, 10, 50]:
        level = level_gen.generate_level(level_num)
        print(f"Level {level_num:3d}: "
              f"Difficulty={level['difficulty']}/10, "
              f"Enemies={level['enemy_count']}, "
              f"Treasures={level['treasure_count']}, "
              f"Boss HP={level['boss_health']}")


def example_cross_platform_consistency():
    """Demonstrate cross-platform consistency."""
    print()
    print("=" * 60)
    print("Cross-Platform Consistency")
    print("=" * 60)
    print()
    print("The same seed always produces the same output,")
    print("regardless of platform or language implementation.")
    print()
    
    world1 = ProceduralWorldGenerator(world_seed_offset=0)
    world2 = ProceduralWorldGenerator(world_seed_offset=0)
    
    chunk1 = world1.generate_chunk(0, 0)
    chunk2 = world2.generate_chunk(0, 0)
    
    print(f"First generation:  {chunk1}")
    print(f"Second generation: {chunk2}")
    print(f"Identical: {chunk1 == chunk2}")


if __name__ == "__main__":
    example_world_generation()
    example_level_generation()
    example_cross_platform_consistency()
    
    print()
    print("=" * 60)
    print("Integration Notes:")
    print("=" * 60)
    print()
    print("Unity (C#): Use the C# implementation in releases/")
    print("Godot (GDScript): Adapt this Python code")
    print("Unreal (C++): Use the C++ implementation in releases/")
    print()
    print("Remember: Store only the world_seed_offset (a single number)")
    print("to regenerate entire worlds on demand!")
    print("=" * 60)
