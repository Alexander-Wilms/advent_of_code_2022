import os
from copy import deepcopy
from pprint import pprint

import numpy as np


class Rope():
    def __init__(self, input_file: str):
        self.width, self.height, start_row, start_col, self.moves = self.determine_grid(input_file)
        self.grid = np.empty((self.height, self.width), dtype=object)
        self.grid_visited_by_tail = np.full((self.height, self.width), False)
        self.start: np.array = np.array([start_row, start_col])
        print('start')
        pprint(self.start)
        self.head: np.array = deepcopy(self.start)
        self.tail: np.array = deepcopy(self.start)
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row, col] = '.'
        print('== Initial State ==')
        print(self)

    def get_direction(self, direction: str) -> np.ndarray:
        match direction:
            case 'U':
                return np.array([-1, 0])
            case 'D':
                return np.array([1, 0])
            case 'L':
                return np.array([0, -1])
            case 'R':
                return np.array([0, 1])

    def move(self):
        motion_str = self.moves.pop(0)
        print('== '+motion_str+' ==\n')
        elements = motion_str.split()
        direction = elements[0]
        magnitude = int(elements[1])
        self.grid_visited_by_tail[self.tail[0], self.tail[1]] = True
        for _ in range(magnitude):
            previous_head = deepcopy(self.head)
            self.head += self.get_direction(direction)

            # print(self)

            difference: list[int] = []
            for idx in range(0, 1+1):
                difference.append(self.head[idx]-self.tail[idx])

            abs_difference = [abs(dir) for dir in difference]

            if min(abs_difference) == 0 and max(abs_difference) == 2:
                self.get_motion_to_catch_up(difference, False)

            if min(abs_difference) >= 1 and max(abs_difference) == 2:
                self.tail = previous_head

            self.grid_visited_by_tail[self.tail[0], self.tail[1]] = True
            # print(self)
            # print('---')

    def get_motion_to_catch_up(self, difference: list[int], anyway: bool):
        pprint(difference)
        abs_difference = [abs(dir) for dir in difference]
        for idx in range(0, 1+1):
            if self.head[idx] == self.tail[idx] or anyway:
                # check difference of axis that isnt the same
                if abs_difference[1-idx] == 2:
                    x = int(difference[1-idx]/abs(difference[1-idx]))*idx
                    y = int(difference[1-idx]/abs(difference[1-idx]))*(1-idx)
                    if not anyway:
                        self.tail += np.array([x, y])
                    else:
                        self.tail += np.array([x, y])

    def get_number_of_cells_visited_by_tail(self) -> int:
        return self.grid_visited_by_tail.sum()

    def determine_grid(self, input_file) -> tuple[int]:
        grid_width = []
        grid_height = []
        moves = []
        with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
            for line in file:
                moves.append(line.strip())
                elements = line.split()
                direction = elements[0]
                magnitude = int(elements[1])
                match direction:
                    case 'U':
                        grid_height.append(-magnitude)
                    case 'D':
                        grid_height.append(magnitude)
                    case 'L':
                        grid_width.append(-magnitude)
                    case 'R':
                        grid_width.append(magnitude)

            min_width = 0
            max_width = 0
            min_height = 0
            max_height = 0

            integrated_width = 0
            integrated_height = 0

            for width in grid_width:
                integrated_width += width
                if integrated_width < min_width:
                    min_width = integrated_width
                if integrated_width > max_width:
                    max_width = integrated_width

            for height in grid_height:
                integrated_height += height
                if integrated_height < min_height:
                    min_height = integrated_height
                if integrated_height > max_height:
                    max_height = integrated_height

            total_width = max_width-min_width+1
            total_height = max_height-min_height+1

            print('min_height: '+str(min_height))
            print('max_height: '+str(max_height))
            print('total_height: '+str(total_height))
            start_y = abs(min_height)

            print('min_width: '+str(min_width))
            print('max_width: '+str(max_width))
            print('total_width: '+str(total_width))
            pprint(total_width)
            start_x = abs(min_width)

            pprint(start_x)
            pprint(start_y)

            return total_width, total_height, start_y, start_x, moves

    def get_number_of_moves(self) -> int:
        return len(self.moves)

    def __str__(self) -> str:
        string = ''

        covered = []
        if np.array_equal(self.tail, self.head):
            covered.append('T')
        if np.array_equal(self.start, self.head):
            covered.append('s')

        for row in range(self.height):
            for col in range(self.width):
                cell = '.'
                cell_idx = np.array([row, col])
                if np.array_equal(self.start, cell_idx):
                    cell = 's'
                if np.array_equal(self.tail, cell_idx):
                    cell = 'T'
                if np.array_equal(self.head, cell_idx):
                    cell = 'H'
                string += cell+' '

            if len(covered) > 0 and row == self.head[0]:
                string += '(H covers '+', '.join(covered)+')'
            string += '\n'
        return string

    def print_visited_grid(self):
        for row in range(self.height):
            for col in range(self.width):
                if not self.grid_visited_by_tail[row, col]:
                    cell = '.'
                else:
                    cell = '#'
                if np.array_equal(self.start, np.array([row, col])):
                    cell = 's'
                print(cell, end=' ')
            print()


def get_solutions(input_file) -> tuple[int]:
    rope: Rope = Rope(input_file)

    for _ in range(rope.get_number_of_moves()):
        rope.move()

    rope.print_visited_grid()

    print('\nsolution to part 1: '+str(rope.get_number_of_cells_visited_by_tail()))

    return rope.get_number_of_cells_visited_by_tail(), None


get_solutions('input.txt')
