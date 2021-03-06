'''
Created on Mar 12, 2020

@author: George Tisdelle
'''
import unittest
import algorithms

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
        
        self.unsolvable = [[4,0,4,6,0,0,2,7,9], 
                           [6,5,7,9,0,0,0,0,0], 
                           [2,0,0,3,0,0,0,4,0], 
                           [1,0,0,0,0,8,5,2,4], 
                           [0,2,6,1,9,0,0,0,8], 
                           [0,7,5,0,0,4,9,0,0], 
                           [5,6,2,0,1,0,0,0,0], 
                           [9,1,0,0,7,0,0,5,0], 
                           [0,0,0,5,0,9,8,0,1]]
        
    def tearDown(self):
        self.puzzle = None
        self.solution = None
        self.unsolvable = None

    def test_solver_simple(self):       
        expected = self.solution
        actual = algorithms.solve(self.puzzle)
        self.assertEquals(expected, actual)
        
        expected = []
        actual = algorithms.solve(self.unsolvable)
        self.assertEquals(expected, actual)
        
    def test_generator(self):
        actual = algorithms.generate_puzzle()
        self.assertIsInstance(actual, list)

if __name__ == "__main__":
    unittest.main()