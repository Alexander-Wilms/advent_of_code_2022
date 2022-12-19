import itertools
from math import factorial
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx


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


valves = dict()
first_valve_found = False
with open('day_16_example.txt') as file:
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

# test of get_total_pressure()
path_example = ['AA', 'DD', 'DD', 'CC', 'BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'FF', 'EE', 'EE', 'DD', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC']
open_valves_example = {2: 'DD', 5: 'BB', 9: 'JJ', 17: 'HH', 21: 'EE', 24: 'CC'}
# simulate_path(0, path_example, 0, open_valves_example)
total_pressure = get_total_pressure(30, open_valves_example)
pprint(total_pressure)
assert total_pressure == 1651

# determine max pressure
useful_valves = dict()
for valve_name, valve in valves.items():
    print(valve)
    if valve.flow_rate > 0:
        useful_valves[valve_name] = valve

# pprint(useful_valves)
useful_valve_names = list(useful_valves.keys())
number_of_usefule_valves = len(useful_valve_names)
number_of_permutations = factorial(number_of_usefule_valves)

# pprint(number_of_permutations)

permutations = list(itertools.permutations(useful_valve_names))
print(len(permutations))
# pprint(permutations)


G = nx.Graph()
for valve_name, valve in valves.items():
    G.add_node(valve_name)
    for connected_valve in valve.tunnels:
        G.add_edge(valve_name, connected_valve)

nx.draw(G, with_labels=True)
plt.show(block=False)

#pprint(nx.shortest_path(G, source='BB', target='II'))

starting_node = 'AA'

possible_solutions = []
for permutation in permutations:
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
        shortest_path = nx.shortest_path(G, source=source, target=target)
        # pprint(shortest_path)
        # add 1 because it takes 1 minute to open the valve
        time += len(shortest_path)
        possible_solution[time] = target
    possible_solutions.append(possible_solution)
    # pprint(possible_solution)
    # print()

max_possible_pressure = 0
solution_for_max_possible_pressure = dict()
for possible_solution in possible_solutions:
    total_pressure = get_total_pressure(30, possible_solution)
    if total_pressure > max_possible_pressure:
        max_possible_pressure = total_pressure
        solution_for_max_possible_pressure = possible_solution

pprint(solution_for_max_possible_pressure)
print(f"solution to part 1: {max_possible_pressure}")
