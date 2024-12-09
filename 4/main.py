from typing import Tuple
from enum import Enum

input_file = './input.txt'

file = open(input_file, "r")

input = file.read()

lines = input.split('\n')

w, h = len(lines[0]), len(lines) - 1
result = [['.' for x in range(w)] for y in range(h)]

xmas_letters = "XMAS!"

direction_vectors = [
    (1,1),
    (1,0),
    (1,-1),
    (0,1),
    (0,0),
    (0,-1),
    (-1,1),
    (-1,0),
    (-1,-1),
]

def add_tuple(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])

# part 1
def find_xmas(coords: Tuple[int, int], lines):
    out = 0
    for dir in direction_vectors:
        state = 0
        new_coords = coords
        try:
            while (lines[new_coords[0]][new_coords[1]] == xmas_letters[state] and new_coords[0] >= 0 and new_coords[1] >= 0 and new_coords[0] <= len(lines[0]) and new_coords[1] <= len(lines)):
                new_coords = add_tuple(new_coords, dir)
                state += 1
        except Exception as _:
            state = 0
        finally:
            if xmas_letters[state] == "!":
                print(f"XMAS starting at {coords} dir: {dir}")
                new_coords = coords
                for i in range(4):
                    # print(f"{new_coords}: {lines[new_coords[0]][new_coords[1]]}")
                    result[new_coords[0]][new_coords[1]] = lines[new_coords[0]][new_coords[1]]
                    new_coords = add_tuple(new_coords, dir)
                out += 1
    return out

no_xmas = 0

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == 'X':
            no_xmas += find_xmas((i,j), lines)

for r in result:
    print(''.join(r))
print(no_xmas)

# part 2
xmas_vectors = [
    [((-1,-1), 'M'),
    ((-1,1), 'M'),
    ((1,1), 'S'),
    ((1,-1), 'S')],
    [((-1,-1), 'S'),
    ((-1,1), 'M'),
    ((1,1), 'M'),
    ((1,-1), 'S')],
    [((-1,-1), 'S'),
    ((-1,1), 'S'),
    ((1,1), 'M'),
    ((1,-1), 'M')],
    [((-1,-1), 'M'),
    ((-1,1), 'S'),
    ((1,1), 'S'),
    ((1,-1), 'M')],
]

def find_x_mas(coords: Tuple[int, int], lines) -> bool:
    out = False
    for case in xmas_vectors:
        out = True
        for dir in case:
            new_coords = add_tuple(coords, dir[0])
            if (lines[new_coords[0]][new_coords[1]] != dir[1]):
                out = False
        if out:
            return True
    return out

no_xmas = 0
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == 'A':
            no_xmas += find_x_mas((i,j), lines)

print(no_xmas)
