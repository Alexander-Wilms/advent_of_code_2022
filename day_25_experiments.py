# first approach:

x0 = Symbol("x0")
x1 = Symbol("x1")
x2 = Symbol("x2")

line_eq = x1 * 5**1 + x0 * 5**0 - 7
pprint(line_eq)
pprint(line_eq.subs(x1, 1))
pprint(solve(line_eq.subs(x1, 1), x0))

line_eq = x1 * 5**1 + x0 * 5**0 - 3
pprint(line_eq)
pprint(line_eq.subs(x1, 1))
pprint(solve(line_eq.subs(x1, 1), x0))

line_eq = x2 * 5**2 + x1 * 5**1 + x0 * 5**0 - 3
pprint(line_eq)
pprint(line_eq.subs(x1, 1))
pprint(solve(line_eq.subs(x1, 1), x0))

x, y, z = symbols("x, y, z", real=True)

nonlinsolve([x * y - 1, 4 * x**2 + y**2 - 5], [x, y])

x3, x2, x1, x0 = symbols("x3, x2, x1, x0", integer=True)

# https://github.com/sympy/sympy/issues/9479

try:
    solution = solve(
        [
            x3 * 5**3 + x2 * 5**2 + x1 * 5**1 + x0 * 5**0 - 107,
            Abs(x3) <= 2,
            Abs(x2) <= 2,
            Abs(x1) <= 2,
            Abs(x0) <= 2,
        ]
    )
except:
    pass

solution = solve([x3 * 5**3 + x2 * 5**2 + x1 * 5**1 + x0 * 5**0 - 107])

pprint(solution)

# example using constraint
problem = Problem()
problem.addVariable("a", [1, 2, 3])
problem.addConstraint(lambda a: a < 3, ("a"))
pprint(problem.getSolutions())
