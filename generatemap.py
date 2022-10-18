from stars import *
import subprocess
from pathlib import Path
import numpy as np
from saveloadmap import MAPS_DIRECTORY, save_map 
from visualize import visualize_graph


MIN_EDGE_WEIGHT = 1
MAX_EDGE_WEIGHT = 10

def get_random_distance():
    return np.random.randint(MIN_EDGE_WEIGHT, MAX_EDGE_WEIGHT)


# this is a function that uses the software "triangle" to create a randomized planar graph
def generate_map(map_name: str, star_map: StarMap):
    map_name = map_name.replace(" ", "_")
    map_dir = MAPS_DIRECTORY + "/{0}".format(map_name)
    path_to_file = "{0}/{1}.node".format(map_dir, map_name)
    Path(map_dir).mkdir(parents=True, exist_ok=True)

    with open(path_to_file, "w") as f:
        lines_to_write = ["{0} 2 0 0\n".format(star_map.number_of_stars())]
        index = 1
        for st in star_map.stars:
            lines_to_write.append("{0}, {1}, {2}\n".format(index, st.x, st.y))
            index += 1
        f.writelines(lines_to_write)

    p = subprocess.Popen(["./triangle/triangle", path_to_file])
    p.wait()


    path_to_file = "{0}/{1}.1.ele".format(map_dir, map_name)
    with open(path_to_file, "r") as f:
        next(f)
        for line in f:
            strs = line.split()
            if strs[0] != "#":
                idx = np.random.randint(1, 4)
                star1, star2, star3 = int(strs[(idx % 3) + 1]), int(strs[(idx + 1) % 3 + 1]), int(strs[(idx + 2) % 3 + 1])

                # for every triangle pick 2 edges
                # this guarantees that every node is connected
                # Still very likely to get a dense "planar" graph
                edge_added = 1 if star_map.is_connected(star2 - 1, star3 - 1) else 0
                if star_map.is_connected(star1 - 1, star2 - 1) == 0 and edge_added < 2:
                    star_map.add_star_path(star1 - 1, star2 - 1, get_random_distance())
                    edge_added += 1
                if star_map.is_connected(star1 - 1, star3 - 1) == 0 and edge_added < 2:
                    star_map.add_star_path(star1 - 1, star3 - 1, get_random_distance())
                    edge_added += 1


    save_map(star_map, map_dir, map_name)

    

if __name__ == "__main__":
    # passes in number of vertices for the sqaure shape map
    map_name = input("type in a name for the map\n")
    star_map = SquareStarMap(10)
    generate_map(map_name, star_map)
    visualize_graph(star_map, star_map.get_star_position())





        