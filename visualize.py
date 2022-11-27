import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
from lib.file.saveloadmap import load_map
from lib.stars.starmap import StarMap
from lib.graph.graph import create_graph




    


def visualize_starmap(star_map: StarMap, pos=None, block_thread=False):
    G, owners = create_graph(star_map)
    visualize_graph(G, owners, pos, block_thread)



def visualize_graph(G, owners, pos=None, block_thread=False):
 # it might not work since there is not guarantee that the adjacency matrix is a planar graph
    if pos is None:
        pos = nx.planar_layout(G)

    edge_owned_groups = []
    # print(G.edges(data=True))
    for owner in owners:
        edges_owned = [(u, v) for (u, v, d) in G.edges(data=True) if d["owner"] == owner]
        edge_owned_groups.append(edges_owned)

    num_of_colors = len(owners)

    # add list of edges where owner is None 
    edges_owned_by_none = [(u, v) for (u, v, d) in G.edges(data=True) if d["owner"] == None]
    edge_owned_groups.insert(0, edges_owned_by_none)

    # cm = plt.get_cmap('gist_rainbow')
    # cNorm  = colors.Normalize(vmin=0, vmax=num_of_colors - 1)
    # scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    # colors_list = [scalarMap.to_rgba(i) for i in range(num_of_colors)]
    colors_list = ["b", "g", "r", "c", "m", "y"]

    # Color None (black) is always the first
    colors_list.insert(0, (0.1, 0.1, 0.1, 1))
    node_color_list = [colors_list[d["owner"] + 1] if d["owner"] is not None else (0, 0, 0, 1) for (n, d) in G.nodes(data=True)]

    # nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_color_list, node_size=25)

    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
    # nx.draw_networkx_edges(
    #     G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
    # )

    for index, edges_owned in enumerate(edge_owned_groups):
        nx.draw_networkx_edges(G, pos, edgelist=edges_owned, width=1, edge_color=colors_list[index])
    

    # node labels
    # nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif", font_color='w')
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size = 10, font_family = 'sans-serif')

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show(block=block_thread)
    plt.pause(0.00000001)
    plt.clf()




if __name__ == "__main__":
    map_dir = input("type in the map directory\n")
    map_name = input("type in the map name\n")
    star_map = load_map(map_dir, map_name)

    visualize_starmap(star_map, star_map.get_star_position(), True)

