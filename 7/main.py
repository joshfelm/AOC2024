input = './input.txt'

file = open(input, "r")

mul = lambda x, y: int(x) * int(y)
add = lambda x, y: int(x) + int(y)
con = lambda x, y: int(str(x) + str(y))

def solve_equation(xs, ys, operators):
    results = []
    if len(xs) == 0:
        return ys
    if len(ys) == 0:
        return solve_equation(xs[2:], [o((xs[0]), (xs[1])) for o in operators], operators)
    else:
        for y in ys:
            results.extend([o((y), (xs[0])) for o in operators])
        return solve_equation(xs[1:], results, operators)


equations = [o.strip().split(':') for o in file.readlines()]

def sum_if_valid(equations, operators):
    result = 0

    for e in equations:
        answer = int(e[0])
        numbers = [n for n in e[1].strip().split(' ')]
        out = solve_equation(numbers, [], operators)
        if int(answer) in out:
             result += answer

    return result


# part 1
operators = [mul, add]

result = sum_if_valid(equations, operators)

print(f"part 1: {result}")

# part 2
operators = [mul, add, con]

result = sum_if_valid(equations, operators)

print(f"part 2: {result}")
