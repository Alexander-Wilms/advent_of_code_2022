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


def solutions_to_snafu(solutions) -> str:
    digits = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    solutions_dict = solutions[0]
    snafu = ''
    for _,  val in solutions_dict.items():
        snafu = digits[val]+snafu
    return snafu


decimal_values = []
with open('day_25_example.txt') as file:
    for line in file:
        decimal_values.append(snafu_to_decimal(line.strip()))

pprint(decimal_values)
pprint(sum(decimal_values))

# solution can be found usin WolframAlpha with the following system of equations and inequalities:
# x3*5^3+x2*5^2+x1*5^1+x0*5^0=107, abs(x3)<=2, abs(x2)<=2, abs(x1)<=2, abs(x0)<=2

# solution to a snafu example using constraint
snafu_problem = Problem()
snafu_problem.addVariables(['x3', 'x2', 'x1', 'x0'], [-2, -1, 0, 1, 2])
snafu_problem.addConstraint(lambda x3, x2, x1, x0: x3*5**3+x2*5**2+x1*5**1+x0*5**0 == 107, ('x3', 'x2', 'x1', 'x0'))
solutions = snafu_problem.getSolutions()
pprint(solutions)
pprint(solutions_to_snafu(solutions))
