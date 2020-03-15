'''
 This sudoku solver uses a backtracking algorithm.
 
 Author: George Tisdelle.
'''

from copy import deepcopy
from __builtin__ import staticmethod, object
from random import shuffle, randint

class PuzzleSolver(object):
    """A utility class to solve_backtrack a sudoku puzzle using backtracking."""
    
    is_finished = False
    
    @staticmethod
    def is_solvable(puzzle):
        p = deepcopy(puzzle)
        global counter
        counter = 0
        
        PuzzleSolver.solve_backtrack(p, [])
        
        return (counter > 1)
    
    @staticmethod
    def __is_in_subgrid(x, puzzle, start_row, start_col):
        """Determines whether the proposed number is in the sub-grid."""
        
        i = 0
        j = 0
        while i < 2:
            while j < 2:
                if (puzzle[start_row + i][start_col + j]) == x:
                    return True
                j += 1
            i += 1
                
        return False
    
    @staticmethod
    def __reject_subgrid(x, puzzle, r, c):
        """Determines whether a proposed change can be added to the current sub-grid."""
        
        start_row = -1
        start_col = -1
        
        if r <= 2:
            start_row = 0
            if c <= 2:
                start_col = 0
            elif c <= 5:
                start_col = 3
            else:
                start_col = 6
                
        elif r <= 5:
            start_row = 3
            if c <= 2:
                start_col = 0
            elif c <= 5:
                start_col = 3
            else:
                start_col = 6
                
        else:
            start_row = 6
            if c <= 2:
                start_col = 0
            elif c <= 5:
                start_col = 3
            else:
                start_col = 6
                
        if (PuzzleSolver.__is_in_subgrid(x, puzzle, start_row, start_col)):
            return True
        
        return False
    
    @staticmethod    
    def reject(x, puzzle, r, c):
        """Determines whether to reject the proposed change to the board."""
        
        # Check if it's used in the row
        for i in range(9):
            if puzzle[r][i] == x:
                return True
        
        # Check if it's used in column
        for i in range(9):
            if puzzle[i][c] == x:
                return True   
        
        # Check if in sub-grid
        if PuzzleSolver.__reject_subgrid(x, puzzle, r, c):
            return True
        
        return False
    
    @staticmethod    
    def find_empty(puzzle):
        """Returns the first empty square on the board."""
        
        for r in range(9):
            for c in range(9):
                if puzzle[r][c] == 0:
                    return [r, c]
                
        return [-1, -1]
    
    @staticmethod
    def solve(puzzle):
        solution = []
        global counter
        counter = 0
        
        PuzzleSolver.solve_backtrack(puzzle, solution)
        
        return solution
        
    @staticmethod
    def solve_backtrack(puzzle, solution):
        """Solves the puzzle and sets solution to the solution."""
        
        global counter
        
        empty = PuzzleSolver.find_empty(puzzle)
        
        if counter > 1:
            return

        if empty == [-1, -1]:
            solution += deepcopy(puzzle)
            counter += 1
            return
        
        
        for x in range(1, 10):

            if (not PuzzleSolver.reject(x, puzzle, empty[0], empty[1])):
            

                puzzle[empty[0]][empty[1]] = x
                
                
                PuzzleSolver.solve_backtrack(puzzle, solution)
                

                puzzle[empty[0]][empty[1]] = 0
        

class PuzzleGenerator(PuzzleSolver):
    
    NUM_ATTEMPTS = 1
    
    @staticmethod
    def generate_puzzle():
        """Generates a partially filled in puzzle with only one solution."""
        
        puzzle = [[0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0]]
        
        possible_numbers = [1,2,3,4,5,6,7,8,9]
        shuffle(possible_numbers)
        
        global is_finished
        is_finished = False
        result = []
        PuzzleGenerator.fill_puzzle_backtrack(puzzle, possible_numbers, result)
        
        PuzzleGenerator.remove_elements(result)
        
        return result
    
    @staticmethod
    def fill_puzzle_backtrack(puzzle, possible_numbers, result):
        """Completely fills a puzzle using backtracking.
        
            @param puzzle: the empty puzzle to be filled in
            @param possible_numbers: list of numbers 1-9 scrambled
        """

        global is_finished
        
        empty = PuzzleGenerator.find_empty(puzzle)
        row = empty[0]
        col = empty[1]
        
        if is_finished:
            return
        
        if empty == [-1, -1]:
            is_finished = True
            result += deepcopy(puzzle)
            return
            
        for i in range(9):
            x = possible_numbers[i]
            
            if not PuzzleSolver.reject(x, puzzle, row, col):
    
                puzzle[row][col] = x
    
                PuzzleGenerator.fill_puzzle_backtrack(puzzle, possible_numbers, result)
        
                puzzle[row][col] = 0
        
    @staticmethod    
    def remove_elements(puzzle):
        attempts = PuzzleGenerator.NUM_ATTEMPTS
    
        while attempts > 0:
                
            # The one time I needed a do loop!
            row = randint(0, 8)
            col = randint(0, 8)
            while puzzle[row][col] == 0:
                row = randint(0, 8)
                col = randint(0, 8)
                
            temp = puzzle[row][col]    
            puzzle[row][col] = 0
            
            global counter
            
            PuzzleSolver.solve(puzzle)
              
            
            if counter > 1:
                puzzle[row][col] = temp
                attempts -= 1
            
                   
                                  
if __name__ == "__main__":
    
    puzzle = [[0,0,4,6,0,0,2,7,9], 
              [6,5,7,9,0,0,0,0,0], 
              [2,0,0,3,0,0,0,4,0], 
              [1,0,0,0,0,8,5,2,4], 
              [0,2,6,1,9,0,0,0,8], 
              [0,7,5,0,0,4,9,0,0], 
              [5,6,2,0,1,0,0,0,0], 
              [9,1,0,0,7,0,0,5,0], 
              [0,0,0,5,0,9,8,0,1]] 
    
    solution = []
  
    PuzzleSolver.solve_backtrack(puzzle, solution)
    
    for x in range(9):
        for y in range(9):
            print solution[x][y],
        print("")
        
