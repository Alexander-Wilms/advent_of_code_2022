from pprint import pprint
import os


def get_solutions(input_file) -> tuple[int]:
    cube_list = []
    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        for line in file:
            string_list = line.strip().split(",")
            int_list = []
            for coord in string_list:
                int_list.append(int(coord))
            # pprint(int_list)
            cube_list.append(int_list)

    total_surface_area = 0
    for cube in cube_list:
        neighbors = 0
        for potential_neighboring_cube in cube_list:
            for axis in range(3):
                for offset in [-1, 1]:
                    if (
                        potential_neighboring_cube[axis] == cube[axis] + offset
                        and potential_neighboring_cube[(axis + 1) % 3]
                        == cube[(axis + 1) % 3]
                        and potential_neighboring_cube[(axis + 2) % 3]
                        == cube[(axis + 2) % 3]
                    ):
                        neighbors += 1
        total_surface_area += 6 - neighbors
        # pprint(neighbors)

    pprint(total_surface_area)

    return total_surface_area, None


get_solutions("input.txt")
