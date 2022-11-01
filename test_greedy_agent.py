from saveloadmap import MAPS_DIRECTORY, load_map
from agents.agent import *
from stars import *
import numpy as np
import networkx as nx
from game import start_game
from graph import create_graph



# checks greedy agent's sum of edge weight is equal to the sum of edge weight of the minimum spanning tree.
def test_greedy_at_map(star_map):
    agents = []

    agents.append(GreedyAgent(star_map, np.random.randint(0, len(star_map.stars))))

    start_game(agents, star_map)

    G, _ = create_graph(star_map)
    mst: nx.Graph = nx.minimum_spanning_tree(G)
    mst_size = 0
    for edge in list(mst.edges(data=True)):
        mst_size += edge[2]['weight']
    print(mst_size)

    greedy_agent_size = 0
    for path in star_map.star_paths:
        # print(path.owner)
        if path.owner == 0:
            greedy_agent_size += path.distance
    print(greedy_agent_size)
    assert(mst_size == greedy_agent_size)

if __name__ == "__main__":
    map_name = input("type in the map name\n")
    map_dir = map_name
    path_name = MAPS_DIRECTORY + "/" + map_dir
    star_map = load_map(path_name, map_name=map_name)
    test_greedy_at_map(star_map)






    

    



