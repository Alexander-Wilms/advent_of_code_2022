import os
import re
from copy import deepcopy
from pprint import pprint


def print_crates(crates_to_print):
    max_stack_size = 0
    stack_no = 1
    for stack in crates_to_print:
        max_stack_size = max(max_stack_size, len(stack))
        print(str(stack_no) + ": " + " ".join(stack[::-1]))
        stack_no += 1


def print_top_crates(part, crates_to_print):
    print_crates(crates_to_print)
    solution = ""
    for stack in crates_to_print:
        top_crate = stack[0][1]
        solution += top_crate
    print("solution to part " + str(part) + ": " + solution)
    return solution


def get_solutions(file_name) -> tuple[str]:
    crates = []
    moves = []
    with open(os.path.join(os.path.dirname(__file__), file_name)) as file:
        for l in file:
            line = l.replace("\n", "")
            print("line: " + line)

            if "[" in line:
                for idx in range(0, len(line), 4):
                    crate = line[idx : idx + 3]
                    print("idx: " + str(idx))
                    print("crate: " + crate)
                    stack_idx = int(idx / 4)
                    if "[" in crate:
                        while len(crates) < stack_idx + 1:
                            crates.append([])
                        crates[stack_idx].append(crate)

            if "move" in line:
                current_moves = re.findall(r"\d+", line)
                pprint(current_moves)

                current_moves_int = []
                for value in current_moves:
                    current_moves_int.append(int(value))

                moves.append(current_moves_int)

    pprint(crates)
    pprint(moves)

    # https://stackoverflow.com/a/42449199/2278742
    crates_part_2 = deepcopy(crates)

    print("crates for part 1 before moving:")
    print_crates(crates)

    for move in moves:
        number_of_crates = move[0]
        assert number_of_crates > 0

        from_stack = move[1] - 1
        to_stack = move[2] - 1

        number_of_crates_on_from_stack = len(crates[from_stack])
        number_of_crates_on_to_stack = len(crates[to_stack])

        move_str = (
            "move "
            + str(number_of_crates)
            + " from "
            + str(from_stack + 1)
            + " to "
            + str(to_stack + 1)
        )
        print(move_str)

        for idx in range(number_of_crates):
            crate = crates[from_stack].pop(0)
            crates[to_stack].insert(0, crate)

        assert number_of_crates_on_from_stack - number_of_crates == len(
            crates[from_stack]
        )
        assert number_of_crates_on_to_stack + number_of_crates == len(crates[to_stack])

    print("crates for part 1 before moving:")
    print_crates(crates)

    for move in moves:
        number_of_crates = move[0]
        from_stack = move[1] - 1
        to_stack = move[2] - 1

        print_crates(crates_part_2)

        move_str = (
            "move "
            + str(number_of_crates)
            + " from "
            + str(from_stack + 1)
            + " to "
            + str(to_stack + 1)
        )
        print(move_str)

        crates_on_crane = []
        for idx in range(number_of_crates):
            crates_on_crane.append(crates_part_2[from_stack].pop(0))

        print("crates on crane:")
        pprint(crates_on_crane)

        crates_on_crane.reverse()

        for crate in crates_on_crane:
            crates_part_2[to_stack].insert(0, crate)

    solution_1 = print_top_crates(1, crates)
    solution_2 = print_top_crates(2, crates_part_2)

    return solution_1, solution_2


get_solutions("input.txt")
