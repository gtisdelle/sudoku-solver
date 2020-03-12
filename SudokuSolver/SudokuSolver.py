'''
 This sudoku solver uses a backtracking algorithm. It was developed to help me
 further learn python.
 
 Author: George Tisdelle.
'''

def is_in_subgrid(x, puzzle, start_row, start_col):
    i = 0
    j = 0
    while i < 2:
        while j < 2:
            if (puzzle[start_row + i][start_col + j]) == x:
                return True
            j += 1
        i += 1
            
    return False

def reject_subgrid(x, puzzle, r, c):
    # Find which sub-grid the empty slot is in.
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
    # Check every location for 0 (empty).
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                return [r, c]
            
    return [-1, -1]

def solve(puzzle):
    empty = find_empty(puzzle)
    
    # This is the base case.
    if empty == [-1, -1]:
        for i in range(9): 
            for j in range(9): 
                print(puzzle[i][j]),
            print ''
        return
    
    # Try a value in the empty slot.
    for x in range(1, 10):
        # Place x in slot and check validity
        if (not reject(x, puzzle, empty[0], empty[1])):
        
            # If true it's temporarily safe to make the assignment
            puzzle[empty[0]][empty[1]] = x
            
            # Try the assignment.
            solve(puzzle)
            
            # If it gets here it failed.
            puzzle[empty[0]][empty[1]] = 0
           
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
    
    solve(puzzle)
