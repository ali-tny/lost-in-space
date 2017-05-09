import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.star import Star

class Star_test(unittest.TestCase):

    def setUp(self):
        #Degrees to radians
        self.d2r = np.pi/180
    def test_init_cartesian(self):
        idnum = 1
        magnitude = 4
        x = 5
        y = 6
        theta = None
        psi = None
        try:
            return Star(idnum, magnitude, x, y)
        except:
            self.fail('Couldn\'t initialise star class')

    def test_init_spherical(self):
        idnum = 1
        magnitude = 4
        x = None
        y = None
        theta = 40
        psi = 11
        try:
            return Star(idnum, magnitude, None, None, theta, psi)
        except:
            self.fail('Couldn\'t initialise star class')
            
    def test_calc_angular_distance_raise(self):
        star = self.test_init_cartesian()
        star2 = self.test_init_spherical()
        with self.assertRaises(Exception, msg='Star angles not set.') as cm:
            star.calc_angular_distance(star2)
        star2 = [1,2,3]
        with self.assertRaises(Exception, msg='Star angles not set.') as cm:
            star.calc_angular_distance(star2)

    def test_calc_angular_distance_1d(self):
        star1 = Star(1, 0, None, None, 40*self.d2r, 0)
        star2 = Star(2, 0, None, None, 50*self.d2r, 0)
        angle = round(star1.calc_angular_distance(star2), 5)
        check = round(10*self.d2r, 5)
        self.assertEquals(angle, check)

    def test_calc_angular_distance_0(self):
        star1 = Star(1, 0, None, None, 40, 11)
        star2 = Star(2, 0, None, None, 40, 11)
        self.assertEquals(star1.calc_angular_distance(star2), 0)

    def test_calc_angular_distance_180(self):
        star1 = Star(1, 0, None, None, 315*self.d2r, 45*self.d2r)
        star2 = Star(2, 0, None, None, 135*self.d2r, -45*self.d2r)
        angle = round(star1.calc_angular_distance(star2), 5)
        check = round(np.pi, 5)
        self.assertEquals(angle, check)

    def test_cartesian_to_spherical_raise(self):
        star = self.test_init_spherical()
        with self.assertRaises(Exception, msg='Star x,y coordinates not set.'):
            star.cartesian_to_spherical()
        star = [1,2,3]
        with self.assertRaises(Exception, msg='Star x,y coordinates not set.'):
            star.cartesian_to_spherical()

    def test_cartesian_to_spherical(self):
        star = Star(1, 1, 100, 0)
        star.cartesian_to_spherical()
        self.assertEquals(star.theta, 0)
        self.assertEquals(star.psi, 0)
        star = Star(1, 1, 0, 100)
        star.cartesian_to_spherical()
        self.assertEquals(star.theta, np.pi/2)
        self.assertEquals(star.psi, 0)

    def test_spherical_to_cartesian_raise(self):
        star = self.test_init_cartesian()
        with self.assertRaises(Exception, msg='Star theta,psi coordinates not \
            set.'):
            star.spherical_to_cartesian()
        star = [1,2,3]
        with self.assertRaises(Exception, msg='Star theta,psi coordinates not \
            set.'):
            star.spherical_to_cartesian()

    def test_spherical_to_cartesian(self):
        star = Star(1, 0, None, None, 45*self.d2r, 45*self.d2r)
        star.spherical_to_cartesian()
        self.assertEquals(round(star.x, 5), 0.5)
        self.assertEquals(round(star.y, 5), 0.5)
        self.assertEquals(round(star.z, 5), round(1/np.sqrt(2), 5))
        star = Star(1, 0, None, None, 0, 0)
        star.spherical_to_cartesian()
        self.assertEquals(star.x, 1)
        self.assertEquals(star.y, 0)
        self.assertEquals(star.z, 0)
        


        

