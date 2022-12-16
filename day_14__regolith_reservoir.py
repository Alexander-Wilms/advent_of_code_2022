from pprint import pprint
import numpy as np


def print_caves(rocks: list[list[int]]):
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

    cave_map = np.ndarray((max_row+1, number_of_columns), dtype=np.object_)

    cave_map[:] = '.'

    pprint(cave_map)

    print_caves_fr(cave_map, min_col)

    filled_rocks = fill_lines(rocks)
    pprint(filled_rocks)

    cave_map[0, col_to_idx(500, min_col)] = '+'

    for rock in filled_rocks:
        for point in rock:
            pprint(point)
            cave_map[point[1], col_to_idx(point[0], min_col)] = '#'

    print_caves_fr(cave_map, min_col)


def col_to_idx(col: int, first_col: int) -> int:
    return col-first_col


def print_caves_fr(cave_map: np.ndarray, first_col: int):
    dimensions = cave_map.shape

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
            print(cave_map[row, col], end=' ')
        print()


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
print_caves(rocks)
