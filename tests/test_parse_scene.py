import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.parse_scene import SceneParser
from startracker.star import Star

class SceneParser_test(unittest.TestCase):

    def setUp(self):
        self.test_csv_path = 'test_input.csv'
        self.test_hip_path = 'test_hip.dat'
        self.test_csv_row = [1,2,0.1, 3,4,0.2, 5,6,0.3, 7,8,0.4]
        self.test_csv_row_uncastable = [1,2,0.1, 'not id',5,2]
        self.test_csv_row_not_groups_of_three = [1,2,0.1, 2,3]
        self.star1 = Star(0,0.1,1,2)
        self.star2 = Star(1,0.2,3,4)
        self.star3 = Star(2,0.3,5,6)
        self.star4 = Star(3,0.4,7,8)

    def test_parse_csv_row(self):
        scene, fail  = SceneParser.parse_csv_row(self.test_csv_row)
        self.assertEquals(len(scene.stars), 4)
        self.assertIn(self.star1, scene.stars)
        self.assertIn(self.star2, scene.stars)
        self.assertIn(self.star3, scene.stars)
        self.assertIn(self.star4, scene.stars)

    def test_parse_csv_row_uncastable(self):
        scene, fail = SceneParser.parse_csv_row(self.test_csv_row_uncastable)
        self.assertEquals(len(scene.stars), 1)
        self.assertIn(self.star1, scene.stars)
        self.assertEquals(fail,[['not id',5,2]])

    def test_parse_csv_row_not_groups_of_three(self):
        scene, fail = SceneParser.parse_csv_row(
                        self.test_csv_row_not_groups_of_three)
        self.assertEquals(len(scene.stars), 0)
        self.assertEquals(fail, self.test_csv_row_not_groups_of_three)

    def test_parse_hip_data(self):
        d2r = np.pi/180
        star1 = Star(118318,6.99,None,None,359.96374383*d2r,11.67370866*d2r)
        star2 = Star(118319,8.23,None,None,359.97391252*d2r,-22.42818030*d2r)
        star3 = Star(118321,9.20,None,None,359.97823891*d2r,-64.37257220*d2r)
        scene, fail = SceneParser.parse_hip_data(self.test_hip_path)
        self.assertEquals(len(scene.stars),3)
        self.assertIn(star1, scene.stars)
        self.assertIn(star2, scene.stars)
        self.assertIn(star3, scene.stars)
        self.assertEquals(len(fail),2)
        self.assertEquals(fail[0][1].strip(),'118320')
        self.assertEquals(fail[1][1],'not_an_id')

    def test_parse_csv(self):
        scenes, fails = SceneParser.parse_csv(self.test_csv_path)
        star1 = Star(0,4.6258962869844291,1092.2860064407901,636.85114847774378)
        star2 = Star(1,4.8178697493028348,1426.1402525032968,1425.6987141468878)
        star3 = Star(0,4.6802248025298114,1365.1549861743506,690.55647884712869)
        star4 = Star(2,4.7534443440485514,393.47343264299639,3.4957577462069356)
        self.assertEquals(len(scenes),2)
        self.assertEquals(len(fails),2)
        self.assertEquals(len(scenes[0].stars),2)
        self.assertIn(star1, scenes[0].stars)
        self.assertIn(star2, scenes[0].stars)
        self.assertEquals(len(scenes[1].stars),2)
        self.assertIn(star3, scenes[1].stars)
        self.assertIn(star4, scenes[1].stars)


