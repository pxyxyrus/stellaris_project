from .star import * 

class StarPath:

    def __init__(self, stars: list[Star], distance):
        self.stars = stars
        self.distance = distance
        self.owner = None # either None or number >= 0
        

    def update(self, stars: list[Star], weight):
        if stars is not None:
            self.stars = stars
        if weight is not None:
            self.weight = weight

