import sys
import numpy as np
from scene import Scene

class Pyramid:

    def __init__(self, scene, full_scene):
        self.scene = scene
        self.full_scene = full_scene

    def find_match(self):
        full_scene = self.full_scene
        scene = self.scene
        print "finding distances"
        max_distance = np.deg2rad(14.2)
        all_distances = full_scene.get_all_angular_distances(max_distance)

        matches = []
        triplets = scene.get_triplets()
        for t in triplets:
            try:
                matches.append(self.find_matching_triplets(t, all_distances))
                print 'Match found!'
            except Exception as e:
                print e
        return matches
            
        
    def find_matching_triplets(self, triplet, all_distances):
        triplet_ds = triplet.get_all_angular_distances()
        d1 = triplet_ds.distances[0]
        d2 = triplet_ds.distances[1]
        d3 = triplet_ds.distances[2]
        #TODO set epsilon properly
        epsilon = 0.001
        rd1s = all_distances.find_close(d1, epsilon)
        matches = []
        for rd1 in rd1s.distances:
            cut1_all_distances = all_distances.reduce_to_one_distance(rd1)
            rd2s = cut1_all_distances.find_close(d2, epsilon)
            for rd2 in rd2s.distances:
                cut2_all_distances=cut1_all_distances.reduce_to_one_distance(rd2)
                rd3s = cut2_all_distances.find_close(d3, epsilon)
                for rd3 in rd3s.distances:
                    if rd1.check_triplet(rd2, rd3):
                        stars = [s for s in rd1.stars|rd2.stars|rd3.stars]
                        matches.append(Scene(stars))
        if not matches: raise Exception('No suitable stars found.')
        return matches


                    
        



            
            
