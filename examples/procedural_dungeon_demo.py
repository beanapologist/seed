#!/usr/bin/env python3
"""
Procedural Dungeon Generator Demo

Demonstrates how GoldenSeed PRNG creates deterministic, reproducible game content.
Same seed = same dungeon, every time, on every platform.

Perfect for:
- Roguelike dungeons
- Procedural level generation
- Multiplayer seed sharing
- Speedrun challenges with consistent maps
"""

from gq import GoldenStreamGenerator


class ProceduralDungeon:
    """Generate deterministic roguelike dungeons from a seed."""

    TILES = {
        'wall': '█',
        'floor': '·',
        'player': '@',
        'treasure': '$',
        'enemy': 'E',
        'stairs': '>',
        'trap': '^',
        'potion': '!',
    }

    def __init__(self, seed=0, width=40, height=15):
        """
        Initialize dungeon generator.

        Args:
            seed: Seed for deterministic generation
            width: Dungeon width in tiles
            height: Dungeon height in tiles
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.prng = GoldenStreamGenerator()

        # Skip to seed position in PRNG stream
        for _ in range(seed):
            next(self.prng)

    def _rand_int(self, max_val):
        """Get a pseudo-random integer from 0 to max_val-1."""
        chunk = next(self.prng)
        return int.from_bytes(chunk[:4], 'big') % max_val

    def _rand_choice(self, choices):
        """Randomly select from a list."""
        return choices[self._rand_int(len(choices))]

    def generate(self):
        """Generate a complete dungeon map."""
        # Start with all walls
        dungeon = [['█' for _ in range(self.width)] for _ in range(self.height)]

        # Carve out rooms using cellular automata
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self._rand_int(100) < 45:  # 45% chance to be floor
                    dungeon[y][x] = '·'

        # Smooth with cellular automata (game of life rules)
        for _ in range(3):
            dungeon = self._smooth_dungeon(dungeon)

        # Place player at a random floor tile
        player_placed = False
        for _ in range(100):
            x, y = self._rand_int(self.width), self._rand_int(self.height)
            if dungeon[y][x] == '·':
                dungeon[y][x] = '@'
                player_placed = True
                break

        # Place treasures (3-7 treasures)
        num_treasures = 3 + self._rand_int(5)
        for _ in range(num_treasures):
            for _ in range(50):
                x, y = self._rand_int(self.width), self._rand_int(self.height)
                if dungeon[y][x] == '·':
                    dungeon[y][x] = '$'
                    break

        # Place enemies (5-10 enemies)
        num_enemies = 5 + self._rand_int(6)
        for _ in range(num_enemies):
            for _ in range(50):
                x, y = self._rand_int(self.width), self._rand_int(self.height)
                if dungeon[y][x] == '·':
                    dungeon[y][x] = 'E'
                    break

        # Place stairs down
        for _ in range(50):
            x, y = self._rand_int(self.width), self._rand_int(self.height)
            if dungeon[y][x] == '·':
                dungeon[y][x] = '>'
                break

        # Place some traps (2-4 traps)
        num_traps = 2 + self._rand_int(3)
        for _ in range(num_traps):
            for _ in range(50):
                x, y = self._rand_int(self.width), self._rand_int(self.height)
                if dungeon[y][x] == '·':
                    dungeon[y][x] = '^'
                    break

        # Place potions (2-3 potions)
        num_potions = 2 + self._rand_int(2)
        for _ in range(num_potions):
            for _ in range(50):
                x, y = self._rand_int(self.width), self._rand_int(self.height)
                if dungeon[y][x] == '·':
                    dungeon[y][x] = '!'
                    break

        return dungeon

    def _smooth_dungeon(self, dungeon):
        """Apply cellular automata smoothing."""
        new_dungeon = [row[:] for row in dungeon]

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # Count wall neighbors
                walls = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dungeon[y + dy][x + dx] == '█':
                            walls += 1

                # If mostly walls, become wall; if mostly floor, become floor
                if walls >= 5:
                    new_dungeon[y][x] = '█'
                elif walls <= 3:
                    new_dungeon[y][x] = '·'

        return new_dungeon

    def display(self):
        """Display the dungeon with legend."""
        dungeon = self.generate()

        print(f"\n╔{'═' * self.width}╗")
        for row in dungeon:
            print(f"║{''.join(row)}║")
        print(f"╚{'═' * self.width}╝")

        print(f"\n🎮 Procedural Dungeon (Seed: {self.seed})")
        print("─" * 44)
        print("  @  Player    $  Treasure    E  Enemy")
        print("  >  Stairs    ^  Trap        !  Potion")
        print("  ·  Floor     █  Wall")
        print()

        return dungeon


def demo():
    """Run the demo showing deterministic generation."""
    print("\n" + "=" * 50)
    print("  🎲 GoldenSeed PRNG: Procedural Dungeon Demo")
    print("=" * 50)
    print("\n✨ Same seed = Same dungeon, every time!\n")

    # Show that seed 42 always generates the same dungeon
    print("🗺️  Dungeon from Seed 42 (Run 1)")
    dungeon1 = ProceduralDungeon(seed=42, width=40, height=15)
    map1 = dungeon1.display()

    print("\n🗺️  Dungeon from Seed 42 (Run 2)")
    dungeon2 = ProceduralDungeon(seed=42, width=40, height=15)
    map2 = dungeon2.display()

    # Verify they're identical
    if map1 == map2:
        print("✅ VERIFIED: Both dungeons are IDENTICAL!")
        print("   → Perfect for speedruns, multiplayer, testing")

    print("\n🗺️  Different Seed (1337) = Different Dungeon")
    dungeon3 = ProceduralDungeon(seed=1337, width=40, height=15)
    dungeon3.display()

    print("\n💡 Use Cases:")
    print("  • Roguelike procedural generation")
    print("  • Minecraft-style world seeds")
    print("  • Multiplayer map sharing (share seed, not map data!)")
    print("  • Speedrun categories by seed")
    print("  • Reproducible testing of game mechanics")
    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    demo()
