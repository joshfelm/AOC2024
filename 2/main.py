import csv
from enum import Enum

input_file = "./input.txt"

class Polarity(Enum):
    NONE = 0
    POS = 1
    NEG = 2
    NEUTRAL = 3

def calculate_polarity(a:int, b:int) -> tuple[Polarity, int]:
    if a - b > 0:
        return (Polarity.POS, abs(a-b))
    elif a - b < 0:
        return (Polarity.NEG, abs(a-b))
    return (Polarity.NEUTRAL, 0)

def process_report(report:list[str], removals_remaining:int) -> bool:
    polarity = Polarity.NONE
    errors = 0
    for i in range(1,len(report)):
        (next_polarity, next_difference) = calculate_polarity(int(report[i]), int(report[i-1]))
        if polarity == Polarity.NONE:
            polarity = next_polarity
        elif polarity == Polarity.NEUTRAL:
            errors += 1
            break
        if next_polarity != polarity or next_difference > 3 or next_difference < 1:
            errors += 1
    if errors > 0:
        if removals_remaining == 0:
            return False
        for i in range(len(report)):
            if (process_report([report[v] for v in range(len(report)) if v != i], removals_remaining-1)):
                return True
    else:
        return True
    return False

# part 1
no_safe = 0

with open(input_file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        polarity = Polarity.NONE
        safe = process_report(row, 0)

        if safe and len(row) > 1:
            no_safe += 1
            # print(f"Row: {row} safe? {safe}")

print(f"part 1: number of safe {no_safe}")

# part 2
no_safe = 0

with open(input_file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        polarity = Polarity.NONE
        safe = process_report(row, 1)

        if safe and len(row) > 1:
            no_safe += 1
        # print(f"Row: {row} safe? {safe}")

print(f"part 2: number of safe {no_safe}")
