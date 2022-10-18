from .star import *
from .starpath import *
import numpy as np
import networkx as nx

class StarMap:

    def __init__(self, stars: list[Star]):
        self.stars = stars
        self.star_paths = []
        self.star_path_dict = {}
        self.adjacency_matrix = np.zeros((self.number_of_stars(), self.number_of_stars()))
        
    def number_of_stars(self):
        return len(self.stars)

    def add_star_path(self, star1_index: int, star2_index: int, distance: int, owner: int=None):
        if self.adjacency_matrix[star1_index][star2_index] == 0 and self.adjacency_matrix[star2_index][star1_index] == 0:
            self.adjacency_matrix[star1_index][star2_index] = self.adjacency_matrix[star2_index][star1_index] = distance
            star_path = StarPath([self.stars[star1_index], self.stars[star2_index]], distance)
            if owner is not None:
                star_path.owner = owner
            self.star_paths.append(star_path)
            self.star_path_dict.setdefault(star1_index, {})[star2_index] = star_path
            self.star_path_dict.setdefault(star2_index, {})[star1_index] = star_path

    def get_star_position(self):
        d = dict()
        for index, st in enumerate(self.stars):
            d[index] = (st.x, st.y)
        return d

    def is_connected(self, star1_index, star2_index):
        return self.adjacency_matrix[star1_index][star2_index]

    def is_all_stars_owned(self):
        for st in self.stars:
            if st.owner is None:
                return False
        return True



# template for creating vertices
class SquareStarMap(StarMap):

    # n by n square starmap
    def __init__(self, n):
        stars = []
        cnt = 0
        for i in range(n):
            for j in range(n):
                x = j * 1 + (0 if i % 2 == 0 else 0.5)
                y = i * 1
                star = Star(x, y, cnt)
                stars.append(star)
                cnt += 1
        super().__init__(stars)
    