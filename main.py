from ortools.linear_solver import pywraplp
from functools import reduce

# Count of each candy
# Example row: {"Whopper", 100}, indicates 100 Whoppers
candy_counts = [
]

num_bags = 60
total_candy = sum(candy_count[1] for candy_count in candy_counts)
candy_per_bag = total_candy // num_bags
all_bags = range(num_bags)
all_candy = range(len(candy_counts))

print(f"Total candy {total_candy}")

candy_limits = []
for candy in all_candy:
    candy_min = candy_counts[candy][1] // num_bags
    candy_max = (candy_min if (candy_counts[candy][1] % num_bags == 0) else (candy_min + 1))
    candy_limits.append([candy_min, candy_max])

solver = pywraplp.Solver.CreateSolver('SCIP')

bags = {}
for bag in all_bags:
    for candy in all_candy:
        bags[(bag, candy)] = solver.IntVar(candy_limits[candy][0], candy_limits[candy][1], name='')
        
# Each candy needs 'n' candy
for bag in all_bags:
    solver.Add(solver.Sum([bags[(bag, candy)] for candy in all_candy]) == candy_per_bag)

# Each candy is fully allocated
for candy in all_candy:
    solver.Add(solver.Sum([bags[(bag, candy)] for bag in all_bags]) == candy_counts[candy][1])

status = solver.Solve()

after_counts = {}
for candy in all_candy:
    after_counts[candy_counts[candy][0]] = 0

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    for bag in all_bags:
        print(f'\nBag {bag+1}')
        for candy in all_candy:
            if bags[(bag, candy)].solution_value() > 0.9:
                after_counts[candy_counts[candy][0]] += bags[(bag,candy)].solution_value()
                print(f'{candy_counts[candy][0]} x {bags[(bag,candy)].solution_value()}')
                
    print("")
    for candy in all_candy:
        print(f"{candy_counts[candy][0]} - Expected: {candy_counts[candy][1]}.0 vs Actual: {after_counts[candy_counts[candy][0]]}")
else:
    print('No solution found.')
