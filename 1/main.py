import pandas as pd
input_file = "./input.txt"

# part 1
df = pd.read_csv(input_file, sep = ' ', header=None)
df[0] = df[0].sort_values(ignore_index=True)
df[1] = df[1].sort_values(ignore_index=True)
print(f"part 1: {sum(abs(df[0] - df[1]))}")

# part 2
similarity_score = 0
word_counts = df[1].value_counts()
for val in df[0]:
    if val in word_counts:
        similarity_score += val * word_counts[val]

print(f"part 2: {similarity_score}")
