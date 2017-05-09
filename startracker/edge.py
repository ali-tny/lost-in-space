class Edge:
    def __init__(self, v, w):
        self.edge = set([v,w])

    def __eq__(self, other):
        if self.edge == other.edge:
            return True
        return False
