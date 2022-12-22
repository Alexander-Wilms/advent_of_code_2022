import re
from copy import deepcopy
from pprint import pprint
from types import NoneType

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from sympy import Symbol
from sympy.solvers import solve
from alive_progress import alive_bar


def draw_tree(G, axs, fig_idx):
    node_names = []
    for node, _ in G.nodes.items():
        node_names.append(node)
    node_weights = nx.get_node_attributes(G, "value")
    node_labels = dict()
    for node_name in node_names:
        node_labels[node_name] = str(node_name)+': '+str(node_weights[node_name])
    # https://stackoverflow.com/a/57512902/2278742
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos=pos, with_labels=True, node_color='w', edge_color='b', labels=node_labels, node_shape='s', bbox=dict(facecolor="white", edgecolor='black', boxstyle='round,pad=0.2'), ax=axs[fig_idx])
    axs[fig_idx].collections[0].set_edgecolor("#000000")


def simplify_tree(G: nx.DiGraph, puzzle_part: int, id_of_number_to_yell='') -> nx.DiGraph:
    G_working_copy = deepcopy(G)
    G_simplified = nx.DiGraph()

    if puzzle_part == 2:
        G_working_copy.nodes['root']['value'] = G_working_copy.nodes['root']['value'].replace('+', '-').replace('*', '-').replace('/', '-')
        G_working_copy.nodes[id_of_number_to_yell]['value'] = 'x'

    done = False
    with alive_bar(G.number_of_nodes()-1) as bar:
        while not done:
            G_simplified = deepcopy(G_working_copy)
            for node, _ in G_working_copy.nodes.items():

                predecessor_count = 0
                for _ in nx.DiGraph.predecessors(G_working_copy, node):
                    predecessor_count += 1

                if predecessor_count == 0 and node != 'root':
                    # print('will be removed: '+node)

                    node_value = G_working_copy.nodes[node]['value']

                    # there should only be one successor
                    for successor in nx.DiGraph.successors(G_working_copy, node):
                        successor_value = G_working_copy.nodes[successor]['value']

                    if puzzle_part == 1:
                        replacement = successor_value.replace(node, str(eval(node_value)))
                    else:
                        node_value = node_value.replace(' ', '')
                        replacement = successor_value.replace(node, '('+node_value+')')

                    G_simplified.remove_node(node)
                    bar()
                    G_simplified.nodes[successor]['value'] = replacement
                G_working_copy = deepcopy(G_simplified)
                if G_simplified.number_of_nodes() == 1:
                    done = True

    return G_simplified


G = nx.DiGraph()

known_values = dict()
unknown_values = dict()

with open('day_21_input.txt') as file:
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

G_simplified_puzzle_part_1 = simplify_tree(G, 1)
solution_part_1 = eval(G_simplified_puzzle_part_1.nodes['root']['value'])
G_simplified_puzzle_part_1.nodes['root']['value'] = solution_part_1
pprint(G_simplified_puzzle_part_1.nodes)


G_simplified_puzzle_part_2 = simplify_tree(G, 2, 'humn')
equation = G_simplified_puzzle_part_2.nodes['root']['value'].strip()
pprint(equation)
x = Symbol('x')
solution_part_2 = solve(equation, x)
pprint(G_simplified_puzzle_part_2.nodes)

print('solution to part 1: '+str(solution_part_1))
print('solution to part 2: '+str(solution_part_2))

fig, axs = plt.subplots(ncols=3)
plt.margins(0.0)
draw_tree(G, axs, 0)
draw_tree(G_simplified_puzzle_part_1, axs, 1)
draw_tree(G_simplified_puzzle_part_2, axs, 2)
fig.tight_layout()

plt.show()
