import numpy as np
from scene import Scene

class Camera:
    
    def __init__(self, scene=None):
        #pixel res
        self.res = (float(1920), float(1440))
        #normalised focal length - since FOV is 10 degrees, and considering
        #sensor width to be 1
        self.f = 0.5/np.tan(np.deg2rad(10) / 2)
        self.scene = scene
        self.orientation = np.eye(3)

    def take_photo(self):
        """Take a photo of the scene in the set orientation (if none set with
        point_at star method, its directly up at the z axis. Returns scene with
        stars taken photograph of, with pixel positions (and spherical/cartesian
        coordinates)"""
        orientation = self.orientation
        scene = self.scene
        stars = []
        for star in scene.stars:
            moved_star = star.reorient(orientation)
            moved_star.project(self)
            if all(a<=b for a,b in zip(moved_star.pixel_pos, self.res)) and \
                 all(a>=b for a,b in zip(moved_star.pixel_pos, (0,0))):
                stars.append(moved_star)
        return Scene(stars)

    def point_at(self, star):
        """Get an orientation matrix pointing the z axis at the star. Guidance
        from David Kirk's Graphics Gems 3, p117"""
        if star.sph==None:
            raise Exception('Star angles not set.')
        star.spherical_to_cartesian()
        star_pos = np.array(star.cartesian)

        #Pick y such that it's different to z
        y = np.array([0,0,1])
        if np.abs(np.dot(y,star_pos))>0.99999:
            y = np.array([0,1,0])

        #Then crossing gives a perpendicular x direction
        x = np.cross(y,star_pos)
        x = x/np.linalg.norm(x)
        #Crossing again gives a perpendicular y direction
        y = np.cross(star_pos,x)
        H = np.array([x,y,star_pos])
        self.orientation = H
        
    def unproject(self, pixel_pos):
        """Converts pixel position on camera image to relative spherical
        coordinates."""
        x, y = pixel_pos
        res_x, res_y = self.res

        #normalise pixel positions
        x = x/res_x - 0.5
        y = y/res_y - 0.5

        #See notes for explanation of these formula - assumes middle of frame is
        #the north pole 
        theta = np.pi - np.arctan2(y,x)

        r = np.sqrt(x**2 + y**2)
        psi1 = np.arctan(r/self.f)
        psi = np.pi/2 - psi1
        return theta, psi

    def project(self, sph_coords):
        """Converts spherical coordinates to pixel position on camera image
        (where centre of image is the north pole)"""
        res_x, res_y = self.res
        theta, psi = sph_coords
        #If star is behind camera, return inf for camera coords 
        if psi<=0:
            return (np.inf, np.inf)

        
        if np.absolute(psi)!=np.pi/2:
            r = np.tan(np.pi/2-psi)*self.f
        else:
            r = 0

        #If we don't translate theta, the x direction will be flipped. Can't do
        # -theta since sin(-x)=-sin(x) but cos(-x)=cos(x). So need pi-theta
        theta = np.pi-theta
        
        x = (np.cos(theta)*r + 0.5)*res_x
        y = (np.sin(theta)*r + 0.5)*res_y
        return x,y
