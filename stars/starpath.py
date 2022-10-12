
class StarPath:

    def __init__(self, stars, distance):
        self.stars = stars
        self.distance = distance
        self.owned = None

    def update(self, stars, weight):
        if stars is not None:
            self.stars = stars
        if weight is not None:
            self.weight = weight

