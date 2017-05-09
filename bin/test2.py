import sys
import time
from parse_scene import SceneParser

hip_data = '../data/hip_main.dat'

t1 = time.time()

scene = SceneParser.parse_hip_data(hip_data)
#scene = scene.cut_low_magnitudes(5.5)
scene = scene.cut_high_magnitudes(5.3)

t2 = time.time()
print t2-t1

#distances = scene.get_all_angular_distances()

t3 = time.time()
print t3-t2

scene.assign_neighbours(0.02)
scene.spherical_to_cartesian()
components = scene.get_connected_components()
for component in components:
    component.calc_h1()
    if component.h1 == 2:
        pass
        #print component
scene.view_spherical()
