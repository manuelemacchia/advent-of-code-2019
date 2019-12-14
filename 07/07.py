phase_setting = {x: int for x in range(0, 6)}

import numpy as np
from itertools import permutations

# Opcodes
ADD = 1
MUL = 2
IN = 3
OUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
STOP = 99

with open('input.txt', 'r') as f:
    program = np.loadtxt(f, dtype=int, delimiter=',').tolist()

# Program
def run(program, phase_setting, input_signal):
    # Load program into memory
    p = program
    i = 0 # counts inputs

    pos = 0
    while p[pos] != STOP:
        opcode = p[pos] % 100 # Extract the last two digits of the opcode
        modes = int((p[pos] - opcode) / 100)
        
        if opcode in [ADD, MUL, LT, EQ]:
            arg_modes = [int(c) for c in reversed(f"{modes:03d}")] # Extract arg modes in the correct order
            args = [p[pos+i+1] if arg_modes[i] == 0 else pos+i+1 for i in range(3)]

            if opcode == ADD:
                p[args[2]] = p[args[0]] + p[args[1]]
            
            elif opcode == MUL:
                p[args[2]] = p[args[0]] * p[args[1]]
            
            elif opcode == LT:
                p[args[2]] = 1 if p[args[0]] < p[args[1]] else 0
            
            elif opcode == EQ:
                p[args[2]] = 1 if p[args[0]] == p[args[1]] else 0
            
            pos = pos + 4

        elif opcode in [JIT, JIF]:
            arg_modes = [int(c) for c in reversed(f"{modes:02d}")]
            args = [p[pos+i+1] if arg_modes[i] == 0 else pos+i+1 for i in range(2)]

            if opcode == JIT:
                pos = p[args[1]] if p[args[0]] != 0 else pos + 3
            
            if opcode == JIF:
                pos = p[args[1]] if p[args[0]] == 0 else pos + 3
        
        elif opcode in [IN, OUT]:
            arg = p[pos+1] if modes == 0 else pos+1

            # Program-specific instructions for IN and OUT opcodes
            if opcode == IN:
                if i == 0:
                    p[arg] = phase_setting
                    i = 1
                else:
                    p[arg] = input_signal

            elif opcode == OUT:
                return p[arg]

            pos = pos + 2
        
        else:
            print(f"Unknown opcode: {opcode}")

# Generate phase settings permutations
phase_settings_perms = list(permutations([0, 1, 2, 3, 4]))

# Find the best phase settings
highest_signal = 0
for phase_settings in phase_settings_perms:
    signal = 0
    for ps in phase_settings:
        signal = run(program, ps, signal)
    
    if highest_signal < signal:
        highest_signal = signal

print(f"Highest signal: {highest_signal}")