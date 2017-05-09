import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.angular_distance import AngularDistance
from startracker.star import Star

class AngularDistanceTest(unittest.TestCase):
    
    def setUp(self):
        star1 = Star(0,1,None,None,0,0)
        star2 = Star(1,1,None,None,np.pi,0)
        star3 = Star(2,1,None,None,np.pi/3,0)
        star4 = Star(3,1,None,None,np.pi/2,0)
        self.d1 = AngularDistance(star1,star2)
        self.d2 = AngularDistance(star1,star3)
        self.d3 = AngularDistance(star2,star3)
        self.d4 = AngularDistance(star1,star4)

    def test_equal_to_self(self):
        self.assertEquals(self.d1, self.d1)

    def test_not_equal_to_others(self):
        self.assertNotEquals(self.d1, self.d2)
        self.assertNotEquals(self.d1, self.d3)
        self.assertNotEquals(self.d1, self.d4)

    def test_check_triplet_true(self):
        self.assertEquals(self.d1.check_triplet(self.d2,self.d3), True)

    def test_check_triplet_false(self):
        self.assertEquals(self.d1.check_triplet(self.d2,self.d4), False)
        
    
