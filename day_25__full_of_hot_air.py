import math
from pprint import pprint

from alive_progress import alive_bar
from constraint import *


def snafu_to_decimal(snafu: str) -> int:
    digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    current_digit = len(snafu)-1
    decimal_value = 0
    for char in snafu:
        decimal_value += digits[char]*pow(5, current_digit)
        current_digit -= 1
    return decimal_value


def decimal_to_snafu(decimal: int) -> str:
    base = 5
    # https://www.geeksforgeeks.org/given-number-n-decimal-base-find-number-digits-base-base-b/
    snafu_digit = (math.floor(math.log(decimal) / math.log(base)) + 1)

    pprint(snafu_digit)
    snafu_problem = Problem()
    equation_string = ' == '+str(decimal)
    var_names = []
    var_String = ''
    equation_part = ''
    conditions = ''
    for snafu in range(snafu_digit+1):
        var_name = chr(ord('a')+snafu)
        snafu_problem.addVariable(var_name, [-2, -1, 0, 1, 2])
        var_names.append(var_name)
        if snafu != 0:
            var_String = ', '+var_String
            equation_part = '+'+equation_part
        var_String = var_name+var_String
        equation_part = f"{var_name}*5**{snafu}{equation_part}"
        conditions += f",abs({var_name})<=2"
    lambda_string = 'lambda '+var_String+': '+equation_part+equation_string
    print(f"{lambda_string.replace('**','^')}{conditions}")
    snafu_problem.addConstraint(eval(lambda_string), var_names)
    solutions = snafu_problem.getSolutions()
    pprint(solutions)
    snafu = solution_to_snafu(solutions[0])
    return snafu


def solution_to_snafu(solution) -> str:
    digits = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    snafu = ''
    for _,  val in solution.items():
        snafu += digits[val]
    # pprint(snafu)
    return snafu.lstrip('0')


file_name = 'day_25_input.txt'

decimal_values = []
line_count = 0
with open(file_name) as file:
    for line in file:
        line_count += 1

with open(file_name) as file:
    with alive_bar(line_count) as bar:
        for line in file:
            original_snafu = line.strip()
            decimal_value = snafu_to_decimal(original_snafu)
            decimal_values.append(decimal_value)
            #reconstructed_snafu = decimal_to_snafu(decimal_value)

            #print(f"{reconstructed_snafu} {decimal_value}")
            bar()

pprint(sum(decimal_values))
print(f"solution to part 1: {decimal_to_snafu(sum(decimal_values))}")

# solution can be found usin WolframAlpha with the following system of equations and inequalities:
# x3*5^3+x2*5^2+x1*5^1+x0*5^0=107, abs(x3)<=2, abs(x2)<=2, abs(x1)<=2, abs(x0)<=2

# solution to a snafu example using constraint
