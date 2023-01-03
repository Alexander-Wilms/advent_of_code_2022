import os
from pprint import pprint

import numpy
from colorama import Back


def print_map(tree_map: numpy.ndarray, highlight: bool = False, highlight_row: int = -1, highlight_col: int = -1):
    (rows, cols) = tree_map.shape
    for row in range(rows):
        for col in range(cols):
            tree = str(tree_map[row, col])
            if highlight and row == highlight_row and col == highlight_col:
                tree = Back.RED + tree
            print(Back.GREEN+tree+' '+Back.RESET, end='')
        print('')


def get_aligned_map(map: numpy.ndarray, row: int, col: int, direction: str) -> tuple[numpy.ndarray, int, int]:
    (rows, cols) = map.shape
    match direction:
        case '→':
            aligned_map = map
            aligned_row = row
            aligned_col = col
        case '↑':
            aligned_map = numpy.rot90(map, axes=(1, 0))
            aligned_row = col
            aligned_col = rows-row-1
        case '←':
            aligned_map = numpy.rot90(map, k=2, axes=(1, 0))
            aligned_row = rows-row-1
            aligned_col = cols-col-1
        case '↓':
            aligned_map = numpy.rot90(map, k=3, axes=(1, 0))
            aligned_row = cols-col-1
            aligned_col = row

    return aligned_map, aligned_row, aligned_col


def is_visible_from_direction(tree_map: numpy.ndarray, row, col, direction: str) -> bool:
    height_of_tree_to_check = tree_map[row, col]

    tree_map_aligned, aligned_row, aligned_col = get_aligned_map(tree_map, row, col, direction)

    visible = True

    for idx in range(aligned_col):
        if tree_map_aligned[aligned_row, idx] >= height_of_tree_to_check:
            visible = False

    return visible


def is_visible(tree_map: numpy.ndarray, row, col) -> bool:
    (rows, cols) = tree_map.shape
    if row == 0 or col == 0 or row == rows-1 or col == cols-1:
        # trees around the edge
        return True
    else:
        visible = False
        for direction in '→↑←↓':
            visible |= is_visible_from_direction(tree_map, row, col, direction)
        return visible


def get_scenic_score(map: numpy.ndarray, row: int, col: int) -> int:
    (rows, cols) = map.shape
    height_of_tree_to_check = map[row, col]
    scenic_score = 1
    for direction in '↑←→↓':
        aligned_map, aligned_row, aligned_col = get_aligned_map(map, row, col, direction)

        viewing_distance = 0
        for idx in range(aligned_col+1, cols):
            value = aligned_map[aligned_row, idx]
            viewing_distance += 1
            if value >= height_of_tree_to_check:
                break

        scenic_score *= viewing_distance
    return scenic_score


def get_solutions(input_file) -> tuple[int]:
    # Fixes ANSI colors for some reason
    # https://stackoverflow.com/a/64222858/2278742
    os.system("")

    height = 0
    line_length_counted = False
    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        for line in file:
            if not line_length_counted:
                # don't count the newline
                width = len(line)-1
                line_length_counted = True
            print(line.strip())
            height += 1

        print(str(width)+', '+str(height))

        trees = numpy.zeros((width, height)).astype(int)

        pprint(trees)

    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        line_count = 0
        for line in file:
            char_count = 0
            for char in line:
                if char != '\n':
                    trees[line_count, char_count] = int(char)
                    char_count += 1
            line_count += 1

        pprint(trees)

    tree_visibility = numpy.full((width, height), False)

    for row in range(height):
        for col in range(width):
            tree_visibility[row, col] = is_visible(trees, row, col)

    print_map(trees)

    pprint(tree_visibility)

    scenic_scores = numpy.zeros((width, height)).astype(int)

    for row in range(height):
        for col in range(width):
            scenic_scores[row, col] = get_scenic_score(trees, row, col)

    pprint(scenic_scores)

    print('solution to part 1: '+str(tree_visibility.sum()))
    print('solution to part 2: '+str(scenic_scores.max()))

    return tree_visibility.sum(), scenic_scores.max()

get_solutions('input.txt')