"""Day 1: Calorie Counting"""

from aocd import get_data

raw = get_data(day=1, year=2022)

data = raw.split("\n\n")

sums = []
for elf in data:
    sums.append(sum(int(v) for v in elf.split("\n")))
calories = max(sums)
print(calories)

sums.sort()
print(sum(sums[-3:]))

# Alt part b
# max_calories = [calories]
# for i in range(2):
#     sums.remove(calories)
#     calories = max(sums)
#     max_calories.append(calories)
# print(sum(max_calories))
