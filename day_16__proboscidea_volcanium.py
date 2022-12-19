import sys
from collections import defaultdict
from copy import deepcopy
from pprint import pprint


def qpprint(object):
    if True:
        pprint(object)


def qprint(string: str = '', end=''):
    if False:
        print(string, end)


def get_total_pressure(time: int, open_valves: dict[str, int]) -> int:
    total_pressure = 0
    for time_step in range(time+1):
        for valve, open_since in open_valves.items():
            if time_step > open_since:
                total_pressure += valves[valve].flow_rate
    return total_pressure


def simulate_path(time: int, path: list[str], idx: int, open_valves: dict()):
    current_valve = path[idx]
    qprint(f"== Minute {time+1} | {current_valve} ==")
    currently_open_valves = []
    total_pressure_per_time_step = 0
    for valve_name, open_since in open_valves.items():
        if open_since < time:
            currently_open_valves.append(valve_name)
            total_pressure_per_time_step += valves[valve_name].flow_rate

    time += 1

    currently_open_valves = []
    total_pressure_per_time_step = 0

    for valve_name, open_since in open_valves.items():
        if open_since < time:
            currently_open_valves.append(valve_name)
            total_pressure_per_time_step += valves[valve_name].flow_rate

    number_of_open_valves = len(currently_open_valves)
    if number_of_open_valves == 0:
        qprint('No valves are open')
    elif number_of_open_valves == 1:
        qprint('Valve '+currently_open_valves[0]+' is open', end='')
    elif number_of_open_valves > 1:
        valve_string = ', '.join(sorted(currently_open_valves))
        qprint(f"Valves {valve_string} are open", end='')
    if number_of_open_valves > 0:
        qprint(f", releasing {total_pressure_per_time_step} pressure.")

    for valve_name, open_since in open_valves.items():
        if open_since == time:
            qprint(f"You open valve {valve_name}")

    if idx+1 < len(path):
        if current_valve != path[idx+1]:
            qprint('You move to valve '+path[idx+1]+'.')
        qprint()

        idx += 1
        simulate_path(time, path, idx, open_valves)


def find_optimal_path(time: int, max_time: int, current_valve: str, path: list[str], total_pressure: int, open_valve, open_valves) -> tuple[list[str], list[str]]:
    if time <= max_time:
        qprint()
        time += 1
        indent = ''
        for _ in range(time-1):
            indent += '\t'

        possible_path = deepcopy(path)
        possible_path.append(current_valve)
        qprint(indent+f"path so far: {possible_path}")

        qprint(indent+"time: "+str(time))
        qprint(indent+f"find_optimal_path({current_valve}, {open_valve})")

        max_open_valves = deepcopy(open_valves)
        if open_valve:
            max_open_valves[current_valve] = time
        qprint(indent+f"open valves: {open_valves}")

        total_pressure = get_total_pressure(max_time, open_valves)
        qprint(indent+'pressure so far: '+str(total_pressure))

        defaultdict(dict)
        pot_paths = defaultdict(dict)
        pot_open_valves = defaultdict(dict)

        possible_tunnels = deepcopy(valves[current_valve].tunnels)
        possible_tunnels.append(current_valve)
        possible_tunnels = sorted(possible_tunnels)

        better_path_found = False
        if time < max_time:
            qprint(indent+f"potential next steps: {possible_tunnels}")

            potential_next_valve_names = []
            max_pressure = 0
            for pot_next_valve_name in possible_tunnels:
                for potential_open_valve in [0, 1]:
                    if (potential_open_valve and pot_next_valve_name not in open_valves.keys() and pot_next_valve_name == current_valve and valves[pot_next_valve_name].flow_rate > 0) or \
                            (not potential_open_valve):
                        potential_next_valve_names.append(pot_next_valve_name)
                        pot_paths[pot_next_valve_name][potential_open_valve], \
                            pot_open_valves[pot_next_valve_name][potential_open_valve] = \
                            find_optimal_path(time, max_time, pot_next_valve_name, possible_path, total_pressure, potential_open_valve, max_open_valves)

                        qprint()
                        qprint(indent+f"open valves so far: {pot_open_valves[pot_next_valve_name][potential_open_valve]}")
                        total_pressure = get_total_pressure(max_time, pot_open_valves[pot_next_valve_name][potential_open_valve])
                        qprint(indent+'pressure so far: '+str(total_pressure))

                        if total_pressure >= max_pressure:
                            max_pressure = total_pressure
                            possible_max_open_valves = deepcopy(pot_open_valves[pot_next_valve_name][potential_open_valve])
                            possible_path_next_path = deepcopy(pot_paths[pot_next_valve_name][potential_open_valve])
                            better_path_found = True

    elif time == max_time:
        pass

    if better_path_found:
        pprint(possible_path_next_path, width=sys.maxsize, compact=True)
        qprint(indent+'better path found')
        qprint(indent+f"returning {possible_path_next_path}")
        qprint(indent+f"returning {possible_max_open_valves}")
        return deepcopy(possible_path_next_path), deepcopy(possible_max_open_valves)
    else:
        pprint(possible_path, width=sys.maxsize, compact=True)
        qprint(indent+f"returning {possible_path}")
        qprint(indent+f"returning {max_open_valves}")
        return deepcopy(possible_path), deepcopy(max_open_valves)


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

        # qpprint(name)
        # qpprint(flow_rate)
        # qpprint(tunnels)
        valves[name] = Valve(name, flow_rate, tunnels)

        if not first_valve_found:
            first_valve = name
            first_valve_found = True


if True:
    # example
    path_example = ['AA', 'DD', 'DD', 'CC', 'BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'FF', 'EE', 'EE', 'DD', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC']
    open_valves_example = {'DD': 2, 'BB': 5, 'JJ': 9, 'HH': 17, 'EE': 21, 'CC': 24}
    # simulate_path(0, path_example, 0, open_valves_example)
    total_pressure = get_total_pressure(30, open_valves_example)
    pprint(total_pressure)
    assert total_pressure == 1651

    print('==========================================================================================')

if True:
    # unit test
    pprint(valves)
    path_result, open_valves = find_optimal_path(0, 1, first_valve, [], 0, 0, dict())
    total_pressure = get_total_pressure(1, open_valves)
    pprint(total_pressure)
    pprint(path_result)
    pprint(open_valves)
    assert total_pressure == 0

    print('==========================================================================================')

if True:
    open_valves = {'DD': 3}
    pprint(get_total_pressure(4, open_valves))

    print('==========================================================================================')

if True:
    path_input = []
    path_result, open_valves = find_optimal_path(0, 4, first_valve, path_input, 0, 0, dict())
    pprint(open_valves)
    pprint(path_result)
    total_pressure = get_total_pressure(4, open_valves)
    pprint(total_pressure)
    assert total_pressure == 20
    path_expected = ['AA', 'DD', 'DD']
    for idx in range(len(path_expected)):
        path_result[idx] == path_expected[idx]

    print('==========================================================================================')

if True:
    path_input = []
    path_result, open_valves = find_optimal_path(0, 6, first_valve, path_input, 0, 0, dict())
    if True:
        pprint(open_valves)
        pprint(path_result)
        total_pressure = get_total_pressure(6, open_valves)
        pprint(total_pressure)
        assert total_pressure == 63
        path_expected = ['AA', 'DD', 'DD', 'EE', 'EE']
        for idx in range(len(path_expected)):
            path_result[idx] == path_expected[idx]

    print('==========================================================================================')


# actual input
if True:
    qpprint(valves)
    path, open_valves = find_optimal_path(0, 30, first_valve, [], 0, 0, dict())
    pprint(path)
    pprint(open_valves)
    total_pressure = get_total_pressure(4, open_valves)
    pprint(total_pressure)
    #simulate_path(0, path, 0, open_valves)
