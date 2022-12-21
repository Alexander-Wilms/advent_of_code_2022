import re
from pprint import pprint
from types import NoneType

import matplotlib.pyplot as plt
import networkx as nx

g = nx.Graph()

known_values = dict()
unknown_values = dict()

with open('day_21_input.txt') as file:
    for line in file:
        line_stripped = line.strip()
        print(line_stripped)
        elements = line_stripped.split(':')
        pprint(elements)
        monkey = elements[0]
        print(monkey)
        g.add_node(monkey, value=elements[1])
        right_side = re.search(r'\d+', elements[1])
        if isinstance(right_side, NoneType):
            print('calc')
            calculation = elements[1].replace(' ', '')
            unknown_values[monkey] = calculation
            connected_nodes = re.split(r'\+|-|\*|/', calculation)
            g.add_edge(connected_nodes[0], monkey)
            g.add_edge(connected_nodes[1], monkey)
        else:
            value = int(right_side.group(0))
            known_values[monkey] = value
            print(str(value))


pprint(known_values)
pprint(unknown_values)


nx.draw(g, with_labels=True, node_color='w', edge_color='b')
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")
plt.show()
