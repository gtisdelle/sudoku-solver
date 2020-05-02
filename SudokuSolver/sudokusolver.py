
import algorithms as alg

class Puzzle:
    def __init__(self):
        self.__puzzle = alg.generate_puzzle()
        
    def get_puzzle(self):
        return self.__puzzle
    
    def set_puzzle(self, puzzle):
        self.__puzzle = puzzle
    
    def solve(self):
        self.__puzzle = alg.solve(self.__puzzle)
