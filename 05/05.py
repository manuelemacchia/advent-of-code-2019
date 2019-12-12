import numpy as np

# Modes
# 0: Position mode (parameters are interpreted as a position)
# 1: Immediate mode (parameters are interpreted as a value)

# Opcodes
ADD = 1 # three parameters
MUL = 2 # three parameters
IN = 3 # one parameter
OUT = 4 # one parameter
JIT = 5 # two parameters
JIF = 6 # two parameters
LT = 7 # three parameters
EQ = 8 # three parameters
STOP = 99 # no arguments

# Part One
with open('input.txt', 'r') as f:
    program = np.loadtxt(f, dtype=int, delimiter=',').tolist()

# Program
def run(program):
    # Load program into memory
    p = program

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
        
        elif opcode in [IN, OUT]:
            arg = p[pos+1] if modes == 0 else pos+1

            if opcode == IN:
                inp = input("Input: ")
                p[arg] = int(inp)

            elif opcode == OUT:
                print(f"Diagnostic code: {p[arg]}")

            pos = pos + 2
        
        elif opcode in [JIT, JIF]:
            arg_modes = [int(c) for c in reversed(f"{modes:02d}")]
            args = [p[pos+i+1] if arg_modes[i] == 0 else pos+i+1 for i in range(2)]

            if opcode == JIT:
                pos = p[args[1]] if p[args[0]] != 0 else pos + 3
            
            if opcode == JIF:
                pos = p[args[1]] if p[args[0]] == 0 else pos + 3
        
        else:
            print(f"Unknown opcode: {opcode}")

run(program)
