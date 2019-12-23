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

class Arcade:
    def __init__(self, program):
        self.p = program
        self.rb = 0
        self.pos = 0
        self.extra_memory_len = 10000
        self.output_mode = 0

        # screen: dict
        # ('x', 'y'): tile_id
        self.screen = {}

        #self.p[0] = 2 # Play for free
    
    def count_tiles(self, tile_id=-1):
        return sum(v == tile_id for v in self.screen.values())

    def map_tiles(self, tile_id):
        if tile_id == 0:
            return ' '
        elif tile_id == 1:
            return 'X' # Wall tile
        elif tile_id == 2:
            return '#' # Block tile
        elif tile_id == 3:
            return '=' # Paddle tile
        elif tile_id == 4:
            return 'O' # Ball tile

    def print_screen(self):
        max_x = max([x for (x, y) in self.screen.keys()])
        max_y = max([y for (x, y) in self.screen.keys()])

        screen_map = {k: self.map_tiles(v) for k, v in self.screen.items()}

        for y in range(0, max_y+1):
            for x in range(0, max_x+1):
                print(screen_map[x, y], end='')
            print()

    def run(self):
        p = self.p # Load program into memory
        rb = self.rb # Relative base
        pos = self.pos # Current position
        output_mode = self.output_mode

        out_x = None
        out_y = None

        score = 0

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
                    inp = input("Input: ")
                    p[args[0]] = int(inp)

                elif opcode == OUT:
                    if output_mode == 0:
                        out_x = p[args[0]]
                        output_mode = 1
                    elif output_mode == 1:
                        out_y = p[args[0]]
                        output_mode = 2
                    elif output_mode == 2:
                        self.screen[(out_x, out_y)] = p[args[0]]
                        output_mode = 0
                
                elif opcode == ARB:
                    rb = rb + p[args[0]]

                pos = pos + 2
            
            else:
                print(f"Unknown opcode: {opcode}")

arcade = Arcade(program)
arcade.run()

arcade.print_screen()
print(f"There are {arcade.count_tiles(2)} block tiles on the screen.")