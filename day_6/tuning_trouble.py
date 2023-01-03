import os
from pprint import pprint


def get_first_idx_after_n_distinct_chars(buffer: str, n: int) -> int:
    idx = 1
    for _ in buffer:
        if idx >= n:
            potential_marker = buffer[idx-n:idx]
            unique_chars = set(potential_marker)
            if len(potential_marker) == len(unique_chars):
                return idx
        idx += 1


pprint(get_first_idx_after_n_distinct_chars('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4))
pprint(get_first_idx_after_n_distinct_chars('bvwbjplbgvbhsrlpgdmjqwftvncz', 4))
pprint(get_first_idx_after_n_distinct_chars('nppdvjthqldpwncqszvftbrmjlhg', 4))
pprint(get_first_idx_after_n_distinct_chars('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4))
pprint(get_first_idx_after_n_distinct_chars('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4))

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as file:
    data = file.read()

solution_part_1 = get_first_idx_after_n_distinct_chars(data, 4)
assert solution_part_1 == 1042
pprint(solution_part_1)

pprint(get_first_idx_after_n_distinct_chars('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14))
pprint(get_first_idx_after_n_distinct_chars('bvwbjplbgvbhsrlpgdmjqwftvncz', 14))
pprint(get_first_idx_after_n_distinct_chars('nppdvjthqldpwncqszvftbrmjlhg', 14))
pprint(get_first_idx_after_n_distinct_chars('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14))
pprint(get_first_idx_after_n_distinct_chars('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14))

print(f"solution to part 1: {solution_part_1}")
print(f"solution to part 2: {get_first_idx_after_n_distinct_chars(data, 14)}")
