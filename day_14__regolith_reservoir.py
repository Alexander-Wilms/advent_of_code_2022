from pprint import pprint
import numpy as np
import os


def create_sim(rocks: list[list[int]]) -> np.ndarray:
    columns = []
    rows = []
    for rock in rocks:
        for point in rock:
            columns.append(point[0])
            rows.append(point[1])

    max_col = max(columns)
    min_col = min(columns)
    max_row = max(rows)

    number_of_columns = max_col-min_col+1

    sim = np.ndarray((max_row+1, number_of_columns), dtype=np.object_)

    sim[:] = '.'

    pprint(sim)

    print_sim(sim, min_col)

    filled_rocks = fill_lines(rocks)
    pprint(filled_rocks)

    sim[0, col_to_idx(500, min_col)] = '+'

    for rock in filled_rocks:
        for point in rock:
            pprint(point)
            sim[point[1], col_to_idx(point[0], min_col)] = '#'

    print_sim(sim, min_col)

    return sim


def col_to_idx(col: int, first_col: int) -> int:
    return col-first_col


def print_sim(sim: np.ndarray, first_col: int):
    dimensions = sim.shape

    col_str_list = []
    col_str_lengths = []
    for col in range(first_col, first_col+dimensions[1]):
        col_str = str(col)
        col_str_list.append(col_str)
        col_str_lengths.append(len(col_str))

    for row in range(max(col_str_lengths)):
        print('  ', end='')
        for col in range(dimensions[1]):
            if row < len(col_str_list[col]):
                print(col_str_list[col][row]+' ', end='')
        print()

    for row in range(dimensions[0]):
        print(str(row), end=' ')
        for col in range(dimensions[1]):
            print(sim[row, col], end=' ')
        print()


def time_step(sim: np.ndarray, min_col: int, active_sand_coord: tuple[int]) -> tuple[np.ndarray, bool, tuple[int]]:
    os.system('clear')
    dim = sim.shape
    active_sand_found = False

    vector = [1, 0]

    # check if active grain of sand has come to a halt
    if active_sand_coord[0]+1 <= dim[0]:
        pprint(active_sand_coord)
        if sim[active_sand_coord[0], active_sand_coord[1]] == 'o' and sim[active_sand_coord[0]+1, active_sand_coord[1]] == '.':
            print('sand can fall')
            active_sand_found = True
            vector = [1, 0]
        elif sim[active_sand_coord[0], active_sand_coord[1]] == 'o' and sim[active_sand_coord[0]+1, active_sand_coord[1]] is not '.':
            if active_sand_coord[1]-1 >= 0:
                if sim[active_sand_coord[0]+1, active_sand_coord[1]-1] == '.':
                    active_sand_found = True
                    vector = [1, -1]
                elif active_sand_coord[1]+1 <= dim[1]:
                    if sim[active_sand_coord[0]+1, active_sand_coord[1]+1] == '.':
                        active_sand_found = True
                        vector = [1, +1]
        else:
            print('sand outside sim')
            return
    else:
        print('sand cannot fall')
        active_sand_found = False

    # spawn a new grain if previous one has come to a halt
    if not active_sand_found:
        print('spawn new sand')
        sim[1, col_to_idx(500, min_col)] = 'o'
        active_sand_coord = [1, col_to_idx(500, min_col)]
        active_sand_found = True
    else:
        # simulate current grain
        sim[active_sand_coord[0], active_sand_coord[1]] = '.'
        sim[active_sand_coord[0]+vector[0], active_sand_coord[1]+vector[1]] = 'o'
        active_sand_coord = [active_sand_coord[0]+vector[0], active_sand_coord[1]+vector[1]]

    return sim, active_sand_found, active_sand_coord


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
            for filler_coordinate in range(first_coordinate, last_coordinate):
                if vertical:
                    filler_point = [constant_coordinate, filler_coordinate]
                else:
                    filler_point = [filler_coordinate, constant_coordinate]
                filled_rock.append(filler_point)

            filled_rock.append(next_point)
            # pprint(point)
        filled_rocks.append(filled_rock)
    return filled_rocks


rocks = []
with open('day_14_input_example.txt') as file:
    for line in file:
        stripped_line = line.strip()
        points = stripped_line.split('->')
        for idx in range(len(points)):
            points[idx] = points[idx].strip()
            points[idx] = points[idx].split(',')
            points[idx] = [int(points[idx][0]), int(points[idx][1])]
        rocks.append(points)

pprint(rocks)
sim = create_sim(rocks)

sim_not_finished = True

min_col = 494

sim[1, col_to_idx(500, min_col)] = 'o'
active_sand_coord = [1, col_to_idx(500, min_col)]

while sim_not_finished:
    sim, sim_not_finished, active_sand_coord = time_step(sim, min_col, active_sand_coord)
    print_sim(sim, min_col)
