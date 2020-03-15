'''
Created on Mar 12, 2020

@author: George Tisdelle
'''
import unittest
from sudokusolver import PuzzleSolver, PuzzleGenerator

class Test(unittest.TestCase):


    def setUp(self):
        self.puzzle = [[0,0,4,6,0,0,2,7,9], 
                       [6,5,7,9,0,0,0,0,0], 
                       [2,0,0,3,0,0,0,4,0], 
                       [1,0,0,0,0,8,5,2,4], 
                       [0,2,6,1,9,0,0,0,8], 
                       [0,7,5,0,0,4,9,0,0], 
                       [5,6,2,0,1,0,0,0,0], 
                       [9,1,0,0,7,0,0,5,0], 
                       [0,0,0,5,0,9,8,0,1]]
        
        self.solution=[[3,8,4,6,5,1,2,7,9],
                       [6,5,7,9,4,2,1,8,3],
                       [2,9,1,3,8,7,6,4,5],
                       [1,3,9,7,6,8,5,2,4],
                       [4,2,6,1,9,5,7,3,8],
                       [8,7,5,2,3,4,9,1,6],
                       [5,6,2,8,1,3,4,9,7],
                       [9,1,8,4,7,6,3,5,2],
                       [7,4,3,5,2,9,8,6,1]]


    def tearDown(self):
        self.puzzle = []
        self.solution = []
        pass


    def testSolverSimple(self):
        actual = []
        assert PuzzleSolver.solve(self.puzzle, actual) == True, "Should return True"
        
        expected = self.solution
        
        assert expected == actual
        
        '''print counter
        
        assert counter == 1, "counter was not incremented the correct amount (1 time)"'''
        
    def testGenerator(self):
        actual = PuzzleGenerator.generate_puzzle()
        assert actual.__class__ == list

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()