import math

input_file = "./input.txt"

file = open(input_file, "r")

#part 1
rules = [[]]
updates = [[]]

lines = file.readlines()

b = lines.index('\n')

rules = [lines[i].strip().split('|') for i in range(b)]
updates = [lines[i].strip().split(',') for i in range(b+1, len(lines)) if lines[i].strip() != '']

def check_update(update):
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]):
                # print(f"Update: {update} failed because of: {rule}")
                return False
    # print(f"Update: {update} passed")
    return True

valid_updates = [u for u in updates if check_update(u)]

sum = 0
for u in valid_updates:
    midpoint = math.floor(len(u)/2)
    sum += int(u[midpoint])

print(f"part 1: {sum}")

# part 2
invalid_updates = [u for u in updates if not check_update(u)]

def fix_update(update):
    # print(f"before: {update}")
    changing = True
    while(changing):
        changing = False
        for rule in rules:
            if rule[0] in update and rule[1] in update:
                index_0 = update.index(rule[0])
                index_1 = update.index(rule[1])
                if index_0 > index_1:
                    changing = True
                    temp = update[index_0]
                    update[index_0] = update[index_1]
                    update[index_1] = temp
    # print(f"after: {update}")
    return update

fixed_updates = [fix_update(u) for u in invalid_updates]

# print(fixed_updates)

sum = 0
for u in fixed_updates:
    midpoint = math.floor(len(u)/2)
    sum += int(u[midpoint])

print(f"part 2: {sum}")

