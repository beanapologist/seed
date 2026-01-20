"""
Prune the Garden - A Subset Sum Puzzle Game

This package provides an educational puzzle game where players solve
subset sum problems by selecting plants that sum to a target value.
"""

from .prune_the_garden import (
    find_subset_sum,
    display_garden,
    display_solution,
    display_reward,
    solve_puzzle,
    play_game,
)

__all__ = [
    'find_subset_sum',
    'display_garden',
    'display_solution',
    'display_reward',
    'solve_puzzle',
    'play_game',
]

__version__ = '1.0.0'
