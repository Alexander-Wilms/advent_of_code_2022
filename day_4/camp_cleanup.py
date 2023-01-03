import os

def get_solutions(file_name) -> tuple[int]:
    fully_contained_pairs = 0
    overlapping_ranges = 0
    with open(os.path.join(os.path.dirname(__file__), file_name)) as file:
        for line in file:
            assignments_raw = line.strip()
            assignments = assignments_raw.split(',')
            indices = []
            for assignment in assignments:
                indices_raw = assignment.split('-')
                indices.append(int(indices_raw[0]))
                indices.append(int(indices_raw[1]))
            # pprint(indices)

            if (indices[0] <= indices[2] and indices[1] >= indices[3]) or \
                    ((indices[2] <= indices[0] and indices[3] >= indices[1])):
                fully_contained_pairs += 1

            first_range = set(range(indices[0], indices[1]+1))
            second_range = set(range(indices[2], indices[3]+1))
            # pprint(first_range)
            # pprint(second_range)

            if not first_range.isdisjoint(second_range):
                overlapping_ranges += 1

    print('solution for part 1: '+str(fully_contained_pairs))
    print('solution for part 2: '+str(overlapping_ranges))

    return fully_contained_pairs, overlapping_ranges

get_solutions('input.txt')
