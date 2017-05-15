import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.camera import Camera
from startracker.star import Star
from startracker.scene import Scene

class CameraTest(unittest.TestCase):

    def setUp(self):
        star1 = Star(0,0,sph=(0,np.pi/2))
        self.scene1 = Scene([star1])
        star1 = Star(1,0,sph=(0,0))
        star2 = Star(2,0,sph=(0,np.deg2rad(5)))
        star3 = Star(3,0,sph=(2*np.pi - np.deg2rad(5),0))
        self.scene2 = Scene([star1,star2,star3])

    def test_take_photo(self):
        cam = Camera(self.scene1)
        scene = cam.take_photo()
        self.assertEquals(len(scene.stars),1)
        star = scene.stars[0]
        self.assertEquals(star.pixel_pos, (960,720))
        
        cam = Camera(self.scene2)
        scene = cam.take_photo()
        self.assertEquals(len(scene.stars),0)
        star = cam.scene.stars[0]
        cam.point_at(star)
        scene = cam.take_photo()
        self.assertEquals(len(scene.stars),3)
        self.assertEquals(tuple(map(round,scene.stars[0].pixel_pos)),(960,720))
        self.assertEquals(tuple(map(round,scene.stars[1].pixel_pos)),(960,1440))
        self.assertEquals(tuple(map(round,scene.stars[2].pixel_pos)),(1920,720))

    def test_unproject(self):
        camera = Camera()
        pixel_pos=(960, 720)
        sph = camera.unproject(pixel_pos)
        self.assertEquals(sph[0], np.pi)
        self.assertEquals(sph[1], np.pi/2)
        pixel_pos=(960, 0)
        sph = camera.unproject(pixel_pos)
        self.assertEquals(sph[0], 3*np.pi/2)
        self.assertEquals(sph[1], np.pi/2-np.deg2rad(5))
        pixel_pos=(960, 1440)
        sph = camera.unproject(pixel_pos)
        self.assertEquals(sph[0], np.pi/2)
        self.assertEquals(sph[1], np.pi/2-np.deg2rad(5))
        pixel_pos=(1920, 720)
        sph = camera.unproject(pixel_pos)
        self.assertEquals(sph[0], np.pi)
        self.assertEquals(sph[1], np.pi/2-np.deg2rad(5))
        pixel_pos=(0, 720)
        sph = camera.unproject(pixel_pos)
        self.assertEquals(sph[0], 0)
        self.assertEquals(sph[1], np.pi/2-np.deg2rad(5))
        pixel_pos=(0, 0)
        pixel_pos2=(1920, 1440)
        sph = camera.unproject(pixel_pos)
        sph2 = camera.unproject(pixel_pos2)
        star1 = Star(0,0,sph=sph)
        star2 = Star(1,0,sph=sph2)
        d = star1.calc_angular_distance(star2)
        actual = 2*np.arctan(np.tan(np.deg2rad(5))*np.sqrt(2))
        self.assertEquals(round(d,5), round(actual, 5))

