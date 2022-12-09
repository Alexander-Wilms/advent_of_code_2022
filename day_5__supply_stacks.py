import re
from pprint import pprint


def print_crates(crates):
    max_stack_size = 0
    stack_no = 1
    for stack in crates:
        max_stack_size = max(max_stack_size, len(stack))
        print(str(stack_no)+': '+' '.join(stack[::-1]))
        stack_no += 1


crates = []
moves = []
with open('day_5_input.txt') as f:
    for l in f:
        line = l.replace('\n', '')
        print('line: '+line)

        if '[' in line:
            for idx in range(0, len(line), 4):
                crate = line[idx:idx+3]
                print('idx: '+str(idx))
                print('crate: '+crate)
                stack_idx = int(idx/4)
                if '[' in crate:
                    while len(crates) < stack_idx+1:
                        crates.append([])
                    crates[stack_idx].append(crate)

        if 'move' in line:
            current_moves = re.findall(r'\d+', line)
            pprint(current_moves)

            current_moves_int = []
            for value in current_moves:
                current_moves_int.append(int(value))

            moves.append(current_moves_int)

pprint(crates)
pprint(moves)

print_crates(crates)


for move in moves:

    number_of_crates = move[0]
    assert number_of_crates > 0

    from_stack = move[1]-1
    to_stack = move[2]-1

    number_of_crates_on_from_stack = len(crates[from_stack])
    number_of_crates_on_to_stack = len(crates[to_stack])

    move_str = 'move '+str(number_of_crates)+' from '+str(from_stack+1)+' to '+str(to_stack+1)

    print(move_str)

    for idx in range(number_of_crates):

        crate = crates[from_stack].pop(0)
        crates[to_stack].insert(0, crate)

    assert number_of_crates_on_from_stack - number_of_crates == len(crates[from_stack])
    assert number_of_crates_on_to_stack + number_of_crates == len(crates[to_stack])


message = ''
for stack in crates:
    top_crate = stack[0][1]
    message += top_crate

print(message)
