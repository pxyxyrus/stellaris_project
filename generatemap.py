from typing import final
from lib.stars import *
import subprocess
import numpy as np
import networkx as nx
from pathlib import Path
from lib.file.saveloadmap import MAPS_DIRECTORY, save_map 
from visualize import visualize_starmap


MIN_EDGE_WEIGHT = 1
MAX_EDGE_WEIGHT = 20

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



    full_graph = nx.Graph()
    for star in star_map.stars:
        full_graph.add_node(star.index)    

    path_to_file = "{0}/{1}.1.ele".format(map_dir, map_name)
    with open(path_to_file, "r") as f:
        next(f)
        for line in f:
            strs = line.split()
            if strs[0] != "#":
                star1, star2, star3 = int(strs[1]) - 1, int(strs[2]) - 1, int(strs[3]) - 1

                if star2 not in full_graph.neighbors(star1):
                    full_graph.add_edge(star1, star2, weight=get_random_distance())
                if star3 not in full_graph.neighbors(star2):
                    full_graph.add_edge(star2, star3, weight=get_random_distance())
                if star1 not in full_graph.neighbors(star3):
                    full_graph.add_edge(star3, star1, weight=get_random_distance())
                # if star_map.is_connected(star1, star2) == 0:
                    # star_map.add_star_path(star1, star2, get_random_distance())
                # if star_map.is_connected(star1, star3) == 0:
                    # star_map.add_star_path(star1, star3, get_random_distance())
                # if star_map.is_connected(star2, star3) == 0:
                    # star_map.add_star_path(star2, star3, get_random_distance())

    final_graph: nx.Graph = nx.minimum_spanning_tree(G=full_graph)
    cnt = len(final_graph.edges)
    edge_list = list(full_graph.edges)
    while cnt < len(edge_list) / 2:
        edge = edge_list[np.random.randint(0, len(edge_list))]
        if edge not in final_graph.edges:
            star1 = edge[0]
            star2 = edge[1]
            final_graph.add_edge(star1, star2, weight=get_random_distance())
            cnt += 1

    for edge in final_graph.edges(data=True):
        star_map.add_star_path(edge[0], edge[1], edge[2]['weight'])

    save_map(star_map, map_dir, map_name)

    

if __name__ == "__main__":
    # map_name = input("type in a name for the map\n")
    # number_of_stars = int(input("type in the number of stars for this map"))
    # if number_of_stars > 16:
    #     star_map = SpiralStarMap(number_of_stars)
    #     generate_map(map_name, star_map)
    #     visualize_starmap(star_map, star_map.get_star_position())
    # else:
    #     print("number of stars has to be greater than 16")

    cnt = 1
    # tiny small medium large huge
    for i in [200, 400, 600, 800, 1000]:
        for _ in range(0, 200):
            star_map = SpiralStarMap(i)
            generate_map("map{}".format(cnt), star_map)
            cnt += 1