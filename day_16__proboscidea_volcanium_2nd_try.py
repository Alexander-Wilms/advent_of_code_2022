import itertools as it
import timeit
from copy import deepcopy
from math import factorial
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from alive_progress import alive_it

seed = 42
np.random.seed(seed)


class Valve():
    def __init__(self, name: str, flow_rate: int, tunnels: list[str]):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.tunnels: list[str] = tunnels

    def __repr__(self) -> str:
        string = self.name+'; '+str(self.flow_rate).rjust(2)+';'
        for tunnel in self.tunnels:
            string += ' '+tunnel
        return string


def get_total_pressure(time: int, open_valves: dict[str, int]) -> int:
    total_pressure = 0
    for time_step in range(time+1):
        for open_since, valve in open_valves.items():
            if time_step > open_since:
                total_pressure += valves[valve].flow_rate
    return total_pressure


def create_graph(valves: dict[str, Valve]) -> nx.Graph:
    G = nx.Graph()
    for valve_name, valve in valves.items():
        G.add_node(valve_name, weight=valve.flow_rate)
        for connected_valve in valve.tunnels:
            G.add_edge(valve_name, connected_valve, weight=1)
    return G


def print_graph(G: nx.Graph, ax):
    # https://www.python-graph-gallery.com/322-network-layout-possibilities
    #pos = nx.fruchterman_reingold_layout(G, seed=seed, iterations=1000)
    pos = nx.spring_layout(G, iterations=1000)
    ax.set_axis_off()
    node_names = []
    for node, _ in G.nodes.items():
        node_names.append(node)
    node_weights = nx.get_node_attributes(G, "weight")
    node_labels = dict()
    for node in node_names:
        node_labels[node] = str(node)+': '+str(node_weights[node])
    pprint(node_weights)
    pprint(node_labels)
    node_colors = [G.nodes[n]['weight'] for n in G.nodes]
    pprint(node_colors)
    nx.draw(G, pos=pos, with_labels=True, labels=node_labels, node_color=node_colors, cmap=plt.cm.gray, vmin=-max(node_colors), ax=ax, node_shape='s', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, ax=ax)


def collapse_graph(G: nx.Graph, first_valve: str) -> nx.Graph:
    C = deepcopy(G)
    # https://stackoverflow.com/a/56933420/2278742
    for node, node_data in G.nodes.items():
        if node is not first_valve:
            if node_data['weight'] == 0:
                for edge in it.product(C.neighbors(node), C.neighbors(node)):
                    if edge[0] is not edge[1]:
                        edge_weight_from = C.get_edge_data(edge[0], node)['weight']
                        edge_weight_to = C.get_edge_data(edge[1], node)['weight']
                        edge_weight_sum = edge_weight_from+edge_weight_to
                        print(f"replacing {node} with edge from {edge[0]} to {edge[1]} of weight {edge_weight_from}+{edge_weight_to}={edge_weight_sum}")
                        C.add_edge(edge[0], edge[1], weight=edge_weight_from+edge_weight_to)
                C.remove_node(node)
    return C


def determine_potential_pressures(valves: nx.Graph, current_valve, remaining_time, opened_valves: dict[int, str]) -> dict[str, int]:
    potential_pressures = dict()
    for node, node_data in valves.nodes.items():
        if node not in opened_valves.values():
            cheapest_path = nx.dijkstra_path(valves, source=current_valve, target=node)
            path_cost = nx.path_weight(valves, cheapest_path, 'weight')+1
            potential_pressure = max(0, node_data['weight']*(remaining_time-path_cost))
            potential_pressures[potential_pressure] = node
    return potential_pressures


def find_path_recursive(valves: nx.Graph, source_valve, number_of_candidates, time, opened_valves) -> list[str]:
    opened_valves = deepcopy(opened_valves)
    opened_valves[time] = source_valve
    indent = ''
    for _ in range(len(opened_valves)):
        indent += '    '
    print(indent+f"find_path_recursive({source_valve}, {opened_valves})")
    #opened_valves = deepcopy(opened_valves)

    potential_pressures = determine_potential_pressures(valves, source_valve, 30-time, opened_valves)
    ranked_candidates = sorted(potential_pressures.keys(), reverse=True)
    print(indent+f"{potential_pressures}")
    candidate_count = 0
    potential_pressures_of_next = dict()
    while candidate_count < number_of_candidates:
        potential_next_valve = potential_pressures[ranked_candidates[candidate_count]]
        print(indent+f"potential next valve: {potential_next_valve}")
        if potential_next_valve not in opened_valves and potential_next_valve is not source_valve:
            potential_pressures_of_next[find_path_recursive(valves, potential_next_valve, number_of_candidates, time, opened_valves)] = potential_next_valve
        candidate_count += 1
    print(indent+f"{potential_pressures_of_next}")
    pprint(ranked_candidates)
    return potential_pressures


def find_path(valves: nx.Graph, current_valve, number_of_candidates, time, opened_valves):
    for valve in valves:
        determine_potential_pressures(valves, current_valve, 2, time, opened_valves)


def compute(valves, starting_node, is_collapsed: bool):
    useful_valve_names = []
    for node, node_data in valves.nodes.items():
        if node_data['weight'] > 0:
            useful_valve_names.append(node)

    useful_valve_names = sorted(useful_valve_names)

    # useful_valve_names.remove(starting_node)

    # pprint(useful_valve_names)

    number_of_usefule_valves = len(useful_valve_names)
    number_of_permutations = factorial(number_of_usefule_valves)

    # pprint(number_of_permutations)

    # https://stackoverflow.com/questions/6503388/prevent-memory-error-in-itertools-permutation
    permutations = it.permutations(useful_valve_names)
    # print(len(permutations))
    # pprint(permutations)

    # with alive_it(permutations_iterator, dual_line=False, title='Calculating possible permutations') as bar:
    # pprint(useful_valves)
    max_time = 30

    possible_solutions = []
    count = 0
    for permutation in alive_it(permutations, total=number_of_permutations):
        #pprint(permutation)
        #print(f"{count/number_of_permutations*100:.0f} %")
        count += 1
        # pprint(permutation)
        possible_solution = dict()
        time = 0
        for idx in range(-1, number_of_usefule_valves-1):
            if idx == -1:
                source = starting_node
                target = permutation[0]
            else:
                source = permutation[idx]
                target = permutation[idx+1]

            # pprint(determine_potential_pressures(valves, source, max_time-time))

            if is_collapsed:
                # collapsed graph has weighted edges, so we need dijkstra
                cheapest_path = nx.dijkstra_path(valves, source=source, target=target)
                path_cost = nx.path_weight(valves, cheapest_path, 'weight')+1
            else:
                try:
                    cheapest_path = nx.shortest_path(useful_valves, source=source, target=target)
                    path_cost = len(cheapest_path)+2
                except:
                    cheapest_path = nx.shortest_path(valves, source=source, target=target)
                    path_cost = len(cheapest_path)
            #print(f"cheapest path from {source} to {target} is {cheapest_path} with a cost of {path_cost}")
            # pprint(shortest_path)
            # add 1 because it takes 1 minute to open the valve
            time += path_cost
            if time <= max_time:
                possible_solution[time] = target
        possible_solutions.append(possible_solution)
        # pprint(possible_solution)
        # print()

    return possible_solutions


start = timeit.default_timer()
input_file = 'day_16_example.txt'

valves = dict()
first_valve_found = False
with open(input_file) as file:
    for line in file:
        line = line.strip()
        # qprint(line)
        line_elements = line.split()
        name = line_elements[1]
        flow_rate = int(line_elements[4].split('=')[1][:-1])
        tunnels = ''.join(line_elements[9:]).split(',')

        # pprint(name)
        # pprint(flow_rate)
        # pprint(tunnels)
        valves[name] = Valve(name, flow_rate, tunnels)

        if not first_valve_found:
            first_valve = name
            first_valve_found = True

if input_file == 'day_16_example.txt':
    # test of get_total_pressure()
    path_example = ['AA', 'DD', 'DD', 'CC', 'BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'FF', 'EE', 'EE', 'DD', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC']
    open_valves_example = {2: 'DD', 5: 'BB', 9: 'JJ', 17: 'HH', 21: 'EE', 24: 'CC'}
    # simulate_path(0, path_example, 0, open_valves_example)
    total_pressure = get_total_pressure(30, open_valves_example)
    # pprint(total_pressure)
    assert total_pressure == 1651

# determine max pressure
useful_valves = dict()
for valve_name, valve in valves.items():
    # print(valve)
    if valve.flow_rate > 0:
        useful_valves[valve_name] = valve

graph = create_graph(valves)

fig, axs = plt.subplots(ncols=2)
graph_collapsed = collapse_graph(graph, first_valve)
print_graph(graph, axs[0])
print_graph(graph_collapsed, axs[1])

is_collapsed = 1
if is_collapsed:
    graph_to_analyze = graph_collapsed
else:
    graph_to_analyze = graph

plt.margins(0.0)
fig.tight_layout()
plt.show(block=False)

#find_path_recursive(graph_collapsed, first_valve, 2, 0, dict())
#find_path(valves, first_valve, 2, 0, [])
possible_solutions = compute(graph_to_analyze, first_valve, is_collapsed)

max_possible_pressure = 0
solution_for_max_possible_pressure = dict()
for possible_solution in possible_solutions:
    total_pressure = get_total_pressure(30, possible_solution)
    if total_pressure > max_possible_pressure:
        max_possible_pressure = total_pressure
        solution_for_max_possible_pressure = possible_solution

pprint(solution_for_max_possible_pressure)
print(f"solution to part 1: {max_possible_pressure}")
stop = timeit.default_timer()
print('time: ', stop - start)

plt.show()
