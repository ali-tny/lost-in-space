import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.star import Star
from startracker.camera import Camera

class Star_test(unittest.TestCase):

    def setUp(self):
        #Degrees to radians
        self.d2r = np.pi/180

    def test_init_cartesian(self):
        idnum = 1
        magnitude = 4
        pixel_pos = (5,6)
        try:
            return Star(idnum, magnitude, pixel_pos)
        except:
            self.fail('Couldn\'t initialise star class')

    def test_init_spherical(self):
        idnum = 1
        magnitude = 4
        sph=(40,11)
        try:
            return Star(idnum, magnitude, sph=sph)
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
        star1 = Star(1, 0, sph=(40*self.d2r, 0))
        star2 = Star(2, 0, sph=(50*self.d2r, 0))
        angle = round(star1.calc_angular_distance(star2), 5)
        check = round(10*self.d2r, 5)
        self.assertEquals(angle, check)

    def test_calc_angular_distance_0(self):
        star1 = Star(1, 0,sph=(40, 11))
        star2 = Star(2, 0,sph=(40, 11))
        self.assertEquals(star1.calc_angular_distance(star2), 0)

    def test_calc_angular_distance_180(self):
        star1 = Star(1, 0,sph=(315*self.d2r, 45*self.d2r))
        star2 = Star(2, 0,sph=(135*self.d2r, -45*self.d2r))
        angle = round(star1.calc_angular_distance(star2), 5)
        check = round(np.pi, 5)
        self.assertEquals(angle, check)

    def test_reorient_raise(self):
        star = Star(1,0)
        with self.assertRaises(Exception,msg='Star theta,psi coordinates not \
            set.'):
            star.reorient(None)

    def test_reorient_no_change(self):
        star_orig = Star(1,0,sph=(0,0))
        star_orig.spherical_to_cartesian()
        star = Star(1,0,sph=(0,0))
        camera = Camera()
        camera.point_at(star)
        orientation = camera.orientation
        new_star = star.reorient(orientation)
        self.assertEquals(star,star_orig)

    def test_reorient(self):
        star = Star(1,0,sph=(0.1204,1.283))
        #star.spherical_to_cartesian()
        camera = Camera()
        camera.point_at(star)
        orientation = camera.orientation
        new_star = star.reorient(orientation)
        self.assertEquals(tuple(map(round,new_star.cartesian)), (0,0,1))

    def test_unproject_raise(self):
        star = self.test_init_spherical()
        with self.assertRaises(Exception, msg='Star x,y coordinates not set.'):
            star.unproject(camera)
        star = [1,2,3]
        with self.assertRaises(Exception, msg='Star x,y coordinates not set.'):
            star.unproject(camera)

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
        camera = Camera()
        star = Star(1, 0,sph=(45*self.d2r, 45*self.d2r))
        star.spherical_to_cartesian()
        self.assertEquals(round(star.cartesian[0], 5), 0.5)
        self.assertEquals(round(star.cartesian[1], 5), 0.5)
        self.assertEquals(round(star.cartesian[2], 5), round(1/np.sqrt(2), 5))
        star = Star(1, 0,sph=(0, 0))
        star.spherical_to_cartesian()
        self.assertEquals(star.cartesian[0], 1)
        self.assertEquals(star.cartesian[1], 0)
        self.assertEquals(star.cartesian[2], 0)

    def test_cartesian_to_spherical_raise(self):
        star = self.test_init_spherical()
        with self.assertRaises(Exception, msg='Star cartesian coordinates not \
            set.'):
            star.cartesian_to_spherical()
        star = [1,2,3]
        with self.assertRaises(Exception, msg='Star cartesian coordinates not \
            set.'):
            star.cartesian_to_spherical()

    def test_cartesian_to_spherical(self):
        camera = Camera()
        star = Star(1, 0)
        star.cartesian = (1/np.sqrt(2), 1/np.sqrt(2), 0)
        star.cartesian_to_spherical()
        self.assertEquals(star.sph[0], np.pi/4)
        self.assertEquals(star.sph[1], 0)
        star = Star(1, 0)
        star.cartesian = (1/np.sqrt(2),0,1/np.sqrt(2),)
        star.cartesian_to_spherical()
        self.assertEquals(star.sph[0], 0)
        self.assertEquals(round(star.sph[1],10),round(np.pi/4,10))
