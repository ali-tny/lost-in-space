import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.star import Star
from startracker.scene import Scene
from startracker.angular_distance import AngularDistance

class Scene_test(unittest.TestCase):
    
    def setUp(self):
        #Degrees to radians
        d2r = np.pi/180
        self.d2r = d2r
        self.star1 = Star(1,3.1,None,None,45*d2r,45*d2r)
        self.star2 = Star(2,4.5,None,None,90*d2r,-45*d2r)
        self.star3 = Star(3,1.3,None,None,180*d2r,60*d2r)
        self.star4 = Star(4,2.4,None,None,225*d2r,20*d2r)
        self.star5 = Star(5,6.1,None,None,315*d2r,-30*d2r)
        stars = [self.star1,self.star2,self.star3,self.star4,self.star5]
        self.scene = Scene(stars)

    def test_cut_low_magnitudes(self):
        scene = self.scene
        scene = scene.cut_low_magnitudes(2)
        self.assertIn(self.star1,scene.stars)
        self.assertIn(self.star2,scene.stars)
        self.assertIn(self.star4,scene.stars)
        self.assertIn(self.star5,scene.stars)
        self.assertNotIn(self.star3,scene.stars)

    def test_cut_high_magnitudes(self):
        scene = self.scene
        scene = scene.cut_high_magnitudes(6)
        self.assertIn(self.star1,scene.stars)
        self.assertIn(self.star2,scene.stars)
        self.assertIn(self.star3,scene.stars)
        self.assertIn(self.star4,scene.stars)
        self.assertNotIn(self.star5,scene.stars)

    def test_get_all_angular_distances_all(self):
        star1 = self.star1
        star2 = self.star2
        star3 = self.star3
        distance1 = AngularDistance(star1, star2)
        distance2 = AngularDistance(star1, star3)
        distance3 = AngularDistance(star2, star3)
        scene = Scene([star1,star2,star3])
        distances = scene.get_all_angular_distances()
        self.assertIn(distance1, distances.distances)
        self.assertIn(distance2, distances.distances)
        self.assertIn(distance3, distances.distances)

    def test_get_all_angular_distances_sorted(self):
        star1 = Star(1,1,None,None,0,np.pi/4)
        star2 = Star(2,1,None,None,0,np.pi/2)
        star3 = Star(3,1,None,None,0,np.pi)
        distance1 = AngularDistance(star1, star2)
        distance2 = AngularDistance(star1, star3)
        distance3 = AngularDistance(star2, star3)
        scene = Scene([star1,star2,star3])
        distances = scene.get_all_angular_distances()
        self.assertEquals(distance1,distances.distances[0])
        self.assertEquals(distance3,distances.distances[1])
        self.assertEquals(distance2,distances.distances[2])
        
    def test_get_triplets(self):
        s1 = self.star1
        s2 = self.star2
        s3 = self.star3
        s4 = self.star4
        stars = [s1,s2,s3,s4]
        scene = Scene(stars)
        left_out = []
        for small_scene in scene.get_triplets():
            self.assertEquals(len(small_scene.stars), 3)
            left_out += [s for s in stars if s not in small_scene.stars]
        for star in left_out:
            self.assertIn(star, stars)


            



        
