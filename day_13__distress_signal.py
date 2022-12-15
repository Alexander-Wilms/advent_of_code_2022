from pprint import pprint

indentation_level = -1


def compare(value_1, value_2) -> int:
    global indentation_level
    indentation_level += 1
    indent = ''
    for _ in range(indentation_level):
        indent += '  '
    #print(indent+'- Compare '+str(value_1)+' vs '+str(value_2))
    if isinstance(value_1, int):
        if isinstance(value_2, int):
            if value_1 < value_2:
                #print(indent+'  - Left side is smaller, so inputs are in the right order')
                retval = -1
            if value_1 > value_2:
                #print(indent+'  - Right side is smaller, so inputs are not in the right order')
                retval = 1
            if value_1 == value_2:
                retval = 0

    if isinstance(value_1, list):
        if isinstance(value_2, list):
            if len(value_1) == len(value_2) == 0:
                retval = 0
            else:
                for idx in range(max(len(value_1), len(value_2))):
                    try:
                        retval = compare(value_1[idx], value_2[idx])
                        if retval == -1 or retval == 1:
                            break
                    except IndexError:
                        if len(value_1) < len(value_2):
                            #print(indent+'  - Left side ran out of items, so inputs are in the right order')
                            retval = -1
                        elif len(value_1) > len(value_2):
                            #print(indent+'  - Right side ran out of items, so inputs are not in the right order')
                            retval = 1

    if isinstance(value_1, list):
        if isinstance(value_2, int):
            #print(indent+'  - Mixed types; convert right to ['+str(value_2)+'] and retry comparison')

            retval = compare(value_1, [value_2])

    if isinstance(value_1, int):
        if isinstance(value_2, list):
            #print(indent+'  - Mixed types; convert left to ['+str(value_1)+'] and retry comparison')

            retval = compare([value_1], value_2)

    indentation_level -= 1
    return retval


packet_idx = 0
pair_count = 1
correctly_ordered = []
packets = []
with open('day_13_input.txt') as file:
    for line in file:
        possible_packet = line.strip()
        if possible_packet:

            packet_idx += 1

            if packet_idx % 2 == 1:
                exec('a='+line.strip())

            if packet_idx % 2 == 0:
                exec('b='+line.strip())

                #print('== Pair '+str(pair_count)+' ==')
                indentation_level = -1
                correctly_ordered.append(compare(a, b))
                packets.append(a)
                packets.append(b)
                # print('')

        else:
            pair_count += 1

# print(correctly_ordered)

sum_of_indices = 0
for idx in range(1, len(correctly_ordered)+1):
    if correctly_ordered[idx-1] == -1:
        sum_of_indices += idx

print('solution to part 1: '+str(sum_of_indices))

# append divider packets
packets.append([[2]])
packets.append([[6]])
# print(packets)

packets_are_sorted = False

while not packets_are_sorted:
    packets_are_sorted = True
    for packet_idx in range(0, len(packets)-1):
        #print('comparing '+str(packet_idx)+' and '+str(packet_idx+1))
        if compare(packets[packet_idx], packets[packet_idx+1]) > 0:
            packets[packet_idx+1], packets[packet_idx] = packets[packet_idx], packets[packet_idx+1]
            packets_are_sorted = False

# print(packets)

# determine divider packet indices
decoder_key = 1
for idx in range(len(packets)):
    if packets[idx] == [[2]] or packets[idx] == [[6]]:
        decoder_key *= idx+1

print('solution to part 2: '+str(decoder_key))
