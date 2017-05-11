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

    def cartesian_to_spherical(self):
        """Convert any cartesian coords of stars to spherical."""
        stars = self.stars
        for star in stars:
            star.cartesian_to_spherical()
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
        x = [star.x for star in self.stars]
        y = [star.y for star in self.stars]
        plt.scatter(x,y)
        for star in self.stars:
            for star2 in star.neighbours:
                plt.plot([star.x, star2.x], [star.y, star2.y])    
        plt.show()

    def view_spherical(self):
        """Plot the stars on a 3d sphere."""
        x = [star.x for star in self.stars]
        y = [star.y for star in self.stars]
        z = [star.z for star in self.stars]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x,y,z)
        for star in self.stars:
            for star2 in star.neighbours:
                ax.plot([star.x,star2.x], [star.y,star2.y], [star.z,star2.z])
        plt.show()

    def view_angular_flat(self):
        """Plot a graph of theta vs psi (2d)"""
        x = [star.theta for star in self.stars]
        y = [star.psi for star in self.stars]
        plt.scatter(x,y)
        for star in self.stars:
            for star2 in star.neighbours:
                plt.plot([star.theta, star2.theta], [star.psi, star2.psi])
        plt.show()





