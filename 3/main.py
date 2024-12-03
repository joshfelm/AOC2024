import re
input_file = "./input.txt"

input = open(input_file, "r").read().replace("\n", "")

def extract_muls(input:str) -> int:
    return sum([int(i[0]) * int(i[1]) for i in [x.split(',') for x in re.findall(r'mul\((\d{1,3},\d{1,3})\)', input)]])

# part 1
print(f"part 1: {extract_muls(input)}")

# part 2
donot = [m.start() for m in re.finditer(r"don't\(\)", input)]
do = [m.start() for m in re.finditer(r"do\(\)", input)]

start = re.split(r"don't\(\)", input)[0]
strings = re.findall(r"do\(\)(.*?)don't\(\)", input[min(donot):])

end = ""

if not max(donot) > max(do) and strings != None:
    end = input[next(x for x in do if x > max(donot)):]

print(f"part 2: {extract_muls(start) + sum([extract_muls(i) for i in strings]) + extract_muls(end)}")
