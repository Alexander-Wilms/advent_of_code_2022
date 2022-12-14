import re
from pprint import pprint


class Monkey():
    def __init__(self, idx: int, starting_items: list[int], operation: str, divisor: int, next_if_true: int, next_if_false: int):
        self.idx = idx
        self.items: list[int] = starting_items
        self.operation: str = operation
        self.divisor: int = divisor
        self.next_if_true = next_if_true
        self.next_if_false = next_if_false
        self.items_inspected_count: int = 0

    def round(self):
        print('Monkey '+str(self.idx)+':')
        # use list of tuples instead of dict, since different items can have the same worry level
        items_to_be_thrown: list[tuple(int, int)] = []
        for item in self.items:
            self.items_inspected_count += 1
            print('\tMonkey inspects an item with a worry level of '+str(item)+'.')
            new_worry_level = eval(self.operation.replace('old', str(item)))
            print('\t\tWorry level changes to '+str(new_worry_level)+'.')
            new_worry_level = int(new_worry_level/3)
            print('\t\tMonkey gets bored with item. Worry level is divided by 3 to '+str(new_worry_level)+'.')
            if new_worry_level % self.divisor == 0:
                print('\t\tCurrent worry level is divisible by '+str(self.divisor)+'.')
                next_monkey = self.next_if_true
            else:
                print('\t\tCurrent worry level is not divisible by '+str(self.divisor)+'.')
                next_monkey = self.next_if_false
            items_to_be_thrown.append((new_worry_level, next_monkey))
            print(f"\t\tItem with worry level {new_worry_level} is thrown to monkey {next_monkey}.")
        self.items = []
        return items_to_be_thrown

    def receive_item(self, item: int):
        self.items.append(item)

    def get_items(self) -> list[int]:
        return self.items

    def get_inspected_items_count(self) -> int:
        return self.items_inspected_count

    def __repr__(self) -> str:
        string_representation = ''
        string_representation += 'Monkey '+str(self.idx)+':\n'
        string_representation += '\tItems:'
        string_representation += str(self.items)+'\n'
        string_representation += '\tOperation: '+self.operation+'\n'
        string_representation += '\tTest: '+str(self.divisor)+'\n'
        string_representation += '\t\tIf true: '+str(self.next_if_true)+'\n'
        string_representation += '\t\tIf false: '+str(self.next_if_false)+'\n'
        return string_representation


def print_worry(monkeys: list[Monkey]):
    for monkey in monkeys:
        print('Monkey '+str(monkey.idx)+': ', end='')
        pprint(monkey.get_items())


def print_inspections(monkeys: list[Monkey]):
    for monkey in monkeys:
        print('Monkey '+str(monkey.idx)+' inspected items '+str(monkey.get_inspected_items_count())+' times')


def get_monkey_business_level(monkeys: list[Monkey]) -> int:
    monkey_business_level = 1
    item_counts = []
    for monkey in monkeys:
        item_counts.append(monkey.get_inspected_items_count())

    sorted_item_counts = sorted(item_counts)
    monkey_business_level = sorted_item_counts[-1]*sorted_item_counts[-2]
    return monkey_business_level


with open('day_11_input.txt') as file:
    monkeys: list[Monkey] = []
    for line in file:
        line = line.strip()
        # collect attributes of current monkey
        if 'Monkey' in line:
            idx = int(re.findall(r'\d+', line)[0])
        if 'Starting items' in line:
            starting_items = re.findall(r'\d+', line)
        if 'Operation' in line:
            tokens = line.split()
            operation = ''.join(tokens[3:])
        if 'Test' in line:
            divisor = int(re.findall(r'\d+', line)[0])
        if 'If true' in line:
            next_if_true = int(re.findall(r'\d+', line)[0])
        if 'If false' in line:
            next_if_false = int(re.findall(r'\d+', line)[0])
            monkey = Monkey(int(idx), starting_items, operation, divisor, next_if_true, next_if_false)
            print(operation)
            pprint(monkey)
            monkeys.append(monkey)


pprint(monkeys)

for game_round in range(1, 20+1):
    print('Round '+str(game_round)+':')
    for monkey in monkeys:
        items_to_be_thrown = monkey.round()
        pprint(items_to_be_thrown)
        for item in items_to_be_thrown:
            pprint(item)
            monkeys[item[1]].receive_item(item[0])
    print()
    print(f"After round {game_round}, the monkeys are holding items with these worry levels:")
    print_worry(monkeys)
    print()

print_inspections(monkeys)

print()

print('solution to part 1: '+str(get_monkey_business_level(monkeys)))
