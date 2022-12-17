from pprint import pprint
import numpy as np


def create_sim(rocks: list[list[int]]) -> tuple[np.ndarray, int]:
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

    filled_rocks = fill_lines(rocks)

    sim[0, col_to_idx(500, min_col)] = '+'

    for rock in filled_rocks:
        for point in rock:
            # pprint(point)
            sim[point[1], col_to_idx(point[0], min_col)] = '#'

    return sim, min_col


def col_to_idx(col: int, first_col: int) -> int:
    return col-first_col


def print_sim(sim: np.ndarray, first_col: int):
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
        print(indent, end=' ')
        for col in range(dimensions[1]):
            if row < len(col_str_list[col]):
                print(col_str_list[col][row]+' ', end='')
        print()

    for row in range(start_drawing_at_row, min(dimensions[0], stop_drawing_at_row)):
        print(str(row).rjust(len(str(dimensions[0]))), end=' ')
        for col in range(dimensions[1]):
            print(sim[row, col], end=' ')
        print()


def time_step(sim: np.ndarray, min_col: int, active_sand_coord: tuple[int], grain_count: int) -> tuple[np.ndarray, bool, tuple[int], int, bool]:
    # os.system('clear')

    # print_sim(sim, min_col)
    print()
    dim = sim.shape
    active_sand_found = False

    vector = [1, 0]

    print('grains of sand: '+str(grain_count))

    pprint(dim)
    pprint(active_sand_coord)

    in_steady_state = False

    # check if active grain of sand has come to a halt
    if active_sand_coord[0]+1 < dim[0]:
        # check if cell below is free
        if sim[active_sand_coord[0], active_sand_coord[1]] == 'o' and sim[active_sand_coord[0]+1, active_sand_coord[1]] == '.':
            print('sand can fall freely')
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
                if sim[active_sand_coord[0]+1, active_sand_coord[1]-1] == '.':
                    print('sand can fall to the left')
                    active_sand_found = True
                    vector = [1, -1]
                    fell_to_the_left = True
            else:
                active_sand_found = False
                sim[active_sand_coord[0], active_sand_coord[1]] = '.'
                grain_count -= 1
                in_steady_state = True

            fell_to_the_right = False
            if not fell_to_the_left:
                if active_sand_coord[1]+1 <= dim[1]:
                    if sim[active_sand_coord[0]+1, active_sand_coord[1]+1] == '.':
                        print('sand can fall to the right')
                        active_sand_found = True
                        vector = [1, +1]
                        fell_to_the_right = True

            if not fell_to_the_left and not fell_to_the_right:
                print('sand cant fall to the left or right')
                # sand would leave sim
                active_sand_found = False
                vector = [0, 0]
    else:
        active_sand_found = True
        sim[active_sand_coord[0], active_sand_coord[1]] = '.'

    # spawn a new grain if previous one has come to a halt
    if not active_sand_found:
        if not in_steady_state:
            print('spawn new sand')
            print()
            sim[1, col_to_idx(500, min_col)] = 'o'
            active_sand_coord = [1, col_to_idx(500, min_col)]
            active_sand_found = True
            grain_count += 1
        else:
            # so the diagram doesn't jump around-2
            print()
    else:
        # simulate current grain
        sim[active_sand_coord[0], active_sand_coord[1]] = '.'
        new_coords = [active_sand_coord[0]+vector[0], active_sand_coord[1]+vector[1]]
        print(f"grain 'x' is falling to coord [{new_coords[0]}, {new_coords[1]}]")
        if new_coords[0] >= dim[0]:
            in_steady_state = True
            return sim, active_sand_found, active_sand_coord, grain_count, in_steady_state
        sim[new_coords[0], new_coords[1]] = 'o'
        active_sand_coord = [new_coords[0], new_coords[1]]

    return sim, active_sand_found, active_sand_coord, grain_count, in_steady_state


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


rocks = []
with open('day_14_input.txt') as file:
    for line in file:
        stripped_line = line.strip()
        points = stripped_line.split('->')
        for idx in range(len(points)):
            points[idx] = points[idx].strip()
            points[idx] = points[idx].split(',')
            points[idx] = [int(points[idx][0]), int(points[idx][1])]
        rocks.append(points)

# pprint(rocks)
sim, min_col = create_sim(rocks)

print_sim(sim, min_col)

sim_not_finished = True

sim[1, col_to_idx(500, min_col)] = 'o'
active_sand_coord = [1, col_to_idx(500, min_col)]
grain_count = 1

last_pause_at_grain_count = -1

update_period = 10

while sim_not_finished:
    sim, sim_not_finished, active_sand_coord, grain_count, in_steady_state = time_step(sim, min_col, active_sand_coord, grain_count)
    if update_period is not -1:
        if update_period is -2:
            #print_sim(sim, min_col)
            pass
        elif grain_count % update_period == 0 and last_pause_at_grain_count is not grain_count:
            last_pause_at_grain_count = grain_count
            print_sim(sim, min_col)
            print('Show an update every x grains (enter -1 to run without pausing or -2 to run without pausing while displaying the simulation):')
            try:
                update_period = int(input())
            except:
                pass
    if in_steady_state:
        break

# sustract 1 because an additional grain was spawned (the first one to flow outside the simulation)
print_sim(sim, min_col)
print('solution to part 1: '+str(grain_count))
