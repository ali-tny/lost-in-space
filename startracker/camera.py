import numpy as np

class Camera:
    
    def __init__(self, scene=None):
        #pixel res
        self.res = (float(1920), float(1440))
        #normalised focal length - since FOV is 10 degrees, and considering
        #sensor width to be 1
        self.f = 0.5/np.tan(np.deg2rad(10) / 2)
        self.scene = scene
        self.orientation = None

    def take_photo(self):
        pass

    def point_at(self, star):
        """Get an orientation matrix pointing the z axis at the star. Guidance
        from David Kirk's Graphics Gems 3, p117"""
        if star.sph==None:
            raise Exception('Star angles not set.')
        star.spherical_to_cartesian()
        star_pos = np.array(self.cartesian).reshape((3,1))
        z_axis = np.array([0,0,1]).reshape((3,1))
        diff = star_pos - z_axis
        norm = np.linalg.norm(diff)
        if norm == 0:
            #Vector is the z axis
            return np.eye(3)
        v = diff/norm
        H = 2*np.dot(v, v.transpose()) - np.eye(3)
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
        theta = np.pi / 2 - theta
        alpha = np.pi - psi
        
        if np.absolute(theta)!=np.pi/2:
            r = np.tan(theta)*self.f
        else:
            r = 0
    
        x = (np.cos(alpha)*r + res_x/2)*res_x
        y = (np.sin(alpha)*r + res_y/2)*res_y
        return x,y
