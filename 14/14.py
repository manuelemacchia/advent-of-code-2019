from math import ceil

with open('14/input.txt', 'r') as f:
    lines = [line.strip().split(" => ") for line in f]

    reactions = {} # e.g., 'FUEL': {'out': 1, 'in': {'A': 7, 'E': 1}}
    for l in lines:
        amount, result = l[1].split(" ")
        reactions[result] = {
            'out': int(amount),
            'in': {r.split(" ")[1]: int(r.split(" ")[0]) for r in l[0].split(", ")}
        }

# Part 1

# Material that can be produced by ore directly
primary = [k for k, v in reactions.items() if 'ORE' in v['in']]

def run(fuel):
    # Initialize to material required
    needs = reactions['FUEL']['in'].copy()
    needs = {k: v*fuel for k, v in needs.items()}

    leftovers = {}

    while not all(need in primary for need in needs):
        iter_needs = needs.copy()
        current_needs = {}

        for need, qty in iter_needs.items():
            if need in primary:
                continue

            if need in leftovers:
                if qty <= leftovers[need]: # if the qty needed is less than the qty in leftovers
                    leftovers[need] -= qty
                    continue
                else:
                    qty = qty - leftovers[need]
                    leftovers[need] = 0

            times = ceil(qty / reactions[need]['out'])

            for req, req_qty in reactions[need]['in'].items():
                if req in current_needs:
                    current_needs[req] += req_qty * times
                else:
                    current_needs[req] = req_qty * times

            leftovers[need] = reactions[need]['out'] * times - qty

            needs.pop(need)

        for need, qty in current_needs.items():
            if need in leftovers:
                if qty <= leftovers[need]:
                    leftovers[need] -= qty
                    continue
                else:
                    qty = qty - leftovers[need]
                    leftovers[need] = 0
            
            if need in needs:
                needs[need] += qty
            else:
                needs[need] = qty

    ore = 0
    for need, qty in needs.items():
        times = ceil(qty / reactions[need]['out'])
        ore += reactions[need]['in']['ORE'] * times

    return ore

print(run(1))

# Part 2

cargo = 1000000000000
leftovers = {}

# By checking possible values of FUEL, we note that we are in the following FUEL range.
# (NOTE: this may change for different inputs. Downside of brute-force approach!)
print(run(3500000), run(4000000))

prev = 0
cur = 0
for fuel in range(3500000, 4000000):
    cur = run(fuel)

    if cur > cargo:
        print(fuel-1, prev)
        break

    prev = cur