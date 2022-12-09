def get_first_marker_idx(buffer: str) -> int:
    idx = 1
    for _ in buffer:
        marker_found = True
        if idx >= 4:
            for i in range(4):
                for j in range(4):
                    if i is not j:
                        if buffer[idx-1-i] == buffer[idx-1-j]:
                            marker_found = False

            if marker_found:
                return idx
        idx += 1


print(str(get_first_marker_idx('mjqjpqmgbljsphdztnvjfqwrcgsmlb')))
print(str(get_first_marker_idx('bvwbjplbgvbhsrlpgdmjqwftvncz')))
print(str(get_first_marker_idx('nppdvjthqldpwncqszvftbrmjlhg')))
print(str(get_first_marker_idx('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')))
print(str(get_first_marker_idx('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')))

with open('day_6_input.txt') as file:
    data = file.read()

print(str(get_first_marker_idx(data)))
