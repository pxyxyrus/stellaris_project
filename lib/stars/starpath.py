from .star import * 

class StarPath:

    def __init__(self, stars: list[Star], distance):
        self.stars = stars
        self.distance = distance
        self.owner = None # either None or number >= 0
        

    def update(self, stars: list[Star], distance):
        if stars is not None:
            self.stars = stars
        if distance is not None:
            self.distance = distance

    def __lt__(self, other) -> bool:
        return self.distance < other.distance

    def __le__(self, other):
        return self.distance <= other.distance

