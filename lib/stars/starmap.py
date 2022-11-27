from .star import *
from .starpath import *
import numpy as np

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



class SpiralStarMap(StarMap):

    # n points with spiral like
    # every points generated pi/4
    def __init__(self, n):
        # r = a + b / pi * (theta ** (1 / c))
        # spiral increases by 2b every cycle(= 2pi)
        theta_steps = np.pi/8
        theta_start = np.pi/2
        theta_end = theta_start + n * theta_steps
        a, b, c = 25, 2, 1

        angles = np.arange(start=theta_start, stop = theta_end, step=theta_steps)
        # angles = np.arange(start=theta_start, stop = theta_end, step=theta_steps)
        
        for index, theta in enumerate(angles):
            if index == 0:
                continue
            if np.random.randint(0, 10) != 0:
                angles[index] = theta + np.pi/np.random.randint(9, 16)


        stars = []
        for index, theta in enumerate(angles):
            r = a + b / np.pi * (theta ** (1 / c))
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            stars.append(Star(x, y, index))

        super().__init__(stars)

