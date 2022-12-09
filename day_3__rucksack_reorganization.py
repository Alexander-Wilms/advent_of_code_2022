def map_item_to_priority(item: str):
    ascii_value = ord(item)
    if ord('a') <= ascii_value <= ord('z'):
        return ascii_value-ord('a')+1
    elif ord('A') <= ascii_value <= ord('Z'):
        return ascii_value-ord('A')+26+1
    else:
        raise ValueError("Can't map item '"+item+"' to a prority")


sum_of_priorities = 0
with open('day_3_input.txt') as f:
    for line in f:
        rucksack = line.strip()
        print(rucksack)
        rucksack_size = len(rucksack)
        if rucksack_size/2 % 1 > 0:
            raise ValueError('Line has uneven number of items')
        print(rucksack_size)
        first_compartment = rucksack[0:int(rucksack_size/2)]
        print(first_compartment)
        second_compartment = rucksack[int(rucksack_size/2):]
        print(second_compartment)
        for first_item in first_compartment:
            for second_item in second_compartment:
                if first_item == second_item:
                    duplicate_item = first_item
                    break
        print(duplicate_item)
        sum_of_priorities += map_item_to_priority(duplicate_item)

print(sum_of_priorities)
