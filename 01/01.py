import numpy as np

# Part One
with open('input.txt', 'r') as f:
    data = np.loadtxt(f)

calc_fuel = lambda x: np.floor(x/3)-2

fuel = calc_fuel(data)
print(f"Total fuel required by modules: {fuel.sum()}")

# Part Two
def add_fuel(mass):
    additional_fuel = calc_fuel(mass)
    
    if additional_fuel > 0:
        return mass + add_fuel(additional_fuel)
    else:
        return mass

fuel = [add_fuel(fuel_i) for fuel_i in fuel]

print(f"Total fuel required to return to Earth: {sum(fuel)}")