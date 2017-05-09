import itertools
import numpy as np

class Component:
    """Represents a connected component in the (undirected) graph of stars"""
    def __init__(self):
        self.vertices = [] 
        self.edges = []
        self.h1 = None

    def add_vertex(self, star):
        self.vertices.append(star)

    def add_edge(self, edge):
        self.edges.append(edge)

    def calc_h1(self):
        """Calculate first homology group dimension (aka number of loops)"""
        #Use Euler characteristic + 1 (since it's connected)
        h1 = len(self.edges)-len(self.vertices)+1
        self.h1 = h1
        return h1

    def sort_vertices_by_magnitude(self):
        self.vertices = sorted(self.vertices, key=lambda x:x.magnitude)
        return self.vertices

    def compare_magnitudes(self, other_component):
        self_vs = self.sort_vertices_by_magnitude()
        other_vs = other_component.sort_vertices_by_magnitude()
        diff = len(self_vs) - len(other_vs)
        if diff>0:
            return self.comp_mags_vertex_lists(self_vs, other_vs, diff), diff
        else:
            return self.comp_mags_vertex_lists(other_vs, self_vs, -diff), -diff
    
    def comp_mags_vertex_lists(self, big_list, small_list, length_diff):
        sublists = itertools.combinations(big_list, len(big_list)-length_diff)   
        min_error=-1
        for sublist in sublists:
            error = self.comp_mags_v_lists_equal(sublist, small_list)
            if min_error==-1 or error<min_error:
                min_error = error
        return min_error

    def comp_mags_v_lists_equal(self, list1, list2):
        error = 0
        for i,v in enumerate(list1):
            error += np.absolute(v.magnitude-list2[i].magnitude)
        return error



        
        

    def __str__(self):
        string = "Component with h1: "+str(self.h1)
        for v in self.vertices:
            string += "\n"+v.__str__()
        return string+"\n"
                
