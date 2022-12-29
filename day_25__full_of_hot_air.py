from pprint import pprint


def snafu_to_decimal(snafu: str) -> int:
    digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    current_digit = len(snafu)-1
    decimal_value = 0
    for char in snafu:
        decimal_value += digits[char]*pow(5, current_digit)
        current_digit -= 1
    return decimal_value


decimal_values = []
with open('day_25_example.txt') as file:
    for line in file:
        decimal_values.append(snafu_to_decimal(line.strip()))

pprint(decimal_values)
pprint(sum(decimal_values))
