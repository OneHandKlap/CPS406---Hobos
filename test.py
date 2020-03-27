import unittest
import random
from hobo import Hobo
import poisson
import hogwartsHobos

class hobo_test(unittest.TestCase):

    def test_hobo_1(self):
        hobo=Hobo()
        trackResults=[[0,0],[1,1],[0,1],[1,1],[0,0]]
        results=hogwartsHobos.simulateGame(5,3,2,3,1,trackResults)

        self.assertEqual(results,[0,0,0,0,0])

if __name__ =='__main__':
    unittest.main()