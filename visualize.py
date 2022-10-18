import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors


from saveloadmap import load_map
from stars.starmap import StarMap



def visualize_graph(star_map: StarMap, pos=None):
    G = nx.Graph()

    for stp in star_map.star_paths:
        G.add_edge(stp.stars[0].index, stp.stars[1].index, weight=stp.distance, owner=stp.owner)
        if stp.owner != None:
            print(stp.stars[0].index, stp.stars[1].index, stp.distance, stp.owner)
        
    for st in star_map.stars:
        G.add_node(st.index, owner=st.owner)


    # it might not work since there is not guarantee that the adjacency matrix is a planar graph
    if pos is None:
        pos = nx.planar_layout(G)
    

    edge_owned_groups = []

    # print(G.edges(data=True))
    for i in range(0, 20):
        edges_owned = [(u, v) for (u, v, o) in G.edges(data=True) if o["owner"] == i]
        if len(edges_owned) > 0:
            edge_owned_groups.append(edges_owned)

    edges_owned_by_none = [(u, v) for (u, v, o) in G.edges(data=True) if o["owner"] == None]
    if len(edges_owned_by_none) > 0:
        edge_owned_groups.insert(0, edges_owned_by_none)

    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["owner"] ==]
    num_of_colors = len(edge_owned_groups)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=num_of_colors - 1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    colors_list = [scalarMap.to_rgba(i) for i in range(num_of_colors)]
    colors_list.insert(0, (0.1, 0.1, 0.1, 1))
    node_color_list = [colors_list[st.owner + 1 if st.owner is not None else 0] for st in star_map.stars]


    # nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_color_list, node_size=250)

    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
    # nx.draw_networkx_edges(
    #     G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
    # )
    for index, edges_owned in enumerate(edge_owned_groups):
        print(index)
        nx.draw_networkx_edges(G, pos, edgelist=edges_owned, width=1, edge_color=colors_list[index])
    

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif", font_color='w')
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()




def visualize_graph2(G, pos = None):
    # it might not work since there is not guarantee that the adjacency matrix is a planar graph
    if pos is None:
        pos = nx.planar_layout(G)

    # elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)

    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
    # nx.draw_networkx_edges(
    #     G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
    # )
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1, edge_color="b")

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    map_dir = input("type in the map directory\n")
    map_name = input("type in the map name\n")
    star_map = load_map(map_dir, map_name)

    visualize_graph(star_map, star_map.get_star_position())

