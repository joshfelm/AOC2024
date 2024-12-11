es = [o.strip().split(':') for o in open('./test_input.txt', 'r').readlines()]

mul = lambda x, y: int(x)*int(y)
add = lambda x, y: int(x)+int(y)
con = lambda x, y: int(str(x)+str(y))

def s(xs, ys, os):
    if len(xs) == 0: return ys
    if len(ys) == 0: return s(xs[1:], [xs[0]], os)
    else: return s(xs[1:], ([o((y), (xs[0])) for o in os for y in ys]), os)

def v(es, os):
    return sum([int(e[0]) for e in es if int(e[0]) in s(e[1].strip().split(' '), [], os)])

print(f"part 1: {v(es, [mul, add])}")
print(f"part 2: {v(es, [mul, add, con])}")
