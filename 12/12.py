from itertools import combinations

with open('input.txt', 'r') as f:
    data = [line[1:-1].split(', ') for line in f.read().strip().split('\n')]

moon_names = ['Io', 'Europa', 'Ganymede', 'Callisto']
moons = {}
for moon_name, moon_position in zip(moon_names, data):
    moons[moon_name] = {'vel': {'x': 0, 'y': 0, 'z': 0}}
    moons[moon_name]['pos'] = {position[0]: int(position[2:]) for position in moon_position}

steps = 1000
for _ in range(0, steps):
    for coord in ['x', 'y', 'z']:
        # Update each moon's velocity by applying gravity
        for moon_pair in set(combinations(moons.keys(), 2)):
            moon_pos = [moons[moon_pair[0]]['pos'][coord], moons[moon_pair[1]]['pos'][coord]]
            if moon_pos[0] > moon_pos[1]:
                moons[moon_pair[0]]['vel'][coord] -= 1
                moons[moon_pair[1]]['vel'][coord] += 1
            elif moon_pos[0] < moon_pos[1]:
                moons[moon_pair[0]]['vel'][coord] += 1
                moons[moon_pair[1]]['vel'][coord] -= 1

        # Update the position of every moon by applying velocity
        for moon in moons.keys():
            moons[moon]['pos'][coord] += moons[moon]['vel'][coord]

def total_energy(moon):
    potential_energy = sum([abs(moons[moon]['pos'][coord]) for coord in ['x', 'y', 'z']])
    kinetic_energy = sum([abs(moons[moon]['vel'][coord]) for coord in ['x', 'y', 'z']])
    return potential_energy * kinetic_energy

print(f"Total energy of the system: {sum([total_energy(moon) for moon in moons.keys()])}")