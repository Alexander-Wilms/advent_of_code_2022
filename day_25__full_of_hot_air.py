from pprint import pprint

digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}

decimal_values = []
with open('day_25_example.txt') as file:
    for line in file:
        stripped_line = line.strip()
        current_digit = len(stripped_line)-1
        decimal_value = 0
        for char in stripped_line:
            decimal_value += digits[char]*pow(5, current_digit)
            current_digit -= 1
        decimal_values.append(decimal_value)

pprint(decimal_values)
pprint(sum(decimal_values))
