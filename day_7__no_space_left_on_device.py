from pprint import pprint


def create_dir(path):
    print("creating dir "+path)
    global filesystem
    path_elements = path.split('/')
    pprint(path_elements)
    for idx in range(1, len(path_elements)):
        match idx:
            case 1:
                filesystem[path_elements[1]] = dict()
            case 2:
                filesystem[path_elements[1]][path_elements[2]] = dict()
            case 3:
                filesystem[path_elements[1]][path_elements[2]][path_elements[3]] = dict()
    pprint(filesystem)


def insert_file(path: str, name: str, size: int):
    print("creating file '"+name+"' in "+path)
    global filesystem
    path_elements = path.split('/')

    pprint(path_elements)
    pprint(len(path_elements))
    match len(path_elements)-1:
        case 1:
            filesystem[name] = size
        case 2:
            filesystem[path_elements[1]][name] = size
        case 3:
            filesystem[path_elements[1]][path_elements[2]][name] = size

    pprint(filesystem)


filesystem = {}
current_path = ''

with open('day_7_input_example.txt') as file:
    for line in file:
        line = line.strip()
        print(line)
        elements = line.split()
        if elements[0] == '$':
            if elements[1] == 'cd':
                if elements[2] == '/':
                    current_path = '/'
                elif elements[2] == '..':
                    current_path_elements = current_path.split('/')
                    current_path = '/'+'/'.join(current_path_elements[0:-2])
                    current_path = current_path.replace('//', '/')
                else:
                    current_path += elements[2]+'/'
        elif elements[0] == 'dir':
            create_dir((current_path+'/'+elements[1]).replace('//', '/'))
        else:
            # this must be ls output
            file_size = int(elements[0])
            file_name = elements[1]
            insert_file(current_path, file_name, file_size)

