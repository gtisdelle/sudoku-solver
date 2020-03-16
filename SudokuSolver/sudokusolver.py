'''
 Randomly generates and solves sudoku puzzles.
 
 Author: George Tisdelle.
'''

from copy import deepcopy
from random import shuffle, randint
    
def is_solvable(puzzle):
    """Returns a boolean of whether the puzzle has a unique solution."""
    
    p = deepcopy(puzzle)
    global counter
    counter = 0
        
    solve_backtrack(p, [])
        
    return (counter > 1)
    
    
def is_in_subgrid(x, puzzle, start_row, start_col):
    """Determines whether the proposed number is in the sub-grid."""
        
    i = 0
    while i <= 2:
        j = 0
        while j <= 2:
            if (puzzle[start_row + i][start_col + j]) == x:
                return True
            j += 1
        i += 1
                
    return False
    
    
def reject_subgrid(x, puzzle, r, c):
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
                
    if (is_in_subgrid(x, puzzle, start_row, start_col)):
        return True
        
    return False
    
        
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
    if reject_subgrid(x, puzzle, r, c):
        return True
        
    return False
    
        
def find_empty(puzzle):
    """Returns the first empty square on the board."""
        
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                return [r, c]
                
    return [-1, -1]
   
 
def solve_backtrack(puzzle, solution):
    """Solves the puzzle and sets solution to the solution."""
        
    global counter
        
    empty = find_empty(puzzle)
        
    if counter > 1:
        return

    if empty == [-1, -1]:
        solution += deepcopy(puzzle)
        counter += 1
        return
        
        
    for x in range(1, 10):

        if (not reject(x, puzzle, empty[0], empty[1])):
            

            puzzle[empty[0]][empty[1]] = x
                
                
            solve_backtrack(puzzle, solution)
                

            puzzle[empty[0]][empty[1]] = 0


def solve(puzzle):
    solution = []
    global counter
    counter = 0
        
    solve_backtrack(puzzle, solution)
        
    return solution


def remove_elements(puzzle):
    """Randomly removes elements from a filled-in puzzle."""
    
    NUM_ATTEMPTS = 1
    
    attempts = NUM_ATTEMPTS
    
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
            
        solve(puzzle)
              
            
        if counter > 1:
            puzzle[row][col] = temp
            attempts -= 1
            
            
def fill_puzzle_backtrack(puzzle, possible_numbers, result):
    """Completely fills a puzzle using backtracking."""

    global is_finished
    
    print "\n"
    for x in range(9):
        for y in range(9):
            print puzzle[x][y],
        print("")
    
        
    empty = find_empty(puzzle)
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
            
        if not reject(x, puzzle, row, col):
    
            puzzle[row][col] = x
    
            fill_puzzle_backtrack(puzzle, possible_numbers, result)
        
            puzzle[row][col] = 0
        
      
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
    fill_puzzle_backtrack(puzzle, possible_numbers, result)
        
    remove_elements(result)
        
    return result
               
                                  
if __name__ == "__main__":    
  
    puzzle = generate_puzzle()
    print("Generated puzzle:\n")
    for x in range(9):
        for y in range(9):
            print puzzle[x][y],
        print("")
    
    print("\n")
        
    solution = solve(puzzle)
    print("Solved puzzle:\n")
    for x in range(9):
        for y in range(9):
            print solution[x][y],
        print("")
        
