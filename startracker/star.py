import numpy as np
from component import Component

class Star:
    def __init__(self, idnum, magnitude, x=None, y=None, theta=None, psi=None):
        self.id = int(idnum)
        self.magnitude = float(magnitude)
        self.x = float(x) if x!=None else None
        self.y = float(y) if y!=None else None
        self.z = None
        self.theta = float(theta) if theta!=None else None
        self.psi = float(psi) if psi!=None else None
        self.neighbours = [] 

    def calc_angular_distance(self, star2):
        """Calculate the distance along a great-circle between the two stars,
        given their spherical coordinates"""
        if self.theta == None or self.psi == None or star2.theta == None or \
                self.psi == None:
            raise Exception('Star angles not set.')
        t1 = self.theta
        t2 = star2.theta
        p1 = self.psi
        p2 = star2.psi
        #Use arclength formula (with radius set to 1) from arccos of the dot
        #product of cartesian vector
        x = np.sin(p1)*np.sin(p2)+np.cos(p1)*np.cos(p2)*np.cos(t1-t2)
        return np.arccos(x)

    def cartesian_to_spherical(self):
        """Converts pixel position on camera image to relative spherical
        coordinates."""
        #pixel res
        res_x = 1920
        res_y = 1440
        #normalised focal length - since FOV is 10 degrees, and considering
        #sensor width to be 1
        f=0.5/np.tan(np.deg2rad(10) / 2)

        #normalise pixel positions
        x = self.x/res_x - 0.5
        y = self.y/res_y - 0.5

        theta = np.pi - np.arctan2(y,x)

        r = np.sqrt(x**2 + y**2)
        psi1 = np.arctan(r/f)
        psi = np.pi/2 - psi1
        self.theta = theta
        self.psi = psi

    def spherical_to_cartesian(self):
        if self.psi == None or self.theta == None:
            raise Exception('Star theta,psi coordinates not set.')
        psi = self.psi
        theta = self.theta
        #self.x = np.sin(theta)*np.cos(psi)
        #self.y = np.sin(theta)*np.sin(psi)
        #self.z = np.cos(theta)
        #Above I believe are wrong (not right from right ascension &
        #declination) I've worked out below myself
        self.x = np.cos(psi)*np.cos(theta)
        self.y = np.cos(psi)*np.sin(theta)
        self.z = np.sin(psi)

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
                "\nx coord: "+str(self.x)+ \
                "\ny coord: "+str(self.y)+ \
                "\nmagnitu: "+str(self.magnitude)
        
    def __eq__(self, other):
        if (self.id == other.id and self.magnitude == other.magnitude and
            self.x == other.x and self.y == other.y and self.z == other.z and
            self.psi == other.psi and self.theta == other.theta):
            return True
        return False
        
    def __hash__(self):
        return self.id
