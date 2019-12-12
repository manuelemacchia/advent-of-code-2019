with open('input.txt', 'r') as f:
    data = f.read()

# Part 1

# A)B -> B directly orbits A
orbits = {}
for l in data.splitlines():
    orbit = l.split(')')
    orbits[orbit[1]] = orbit[0]

# Set of all objects that are orbited by some other object
all_orbited = set([orbit[0] for orbit in orbits])

# Set of all objects that do not have any other object orbiting them (tree leaves)
leaves = [k for k in orbits.keys() if k not in all_orbited]

def chain_objects(chain):
    if chain[-1] == 'COM':
        return chain
    
    chain.append(orbits[chain[-1]])
    return chain_objects(chain)

# chain_objects for every leaf and then count the length of each list
chains = [chain_objects([leaf]) for leaf in leaves]

n_indirect_orbits = sum([len(chain) - 2 for chain in chains])
n_direct_orbits = len(orbits)

print(f"Total number of orbits: {n_direct_orbits + n_indirect_orbits}")

# Part 2

you = None
san = None
for chain in chains:
    if chain[0] == 'YOU':
        you = chain
    
    if chain[0] == 'SAN':
        san = chain

intersect = set(you).intersection(san)
distance = len(you) + len(san) - 2 * len(intersect) - 2 

print(f"Nodes between you and Santa: {distance}")