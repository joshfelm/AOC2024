from enum import Enum
from typing import Tuple
import re
from progress.bar import Bar

input_file = "./input.txt"

def add_tuple(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])

def find_ids(str, ch):
    return [i for i, c in enumerate(str) if c == ch]

class Square(Enum):
    open = 0,
    obstacle = 1,
    guard = 2,

class Direction(Enum):
    up = 0,
    down = 1,
    left = 2,
    right = 3

    def __repr__(self):
        if self == Direction.up:
            return "up"
        elif self == Direction.down:
            return "down"
        elif self == Direction.right:
            return "right"
        elif self == Direction.left:
            return "left"
        return ""

class Guard:
    direction: Direction
    position: Tuple[int, int]

    def __init__(self, direction, position):
        self.direction = direction
        self.position = position

    def get_direction(self) -> Tuple[int, int]:
        if self.direction == Direction.up:
            return (-1,0)
        elif self.direction == Direction.down:
            return (1,0)
        elif self.direction == Direction.right:
            return (0,1)
        elif self.direction == Direction.left:
            return (0, -1)
        return (0,0)

    def rotate(self):
        if self.direction == Direction.up:
            self.direction = Direction.right
        elif self.direction == Direction.down:
            self.direction = Direction.left
        elif self.direction == Direction.right:
            self.direction = Direction.down
        elif self.direction == Direction.left:
            self.direction = Direction.up

class Maze:
    height: int
    width: int
    grid: list[list[Square]]
    guard: Guard
    visited_spots: dict[Tuple[int,int], list[Direction]]
    new_obstacle_spots: list[Tuple[int, int]]
    state: bool
    step_count: int

    def __init__(self, file):
        self.step_count = 0
        self.visited_spots = {}
        self.new_obstacle_spots = []
        file = open(input_file, "r")
        lines = file.readlines()
        self.width = len(lines[0])
        self.height = len(lines)-1
        self.grid = [ [Square.open]*self.width for _ in range(self.height)]
        self.state = False
        i = 0
        for l in lines:
            for obstacle in find_ids(l, '#'):
                # print(obstacle)
                self.grid[i][obstacle] = Square.obstacle
            if re.search(r"[\^v<>]", l):
                guard_str = re.findall(r"[\^v<>]", l)[0]
                direction = Direction.up
                if guard_str == '^':
                    direction = Direction.up
                elif guard_str == 'v':
                    direction = Direction.down
                elif guard_str == '<':
                    direction = Direction.left
                elif direction == 'v':
                    direction = Direction.right
                self.guard = Guard(direction, (i, l.index(guard_str)))
                self.grid[i][l.index(guard_str)] = Square.guard
                self.visited_spots[(i, l.index(guard_str))] = [direction]
            i += 1

    def print_grid(self):
        x = 0
        for l in self.grid:
            line = ''
            y = 0
            for sq in l:
                if sq == Square.open:
                    if (x, y) in self.visited_spots:
                        line += 'X'
                    else:
                        line += '.'
                elif sq == Square.obstacle:
                    line += '#'
                elif sq == Square.guard:
                    if self.guard.direction == Direction.up:
                        line += '^'
                    if self.guard.direction == Direction.down:
                        line += 'v'
                    if self.guard.direction == Direction.left:
                        line += '<'
                    if self.guard.direction == Direction.right:
                        line += '>'
                y += 1
            x += 1
            print(line)

    def update_square(self, position: Tuple[int, int], new_state: Square):
        self.grid[position[0]][position[1]] = new_state


    def step(self):
        print(f"step: {self.step_count}")
        self.step_count += 1
        new_position = add_tuple(self.guard.position, self.guard.get_direction())
        if new_position[0] >= self.height or new_position[0] < 0 or new_position[1] >= self.width or new_position[1] < 0:
            self.state = True
            return
        # print(f"f{new_position[0]}, {self.width}, {self.height}")
        if self.grid[new_position[0]][new_position[1]] == Square.obstacle:
            self.guard.rotate()
            new_position = add_tuple(self.guard.position, self.guard.get_direction())
        else:
            if new_position not in self.visited_spots:
                self.visited_spots[new_position] = [self.guard.direction]
            else:
                self.visited_spots[new_position].append(self.guard.direction)
            self.update_square(self.guard.position, Square.open)
            self.guard.position = new_position
            self.update_square(self.guard.position, Square.guard)

    def ghost_run(self, new_obstacle) -> bool:
        if self.grid[new_obstacle[0]][new_obstacle[1]] == Square.obstacle or self.grid[new_obstacle[0]][new_obstacle[1]] == Square.guard:
            return False
        self.update_square(new_obstacle, Square.obstacle)
        while(True):
            new_position = add_tuple(self.guard.position, self.guard.get_direction())
            if new_position[0] >= self.height or new_position[0] < 0 or new_position[1] >= self.width or new_position[1] < 0:
                return False
            # print(f"f{new_position[0]}, {self.width}, {self.height}")
            if self.grid[new_position[0]][new_position[1]] == Square.obstacle:
                self.guard.rotate()
                new_position = add_tuple(self.guard.position, self.guard.get_direction())
            else:
                if new_position not in self.visited_spots:
                    self.visited_spots[new_position] = [self.guard.direction]
                else:
                    if self.guard.direction in self.visited_spots[new_position]:
                        return True
                    self.visited_spots[new_position].append(self.guard.direction)
                self.update_square(self.guard.position, Square.open)
                self.guard.position = new_position
                self.update_square(self.guard.position, Square.guard)

maze = Maze(input_file)

maze.print_grid()

print()
while(not maze.state):
    maze.step()
    # maze.print_grid()
    # print()
    # input()

maze.print_grid()

print(f"part 1: {len(maze.visited_spots)}")

new_obstacles = 0
bar = Bar('Processing', max=len(maze.visited_spots))
for s in maze.visited_spots:
    ghost_maze = Maze(input_file)
    if ghost_maze.ghost_run(s):
        new_obstacles += 1
    bar.next()
bar.finish()

print(f"part 2: {(new_obstacles)}")
