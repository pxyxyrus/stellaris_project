from typing import List, Tuple
import networkx as nx
from lib.stars import StarMap



def create_graph(star_map: StarMap) -> Tuple[nx.Graph, List[int]]:
    G = nx.Graph()

    owners = []
    for stp in star_map.star_paths:
        G.add_edge(stp.stars[0].index, stp.stars[1].index, weight=stp.distance, owner=stp.owner)
        if stp.owner is not None and stp.owner not in owners:
            owners.append(stp.owner)
        
    for st in star_map.stars:
        G.add_node(st.index, owner=st.owner)
        if st.owner is not None and st.owner not in owners:
            owners.append(st.owner)

    owners.sort()
    return (G, owners)









