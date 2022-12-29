from pprint import pprint

from constraint import *
from sympy import Abs, Symbol, nonlinsolve, solve, symbols


def snafu_to_decimal(snafu: str) -> int:
    digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    current_digit = len(snafu)-1
    decimal_value = 0
    for char in snafu:
        decimal_value += digits[char]*pow(5, current_digit)
        current_digit -= 1
    return decimal_value


def decimal_to_snafu(decimal: int) -> str:
    # pprint(decimal)
    snafu_problem = Problem()
    var_names = []
    for snafu_digit in range(6):
        var_name = 'x'+str(snafu_digit)
        snafu_problem.addVariable(var_name, [-2, -1, 0, 1, 2])
        var_names.append(var_name)
    snafu_problem.addConstraint(lambda x5, x4, x3, x2, x1, x0: x5*5**5+x4*5**4+x3*5**3+x2*5**2+x1*5**1+x0*5**0 == decimal, var_names)
    solution = snafu_problem.getSolution()
    # pprint(solution)
    snafu = solution_to_snafu(solution)
    return snafu


def solution_to_snafu(solution) -> str:
    digits = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    snafu = ''
    for _,  val in solution.items():
        snafu += digits[val]
    # pprint(snafu)
    return snafu.lstrip('0')


decimal_values = dict()
with open('day_25_example.txt') as file:
    for line in file:
        original_snafu = line.strip()
        decimal_value = snafu_to_decimal(original_snafu)
        reconstructed_snafu = decimal_to_snafu(decimal_value)

        print(f"{reconstructed_snafu} {decimal_value}")

# solution can be found usin WolframAlpha with the following system of equations and inequalities:
# x3*5^3+x2*5^2+x1*5^1+x0*5^0=107, abs(x3)<=2, abs(x2)<=2, abs(x1)<=2, abs(x0)<=2

# solution to a snafu example using constraint
