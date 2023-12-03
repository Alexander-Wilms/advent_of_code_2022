import math
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
from alive_progress import alive_bar

# sys.setrecursionlimit(10**6)


def sign(x):
    return x / abs(x)


def get_nth_successor(G: nx.DiGraph, node: int, n: int) -> int:
    n = n % G.number_of_nodes()
    if n == 0:
        # print(f"-> {node}")
        return node
    else:
        successors = []
        for idx in range(n):
            successor_count = 0
            for successor in G.successors(node):
                successor_count += 1
            if successor_count == 0:
                raise ValueError
            successors.append(successor)
            node = successor
        return successors[-1]


def get_nth_predecessor(G: nx.DiGraph, node: int, n: int) -> int:
    n = n % G.number_of_nodes()
    if n == 0:
        # print(f"-> {node}")
        return node
    else:
        predecessors = []
        for idx in range(n):
            predecessor_count = 0
            for predecessor in G.predecessors(node):
                predecessor_count += 1
            if predecessor_count == 0:
                raise ValueError
            predecessors.append(predecessor)
            node = predecessor
        return predecessors[-1]


def print_sequence(G: nx.DiGraph, first: int):
    G.number_of_nodes()
    node = first
    node_value = G.nodes[node]["value"]
    node_sequence = []
    for successor in G.successors(node):
        pass
    node_sequence.append(f"({node}: {node_value:>2})")
    for _ in range(G.number_of_nodes() - 1):
        node_value = G.nodes[successor]["value"]
        node = get_nth_successor(G, node, 1)
        node_sequence.append(f"({node}: {node_value:>2})")
        for successor in G.successors(node):
            pass
    pprint(node_sequence)


def get_grove_coordinates(G: nx.DiGraph, idx_of_zero: int) -> int:
    G.number_of_nodes()
    summands = []
    for coordinte_factor_idx_offset in [1000, 2000, 3000]:
        summand = G.nodes[
            get_nth_successor(G, idx_of_zero, coordinte_factor_idx_offset)
        ]["value"]
        summands.append(summand)
    pprint(summands)
    return sum(summands)


sequence = []
sequence_pointers = dict()

G = nx.DiGraph()

enable_first_visualization = False
enable_visualization = False

line_idx = 0
with open("day_20_example.txt") as file:
    for line in file:
        # print(line.strip())
        number = int(line.strip())
        if number == 0:
            idx_of_zero = line_idx
        G.add_node(line_idx, value=number)
        sequence.append(number)
        sequence_pointers[line_idx] = number
        line_idx += 1

node_labels = dict()
for node, node_data in G.nodes.items():
    node_labels[node] = str(node) + ": " + str(node_data["value"])
    G.add_edge(node, (node + 1 + len(sequence)) % len(sequence))

for node, _ in G.nodes.items():
    if not G.has_predecessor(node, (node - 1 + len(sequence)) % len(sequence)):
        print(f"node {node} has no predecessor")
        input()

if enable_visualization or enable_first_visualization:
    dim = math.ceil(math.sqrt(len(sequence)))
    fig, axs = plt.subplots(dim, dim)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.margins(0.0)
    fig.tight_layout()
    axs = axs.ravel()

    pos = nx.circular_layout(G)
    rad = 0.25

    nx.draw(
        G,
        pos,
        labels=node_labels,
        node_color="w",
        edgecolors="black",
        node_size=1100,
        ax=axs[0],
    )
    plt.show(block=False)

print("Initial arrangement:")
print_sequence(G, 0)

with alive_bar(len(sequence)) as bar:
    for idx in range(len(sequence)):
        if enable_visualization:
            plt.pause(1)
        current_number = G.nodes[idx]["value"]

        if current_number != 0:
            idx_prev = get_nth_predecessor(G, idx, 1)
            idx_next = get_nth_successor(G, idx, 1)

            if current_number > 0:
                idx_next_after_mixing = get_nth_successor(G, idx, current_number + 1)
                for idx_prev_after_mixing in G.predecessors(idx_next_after_mixing):
                    pass
            elif current_number < 0:
                idx_next_after_mixing = get_nth_predecessor(G, idx, abs(current_number))
                for idx_prev_after_mixing in G.predecessors(idx_next_after_mixing):
                    pass

            # print(f"({idx}: {current_number}) moves from between ({idx_prev}: {G.nodes[idx_prev]['value']}) and ({idx_next}: {G.nodes[idx_next]['value']}) to between ({idx_prev_after_mixing}: {G.nodes[idx_prev_after_mixing]['value']}) and ({idx_next_after_mixing}: {G.nodes[idx_next_after_mixing]['value']})")

            G.remove_edge(idx_prev_after_mixing, idx_next_after_mixing)

            G.remove_edge(idx_prev, idx)
            G.remove_edge(idx, idx_next)

            G.add_edge(idx_prev, idx_next)

            G.add_edge(idx_prev_after_mixing, idx)
            G.add_edge(idx, idx_next_after_mixing)

            pos = nx.circular_layout(G)
        if enable_visualization:
            # plt.clf()
            # plt.title('Iteration {}'.format(idx))
            nx.draw(
                G,
                pos,
                labels=node_labels,
                node_color="w",
                edgecolors="black",
                node_size=1100,
                ax=axs[idx + 1],
            )
            plt.show(block=False)
            # input()
            fig.tight_layout()

        # print_sequence(G, idx)
        bar()

print_sequence(G, 0)

# 17042 is too high
print(f"solution to part 1: {get_grove_coordinates(G, idx_of_zero)}")

if enable_visualization:
    plt.show()
