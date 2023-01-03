import os
from pprint import pprint

def get_solutions(input_file) -> tuple[int]:
    calories_of_current_elf = 0
    calories_of_each_elf = []
    no_newline_before_eof = 0
    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        for line in file:
            # print(line.strip())
            if line == '\n':
                calories_of_each_elf.append(calories_of_current_elf)
                calories_of_current_elf = 0
                no_newline_before_eof = 0
            else:
                calories_of_current_elf += int(line)
                no_newline_before_eof = 1

    if no_newline_before_eof:
        calories_of_each_elf.append(calories_of_current_elf)

    # pprint(calories_of_each_elf)

    max_value_part_1 = max(calories_of_each_elf)
    print(max_value_part_1)

    max_value_part_2 = 0
    for _ in range(1,3+1):
        max_value = max(calories_of_each_elf)
        max_value_part_2 += max_value
        max_idx = calories_of_each_elf.index(max_value)
        calories_of_each_elf[max_idx] = 0

    print(max_value_part_2)

    return max_value_part_1, max_value_part_2

get_solutions('input.txt')