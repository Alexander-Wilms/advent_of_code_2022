"""Commenting out the print() and pprint() staments speeds up the code significantly.
E.g. the solution to part 2 can be computed in 6 seconds"""
from copy import deepcopy
from datetime import datetime

import numpy as np


def create_sim(rocks: list[list[int]], puzzle_part: int) -> tuple[np.ndarray, int]:
    columns = []
    rows = []
    for rock in rocks:
        for point in rock:
            columns.append(point[0])
            rows.append(point[1])

    max_col = max(columns)
    min_col = min(columns)
    max_row = max(rows)

    if puzzle_part == 2:
        max_row += 2
        min_col -= max_row
        max_col += max_row
        # add floor for visualization
        rocks.append([[min_col, max_row], [max_col, max_row]])

    number_of_columns = max_col-min_col+1

    # pprint(rocks)

    filled_rocks = fill_lines(rocks)

    sim = np.ndarray((max_row+1, number_of_columns), dtype=np.object_)

    sim[:] = '.'

    for rock in filled_rocks:
        for point in rock:
            # pprint(point)
            sim[point[1], col_to_idx(point[0], min_col)] = '#'

    return sim, min_col


def col_to_idx(col: int, first_col: int) -> int:
    return col-first_col


def show_sim(sim: np.ndarray, first_col: int):
    dimensions = sim.shape

    start_drawing_at_row = 0
    stop_drawing_at_row = 999

    col_str_list = []
    col_str_lengths = []
    for col in range(first_col, first_col+dimensions[1]):
        col_str = str(col)
        col_str_list.append(col_str)
        col_str_lengths.append(len(col_str))

    indent = ''
    for _ in range(len(str(dimensions[0]))):
        indent += ' '

    for row in range(max(col_str_lengths)):
        # print(indent, end=' ')
        for col in range(dimensions[1]):
            if row < len(col_str_list[col]):
                # print(col_str_list[col][row]+' ', end='')
                # print()
                pass

    for row in range(start_drawing_at_row, min(dimensions[0], stop_drawing_at_row)):
        # print(str(row).rjust(len(str(dimensions[0]))), end=' ')
        for col in range(dimensions[1]):
            # print(sim[row, col], end=' ')
            # print()
            pass


def time_step(sim: np.ndarray, min_col: int, active_sand_coord: tuple[int], spawn_point: list[int], puzzle_part: int) -> tuple[np.ndarray, bool, tuple[int], bool, bool]:
    if show_sim_toggle:
        # os.system('clear')
        show_sim(sim, min_col)

    # print()
    dim = sim.shape
    active_sand_found = False
    spawn_point_reached = False

    vector = [1, 0]

    # print(f"{active_sand_coord=}")

    in_steady_state = False

    # print(f"{spawn_point=}")

    # check if active grain of sand has come to a halt
    if active_sand_coord[0]+1 < dim[0]:

        if sim[active_sand_coord[0]+1, active_sand_coord[1]] == '.':
            # check if cell below is free
            # print('sand can fall freely')
            active_sand_found = True
            free_fall_height = 0
            for cell in range(active_sand_coord[0]+1, dim[0]):
                if sim[cell, active_sand_coord[1]] == '.':
                    free_fall_height += 1
                else:
                    break
            vector = [free_fall_height, 0]
        # check if cell below is not free
        else:

            fell_to_the_left = False
            if active_sand_coord[1]-1 >= 0:
                if (sim[active_sand_coord[0]+1, active_sand_coord[1]-1] == '.'):
                    active_sand_found = True
                    fell_to_the_left = True
                    vector = [1, -1]
                    # print('sand can fall to the left')
            else:
                active_sand_found = False
                sim[active_sand_coord[0], active_sand_coord[1]] = '.'
                in_steady_state = True

            fell_to_the_right = False
            if not fell_to_the_left:
                if active_sand_coord[1]+1 <= dim[1]:
                    if active_sand_coord[0]+1 < sim.shape[0] and active_sand_coord[1]+1 < sim.shape[1]:
                        if sim[active_sand_coord[0]+1, active_sand_coord[1]+1] == '.':
                            active_sand_found = True
                            fell_to_the_right = True
                            vector = [1, 1]
                            # print('sand can fall to the right')

            if not fell_to_the_left and not fell_to_the_right:
                # print('sand cant fall to the left or right')
                # sand would leave sim
                active_sand_found = False
                vector = [0, 0]
    else:
        active_sand_found = True
        sim[active_sand_coord[0], active_sand_coord[1]] = '.'

    # spawn a new grain if previous one has come to a halt
    if not active_sand_found:
        if not in_steady_state:
            # print('spawn new sand')
            # print()
            sim[spawn_point[0], spawn_point[1]] = 'o'
            active_sand_coord = [spawn_point[0], spawn_point[1]]
            active_sand_found = True

            if puzzle_part == 2:
                if spawn_point == default_spawn_point:
                    if (sim[default_spawn_point[0], default_spawn_point[1]] != '.') and \
                        (sim[default_spawn_point[0]+1, default_spawn_point[1]-1]) != '.' and \
                        (sim[default_spawn_point[0]+1, default_spawn_point[1]]) != '.' and \
                            (sim[default_spawn_point[0]+1, default_spawn_point[1]+1]) != '.':
                        spawn_point_reached = True
                        # print('spawn point reached')
                        return sim, active_sand_found, active_sand_coord, in_steady_state, spawn_point_reached
    else:
        # simulate current grain
        sim[active_sand_coord[0], active_sand_coord[1]] = '.'
        new_coords = [active_sand_coord[0]+vector[0], active_sand_coord[1]+vector[1]]
        # print(f"grain 'x' is falling to coord [{new_coords[0]}, {new_coords[1]}]")
        if new_coords[0] >= dim[0] and puzzle_part == 1:
            # print('sand grain leaves sim')
            in_steady_state = True
            return sim, active_sand_found, active_sand_coord, in_steady_state, spawn_point_reached
        sim[new_coords[0], new_coords[1]] = 'o'
        active_sand_coord = [new_coords[0], new_coords[1]]

    return sim, active_sand_found, active_sand_coord, in_steady_state, spawn_point_reached


def count_grains(sim: np.ndarray) -> int:
    grain_count = 0
    for row in range(sim.shape[0]):
        for col in range(sim.shape[1]):
            if sim[row, col] == 'o' or sim[row, col] == 'x':
                grain_count += 1
    return grain_count


def fill_lines(rocks: list[list[int]]) -> list[list[int]]:
    filled_rocks = []
    for rock in rocks:
        filled_rock = []
        for point_idx in range(len(rock)-1):

            point = rock[point_idx]
            next_point = rock[point_idx+1]
            if point[0] == next_point[0]:
                vertical = True
                constant_coordinate = point[0]
                first_coordinate = point[1]
                last_coordinate = next_point[1]
            else:
                vertical = False
                constant_coordinate = point[1]
                last_coordinate = point[0]
                first_coordinate = next_point[0]

            filled_rock.append(point)
            if first_coordinate <= last_coordinate:
                step = 1
            else:
                step = -1
            for filler_coordinate in range(first_coordinate, last_coordinate, step):
                if vertical:
                    filler_point = [constant_coordinate, filler_coordinate]
                else:
                    filler_point = [filler_coordinate, constant_coordinate]
                filled_rock.append(filler_point)

            filled_rock.append(next_point)
            # pprint(point)
        filled_rocks.append(filled_rock)
    return filled_rocks


start = datetime.now()
file_name = 'day_14_input.txt'
puzzle_part = 2
sim_not_finished = True
spawn_point_reached = False
show_sim_toggle = False

rocks = []

with open(file_name) as file:
    for line in file:
        stripped_line = line.strip()
        points = stripped_line.split('->')
        for idx in range(len(points)):
            points[idx] = points[idx].strip()
            points[idx] = points[idx].split(',')
            points[idx] = [int(points[idx][0]), int(points[idx][1])]
        rocks.append(points)

# pprint(rocks)
sim, min_col = create_sim(rocks, puzzle_part)
show_sim(sim, min_col)

default_spawn_point = [0, col_to_idx(500, min_col)]
spawn_point = deepcopy(default_spawn_point)
sim[spawn_point[0], spawn_point[1]] = 'o'
active_sand_coord = [spawn_point[0], spawn_point[1]]

while sim_not_finished:
    sim, sim_not_finished, active_sand_coord, in_steady_state, spawn_point_reached = time_step(sim, min_col, active_sand_coord, spawn_point, puzzle_part)
    if puzzle_part == 1 and in_steady_state:
        break
    if puzzle_part == 2 and spawn_point_reached:
        break

show_sim(sim, min_col)

print('solution to part '+str(puzzle_part)+': '+str(count_grains(sim)))
print("time: "+str(datetime.now()-start))
