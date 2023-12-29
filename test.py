# import numpy as np
# import matplotlib.pyplot as plt
# import networkx as nx

# def community_layout(g, partition):
#     """
#     Compute the layout for a modular graph.


#     Arguments:
#     ----------
#     g -- networkx.Graph or networkx.DiGraph instance
#         graph to plot

#     partition -- dict mapping int node -> int community
#         graph partitions


#     Returns:
#     --------
#     pos -- dict mapping int node -> (float x, float y)
#         node positions

#     """

#     pos_communities = _position_communities(g, partition, scale=3.)

#     pos_nodes = _position_nodes(g, partition, scale=1.)

#     # combine positions
#     pos = dict()
#     for node in g.nodes():
#         pos[node] = pos_communities[node] + pos_nodes[node]

#     return pos

# def _position_communities(g, partition, **kwargs):

#     # create a weighted graph, in which each node corresponds to a community,
#     # and each edge weight to the number of edges between communities
#     between_community_edges = _find_between_community_edges(g, partition)

#     communities = set(partition.values())
#     hypergraph = nx.DiGraph()
#     hypergraph.add_nodes_from(communities)
#     for (ci, cj), edges in between_community_edges.items():
#         hypergraph.add_edge(ci, cj, weight=len(edges))

#     # find layout for communities
#     pos_communities = nx.spring_layout(hypergraph, **kwargs)

#     # set node positions to position of community
#     pos = dict()
#     for node, community in partition.items():
#         pos[node] = pos_communities[community]

#     return pos

# def _find_between_community_edges(g, partition):

#     edges = dict()

#     for (ni, nj) in g.edges():
#         ci = partition[ni]
#         cj = partition[nj]

#         if ci != cj:
#             try:
#                 edges[(ci, cj)] += [(ni, nj)]
#             except KeyError:
#                 edges[(ci, cj)] = [(ni, nj)]

#     return edges

# def _position_nodes(g, partition, **kwargs):
#     """
#     Positions nodes within communities.
#     """

#     communities = dict()
#     for node, community in partition.items():
#         try:
#             communities[community] += [node]
#         except KeyError:
#             communities[community] = [node]

#     pos = dict()
#     for ci, nodes in communities.items():
#         subgraph = g.subgraph(nodes)
#         pos_subgraph = nx.spring_layout(subgraph, **kwargs)
#         pos.update(pos_subgraph)

#     return pos

# def test():
#     # to install networkx 2.0 compatible version of python-louvain use:
#     # pip install -U git+https://github.com/taynaud/python-louvain.git@networkx2
#     from community import community_louvain

#     g = nx.karate_club_graph()
#     partition = community_louvain.best_partition(g)
#     pos = community_layout(g, partition)

#     nx.draw(g, pos, node_color=list(partition.values())); plt.show()
#     return

# test()



# G.add_node("router")
# for i in range(1, 5):
#     G.add_node(f"switch_{i}")
#     for j in range(1, 5):
#         G.add_node("PC_" + str(i) + "_" + str(j))

# G.add_edge("router", "switch_1")
# G.add_edge("router", "switch_2")
# G.add_edge("router", "switch_3")
# G.add_edge("router", "switch_4")
# for u in range(1, 5):
#     for v in range(1, 5):
#         G.add_edge("switch_" + str(u), "PC_" + str(u) + "_" + str(v))

# # Get a reproducible layout and create figure
# pos = nx.multipartite_layout(G)
# # fig, ax = plt.subplots()

# # Note: the min_source/target_margin kwargs only work with FancyArrowPatch objects.
# # Force the use of FancyArrowPatch for edge drawing by setting `arrows=True`,
# # but suppress arrowheads with `arrowstyle="-"`
# nx.draw(
#     G,
#     pos=pos,
#     # ax=ax,
#     # min_source_margin=15,
#     # min_target_margin=15,
# )

# plt.show()

############################


import networkx as nx
import matplotlib.pyplot as plt

# Create a network graph
G = nx.Graph()

# Add central clients or routers for each AS
central_clients = [f"AS_Central_Client{i}" for i in range(1, 5)]
G.add_nodes_from(central_clients)

#Add Nodes for each AS 1-4
for u in range(1,5):
    for v in range(1, 6):
        G.add_node(f"AS{u}_client{v}")

# Add nodes for the transit AS
G.add_node("transit_AS_1")
G.add_node("transit_AS_2")

# Add nodes for the last AS with the target client
G.add_node("Last_AS_Central_Client")
last_as = [f"Last_AS_Client{i}" for i in range(1, 6)]
G.add_nodes_from(last_as)

### Add edges
# # Connect central clients to their respective clients (star-shaped topology)
for u in range (4):
    for v in range(1,6):
        G.add_edge(central_clients[u], f"AS{u+1}_client{v}")

# # Connect central client to transit AS (star-shaped topology)
G.add_edges_from([("transit_AS_1", client) for client in central_clients])

# # Connect central client to last AS (star-shaped topology)
for i in range(1,6):
    G.add_edge("Last_AS_Central_Client", f"Last_AS_Client{i}")

# Connect Transit AS and Last AS
G.add_edge("transit_AS_2", "Last_AS_Central_Client")    
G.add_edge("transit_AS_1", "transit_AS_2")

# Organize  layout for a quasi dumbbell topology with star-shaped subnetworks and AS
pos = {
    "AS_Central_Client1": (1,1),
    "AS_Central_Client2": (2,1),
    "AS_Central_Client3": (3,1),
    "AS_Central_Client4": (4,1),
    "AS1_client1": (0.66, 0.8),
    "AS1_client2": (0.82, 0.65),
    "AS1_client3": (1, 0.6),
    "AS1_client4": (1.16, 0.65),
    "AS1_client5": (1.32, 0.8),
    "AS2_client1": (1.66, 0.8),
    "AS2_client2": (1.82, 0.65),
    "AS2_client3": (2, 0.6),
    "AS2_client4": (2.16, 0.65),
    "AS2_client5": (2.32, 0.8),
    "AS3_client1": (2.66, 0.8),
    "AS3_client2": (2.82, 0.65),
    "AS3_client3": (3, 0.6),
    "AS3_client4": (3.16, 0.65),
    "AS3_client5": (3.32, 0.8),
    "AS4_client1": (3.66, 0.8),
    "AS4_client2": (3.82, 0.65),
    "AS4_client3": (4, 0.6),
    "AS4_client4": (4.16, 0.65),
    "AS4_client5": (4.32, 0.8),
    "transit_AS_1": (2.5, 2),
    "transit_AS_2": (2.5, 2.5),
    "Last_AS_Central_Client": (2.5,3.5),
    "Last_AS_Client1": (2.16, 3.7),
    "Last_AS_Client2": (2.32, 3.85),
    "Last_AS_Client3": (2.5, 3.9),
    "Last_AS_Client4": (2.66, 3.85),
    "Last_AS_Client5": (2.82, 3.7)
}

# Visualize the graph
# nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue', font_color='black', font_size=8, edge_color='gray', alpha=0.7)
# plt.title("Dumbbell Topology with Star-Shaped Subnetworks and AS")

nx.draw(G,pos,node_size=300, node_color='skyblue', edge_color='gray')

plt.show()