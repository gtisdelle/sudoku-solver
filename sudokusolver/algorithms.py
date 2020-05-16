"""Algorithms to generate and solve Sudoku puzzles

This module encapsulates the backtracking algorithms used to generate
and solve Sudoku puzzle represented as lists.
"""
from copy import deepcopy
from random import shuffle, randint


def generate_puzzle():
    """Generate a partially filled in puzzle with only one solution.

    Returns:
        list: a partially filled in Sudoku puzzle with one solution
    """
    puzzle = []
    row = []
    for _ in range(9):
        for _ in range(9):
            row.append(0)
        puzzle.append(row)
        row = []
    possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shuffle(possible_numbers)
    result = []

    _fill_puzzle_backtrack(puzzle, possible_numbers, result)
    _remove_elements(result)

    return result


def solve(puzzle):
    """Solve the Sudoku puzzle using backtracking

    This function does not modify the puzzle passed by reference. The
    solved puzzle is returned.

    Args:
        puzzle (list): the puzzle to be solved

    Returns:
        list: the solved puzzle
    """
    solution = []
    _solve_backtrack(deepcopy(puzzle), solution)
    return solution


def _fill_puzzle_backtrack(puzzle, possible_numbers, result):
    """Completely fill a puzzle using backtracking."""
    empty = _find_empty(puzzle)
    row = empty[0]
    col = empty[1]

    if empty == [-1, -1]:
        result += deepcopy(puzzle)
        return True

    for i in range(9):
        value = possible_numbers[i]
        if not _reject(value, puzzle, row, col):
            puzzle[row][col] = value
            if _fill_puzzle_backtrack(puzzle, possible_numbers, result):
                return True
            puzzle[row][col] = 0
    return False


def _find_empty(puzzle):
    """Return the first empty square on the board."""
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return [row, col]

    return [-1, -1]


def _is_in_subgrid(value, puzzle, start_row, start_col):
    """Determine whether the proposed number is in the sub-grid."""
    i = 0
    while i <= 2:
        j = 0
        while j <= 2:
            if (puzzle[start_row + i][start_col + j]) == value:
                return True
            j += 1
        i += 1

    return False


def _reject(value, puzzle, row, col):
    """Determine whether to reject the proposed change to the board."""
    # Check if it's used in the row
    for i in range(9):
        if puzzle[row][i] == value:
            return True

    # Check if it's used in column
    for i in range(9):
        if puzzle[i][col] == value:
            return True

    # Check if in sub-grid
    if _reject_subgrid(value, puzzle, row, col):
        return True

    return False


def _reject_subgrid(value, puzzle, row, col):
    """Determine whether a proposed change can be added to the current sub-grid."""
    start_row = -1
    start_col = -1

    if col <= 2:
        start_col = 0
    elif col <= 5:
        start_col = 3
    else:
        start_col = 6

    if row <= 2:
        start_row = 0
    elif row <= 5:
        start_row = 3
    else:
        start_row = 6

    if _is_in_subgrid(value, puzzle, start_row, start_col):
        return True

    return False


def _remove_elements(puzzle):
    """Randomly remove elements from a filled-in puzzle."""
    
    counter = 0
    def count_solutions_backtrack(puzzle):
        """Solve the puzzle as many different ways as possible."""
        nonlocal counter
        empty = _find_empty(puzzle)

        if counter > 1:
            return

        if empty == [-1, -1]:
            counter += 1
            return

        for i in range(1, 10):
            if not _reject(i, puzzle, empty[0], empty[1]):
                puzzle[empty[0]][empty[1]] = i
                count_solutions_backtrack(puzzle)
                puzzle[empty[0]][empty[1]] = 0

    attempts = 1
    while attempts > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        while puzzle[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)

        temp = puzzle[row][col]
        puzzle[row][col] = 0
        counter = 0
        count_solutions_backtrack(deepcopy(puzzle))
        if counter > 1:
            puzzle[row][col] = temp
            attempts -= 1


def _solve_backtrack(puzzle, solution):
    """Solve the puzzle and set solution to the solution."""
    empty = _find_empty(puzzle)

    if empty == [-1, -1]:
        solution += deepcopy(puzzle)
        return True

    for i in range(1, 10):
        if not _reject(i, puzzle, empty[0], empty[1]):
            puzzle[empty[0]][empty[1]] = i
            if _solve_backtrack(puzzle, solution):
                return True
            puzzle[empty[0]][empty[1]] = 0
    return False
