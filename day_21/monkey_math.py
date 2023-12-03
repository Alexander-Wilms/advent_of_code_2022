import os
import re
from copy import deepcopy
from pprint import pprint
from types import NoneType

import matplotlib.pyplot as plt
import networkx as nx
from alive_progress import alive_bar
from networkx.drawing.nx_agraph import graphviz_layout
from sympy import Symbol
from sympy.solvers import solve
import netgraph as ng


def draw_tree(G, axs, fig_idx):
    node_names = []
    for node, _ in G.nodes.items():
        node_names.append(node)
    node_weights = nx.get_node_attributes(G, "value")
    node_labels = dict()
    for node_name in node_names:
        node_labels[node_name] = str(node_name) + ": " + str(node_weights[node_name])
    # https://stackoverflow.com/a/57512902/2278742
    pos = graphviz_layout(G, prog="dot")
    nx.draw(
        G,
        pos=pos,
        with_labels=True,
        node_color="w",
        edge_color="b",
        labels=node_labels,
        node_shape="s",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.2"),
        ax=axs[fig_idx],
    )
    axs[fig_idx].collections[0].set_edgecolor("#000000")


def simplify_tree(G: nx.DiGraph, id_of_number_to_yell="") -> nx.DiGraph:
    G_working_copy = deepcopy(G)
    G_simplified = nx.DiGraph()

    G_working_copy.nodes["root"]["value"] = (
        G_working_copy.nodes["root"]["value"]
        .replace("+", "$")
        .replace("*", "$")
        .replace("/", "$")
    )
    G_working_copy.nodes[id_of_number_to_yell]["value"] = "x"

    done = False
    with alive_bar(G.number_of_nodes() - 1) as bar:
        while not done:
            G_simplified = deepcopy(G_working_copy)
            for node, _ in G_working_copy.nodes.items():
                predecessor_count = 0
                for _ in nx.DiGraph.predecessors(G_working_copy, node):
                    predecessor_count += 1

                if predecessor_count == 0 and node != "root":
                    # print('will be removed: '+node)

                    node_value = G_working_copy.nodes[node]["value"]

                    # there should only be one successor
                    for successor in nx.DiGraph.successors(G_working_copy, node):
                        successor_value = G_working_copy.nodes[successor]["value"]

                    replacement = successor_value.replace(node, "(" + node_value + ")")

                    G_simplified.remove_node(node)
                    bar()
                    G_simplified.nodes[successor]["value"] = replacement
                G_working_copy = deepcopy(G_simplified)
                if G_simplified.number_of_nodes() == 1:
                    done = True

    return G_simplified


def get_solution(G: nx.DiGraph) -> tuple[nx.DiGraph, int, int]:
    variable_part_2 = "humn"
    G_simplified = simplify_tree(G, variable_part_2)
    equation = G_simplified.nodes["root"]["value"]
    solution_part_1 = eval(
        equation.replace("$", "+").replace("x", G.nodes[variable_part_2]["value"])
    )
    solution_part_2 = solve(equation.replace("$", "-"), Symbol("x"))[0]
    G_simplified.nodes["root"]["value"] = f"{solution_part_1}\n{solution_part_2}"
    pprint(G_simplified.nodes)
    print("solution to part 1: " + str(solution_part_1))
    print("solution to part 2: " + str(solution_part_2))
    return G_simplified, solution_part_1, solution_part_2


def get_solutions(input_file) -> tuple[int]:
    G = nx.DiGraph()

    known_values = dict()
    unknown_values = dict()

    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        for line in file:
            line_stripped = line.strip()
            # print(line_stripped)
            elements = line_stripped.split(":")
            # pprint(elements)
            monkey = elements[0]
            # print(monkey)
            G.add_node(monkey, value=elements[1])
            right_side = re.search(r"\d+", elements[1])
            if isinstance(right_side, NoneType):
                calculation = elements[1].replace(" ", "")
                unknown_values[monkey] = calculation
                connected_nodes = re.split(r"\+|-|\*|/", calculation)
                G.add_edge(connected_nodes[0], monkey)
                G.add_edge(connected_nodes[1], monkey)
            else:
                value = int(right_side.group(0))
                known_values[monkey] = value
                # print(str(value))

    pprint(known_values)
    pprint(unknown_values)

    G_simplified, solution_part_1, solution_part_2 = get_solution(G)

    fig, axs = plt.subplots(ncols=2)

    # netgraph requires patch to work with only a single node:
    # https://github.com/paulbrodersen/netgraph/issues/33#issuecomment-1367006179
    netgraph = False
    if netgraph:
        ng.Graph(
            G,
            ax=axs[0],
            node_labels=True,
            node_layout="dot",
            node_label_fontdict={"size": 12},
        )
        ng.Graph(G_simplified, ax=axs[1], node_labels=True)
    else:
        plt.margins(0.0)
        draw_tree(G, axs, 0)
        draw_tree(G_simplified, axs, 1)
        fig.tight_layout()

    plt.show(block=True)

    return solution_part_1, solution_part_2


get_solutions("input.txt")
