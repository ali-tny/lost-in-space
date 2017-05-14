import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
from distances import Distances

class Scene:
    def __init__(self, stars):
        self.stars = stars

    def cut_low_magnitudes(self, magnitude_cutoff):
        """Remove stars from the scene lower than a given magnitude."""
        stars = self.stars
        stars = [star for star in stars if star.magnitude > magnitude_cutoff]
        return Scene(stars)

    def cut_high_magnitudes(self, magnitude_limit):
        """Remove stars from the scene higher than a given magnitude."""
        stars = self.stars
        stars = [star for star in stars if star.magnitude < magnitude_limit]
        return Scene(stars)

    def assign_neighbours(self, epsilon):
        """Assign neighbours (other stars in scene with angular distance less
        than epsilon)"""
        stars = self.stars
        for i, star in enumerate(stars):
            other_stars = stars[i+1:]
            for other_star in other_stars:
                if star.calc_angular_distance(other_star) < epsilon:
                     star.neighbours.append(other_star)
                     other_star.neighbours.append(star)
    
    def get_all_angular_distances(self, max_distance=None):
        stars = self.stars
        distances = Distances() 
        for i, star in enumerate(stars):
            other_stars = stars[i+1:]
            for other_star in other_stars:
                distances.add_distance(star, other_star, max_distance)
        distances.sort()
        return distances

    def get_triplets(self):
        stars = self.stars
        triplets_stars = itertools.combinations(stars, 3)
        for triplet in triplets_stars:
            yield Scene(triplet)

    def unproject(self, camera):
        """Unproject any pixel positions of stars on camera image to relative 
        spherical coordinates"""
        stars = self.stars
        for star in stars:
            star.unproject(camera)
        self.stars = stars

    def spherical_to_cartesian(self):
        """Convert any spherical coords of stars to cartesian."""
        stars = self.stars
        for star in stars:
            star.spherical_to_cartesian()
        self.stars = stars

    def get_connected_components(self):
        #Copy stars
        stars = self.stars[:]
        components = []
        while stars:
            star = stars.pop()
            component = star.get_connected_component()
            components.append(component)
            stars = [star for star in stars if star not in component.vertices]
        return components

    def view(self):
        """Plot scene on graph."""
        x = [star.pixel_pos[0] for star in self.stars]
        y = [star.pixel_pos[1] for star in self.stars]
        plt.scatter(x,y)
        for star in self.stars:
            for star2 in star.neighbours:
                x1, y1 = star.pixel_pos
                x2, y2 = star2.pixel_pos
                plt.plot([x1, x2], [y1, y2])    
        plt.show()

    def view_spherical(self):
        """Plot the stars on a 3d sphere."""
        x = [star.cartesian[0] for star in self.stars]
        y = [star.cartesian[1] for star in self.stars]
        z = [star.cartesian[2] for star in self.stars]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x,y,z)
        for star in self.stars:
            for star2 in star.neighbours:
                x1,y1,z1 = star.cartesian
                x2,y2,z2 = star2.cartesian
                ax.plot([x1,x2], [y1,y2], [z1,z2])
        plt.show()

    def view_angular_flat(self):
        """Plot a graph of theta vs psi (2d)"""
        x = [star.sph[0] for star in self.stars]
        y = [star.sph[1] for star in self.stars]
        plt.scatter(x,y)
        for star in self.stars:
            for star2 in star.neighbours:
                t1, p1 = star.sph
                t2, p2 = star2.sph
                plt.plot([t1, t2], [p1, p2])
        plt.show()

