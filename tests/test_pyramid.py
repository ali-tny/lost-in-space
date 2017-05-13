import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.pyramid import Pyramid
from startracker.star import Star
from startracker.scene import Scene
from startracker.angular_distance import AngularDistance

class PyramidTest(unittest.TestCase):

    def setUp(self):
        s1 = Star(0,0,sph=(0,0))
        s2 = Star(1,0,sph=(np.pi/3,0))
        s3 = Star(2,0,sph=(0,np.pi/6))
        self.scene = Scene([s1,s2,s3])

    def test_find_matching_triplets(self):
        ms1 = Star(3,0,sph=(np.pi,0))
        ms2 = Star(4,0,sph=(4*np.pi/3,0))
        ms3 = Star(5,0,sph=(np.pi,np.pi/6))
        ms4 = Star(6,0,sph=(5*np.pi/6,0))
        ms5 = Star(7,0,sph=(np.pi,np.pi/2))
        ms6 = Star(8,0,sph=(np.pi/2,np.pi/6))
        full_scene = Scene([ms1,ms2,ms3,ms4,ms5,ms6])

        distances = full_scene.get_all_angular_distances()
        
        pyramid = Pyramid(self.scene,full_scene)
        matches = pyramid.find_matching_triplets(self.scene,distances)
        self.assertEquals(len(matches), 1)
        
        self.assertIn(ms1,matches[0].stars)
        self.assertIn(ms2,matches[0].stars)
        self.assertIn(ms3,matches[0].stars)
        
    def test_find_matching_triplets_many(self):
        ms1 = Star(3,0,sph=(np.pi,0))
        ms2 = Star(4,0,sph=(4*np.pi/3,0))
        ms3 = Star(5,0,sph=(np.pi,np.pi/6))
        ms4 = Star(6,0,sph=(2*np.pi/3,0))
        full_scene = Scene([ms1,ms2,ms3,ms4])

        distances = full_scene.get_all_angular_distances()
        
        pyramid = Pyramid(self.scene,full_scene)
        matches = pyramid.find_matching_triplets(self.scene,distances)
        self.assertEquals(len(matches), 2)
        
        self.assertIn(ms1,matches[0].stars)
        self.assertIn(ms3,matches[0].stars)

        self.assertIn(ms1,matches[1].stars)
        self.assertIn(ms3,matches[1].stars)

        odd1 = [s for s in matches[0].stars if s not in matches[1].stars]
        odd2 = [s for s in matches[1].stars if s not in matches[0].stars]
        self.assertEquals(len(odd1+odd2),2)
        self.assertIn(ms2,odd1+odd2)
        self.assertIn(ms4,odd1+odd2)

    def test_find_matching_triplets_none(self):
        ms1 = Star(3,0,sph=(np.pi,0))
        ms2 = Star(4,0,sph=(4*np.pi/3,0))
        ms3 = Star(5,0,sph=(np.pi,np.pi/6+0.001))
        full_scene = Scene([ms1,ms2,ms3])

        distances = full_scene.get_all_angular_distances()
        
        pyramid = Pyramid(self.scene,full_scene)
        with self.assertRaises(Exception, msg='No suitable stars found.'):
            matches = pyramid.find_matching_triplets(self.scene,distances)
         

    
