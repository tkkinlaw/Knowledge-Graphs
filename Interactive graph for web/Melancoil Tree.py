import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph
import http_server

G = nx.DiGraph()

# Define the is_happy function

def is_happy(n, visited):
    if n == 1:
        return True, visited
    elif n in visited:
        return False, visited
    else:
        visited.append(n)
        next_num = sum(int(digit) ** 2 for digit in str(n))
        return is_happy(next_num, visited)

# Create the melancoil tree

for i in range(1, 100):
    happy, tree = is_happy(i, [])

    # Skips happy numbers
    if happy:
        continue

    # Add the entire sequence to the tree
    for j in range(0, len(tree)-1):
        G.add_edge(tree[j], tree[j+1])

nx.draw(G, node_color='lightblue', node_size=500, arrows=True)

# Display the graph
#plt.show()

for n in G:
    G.node[n]['name'] = n
d = json_graph.node_link_data(G)
json.dump(d, open('force/force.json','w'))