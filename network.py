import networkx as nx
import matplotlib.pyplot as plt

# Create a network graph
G = nx.Graph()

# Add nodes
nodes = ["Server", "Router A", "Router B", "Router C", "Attacker 1", "Attacker 2", "Botnet"]
G.add_nodes_from(nodes)

# Add connections (links) between nodes
connections = [("Server", "Router A"), ("Router A", "Router B"), ("Router B", "Router C"),
               ("Router C", "Server"), ("Router A", "Attacker 1"), ("Router A", "Attacker 2"),
               ("Attacker 1", "Botnet"), ("Attacker 2", "Botnet")]

G.add_edges_from(connections)

# Visualize the initial graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue', font_color='black', font_size=10, edge_color='gray')
plt.title("Network Visualization (Before DDoS Attack)")
plt.show()

# Apply blackholing (remove connections from attacked node)
G.remove_edges_from([("Router A", "Attacker 1"), ("Router A", "Attacker 2")])

# Visualize the modified graph after applying blackholing
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue', font_color='black', font_size=10, edge_color='gray')
plt.title("Network Visualization (After Applying Blackholing)")
plt.show()