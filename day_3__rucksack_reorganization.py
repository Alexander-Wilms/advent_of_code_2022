from pprint import pprint


def map_item_to_priority(item: str):
    ascii_value = ord(item)
    if ord("a") <= ascii_value <= ord("z"):
        return ascii_value - ord("a") + 1
    elif ord("A") <= ascii_value <= ord("Z"):
        return ascii_value - ord("A") + 26 + 1
    else:
        raise ValueError("Can't map item '" + item + "' to a prority")


sum_of_priorities = 0
with open("day_3_input.txt") as f:
    for line in f:
        rucksack = line.strip()
        print(rucksack)
        rucksack_size = len(rucksack)
        if rucksack_size / 2 % 1 > 0:
            raise ValueError("Line has uneven number of items")
        print(rucksack_size)
        first_compartment = rucksack[0 : int(rucksack_size / 2)]
        print(first_compartment)
        second_compartment = rucksack[int(rucksack_size / 2) :]
        print(second_compartment)
        for first_item in first_compartment:
            for second_item in second_compartment:
                if first_item == second_item:
                    duplicate_item = first_item
                    break
        print(duplicate_item)
        sum_of_priorities += map_item_to_priority(duplicate_item)

print("answer for part 1: " + str(sum_of_priorities))

lines = []
with open("day_3_input.txt") as f:
    for line in f:
        lines.append(line.strip())

pprint(lines)

sum_of_priorities = 0
done_with_group = False
for line_idx in range(0, len(lines), 3):
    print(line_idx)

    first_line = lines[line_idx]
    second_line = lines[line_idx + 1]
    third_line = lines[line_idx + 2]

    print(first_line)
    print(second_line)
    print(third_line)

    done_with_group = False

    for char_first_line in first_line:
        for char_second_line in second_line:
            for char_third_line in third_line:
                if char_first_line == char_second_line == char_third_line:
                    if not done_with_group:
                        print(char_first_line)
                        sum_of_priorities += map_item_to_priority(char_first_line)
                        done_with_group = True
                        break

    print("---")

print("answer for part 2: " + str(sum_of_priorities))
