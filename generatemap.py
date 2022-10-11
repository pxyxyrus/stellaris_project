import starmap
import star
import subprocess
from pathlib import Path
import numpy as np

from visualize import visualize_graph


MIN_EDGE_WEIGHT = 1
MAX_EDGE_WEIGHT = 10

def get_random_distance():
    return np.random.randint(MIN_EDGE_WEIGHT, MAX_EDGE_WEIGHT)


def generate_map(map_name: str, starMap: starmap.StarMap):
    map_name = map_name.replace(" ", "_")
    map_dir = "./maps/{0}".format(map_name)
    path_to_file = "{0}/{1}.node".format(map_dir, map_name)
    Path(map_dir).mkdir(parents=True, exist_ok=True)

    with open(path_to_file, "w") as f:
        lines_to_write = ["{0} 2 0 0\n".format(starMap.number_of_stars())]
        index = 1
        for st in starMap.stars:
            print(st)
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
                edge_added = 1 if starMap.is_connected(star2 - 1, star3 - 1) else 0
                if starMap.is_connected(star1 - 1, star2 - 1) == 0 and edge_added < 2:
                    starMap.add_star_path(star1 - 1, star2 - 1, get_random_distance())
                    edge_added += 1
                if starMap.is_connected(star1 - 1, star3 - 1) == 0 and edge_added < 2:
                    starMap.add_star_path(star1 - 1, star3 - 1, get_random_distance())
                    edge_added += 1


    
    path_to_file = "{0}/{1}.map".format(map_dir, map_name)  
    with open(path_to_file, "w") as f:
        lines_to_write = ["{0}\n".format(starMap.number_of_stars())]
        index = 0
        for st in starMap.stars:
            print(st)
            lines_to_write.append("{0} {1} {2}\n".format(index, st.x, st.y))
            index += 1
        
        for stp in starMap.star_paths:
            lines_to_write.append("{0} {1} {2}\n".format(stp.stars[0], stp.stars[1], stp.distance))

        f.writelines(lines_to_write)


def load_map(map_name):
    map_name = map_name.replace(" ", "_")
    map_dir = "./maps/{0}".format(map_name)
    path_to_file = "{0}/{1}.map".format(map_dir, map_name)

    with open(path_to_file, "r") as f:
        num_of_stars = int(next(f))
        stars = [None for i in range(0, num_of_stars)]
        for _ in range(0, num_of_stars):
            line = next(f)
            strs = line.split()
            star_num, x, y = int(strs[0]), float(strs[1]), float(strs[2])
            stars[star_num] = star.Star(x, y)
            stars.append(star)
        starMap = starmap.StarMap(stars)
        for line in f:
            strs = line.split()
            star1, star2, distance = int(strs[0]), int(strs[1]), int(strs[2])
            starMap.add_star_path(star1, star2, distance)
    return starMap

    

if __name__ == "__main__":
    # passes in number of vertices for the sqaure shape map
    map_name = input("type in a name for the map\n")
    starMap = starmap.SquareStarMap(10)
    print(starMap.number_of_stars())
    generate_map(map_name, starMap)
    visualize_graph(starMap.adjacencyMatrix, starMap.get_star_position())





        