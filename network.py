import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots()
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

nx.draw(G,pos,node_size=200, node_color='skyblue', edge_color='gray')

#Add Background Patches for AS 1
ax.add_patch(Rectangle((0.55,0.4),0.9,0.8,
                       facecolor = 'lightgrey',
                       edgecolor = 'black',
                       alpha = 0.5,
                       ))

#Add Background Patches for AS 2
ax.add_patch(Rectangle((1.55,0.4),0.9,0.8,
                       facecolor = 'lightgrey',
                       edgecolor = 'black',
                       alpha = 0.5,
                       ))

#Add Background Patches for AS 3
ax.add_patch(Rectangle((2.55,0.4),0.9,0.8,
                       facecolor = 'lightgrey',
                       edgecolor = 'black',
                       alpha = 0.5,
                       ))

#Add Background Patches for AS 4
ax.add_patch(Rectangle((3.55,0.4),0.9,0.8,
                       facecolor = 'lightgrey',
                       edgecolor = 'black',
                       alpha = 0.5,
                       ))

#Add BG Patch for Transit AS / AS 5
ax.add_patch(Rectangle((2.2,1.7),0.6,1,
                       facecolor = 'lightgrey',
                       edgecolor = 'black',
                       alpha = 0.5,
                       ))

#Add BG Patch for Last AS / AS 6
ax.add_patch(Rectangle((2.05,3.2),0.9,1,
                       facecolor = 'lightgrey',
                       edgecolor = 'black',
                       alpha = 0.5,
                       ))

# Add Patch Labels
plt.text(0.6, 0.4, "AS 1", fontsize='small')
plt.text(1.6, 0.4, "AS 2", fontsize='small')
plt.text(2.6, 0.4, "AS 3", fontsize='small')
plt.text(3.6, 0.4, "AS 4", fontsize='small')
plt.text(2.3, 1.7, "AS 5", fontsize='small')
plt.text(2.1, 3.2, "AS 6", fontsize='small')

plt.show()