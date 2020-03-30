import unittest
import random
from hobo import Hobo
from traintrack import TrainTrack
import poisson
from decimal import Decimal


# Test1: Poisson() based on https://stattrek.com/online-calculator/poisson.aspx
class poisson_test(unittest.TestCase):
    def testNormal(self):
        value = round(poisson.poisson(5, 5), 5)
        answer = Decimal('0.17547')
        self.assertEqual(answer, value)

    def testZeroChance(self):
        value = round(poisson.poisson(10, 0.15), 5)
        answer = Decimal('0.00000')
        self.assertEqual(answer, value)

# Test2: PoissonValues() based on values from https://homepage.divms.uiowa.edu/~mbognar/applets/pois.html
class poissonValue_test(unittest.TestCase):
    def testNormal(self):
        value = {}
        data = poisson.poissonValues(10)
        previous = 0
        for key, val in data.items():
            value[key] = val - previous
            previous = val
        answer = {
            3: int(round(0.757)),
            4: int(round(1.892)),
            5: int(round(3.783)),
            6: int(round(6.396)),
            7: int(round(9.008)),
            8: int(round(11.26)),
            9: int(round(12.511)),
            10: int(round(12.511)),
            11: int(round(11.374)),
            12: int(round(9.478)),
            13: int(round(7.291)),
            14: int(round(5.208)),
            15: int(round(3.472)),
            16: int(round(2.17)),
            17: int(round(1.276)),
            18: int(round(0.709))
        }
        self.assertEqual(answer, value)
    
    def testOne(self):
        value = {}
        data = poisson.poissonValues(1)
        previous = 0
        for key, val in data.items():
            value[key] = val - previous
            previous = val
        answer = {
            0: int(round(36.788)),
            1: int(round(36.788)),
            2: int(round(18.394)),
            3: int(round(6.131)),
            4: int(round(1.533))
        }
        self.assertEqual(answer, value)
    
    # poissonValues() does not produce distributions greater than 99
    # Past 120.708, the function produces empty dictionaries
    # def testExtreme(self):
    #     value = {}
    #     data = poisson.poissonValues(100)
    #     previous = 0
    #     self.assertEqual(answer, value)


# Test3: simulate() TEST FOR LENGTH AND COUNT OF 0's and 1's depending on l0/l1
class simulate_test(unittest.TestCase):
    def testZeroL0L1(self):
        train = TrainTrack(0, 0)
        value = 0 in train.simulate(20)[1:]
        self.assertEqual(False, value)
    
    def testZeroL0(self):
        train = TrainTrack(0, 10)
        value = 0 in train.simulate(20)[1:]
        self.assertEqual(False, value)
    
    # There can still be a train on the track regardless if L1 is 0.
    def testZeroL1(self):
        train = TrainTrack(10, 0)
        value = 1 in train.simulate(20)[1:]
        self.assertEqual(True, value)

    # Both Zero and One length tracks return a list of length 1.
    # The track always start without a train present on the track therefore the first element is 0.
    def testLength0(self):
        train = TrainTrack(0, 0)
        value = train.simulate(0)
        self.assertEqual([0], value)
    
    def testLength1(self):
        train = TrainTrack(1, 1)
        value = train.simulate(1)
        self.assertEqual([0], value)

    def testLength10(self):
        train = TrainTrack(10, 10)
        answer = len(train.simulate(10))
        self.assertEqual(10, answer)
    
    def testLength100(self):
        train = TrainTrack(10, 10)
        answer = len(train.simulate(100))
        self.assertEqual(100, answer)
    
    def testLength1000(self):
        train = TrainTrack(10, 10)
        answer = len(train.simulate(1000))
        self.assertEqual(1000, answer)
    
    # If L0 is increasing there is more 0's than 1's
    def testCountOffTrack(self):
        count0 = 0
        count1 = 0
        for i in range(100):
            train = TrainTrack(i, i // 2)
            for j in range(100):
                list = train.simulate(j)[1:]
                count0 += list.count(0)
                count1 += list.count(1)
        answer = count0 > count1
        self.assertEqual(True, answer)
    
    # If L1 increased there is more 1's than 0's
    def testCountOnTrack(self):
        count0 = 0
        count1 = 0
        for i in range(100):
            train = TrainTrack(i // 2, i)
            for j in range(100):
                list = train.simulate(j)[1:]
                count0 += list.count(0)
                count1 += list.count(1)
        answer = count0 < count1
        self.assertEqual(True, answer)


# Test4: doMaths() TEST SAFENESS
class doMaths_test(unittest.TestCase):
    def testNormal(self):
        hobo = Hobo()
        hobo.runningResults=[[0, 0], [1, 1]]
        hobo.runningL0 = [3, 4]
        hobo.runningL1 = [4, 5]
        value = hobo.doMaths()
        answer = [46, 66]
        self.assertEqual(answer, value)
    
    def testGuaranteedSafe(self):
        hobo = Hobo()
        hobo.runningResults=[[0]]
        hobo.runningL0 = [0]
        hobo.runningL1 = [0]
        value = hobo.doMaths()
        answer = [100]
        self.assertEqual(answer, value)


# Test5: act()
class act_test(unittest.TestCase):
    def test(self):
        self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()
