#!/usr/bin/env python3
"""
Unit tests for Prune the Garden game.

Tests validate:
- Subset sum algorithm correctness
- Edge cases (empty input, no solution, negative numbers)
- Multiple solutions
- Game display functions
- Integration scenarios
"""

import unittest
import sys
import os
from io import StringIO

# Add the game directory to path
sys.path.insert(0, os.path.dirname(__file__))

from prune_the_garden import (
    find_subset_sum,
    display_garden,
    display_solution,
    display_reward,
    solve_puzzle,
    play_game,
)


class TestSubsetSum(unittest.TestCase):
    """Test suite for subset sum algorithm."""
    
    def test_basic_solution(self):
        """Test basic subset sum with single solution."""
        plants = [2, 8]
        target = 10
        solutions = find_subset_sum(plants, target)
        self.assertEqual(len(solutions), 1)
        self.assertEqual(sum(solutions[0]), target)
    
    def test_multiple_solutions(self):
        """Test case with multiple valid solutions."""
        plants = [2, 4, 6, 8, 10]
        target = 10
        solutions = find_subset_sum(plants, target)
        
        # Should find at least [2, 8], [4, 6], [10]
        self.assertGreaterEqual(len(solutions), 3)
        
        # Verify all solutions sum to target
        for solution in solutions:
            self.assertEqual(sum(solution), target)
    
    def test_no_solution(self):
        """Test case where no solution exists."""
        plants = [2, 4, 6]
        target = 5
        solutions = find_subset_sum(plants, target)
        self.assertEqual(len(solutions), 0)
    
    def test_empty_garden(self):
        """Test with empty garden."""
        plants = []
        target = 0
        solutions = find_subset_sum(plants, target)
        # Empty set sums to 0
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0], [])
        
    def test_empty_garden_nonzero_target(self):
        """Test with empty garden and non-zero target."""
        plants = []
        target = 5
        solutions = find_subset_sum(plants, target)
        self.assertEqual(len(solutions), 0)
    
    def test_single_plant_match(self):
        """Test with single plant that matches target."""
        plants = [10]
        target = 10
        solutions = find_subset_sum(plants, target)
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0], [10])
    
    def test_single_plant_no_match(self):
        """Test with single plant that doesn't match target."""
        plants = [10]
        target = 5
        solutions = find_subset_sum(plants, target)
        self.assertEqual(len(solutions), 0)
    
    def test_negative_numbers(self):
        """Test with negative numbers in garden."""
        plants = [5, -2, 3, -5, -1]
        target = 0
        solutions = find_subset_sum(plants, target)
        
        # Should find solutions
        self.assertGreater(len(solutions), 0)
        
        # Verify all solutions sum to 0
        for solution in solutions:
            self.assertEqual(sum(solution), 0)
    
    def test_all_plants_sum_to_target(self):
        """Test where all plants together sum to target."""
        plants = [1, 2, 3, 4]
        target = 10
        solutions = find_subset_sum(plants, target)
        
        # Should find solution [1, 2, 3, 4]
        self.assertGreater(len(solutions), 0)
        
        # Check if full set is one of the solutions
        full_set_found = False
        for solution in solutions:
            if sorted(solution) == sorted(plants):
                full_set_found = True
                break
        self.assertTrue(full_set_found)
    
    def test_complex_garden(self):
        """Test with larger garden and multiple solutions."""
        plants = [1, 2, 3, 4, 5, 6, 7]
        target = 10
        solutions = find_subset_sum(plants, target)
        
        # Should find multiple solutions
        self.assertGreater(len(solutions), 5)
        
        # Verify all solutions
        for solution in solutions:
            self.assertEqual(sum(solution), target)
    
    def test_duplicates(self):
        """Test with duplicate values in garden."""
        plants = [2, 2, 4, 4]
        target = 8
        solutions = find_subset_sum(plants, target)
        
        # Should find solutions
        self.assertGreater(len(solutions), 0)
        
        # Verify all solutions sum to target
        for solution in solutions:
            self.assertEqual(sum(solution), target)
    
    def test_zero_target_positive_plants(self):
        """Test with target 0 and only positive plants."""
        plants = [1, 2, 3]
        target = 0
        solutions = find_subset_sum(plants, target)
        
        # Only empty set sums to 0
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0], [])
    
    def test_large_target(self):
        """Test with target larger than sum of all plants."""
        plants = [1, 2, 3]
        target = 100
        solutions = find_subset_sum(plants, target)
        self.assertEqual(len(solutions), 0)


class TestDisplayFunctions(unittest.TestCase):
    """Test suite for display/UI functions."""
    
    def test_display_garden(self):
        """Test garden display function."""
        plants = [2, 4, 6]
        
        # Capture output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        display_garden(plants)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Check that output contains plant values
        self.assertIn("2", output)
        self.assertIn("4", output)
        self.assertIn("6", output)
        self.assertIn("Garden State", output)
    
    def test_display_solution(self):
        """Test solution display function."""
        solution = [2, 8]
        target = 10
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        display_solution(solution, target)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Check output contains solution
        self.assertIn("2", output)
        self.assertIn("8", output)
    
    def test_display_reward(self):
        """Test reward display function."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        display_reward()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Check for congratulatory message
        self.assertIn("CONGRATULATIONS", output)
        self.assertIn("Master Gardener", output)


class TestSolvePuzzle(unittest.TestCase):
    """Test suite for solve_puzzle function."""
    
    def test_solve_with_solution(self):
        """Test solving puzzle with valid solutions."""
        plants = [2, 4, 6, 8, 10]
        target = 10
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        solutions = solve_puzzle(plants, target)
        
        sys.stdout = sys.__stdout__
        
        # Should return solutions
        self.assertGreater(len(solutions), 0)
        
        # Output should indicate success
        output = captured_output.getvalue()
        self.assertIn("Found", output)
        self.assertIn("solution", output)
    
    def test_solve_without_solution(self):
        """Test solving puzzle with no solutions."""
        plants = [2, 4, 6]
        target = 5
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        solutions = solve_puzzle(plants, target)
        
        sys.stdout = sys.__stdout__
        
        # Should return empty list
        self.assertEqual(len(solutions), 0)
        
        # Output should indicate no solution
        output = captured_output.getvalue()
        self.assertIn("No solution", output)
    
    def test_solve_zero_target(self):
        """Test solving with target 0 shows reward."""
        plants = [5, -5]
        target = 0
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        solutions = solve_puzzle(plants, target)
        
        sys.stdout = sys.__stdout__
        
        # Should have solutions
        self.assertGreater(len(solutions), 0)
        
        # Output should include reward
        output = captured_output.getvalue()
        self.assertIn("Master Gardener", output)


class TestPlayGame(unittest.TestCase):
    """Test suite for play_game function."""
    
    def test_play_game_complete(self):
        """Test playing a complete game."""
        plants = [2, 4, 6, 8, 10]
        target = 10
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        play_game(plants, target)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Check for game elements
        self.assertIn("Welcome", output)
        self.assertIn("Garden", output)
        self.assertIn("solution", output.lower())


class TestIntegration(unittest.TestCase):
    """Integration tests for complete game scenarios."""
    
    def test_example_1(self):
        """Test example 1 from problem statement."""
        plants = [2, 4, 6, 8, 10]
        target = 10
        solutions = find_subset_sum(plants, target)
        
        # Should find [2, 8], [4, 6], and [10]
        self.assertGreaterEqual(len(solutions), 3)
        
        # Check specific solutions exist
        solution_sets = [sorted(s) for s in solutions]
        self.assertIn([2, 8], solution_sets)
        self.assertIn([4, 6], solution_sets)
        self.assertIn([10], solution_sets)
    
    def test_example_2_no_solution(self):
        """Test edge case where no solution is possible."""
        plants = [2, 4, 6]
        target = 5
        solutions = find_subset_sum(plants, target)
        
        self.assertEqual(len(solutions), 0)


if __name__ == "__main__":
    unittest.main()
