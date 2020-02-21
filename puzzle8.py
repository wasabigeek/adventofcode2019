def build_layers(input, width=None, height=None):
    layers = []
    digits = list(map(
        lambda x: int(x),
        list(input)
    ))
    
    digits_per_layer = width * height

    while len(digits) > 0:
        layers.append(digits[0:digits_per_layer])
        digits = digits[digits_per_layer:]
        
    return layers

def find_least_zeros(layers):
    least_index = 0
    least_zeroes = 999999
    for index, layer in enumerate(layers):
        count_zeros = count_numbers(layer, 0)
        
        if count_zeros < least_zeroes:
            least_index = index
            least_zeroes = count_zeros
        
    return layers[least_index]
    
    
def count_numbers(layer, number):
    return len(list(filter(
        lambda x: x == number,
        layer
    )))

def multiply(layer):
    return count_numbers(layer, 1) * count_numbers(layer, 2)

def collapse(layers):
    final = []
    for pixel in list(zip(*layers)):
        current_pixel = None
        for p_layer in pixel:
            if current_pixel is None:
                current_pixel = p_layer
            elif current_pixel == 2:
                current_pixel = p_layer
            elif current_pixel in [0, 1]:
                continue
        final.append(current_pixel)
        
    return final


with open('./puzzle8_input.txt') as f:
    input = f.read().split('\n')[0]
    layers = build_layers(input, width=25, height=6)
    # print(layers)
    
    # least_zeros = find_least_zeros(layers)
    # print(least_zeros)
    
    # print(multiply(least_zeros))
    final = collapse(layers)
    
    final = ''.join(map(lambda x: str(x), final))
    
    final = build_layers(final, width=25, height=1)
    for l in final:
        print(l)

