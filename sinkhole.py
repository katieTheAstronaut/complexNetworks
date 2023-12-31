import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random

# Abbildung und Netzwerkgraph erstellen
fig, ax = plt.subplots()
G = nx.Graph()

######## Knoten erstellen
# Zentrale Clients / Router für jedes AS erstellen
central_clients = [f"AS_Central_Client{i}" for i in range(1, 5)]
G.add_nodes_from(central_clients)
G.add_node("Last_AS_Central_Client")

# Für jedes AS (1-4) Knoten erstellen
for u in range(1,5):
    for v in range(1, 6):
        G.add_node(f"AS{u}_client{v}")

# Knoten für Transit-AS erstellen
G.add_nodes_from(["transit_AS_1", "transit_AS_2"])
G.add_nodes_from([f"Transit_client{i}" for i in range(1,6)])


# Knoten für oberes AS (6) erstellen
last_as = [f"Last_AS_Client{i}" for i in range(1, 6)]
G.add_nodes_from(last_as)

######## Kanten hinzufügen
# Router mit Clients in ihrem AS verbinden
for u in range (4):
    for v in range(1,6):
        G.add_edge(central_clients[u], f"AS{u+1}_client{v}", color='lightgrey')

# Router mit Transit-AS verbinden
G.add_edges_from([("transit_AS_1", client) for client in central_clients], color='lightgrey')

# Transit-AS Clients verbinden
G.add_edges_from([("transit_AS_1", f"Transit_client{i}") for i in range(1,6)], color='lightgrey')
G.add_edges_from([("transit_AS_2", f"Transit_client{i}") for i in range(1,6)], color='lightgrey')

# Oberes AS verbinden
for i in range(1,6):
    G.add_edge("Last_AS_Central_Client", f"Last_AS_Client{i}", color='lightgrey')
G.add_edge("transit_AS_2", "Last_AS_Central_Client", color='lightgrey')    

####### Positionierung der Knoten festlegen
pos = {}
x_values_central = [1, 2, 3, 4]
x_values = [0.66,0.82,1,1.16,1.32]
y_values = [0.8, 0.65, 0.6, 0.65, 0.8]
y_values_last = [3.7, 3.85, 3.9, 3.85, 3.7]

# AS1-4 Edge Router 
for i, x in enumerate(x_values_central, start=1):
    pos[f"AS_Central_Client{i}"] = (x, 1)

# AS 1-4 Clients 
counter =0
for as_id in ["AS1", "AS2", "AS3", "AS4"]:
    for i in range(1,6):
        pos[f"{as_id}_client{i}"] = (x_values[i-1] + counter, y_values[i-1])
    counter +=1    

# Transit-AS und Clients
pos["transit_AS_1"]= (2.5, 2)
pos["transit_AS_2"]= (2.5, 2.5)
for i in range(1, 6):
    pos[f"Transit_client{i}"] = (x_values[i-1] + 1.5, 2.25)

# Oberes AS
pos["Last_AS_Central_Client"] = (2.5, 3.5)
for i in range(1, 6):
    pos[f"Last_AS_Client{i}"] = (x_values[i-1] + 1.5, y_values_last[i-1])


####### Graph visualisieren
# AS-Boxen erstellen
DEFAULT_COLOUR = 'lightgrey'
HIGHLIGHT_COLOUR = 'lightyellow'
BOX_EDGE = 'black'
ALPHA = 0.5

as_rectangles = [
    ((0.55, 0.4), 0.9, 0.8),
    ((1.55, 0.4), 0.9, 0.8),
    ((2.55, 0.4), 0.9, 0.8),
    ((3.55, 0.4), 0.9, 0.8),
    ((2.05, 3.2), 0.9, 1)
]

for rect_params in as_rectangles:
    ax.add_patch(Rectangle(*rect_params, facecolor=DEFAULT_COLOUR, alpha = ALPHA, edgecolor=BOX_EDGE))
ax.add_patch(Rectangle((2.05, 1.7), 0.9, 1, facecolor=HIGHLIGHT_COLOUR, alpha = ALPHA, edgecolor=BOX_EDGE))

# Labels für AS Boxen hinzufügen
as_positions = [(0.6, 0.42), (1.6, 0.42), (2.6, 0.42), (3.6, 0.42), (2.3, 1.72), (2.1, 3.22)]
as_labels = ["AS 1 (Enterprise)", "AS 2 (Enterprise)", "AS 3 (Enterprise)", "AS 4 (Enterprise)", "AS 5 (ISP)", "AS 6 (Enterprise)"]
for position, label in zip(as_positions, as_labels):
    plt.text(position[0], position[1], label, fontsize='x-small')

########## Botnetz erstellen
# Angreifer und Handler/ C&Cs darstellen
G.add_nodes_from(["Attacker", "Handler_1","Handler_2"])
pos["Attacker"] = (2.5, -1)
pos["Handler_1"] = (1.5, -0.5)
pos["Handler_2"] = (3.5, -0.5)
plt.text(2.4, -1.3, "Angreifer", fontsize = 'small')
plt.text(1.4, -0.8, "Handler 1", fontsize = 'small')
plt.text(3.4, -0.8, "Handler 2", fontsize = 'small')

# Liste von Bots: Für jeden Client in AS 1-4 zufällig wählen, ob infiziert
bot = []
for i in range (1,5):
    for j in range (1,6):
        if random.choice([True, False]) == True:
            bot.append(f"AS{i}_client{j}")

# Fehlende Kanten zeichnen
G.add_edge("Attacker", "Handler_1",color='lightpink')
G.add_edge("Attacker", "Handler_2", color='lightpink')

############# DDoS-Angriff darstellen // bei Sinkhole 
for bots in bot:
    G.add_edge(bots, "Handler_1" if int(bots[2]) <3 else "Handler_2", color='lightgrey') # Bots mit Handlern verbinden, aber inaktiv (grau)
    G.add_edge(bots, "Sinkhole", color='lightpink') # Verbindung zwischen Bots und Sinkhole
    
attackers = ["Attacker", "Handler_1", "Handler_2"]
target_node = ["Last_AS_Client2"]

#############Sinkhole
# Knoten und Box für Sinkhole darstellen
G.add_node("Sinkhole")    
pos["Sinkhole"] = (0, -0.5)
plt.text(-0.2, -0.9, "Sinkhole System", fontsize = 'small')
ax.add_patch(Rectangle((-0.3, -0.7), 0.7, 0.6, facecolor='red', alpha = ALPHA, edgecolor=BOX_EDGE))

# Farben etc.
edges = G.edges()
edge_colours = nx.get_edge_attributes(G,'color').values()
colour_map = ['red' if node in attackers else 'grey' if node in bot else 'black' if node == "Sinkhole" else 'green' if node in target_node else 'skyblue' for node in G]

# Graph zeichnen
nx.draw(G,pos,node_size=100, node_color=colour_map, edge_color=edge_colours)

# Abbildung anzeigen
plt.show()