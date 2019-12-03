import csv

# Part One
def distance(p, q):
    """Calculate the Manhattan distance between two n-dimensional vectors"""
    return sum([abs(p_i - q_i) for p_i, q_i in zip(p, q)])

def occupied_coordinates(turns, start=(0, 0)):
    """Calculate coordinates occupied by a wire"""

    coords = [] # List of tuples (x, y)
    current_state = start

    for direction, length in turns:
        if direction == 'U': # Up
            for i in range(length):
                coords.append((current_state[0], current_state[1] + i+1))
            
            current_state = (current_state[0], current_state[1] + length)

        if direction == 'D': # Down
            for i in range(length):
                coords.append((current_state[0], current_state[1] - (i+1)))
            
            current_state = (current_state[0], current_state[1] - length)
        
        if direction == 'L': # Left
            for i in range(length):
                coords.append((current_state[0] - (i+1), current_state[1]))
            
            current_state = (current_state[0] - length, current_state[1])

        if direction == 'R': # Right
            for i in range(length):
                coords.append((current_state[0] + i+1, current_state[1]))
            
            current_state = (current_state[0] + length, current_state[1])
                
    return coords

# Input and preprocessing
wires = []
with open('input.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        wires.append(row)

turns = []
for wire in wires:
    l = []
    for turn in wire:
        l.append((turn[0], int(turn[1:])))
    
    turns.append(l)

# Calculate coordinates occupied by each wire and store them in a list
coordinates = []
for i in range(len(wires)):
    coordinates.append(occupied_coordinates(turns[i]))

def coordinate_intersection(wire1, wire2):
    """Calculate intersections between two wires"""
    return list(set(wire1).intersection(wire2))

intersections = coordinate_intersection(coordinates[0], coordinates[1])

distances = [distance(intersection, (0, 0)) for intersection in intersections]

print(f"Minimum distance: {min(distances)}")