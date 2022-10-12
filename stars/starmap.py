from star import *
from starpath import *
import numpy as np
import networkx as nx

class StarMap:

    def __init__(self, stars: list[Star]):
        self.stars = stars
        self.star_paths = []
        self.adjacency_matrix = np.zeros((self.number_of_stars(), self.number_of_stars()))
        
    def number_of_stars(self):
        return len(self.stars)

    def add_star_path(self, star1, star2, distance):
        if self.adjacency_matrix[star1][star2] == 0 and self.adjacency_matrix[star2][star1] == 0:
            self.adjacency_matrix[star1][star2] = self.adjacency_matrix[star2][star1] = distance
            self.star_paths.append(StarPath([star1, star2], distance))

    def get_star_position(self):
        d = dict()
        for idx, st in enumerate(self.stars):
            d['{}'.format(idx)] = (st.x, st.y)
        return d

    def is_connected(self, star1, star2):
        if self.adjacency_matrix[star1][star2] == self.adjacency_matrix[star2][star1]:
            return self.adjacency_matrix[star1][star2]
        return 0

    def is_all_stars_owned(self):
        for st in self.stars:
            if not st.owned:
                False
        return True



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
    