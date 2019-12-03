# Part One
directions = {
    'x': {'U': 0, 'D': 0, 'L': -1, 'R': 1},
    'y': {'U': 1, 'D': -1, 'L': 0, 'R': 0}
}

def occupied_coordinates(turns, start=(0, 0)):
    """Calculate coordinates occupied by a wire"""
    coords = [] # List of tuples (x, y)
    pos = start

    for direction, length in turns:
        for i in range(1, length+1):
            coords.append(((pos[0] + directions['x'][direction] * i), (pos[1] + directions['y'][direction] * i)))

        pos = (pos[0] + directions['x'][direction] * length), (pos[1] + directions['y'][direction] * length)
                
    return coords

# Input
import csv

wires = []
with open('input.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        wires.append(row)

# Store each turn that each wire makes as a tuple (direction, number of steps)
wire_turns = [[(turn[0], int(turn[1:])) for turn in wire] for wire in wires]

# Calculate coordinates occupied by each wire and store them in a set
coordinates = [occupied_coordinates(wire_turns[i]) for i in range(len(wires))]

# Calculate the intersection between the two wires
intersections = set(coordinates[0]).intersection(coordinates[1])

# Calculate the Manhattan distance between each intersection and the center
center = (0, 0)
distances = [sum(abs(p_i - q_i) for p_i, q_i in zip(intersection, center)) for intersection in intersections]

print(f"Minimum distance: {min(distances)}")

# Part Two
def distance_steps(wire_coords, point):
    """Calculate the distance in steps for a wire to reach a point"""
    dist = 0
    for coord in wire_coords:
        dist += 1

        if coord == point:
            break
    
    return dist

combined = [sum([distance_steps(wire_coords, intersection) for wire_coords in coordinates]) for intersection in intersections]

print(f"Minimum distance in steps: {min(combined)}")