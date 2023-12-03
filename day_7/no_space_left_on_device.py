from functools import reduce
from pprint import pprint
import os


def get_sizes(filesystem: dict, name, dir_sizes: list[int]) -> tuple[int, list[int]]:
    size = 0
    if isinstance(filesystem, dict):
        for k, v in filesystem.items():
            if isinstance(v, dict):
                tmp, dir_sizes = get_sizes(v, k, dir_sizes)
                size += tmp
            else:
                size += v
        print(f"The total size of directory {name} is {size}")
        pprint(dir_sizes)
        dir_sizes.append(size)
        pprint(dir_sizes)
        return size, dir_sizes
    else:
        return v, dir_sizes


def create_dir(path):
    print("creating dir " + path)
    # https://stackoverflow.com/a/9320375/2278742
    path_elements = path.split("/")
    # get dict addressed by path in global variable 'filesystem', which contains nested dicts
    key = path_elements[1:]
    my_dict = reduce(dict.get, key[:-1], filesystem)
    my_dict[key[-1]] = dict()


def insert_file(path: str, name: str, size: int):
    print("creating file '" + name + "' in " + path)
    path_with_file = path + "/" + name
    path_with_file = path_with_file.replace("//", "/")
    path_elements = path_with_file.split("/")
    key = path_elements[1:]
    # get dict addressed by path in global variable 'filesystem', which contains nested dicts
    my_dict = reduce(dict.get, key[:-1], filesystem)
    my_dict[key[-1]] = size


def get_solutions(file_name):
    current_path = ""

    input_file = "input.txt"

    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        for line in file:
            line = line.strip()
            print(line)
            elements = line.split()
            if elements[0] == "$":
                if elements[1] == "cd":
                    if elements[2] == "/":
                        current_path = "/"
                    elif elements[2] == "..":
                        current_path_elements = current_path.split("/")
                        current_path = "/" + "/".join(current_path_elements[0:-2]) + "/"
                        current_path = current_path.replace("//", "/")
                    else:
                        current_path += "/" + elements[2] + "/"
                        current_path = current_path.replace("//", "/")
            elif elements[0] == "dir":
                create_dir((current_path + "/" + elements[1]).replace("//", "/"))
            else:
                # this must be ls output
                file_size = int(elements[0])
                file_name = elements[1]
                insert_file(current_path, file_name, file_size)
            print(current_path)

    if input_file == "day_7_input_example.txt":
        filesystem_expected = {
            "a": {"e": {"i": 584}, "f": 29116, "g": 2557, "h.lst": 62596},
            "b.txt": 14848514,
            "c.dat": 8504156,
            "d": {"d.ext": 5626152, "d.log": 8033020, "j": 4060174, "k": 7214296},
        }
        assert filesystem == filesystem_expected

    directory_sizes = get_sizes(filesystem, "/", [])[1]
    pprint(directory_sizes)

    sum = 0
    for size in directory_sizes:
        if size <= 100000:
            sum += size

    total_disk_space = 70000000
    used_disk_space = max(directory_sizes)
    unused_disk_space = total_disk_space - used_disk_space
    required_unused_disk_space = 30000000
    required_to_be_deleted = required_unused_disk_space - unused_disk_space

    if required_to_be_deleted > 0:
        size_of_deleted_directory = 0
        for size_of_deletion_candidate in sorted(directory_sizes):
            if size_of_deletion_candidate > required_to_be_deleted:
                size_of_deleted_directory = size_of_deletion_candidate
                break

    print("solution to part 1: " + str(sum))
    print("solution to part 2: " + str(size_of_deleted_directory))

    return sum, size_of_deleted_directory


filesystem = {}
get_solutions("input.txt")
