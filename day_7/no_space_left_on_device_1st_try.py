from pprint import pprint
import os


class Node:
    def __init__(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name


class File(Node):
    def __init__(self, name: str, size: int):
        Node.__init__(self, name)
        self.size = size

    def __repr__(self):
        return self.name


class Directory(Node):
    def __init__(self, name: str):
        Node.__init__(self, name)
        self.children = dict()

    def mkdir(self, name: str):
        self.children[name] = Directory(name)
        pprint(self.children)

    def add_file(self, file: File):
        self.children.append(file)

    def ls(self):
        if len(self.children) > 0:
            for child in self.children:
                print(child+' ')

    def get_children(self) -> dict[str, Node]:
        return self.children

    def get_child(self, name: str) -> Node:
        return self.children[name]

    def set_node(self, node: Node):
        self.children[dir.get_name()] = node

    def cd(self, name: str) -> Node:
        if name in self.children:
            for child in self.children:
                if name == child.get_name():
                    return child

    def __repr__(self):
        return self.name


class Filesystem():
    def __init__(self):
        self.root: Directory = Directory('root')
        self.present_working_directory = '/'

    def cd(self, target: str) -> bool:
        print('$ cd '+target)
        absolute_path = self.get_absolute_path(target)
        if self.directory_exists(absolute_path):
            self.present_working_directory = absolute_path
            print(self.present_working_directory)
            return True
        else:
            print('cd: '+target+': No such file or directory')
            return False

    def ls(self):
        print('$ ls')
        pwd = self.present_working_directory
        print(pwd)
        path_elements = pwd.split('/')
        # pprint(path_elements)
        # pprint(path_elements)
        current_dir = self.root
        for dir in path_elements[1:]:
            #print("checking if '"+dir+"' exists in '"+current_dir.get_name()+"'")
            children = current_dir.get_children()
            # pprint(children)
            children_names = children.keys()
            # pprint(children_names)
            if dir in children_names:
                # print('yes')
                current_dir = children[dir]
            else:
                return False
        current_dir.ls()
        return True

    def pwd(self):
        print('$ pwd')
        print(self.present_working_directory)

    def mkdir(self, name: str):
        print('$ mkdir '+name)
        print(self.present_working_directory)

        self.get_directory(self.present_working_directory, 'mkdir')
        #pwd_dir = self.get_directory(pwd_str)
        #pwd.mkdir(name)
        # if path_elements[0] == '' and path_elements[1] == '':
        #    self.root.mkdir(name)

        # pprint(path_elements)

    def set_directory(self, path: str, node: Node):
        print('set_directory('+path+')')
        absolute_path = self.get_absolute_path(path)
        path_elements = absolute_path.split('/')
        pprint(path_elements)
        current_dir: Directory = self.root
        for dir in path_elements[1:]:
            children = current_dir.get_children()
            children_names = children.keys()
            if dir in children_names:
                current_dir = children[dir]
            else:
                raise ValueError('Directory '+dir+' does not exist in '+current_dir.get_name())
        current_dir.set_node(dir)

    def get_directory(self, path: str, action: str) -> Directory:
        print('get_directory('+path+')')
        if path == '/':
            return self.root
        absolute_path = self.get_absolute_path(path)
        path_elements = absolute_path.split('/')
        pprint(path_elements)
        current_dir = self.root
        for dir in path_elements[1:]:
            children = current_dir.get_children()
            children_names = children.keys()
            if dir in children_names:
                current_dir = children[dir]
            else:
                raise ValueError('Directory '+dir+' does not exist in '+current_dir.get_name())
        if action == 'mkdir':
            current_dir.mkdir('test')
        return current_dir

    def directory_exists(self, path: str) -> bool:
        print('directory_exists('+path+')')
        try:
            self.get_directory(path, 'none')
            return True
        except ValueError:
            return False

    def get_absolute_path(self, path: str) -> str:
        print('get_absolute_path('+path+')')
        is_absolute_path = path[0] == '/'

        if is_absolute_path:
            absolute_path = path
        elif path == '..':
            path_elements = path.split('/')
            return '/'.join(path_elements[0:-1])
        else:
            absolute_path = self.present_working_directory+'/'+path
        
        return absolute_path.replace('//','/')

    def touch(self):
        pass


os.system('clear')
fs = Filesystem()

fs.pwd()
fs.ls()
fs.mkdir('usr')
fs.ls()
fs.cd('usr')
fs.ls()
fs.pwd()
fs.cd('/usr/share/bin')
fs.mkdir('share')
fs.ls()
fs.cd('share')
fs.pwd()
fs.mkdir('bin')
fs.get_directory('/usr/share/bin', 'none')
pprint(fs.directory_exists('/usr/share/bin'))


# current_path = ''

# with open('day_7_input_example.txt') as file:
#     for line in file:
#         print(line.strip())
#         if 'cd' in line:
#             cd_target = line.split(' ')[1]

#             root.
