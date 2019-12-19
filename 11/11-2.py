# Opcodes
ADD = 1
MUL = 2
IN = 3
OUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
ARB = 9
STOP = 99

with open('input.txt', 'r') as f:
    program = list(map(int, f.read().split(',')))

class Robot:
    def __init__(self, program):
        self.p = program
        self.rb = 0
        self.pos = 0
        self.extra_memory_len = 10000
        self.inp_mode = 0

        self.x = 0
        self.y = 0
        self.facing = 'UP'

        # self.painted: dict with keys: tuple, values: int
        # {(x, y): 0 if black, 1 if white}
        # Since all panels start as black painted panels, if a pair of
        # coordinates (x_1, y_1) are not part of the set of keys of the
        # dictionary, it means that (x_1, y_1) is painted black, having
        # never been repainted by the robot.
        self.painted = {}

    def panel_color(self, coord_x, coord_y):
        # return 0: the robot is currently over a black panel
        # return 1: the robot is currently over a white panel
        return self.painted.get((coord_x, coord_y), 0)
    
    def paint(self, color):
        # color == 0: paint the current panel black
        # color == 1: paint the current panel white
        self.painted[(self.x, self.y)] = color
    
    def turn_and_advance(self, direction):
        # direction == 0: turn left 90 degrees
        # direction == 1: turn right 90 degrees

        # Turn
        if self.facing == 'UP':
            if direction == 0:
                self.facing = 'LEFT'
            elif direction == 1:
                self.facing = 'RIGHT'
        
        elif self.facing == 'LEFT':
            if direction == 0:
                self.facing = 'DOWN'
            elif direction == 1:
                self.facing = 'UP'
        
        elif self.facing == 'RIGHT':
            if direction == 0:
                self.facing = 'UP'
            elif direction == 1:
                self.facing = 'DOWN'
        
        elif self.facing == 'DOWN':
            if direction == 0:
                self.facing = 'RIGHT'
            elif direction == 1:
                self.facing = 'LEFT'

        # Advance
        if self.facing == 'UP':
            self.y += 1
        elif self.facing == 'RIGHT':
            self.x += 1
        elif self.facing == 'LEFT':
            self.x -= 1
        elif self.facing == 'DOWN':
            self.y -= 1

    def count_painted(self):
        return len(self.painted)

    def display(self):
        bounds = {
            'left': min([coords[0] for coords in self.painted.keys()]),
            'right': max([coords[0] for coords in self.painted.keys()]),
            'upper': max([coords[1] for coords in self.painted.keys()]),
            'lower': min([coords[1] for coords in self.painted.keys()])
        }

        for y in range(bounds['upper'], bounds['lower']-1, -1):
            for x in range(bounds['left'], bounds['right']+1):
                if self.panel_color(x, y) == 1:
                    print('#', end='')
                else:
                    print(' ', end='')
            print()

    def run(self):
        p = self.p # Load program into memory
        rb = self.rb # Relative base
        pos = self.pos # Current position
        inp_mode = self.inp_mode # Input mode

        # Extend the program memory beyond the initial program
        extra_memory_len = self.extra_memory_len
        p = program + [0 for i in range(extra_memory_len)]

        while p[pos] != STOP:
            opcode = p[pos] % 100 # Extract the last two digits of the opcode
            modes = int((p[pos] - opcode) / 100)
            args = []

            if opcode in [ADD, MUL, LT, EQ]:
                modes = reversed(f"{modes:03d}")
            
            elif opcode in [JIT, JIF]:
                modes = reversed(f"{modes:02d}")
            
            elif opcode in [IN, OUT, ARB]:
                modes = [modes]
            
            arg_modes = [int(c) for c in modes]

            for i in range(len(arg_modes)):
                if arg_modes[i] == 0: # Position mode
                    args.append(p[pos+i+1])

                elif arg_modes[i] == 1: # Immediate mode
                    args.append(pos+i+1)
                
                elif arg_modes[i] == 2: # Relative mode
                    args.append(p[pos+i+1] + rb)
            
            if opcode in [ADD, MUL, LT, EQ]:
                if opcode == ADD:
                    p[args[2]] = p[args[0]] + p[args[1]]
                
                elif opcode == MUL:
                    p[args[2]] = p[args[0]] * p[args[1]]
                
                elif opcode == LT:
                    p[args[2]] = 1 if p[args[0]] < p[args[1]] else 0
                
                elif opcode == EQ:
                    p[args[2]] = 1 if p[args[0]] == p[args[1]] else 0
                
                pos = pos + 4

            elif opcode == JIT:
                pos = p[args[1]] if p[args[0]] != 0 else pos + 3
            
            elif opcode == JIF:
                pos = p[args[1]] if p[args[0]] == 0 else pos + 3
            
            elif opcode in [IN, OUT, ARB]:
                if opcode == IN:
                    p[args[0]] = self.panel_color(self.x, self.y)

                elif opcode == OUT:
                    if inp_mode == 0:
                        self.paint(p[args[0]])
                        inp_mode = 1
                    elif inp_mode == 1:
                        self.turn_and_advance(p[args[0]])
                        inp_mode = 0
                
                elif opcode == ARB:
                    rb = rb + p[args[0]]

                pos = pos + 2
            
            else:
                print(f"Unknown opcode: {opcode}")

robot = Robot(program)
robot.paint(1)
robot.run()
robot.display()