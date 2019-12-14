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
class Amplifier:
    def __init__(self, program, number, phase_setting, pos):
        self.p = program
        self.number = number
        self.phase_setting = phase_setting
        self.pos = pos
        self.input_mode = 0
        self.is_stopped = False
    
    def get_code(self):
        return self.p[self.pos]

    def run(self, input_signal):
        while self.p[self.pos] != STOP:
            opcode = self.p[self.pos] % 100 # Extract the last two digits of the opcode
            modes = int((self.p[self.pos] - opcode) / 100)
            
            if opcode in [ADD, MUL, LT, EQ]:
                arg_modes = [int(c) for c in reversed(f"{modes:03d}")] # Extract arg modes in the correct order
                args = [self.p[self.pos+i+1] if arg_modes[i] == 0 else self.pos+i+1 for i in range(3)]

                if opcode == ADD:
                    self.p[args[2]] = self.p[args[0]] + self.p[args[1]]
                
                elif opcode == MUL:
                    self.p[args[2]] = self.p[args[0]] * self.p[args[1]]
                
                elif opcode == LT:
                    self.p[args[2]] = 1 if self.p[args[0]] < self.p[args[1]] else 0
                
                elif opcode == EQ:
                    self.p[args[2]] = 1 if self.p[args[0]] == self.p[args[1]] else 0
                
                self.pos = self.pos + 4

            elif opcode in [JIT, JIF]:
                arg_modes = [int(c) for c in reversed(f"{modes:02d}")]
                args = [self.p[self.pos+i+1] if arg_modes[i] == 0 else self.pos+i+1 for i in range(2)]

                if opcode == JIT:
                    self.pos = self.p[args[1]] if self.p[args[0]] != 0 else self.pos + 3
                
                if opcode == JIF:
                    self.pos = self.p[args[1]] if self.p[args[0]] == 0 else self.pos + 3
            
            elif opcode in [IN, OUT]:
                arg = self.p[self.pos+1] if modes == 0 else self.pos+1
                self.pos = self.pos + 2

                # Program-specific instructions for IN and OUT opcodes
                if opcode == IN:
                    if self.input_mode == 0:
                        self.p[arg] = self.phase_setting
                        self.input_mode = 1
                    else:
                        self.p[arg] = input_signal

                elif opcode == OUT:
                    return self.p[arg] # Output
            
            else:
                print(f"Unknown opcode: {opcode}")

# Generate phase settings permutations
phase_settings_perms = list(permutations([5, 6, 7, 8, 9]))

# Find the best phase settings
highest_signal = 0
for phase_settings in phase_settings_perms:
    amps = [Amplifier(program, i, phase_settings[i], 0) for i in range(5)]
    output = 0

    while amps[4].get_code() != STOP:
        output = amps[4].run(amps[3].run(amps[2].run(amps[1].run(amps[0].run(output)))))
        
    if highest_signal < output:
        highest_signal = output

print(f"Highest signal: {highest_signal}")