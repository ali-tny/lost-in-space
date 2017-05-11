import numpy as np
import bisect
from angular_distance import AngularDistance

class Distances:
    """Stores angular distances from a scene. Use a set? then direct lookup is
    linear. Currently using list to use bisect module for closest match - how
    efficient is this?"""
    
    def __init__(self):
        self.distances = []
        self.sorted = False

    def add_distance(self, star1, star2, max_distance=None):
        d = AngularDistance(star1, star2)
        if max_distance:
            if d.distance < max_distance:
                self.distances.append(d)
        else:
            self.distances.append(d)

    def sort(self):
        self.distances = sorted(self.distances, key=lambda x:x.distance)
        self.sorted = True

    def find_close(self, other_distance, epsilon):
        """Find distances in the collection closest to the distance given."""
        if not self.sorted: self.sort()
        d_check_low = other_distance.distance - epsilon
        d_check_high = other_distance.distance + epsilon
        distance_array = [d.distance for d in self.distances]
        #bisect module uses o(logn) c implementation (way faster)
        i = bisect.bisect_left(distance_array, d_check_low)
        j = bisect.bisect_right(distance_array, d_check_high,i)
        close_ds = self.distances[i:j]
        rtn_distances = Distances()
        rtn_distances.distances = close_ds
        return rtn_distances

    def reduce_to_one_distance(self, distance):
        """Return a new Distances with only distances from a given star."""
        #NOTE we use list version here! different for sets
        ds = [d for d in self.distances if len(distance.stars & d.stars)>0]
        distances = Distances()
        distances.distances = ds
        return distances
        
