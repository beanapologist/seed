# 🌳 Prune the Garden - Subset Sum Puzzle Game

**Prune the Garden** is an educational puzzle game where players solve subset sum problems to simulate "pruning the garden" by selecting plants whose values sum to a target value.

## 🎮 Game Rules

### Objective
Select a subset of plants (numbers) from your garden that sum exactly to the target value.

### How to Win
- Find any combination of plants that adds up to the target sum
- **Special Achievement**: When the target is 0, you completely prune the garden and receive the "Master Gardener" reward! 🏆

### Game Elements
- **Plants**: Each plant has a numerical value (can be positive or negative)
- **Target**: The sum you need to achieve by selecting plants
- **Solutions**: There may be multiple ways to prune the garden!

## 🚀 How to Run

### Basic Usage

```bash
python3 prune_the_garden.py
```

This runs the game with several example puzzles demonstrating different scenarios.

### Using as a Module

You can also import and use the game functions in your own Python code:

```python
from prune_the_garden import find_subset_sum, play_game, solve_puzzle

# Find all solutions for a puzzle
plants = [2, 4, 6, 8, 10]
target = 10
solutions = find_subset_sum(plants, target)
print(f"Found {len(solutions)} solutions: {solutions}")

# Play a game round
play_game(plants, target)

# Just solve and display solutions
solve_puzzle(plants, target)
```

## 📝 Examples

### Example 1: Basic Puzzle
**Garden**: `[2, 4, 6, 8, 10]`  
**Target**: `10`  
**Solutions**: 
- `[2, 8]` → 2 + 8 = 10 ✅
- `[4, 6]` → 4 + 6 = 10 ✅
- `[10]` → 10 = 10 ✅

### Example 2: Balance the Garden (Target = 0)
**Garden**: `[5, -2, 3, -5, -1]`  
**Target**: `0`  
**Solutions**: 
- `[5, -5]` → 5 + (-5) = 0 ✅
- `[-2, 3, -1]` → -2 + 3 + (-1) = 0 ✅
- And more!

This earns you the special **Master Gardener** achievement! 🏆

### Example 3: No Solution
**Garden**: `[2, 4, 6]`  
**Target**: `5`  
**Result**: No combination of plants can sum to 5 ❌

### Example 4: Complex Garden
**Garden**: `[1, 2, 3, 4, 5, 6, 7]`  
**Target**: `10`  
**Solutions**: Many combinations possible! (e.g., [1, 2, 3, 4], [1, 4, 5], [2, 3, 5], etc.)

## 🧮 Algorithm

The game uses **recursive backtracking** to find all possible subsets that sum to the target value.

### Time Complexity
- O(2^n) in the worst case, where n is the number of plants
- Space complexity: O(n) for the recursion stack

### How It Works
1. Recursively explore all possible subsets by including or excluding each plant
2. Check if the current subset sums to the target value
3. Collect all valid solutions
4. Handle edge cases (empty garden, no solution, negative values)

## 🎯 Educational Value

This game teaches:
- **Subset Sum Problem**: A classic computational problem in computer science
- **Dynamic Programming**: An efficient problem-solving technique
- **Algorithm Design**: How to break down complex problems
- **Combinatorics**: Understanding combinations and permutations

## 🧪 Testing

The game includes comprehensive unit tests. To run them:

```bash
# From the repository root
python3 -m unittest games.prune-the-garden.test_prune_the_garden

# Or run tests directly
python3 test_prune_the_garden.py
```

## 🔧 Requirements

- Python 3.8 or higher
- No external dependencies required!

## 📖 Code Documentation

All functions include detailed docstrings with:
- Parameter descriptions
- Return value specifications
- Example usage
- Edge case handling

Key functions:
- `find_subset_sum(plants, target)`: Core algorithm to find all solutions
- `play_game(plants, target)`: Play a complete game round
- `solve_puzzle(plants, target)`: Solve and display solutions
- `display_garden(plants)`: Show current garden state
- `display_reward()`: Show achievement animation

## 🎨 Features

- ✨ Colorful emoji-based UI for better user experience
- 🎯 Multiple example puzzles with varying difficulty
- 🏆 Special achievement for completely pruning the garden
- ❌ Clear feedback when no solution exists
- 📊 Displays all possible solutions, not just one

## 🤝 Contributing

Feel free to:
- Add more example puzzles
- Improve the UI/UX
- Optimize the algorithm
- Add new game modes (timed challenges, hints, etc.)

## 📄 License

This game is part of the GoldenSeed project and follows the same GPL-3.0-or-later license with military-industrial prohibitions.

---

**Happy Pruning!** 🌱✂️🌳
