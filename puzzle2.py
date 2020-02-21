# warning: mutates intcode
def add(start_index, intcode):
    num1 = _get_num(start_index + 1, intcode)
    num2 = _get_num(start_index + 2, intcode)
    output_index = intcode[start_index + 3]

    if isinstance(num1, Integer) and isinstance(num2, integer):
        intcode[output_index] = num1 + num2
    else:
        intcode[output_index] = f'({num1} + {num2})'

    next_index = start_index + 4
    return next_index

# warning: mutates intcode
def multiply(start_index, intcode):
    num1 = _get_num(start_index + 1, intcode)
    num2 = _get_num(start_index + 2, intcode)
    output_index = intcode[start_index + 3]

    if isinstance(num1, Integer) and isinstance(num2, integer):
        intcode[output_index] = num1 * num2
    else:
        intcode[output_index] = f'{num1} * {num2}'

    next_index = start_index + 4
    return next_index

def terminate(_, intcode):
    return len(intcode)

# retrieve position from index, them number from that position
def _get_num(index, intcode):
    return intcode[intcode[index]]
    
OPCODES = {
        '1': add,
        '2': multiply,
        '99': terminate
    }

def execute(intcode):  
    index = 0

    while index < len(intcode):
        at_index = intcode[index]
        if str(at_index) in OPCODES:
            op = OPCODES[str(at_index)]
            index = op(index, intcode)
        print(intcode)

    return intcode

input = (
        1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,9,19,23,1,13,23,27,1,5,27,31,2,31,6,35,1,35,5,39,1,9,39,43,1,43,5,47,1,47,5,51,2,10,51,55,1,5,55,59,1,59,5,63,2,63,9,67,1,67,5,71,2,9,71,75,1,75,5,79,1,10,79,83,1,83,10,87,1,10,87,91,1,6,91,95,2,95,6,99,2,99,9,103,1,103,6,107,1,13,107,111,1,13,111,115,2,115,9,119,1,119,6,123,2,9,123,127,1,127,5,131,1,131,5,135,1,135,5,139,2,10,139,143,2,143,10,147,1,147,5,151,1,151,2,155,1,155,13,0,99,2,14,0,0
    )
    
i = 0
while i < len(input):
    print(input[i:i+4])
    i+=4

def execute_prog(noun, verb):
    _input = list(input)
    _input[1] = noun
    _input[2] = verb
    return execute(_input)

def brute():
    possible_values = range(0, len(input))
        
    for j in possible_values:
        for k in possible_values:
            result = execute_prog(j, k)[0]
            # print(result)
            break
            if result == 19690720:
                noun = j
                verb = k
                break
    
    print(100 * noun + verb)

result = execute_prog("n", "v")
print(result)[0]

