class AngularDistance:
    
    def __init__(self, star1, star2):
        self.stars = set([star1, star2])
        self.distance = star1.calc_angular_distance(star2)

    def check_triplet(self, d2, d3):
        if len(self.stars | d2.stars | d3.stars) == 3:
            return True
        else:
            return False

    def __eq__(self, other):
        return (self.distance == other.distance and self.stars == other.stars)

    def __hash__(self):
        h = str(self.distance)
        for star in star:
            h += star.__hash__()
        return h

    def __str__(self):
        s = "Distance: "+str(self.distance)+"\n"
        for star in self.stars:
            s+=star.__str__()+"\n"
        return s+"\n"



