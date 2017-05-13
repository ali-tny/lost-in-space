import sys
import numpy as np
from component import Component

class Star:
    def __init__(self, idnum, magnitude, pixel_pos=None, sph=None):
        self.id = int(idnum)
        self.magnitude = float(magnitude)
        self.cartesian = (None,None,None)
        self.pix_pos = tuple(map(float,pixel_pos)) if pixel_pos!=None else None
        self.sph = tuple(map(float,sph)) if sph!=None else None
        self.neighbours = [] 
        self.matches = []

    def calc_angular_distance(self, star2):
        """Calculate the distance along a great-circle between the two stars,
        given their spherical coordinates"""
        if self.sph==None or star2.sph==None:
            raise Exception('Star angles not set.')
        t1, p1 = self.sph
        t2, p2 = star2.sph
        #Use arclength formula (with radius set to 1) from arccos of the dot
        #product of cartesian vector
        x = np.sin(p1)*np.sin(p2)+np.cos(p1)*np.cos(p2)*np.cos(t1-t2)
        return np.arccos(x)

    def unproject(self, camera):
        """Converts pixel position on camera image to relative spherical
        coordinates."""
        pixel_pos = self.pix_pos
        if pixel_pos==None:
            raise Exception('Star pixel coordinates not set')
        sph = camera.unproject(pixel_pos)
        self.sph = sph

    def spherical_to_cartesian(self):
        if self.sph==None:
            raise Exception('Star theta,psi coordinates not set.')
        theta, psi = self.sph
        x = np.cos(psi)*np.cos(theta)
        y = np.cos(psi)*np.sin(theta)
        z = np.sin(psi)
        self.cartesian = (x,y,z)

    def get_connected_component(self, component=None):
        if component==None:
            component = Component()
        component.add_vertex(self)
        for neighbour in self.neighbours:
            edge = set([self, neighbour])
            if edge not in component.edges:
                component.add_edge(edge)
            if neighbour not in component.vertices:
                component = neighbour.get_connected_component(component)
        return component

    def __str__(self):
        return "STAR id: "+str(self.id)+ \
                "\nx coord: "+str(self.pixel_pos[0])+ \
                "\ny coord: "+str(self.pixel_pos[1])+ \
                "\nmagnitu: "+str(self.magnitude)
        
    def __eq__(self, other):
        if (self.id == other.id and self.magnitude == other.magnitude and
            self.cartesian == other.cartesian and self.sph == other.sph):
            return True
        return False
        
    def __hash__(self):
        return self.id
