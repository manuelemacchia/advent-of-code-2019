import numpy as np

# Input bounds
MIN_INPUT = 0
MAX_INPUT = 99

# Opcodes
STOP = 99
ADD = 1
MUL = 2

# Part One
with open('input.txt', 'r') as f:
    program = np.loadtxt(f, dtype=int, delimiter=',').tolist()

# Program
def run(program, noun, verb):
    # Load program into memory
    p = program[:]

    # Run the program with the assigned inputs
    p[1] = noun
    p[2] = verb

    pos = 0
    while p[pos] != STOP:
        result_pos = p[pos+3]

        if p[pos] == ADD:
            p[result_pos] = p[p[pos+1]] + p[p[pos+2]]
        
        if p[pos] == MUL:
            p[result_pos] = p[p[pos+1]] * p[p[pos+2]]

        pos = pos + 4

    return p[0]

print(f"Output: {run(program, 12, 2)}")

# Part Two
output = 19690720

def check_output(output):
    for i in range(MIN_INPUT, MAX_INPUT):
        for j in range(MIN_INPUT, MAX_INPUT):
            out = run(program, i, j)

            if (output == out):
                return i, j

noun, verb = check_output(output)

print(f"Verb: {verb} Noun: {noun}")
print(f"Output: {100*noun+verb}")