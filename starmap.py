from star import *
from starpath import *
import numpy as np


class StarMap:

    def __init__(self, stars):
        self.stars = stars
        self.star_paths = []
        self.adjacencyMatrix = np.zeros((self.number_of_stars(), self.number_of_stars()))
        
    def number_of_stars(self):
        return len(self.stars)

    def add_star_path(self, star1, star2, distance):
        if self.adjacencyMatrix[star1][star2] == 0 and self.adjacencyMatrix[star2][star1] == 0:
            self.adjacencyMatrix[star1][star2] = self.adjacencyMatrix[star2][star1] = distance
            self.star_paths.append(StarPath([star1, star2], distance))

    def get_star_position(self):
        d = dict()
        for idx, st in enumerate(self.stars):
            d['{}'.format(idx)] = (st.x, st.y)
        return d

    def is_connected(self, star1, star2):
        if self.adjacencyMatrix[star1][star2] == self.adjacencyMatrix[star2][star1]:
            return self.adjacencyMatrix[star1][star2]
        return 0



# template for creating vertices
class SquareStarMap(StarMap):

    # n by n square starmap
    def __init__(self, n):
        stars = []
        for i in range(n):
            for j in range(n):
                x = j * 1 + (0 if i % 2 == 0 else 0.5)
                y = i * 1
                star = Star(x, y)
                stars.append(star)
        super().__init__(stars)
    