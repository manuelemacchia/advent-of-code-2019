with open('input.txt', 'r') as f:
    data = f.read()

width = 25
height = 6

# Part One

layers = [data[i:i+width*height] for i in range(0, len(data)-1, width*height)]
zeroes_count = [layer.count('0') for layer in layers]
layer_id = zeroes_count.index(min(zeroes_count))

print(layers[layer_id].count('1') * layers[layer_id].count('2'))

# Part Two

black = '0'
white = '1'
transparent = '2'

def calc_pixel(layer):
    for pixel in layer:
        if pixel == transparent:
            continue
        
        return pixel

pixel_layers = [[layer[i] for layer in layers] for i in range(len(layers[0]))]
image = [calc_pixel(pixel_layer) for pixel_layer in pixel_layers]

for i, c in enumerate(image):
    if c == black:
        print(' ', end='')
    elif c == white:
        print('#', end='')
    
    if (i+1) % width == 0:
        print()