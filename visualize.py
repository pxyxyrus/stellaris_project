import networkx as nx
import matplotlib.pyplot as plt

from load_map import load_map



def visualize_graph(star_map, adjacency_matrix, pos=None):
    G = nx.Graph()

    for i in range(0, adjacency_matrix.shape[0]):
        for j in range(0, i):
            if adjacency_matrix[i][j] == 0:
                continue
            else:
                G.add_edge("{}".format(i), "{}".format(j), weight=adjacency_matrix[i][j])
                edgeNum += 1


    # it might not work since there is not guarantee that the adjacency matrix is a planar graph
    if pos == None:
        pos = nx.planar_layout(G)
        print(pos)

    # elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=250)

    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
    # nx.draw_networkx_edges(
    #     G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
    # )
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1, edge_color="b")

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")
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
    if pos == None:
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
    map_name = input("type in the map name\n")
    star_map = load_map(map_name)
    visualize_graph(star_map, star_map.adjacency_matrix, star_map.get_star_position())

