
import algorithms as alg

class Puzzle:
    def __init__(self):
        self._puzzle = alg.generate_puzzle()
        
    def get_puzzle(self):
        return self._puzzle
    
    def set_puzzle(self, puzzle):
        self._puzzle = puzzle
    
    def solve(self):
        self._puzzle = alg.solve(self._puzzle)
