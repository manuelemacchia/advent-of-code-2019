with open('input.txt', 'r') as f:
    data = list(map(int, f.read().strip()))

base_pattern = [0, 1, 0, -1]
n_phases = 100

output = data
for phase_i in range(n_phases):
    inp = output
    output = []
    for pos, d in enumerate(inp):
        pattern = [item for item in base_pattern for _ in range(pos+1)]
        pattern = [item for _ in range(int(len(data)/len(pattern)) + 1) for item in pattern]
        pattern = pattern[1:]
        
        result = 0
        for i, item in enumerate(inp):
            result = result + item*pattern[i]

        result = abs(result) % 10

        output.append(result)

for d in output:
    print(d, end='')