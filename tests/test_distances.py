import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.distances import Distances
from startracker.star import Star
from startracker.angular_distance import AngularDistance

class Distances_test(unittest.TestCase):
    
    def setUp(self):
        distances = Distances()
        self.star1 = Star(1,0,sph=(0,0))
        self.star2 = Star(2,0,sph=(np.pi/3,0))
        self.star3 = Star(3,0,sph=(np.pi,0))
        self.star4 = Star(4,0,sph=(2*np.pi/3+0.001,0))
        self.distance12 = AngularDistance(self.star1,self.star2)
        self.distance13 = AngularDistance(self.star1,self.star3)
        self.distance23 = AngularDistance(self.star2,self.star3)
        distances.add_distance(self.star1,self.star3)
        distances.add_distance(self.star1,self.star2)
        distances.add_distance(self.star2,self.star3)
        self.distances = distances

    def test_add_distance(self):
        distances = self.distances
        distances.add_distance(self.star1,self.star2)
        self.assertIn(self.distance12, distances.distances)

    def test_sort(self):
        distances = self.distances
        distances.sort()
        self.assertEquals(self.distance12,distances.distances[0])
        self.assertEquals(self.distance23,distances.distances[1])
        self.assertEquals(self.distance13,distances.distances[2])

    def test_find_close_single(self):
        distances = self.distances
        d_check = AngularDistance(self.star1,self.star4)
        epsilon = 0.01
        close = distances.find_close(d_check,epsilon)
        self.assertEquals(close.distances, [self.distance23])

    def test_find_close_several(self):
        distances = self.distances
        d_check = AngularDistance(self.star1,Star(5,0,sph=(np.pi/3,0)))
        epsilon = np.pi/3+0.1
        close = distances.find_close(d_check,epsilon)
        self.assertEquals(len(close.distances), 2)
        self.assertIn(self.distance12, close.distances)
        self.assertIn(self.distance23, close.distances)
        
    def test_find_close_all(self):
        distances = self.distances
        d_check = AngularDistance(self.star1,self.star4)
        epsilon = np.pi
        close = distances.find_close(d_check,epsilon)
        self.assertEquals(len(close.distances), 3)
        self.assertIn(self.distance12, close.distances)
        self.assertIn(self.distance23, close.distances)
        self.assertIn(self.distance13, close.distances)
       
    def test_find_close_not_close_enough(self):
        distances = self.distances
        d_check = AngularDistance(self.star1,self.star4)
        epsilon = 0.0001
        close = distances.find_close(d_check,epsilon)
        self.assertEquals(close.distances, [])

    def test_reduce_to_one_distance(self):
        distances = self.distances
        distances.add_distance(self.star1, self.star4)
        new_distances = distances.reduce_to_one_distance(self.distance23)
        self.assertEquals(len(new_distances.distances), 3)
        self.assertIn(self.distance23, new_distances.distances)
        self.assertIn(self.distance12, new_distances.distances)
        self.assertIn(self.distance13, new_distances.distances)

        
    def test_reduce_to_one_distance_no_change(self):
        distances = self.distances
        new_distances = distances.reduce_to_one_distance(self.distance12)
        self.assertEquals(len(distances.distances),len(new_distances.distances))
        for d in distances.distances:
            self.assertIn(d, new_distances.distances)


    def test_reduce_to_one_distance_all_gone(self):
        distances = self.distances 
        d = AngularDistance(self.star4, Star(5,0,sph=(0,0)))
        new_distances = distances.reduce_to_one_distance(d)
        self.assertEquals(new_distances.distances, [])
    
