import re
from copy import deepcopy
from pprint import pprint
from types import NoneType

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def draw_tree(G, axs, fig_idx):
    node_names = []
    for node, _ in G.nodes.items():
        node_names.append(node)
    node_weights = nx.get_node_attributes(G, "value")
    node_labels = dict()
    for node_name in node_names:
        node_labels[node_name] = str(node_name)+': '+str(node_weights[node_name])
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos=pos, with_labels=True, node_color='w', edge_color='b', labels=node_labels, node_shape='s', bbox=dict(facecolor="white", edgecolor='black', boxstyle='round,pad=0.2'), ax=axs[fig_idx])
    axs[fig_idx].collections[0].set_edgecolor("#000000")


G = nx.DiGraph()

known_values = dict()
unknown_values = dict()

with open('day_21_example.txt') as file:
    for line in file:
        line_stripped = line.strip()
        # print(line_stripped)
        elements = line_stripped.split(':')
        # pprint(elements)
        monkey = elements[0]
        # print(monkey)
        G.add_node(monkey, value=elements[1])
        right_side = re.search(r'\d+', elements[1])
        if isinstance(right_side, NoneType):
            calculation = elements[1].replace(' ', '')
            unknown_values[monkey] = calculation
            connected_nodes = re.split(r'\+|-|\*|/', calculation)
            G.add_edge(connected_nodes[0], monkey)
            G.add_edge(connected_nodes[1], monkey)
        else:
            value = int(right_side.group(0))
            known_values[monkey] = value
            # print(str(value))


pprint(known_values)
pprint(unknown_values)

G_working_copy = deepcopy(G)
G_simplified = nx.DiGraph()

done = False

while not done:
    G_simplified = deepcopy(G_working_copy)
    for node, _ in G_working_copy.nodes.items():
        predecessor_count = 0
        for _ in nx.DiGraph.predecessors(G_working_copy, node):
            predecessor_count += 1

        if predecessor_count == 0 and node != 'root':
            print('will be removed: '+node)

            node_value = G_working_copy.nodes[node]['value']

            # there should only be one successor
            for successor in nx.DiGraph.successors(G_working_copy, node):
                successor_value = G_working_copy.nodes[successor]['value']

            replacement = successor_value.replace(node, str(eval(node_value)))

            G_simplified.remove_node(node)
            G_simplified.nodes[successor]['value'] = replacement
        G_working_copy = deepcopy(G_simplified)
        if G_simplified.number_of_nodes() == 1:
            done = True

G_simplified.nodes['root']['value'] = eval(G_simplified.nodes['root']['value'])
pprint(G_simplified.nodes)

print('solution to part 1: '+str(G_simplified.nodes['root']['value']))
fig, axs = plt.subplots(ncols=2)
plt.margins(0.0)
draw_tree(G, axs, 0)
draw_tree(G_simplified, axs, 1)
fig.tight_layout()

plt.show()
