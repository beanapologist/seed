#!/usr/bin/env python3
"""
Prune the Garden - A Subset Sum Puzzle Game

Players must solve subset sum problems to simulate 'pruning the garden' by
reducing values to zero. When a player successfully prunes the garden
(reduces the sum to 0), they receive a reward.

This game is for entertainment and educational purposes only.
"""


def find_subset_sum(plants, target):
    """
    Find all subsets of plants that sum to the target value.
    
    Uses recursive backtracking to find all possible solutions.
    Works with both positive and negative numbers.
    
    Args:
        plants: List of integers representing plant values
        target: Integer target sum to achieve
        
    Returns:
        List of lists, where each inner list is a subset that sums to target.
        Returns empty list if no solution exists.
        
    Examples:
        >>> find_subset_sum([2, 4, 6, 8, 10], 10)
        [[2, 8], [4, 6], [10]]
        >>> find_subset_sum([1, 2, 3], 7)
        []
    """
    if not plants:
        return [[]] if target == 0 else []
    
    solutions = []
    has_negative = any(p < 0 for p in plants)
    
    def backtrack(index, current_subset, current_sum):
        """Recursive backtracking to find all solutions."""
        # Found a solution - add it and continue searching for more
        # Note: We don't return here because we want to find ALL solutions
        if current_sum == target:
            solutions.append(current_subset[:])
        
        # Pruning: if all remaining plants are positive and we've exceeded target, stop
        if not has_negative and current_sum > target:
            return
        
        # Try all remaining plants
        for i in range(index, len(plants)):
            # Include this plant
            current_subset.append(plants[i])
            backtrack(i + 1, current_subset, current_sum + plants[i])
            # Backtrack
            current_subset.pop()
    
    backtrack(0, [], 0)
    return solutions


def display_garden(plants):
    """
    Display the current garden state.
    
    Args:
        plants: List of integers representing plant values
    """
    print("\n🌱 Current Garden State 🌱")
    print("=" * 40)
    for i, plant in enumerate(plants, 1):
        print(f"  Plant {i}: {plant}")
    print("=" * 40)
    print(f"Total value: {sum(plants)}")
    print()


def display_solution(solution, target):
    """
    Display a solution to the player.
    
    Args:
        solution: List of integers representing the subset
        target: The target sum
    """
    print(f"✂️  Prune these plants: {solution}")
    print(f"   Sum: {' + '.join(map(str, solution))} = {sum(solution)}")
    if sum(solution) == target:
        print("   ✅ This achieves the target!")


def display_reward():
    """Display reward message when player successfully prunes the garden."""
    print("\n" + "🎉" * 20)
    print("🎉" + " " * 36 + "🎉")
    print("🎉  CONGRATULATIONS! Garden Pruned!  🎉")
    print("🎉" + " " * 36 + "🎉")
    print("🎉" * 20)
    print("\n✨ You successfully reduced the garden to zero! ✨")
    print("🏆 Achievement Unlocked: Master Gardener! 🏆\n")


def solve_puzzle(plants, target):
    """
    Solve the pruning puzzle and display all solutions.
    
    Args:
        plants: List of integers representing plant values
        target: Integer target sum to achieve
        
    Returns:
        List of all solutions, or empty list if none exist
    """
    print(f"\n🎯 Target: Prune plants totaling {target}")
    
    solutions = find_subset_sum(plants, target)
    
    if not solutions:
        print("\n❌ No solution exists for this garden!")
        print("   The garden cannot be pruned to achieve the target.\n")
        return []
    
    print(f"\n✅ Found {len(solutions)} solution(s)!\n")
    
    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}:")
        display_solution(solution, target)
        print()
    
    # Special reward if target is 0 (completely pruning the garden)
    if target == 0 and solutions:
        display_reward()
    elif solutions:
        print("🎊 Great job! You found valid pruning strategies! 🎊\n")
    
    return solutions


def play_game(plants, target):
    """
    Play a single round of Prune the Garden.
    
    Args:
        plants: List of integers representing plant values
        target: Integer target sum to achieve
    """
    print("\n" + "=" * 50)
    print("🌳  Welcome to Prune the Garden! 🌳")
    print("=" * 50)
    print("\nGoal: Select plants whose values sum to the target.")
    print("When you prune the garden perfectly (sum = 0),")
    print("you receive a special reward!\n")
    
    display_garden(plants)
    solve_puzzle(plants, target)


def main():
    """Main entry point for the game."""
    print("\n" + "🌻" * 25)
    print("     PRUNE THE GARDEN - Subset Sum Puzzle Game")
    print("🌻" * 25)
    
    # Example 1: Standard puzzle
    print("\n📋 Example 1: Find plants summing to 10")
    plants1 = [2, 4, 6, 8, 10]
    play_game(plants1, 10)
    
    # Example 2: Prune entire garden (sum to 0 from differences)
    print("\n📋 Example 2: Balance the garden (reach 0)")
    plants2 = [5, -2, 3, -5, -1]
    play_game(plants2, 0)
    
    # Example 3: No solution
    print("\n📋 Example 3: Impossible garden")
    plants3 = [2, 4, 6]
    play_game(plants3, 5)
    
    # Example 4: Complex puzzle
    print("\n📋 Example 4: Complex garden")
    plants4 = [1, 2, 3, 4, 5, 6, 7]
    play_game(plants4, 10)
    
    print("\n" + "=" * 50)
    print("Thanks for playing Prune the Garden! 🌱")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
