# retrieve position from index, them number from that position
def get_from_pos(index, intcode):
    return intcode[intcode[index]]
def get_immediate(index, intcode):
    return intcode[index]


def equals(param_1_mode, param_2_mode):
    def _equals(start_index, intcode, input=None):
        first_param = param_1_mode(start_index + 1, intcode)
        second_param = param_2_mode(start_index + 2, intcode)
        third_param = intcode[start_index + 3]
        if first_param == second_param:
            intcode[third_param] = 1
        else:
            intcode[third_param] = 0
        
        new_index = start_index + 4
        return new_index, None

    return _equals

def less_than(param_1_mode, param_2_mode):
    def _less_than(start_index, intcode, input=None):
        first_param = param_1_mode(start_index + 1, intcode)
        second_param = param_2_mode(start_index + 2, intcode)
        third_param = third_param = intcode[start_index + 3]
        
        if first_param < second_param:
            intcode[third_param] = 1
        else:
            intcode[third_param] = 0
        
        new_index = start_index + 4
        return new_index, None

    return _less_than

def jump_if_true(param_1_mode, param_2_mode):
    def _jump_if_true(start_index, intcode, input=None):
        first_param = param_1_mode(start_index + 1, intcode)
        if first_param == 0:
            return start_index + 3, None
        
        new_index = param_2_mode(start_index + 2, intcode)
        return new_index, None

    return _jump_if_true
    
def jump_if_false(param_1_mode, param_2_mode):
    def _jump_if_false(start_index, intcode, input=None):
        first_param = param_1_mode(start_index + 1, intcode)
        if first_param != 0:
            return start_index + 3, None
        
        new_index = param_2_mode(start_index + 2, intcode)
        return new_index, None

    return _jump_if_false

# TODO: support param mode
def take_input(start_index, intcode, input=None):
    if input is None:
        raise AttributeError()

    out_index = get_immediate(start_index + 1, intcode)
    # print(out_index)
    intcode[out_index] = input
    
    next_index = start_index + 2
    return next_index, None
    

def output_op(param_1_mode):
    def _output_op(start_index, intcode, input=None):
        output_value = param_1_mode(start_index + 1, intcode)
        
        next_index = start_index + 2

        return next_index, output_value
        
    return _output_op

def add(param_1_mode, param_2_mode):
    def _add(start_index, intcode, input=None):
        num1 = param_1_mode(start_index + 1, intcode)
        num2 = param_2_mode(start_index + 2, intcode)
        output_index = intcode[start_index + 3]
    
        intcode[output_index] = num1 + num2
    
        next_index = start_index + 4
        return next_index, None
        
    return _add

# warning: mutates intcode
def multiply(param_1_mode, param_2_mode):
    def _multiply(start_index, intcode, input=None):
        num1 = param_1_mode(start_index + 1, intcode)
        num2 = param_2_mode(start_index + 2, intcode)
        output_index = intcode[start_index + 3]
    
        intcode[output_index] = num1 * num2
    
        next_index = start_index + 4
        return next_index, None

    return _multiply
    
def terminate(_, intcode, input=None):
    return len(intcode), None

def _parse_instructor(opcode):
    "Parse the first value of the instruction into opcode and param modes, or return None"

    OPCODES = {
        '1': add,
        '2': multiply,
        '3': take_input,
        '4': output_op,
        '5': jump_if_true,
        '6': jump_if_false,
        '7': less_than,
        '8': equals,
    }
    PARAM_MODES = {
        "0": get_from_pos,
        "1": get_immediate
    }

    instructor = str(opcode)

    # handle numbers like 13
    if len(instructor) > 1 and instructor[-2] != '0':
        return None
    # lol why does this have a diff parameter mode
    elif instructor in ['3']:
        return OPCODES[instructor]
    # 1 params
    elif instructor[-1] in ['4']:
        padding = 3 - len(str(opcode))
    # 2 params, plus last always in "positional"
    elif instructor[-1] in ['1', '2', '5', '6', '7', '8']:
        padding = 4 - len(str(opcode))
    else:
        return None

    padded_opcode = f'{"0" * padding}{str(opcode)}'

    param_modes_str = list(padded_opcode[:-2])
    param_modes = {}
    param_counter = 0
    #print("param modes:", param_modes_str)
    while len(param_modes_str) > 0:
        param_counter += 1
        param_modes[f'param_{param_counter}_mode'] = PARAM_MODES[param_modes_str.pop()]


    opcode = instructor[-1]  # ignore 99
    op = OPCODES[opcode]
    
    return op(**param_modes)


def _get_op(code):
    # last digit?

    opcode = str(code)
    if opcode == '99': 
        op = terminate
    else:
        op = _parse_instructor(opcode)
    return op


def execute(intcode, input=9999):  
    index = 0
    outputs = []

    while index < len(intcode):
        op = _get_op(intcode[index])
        print("current code:", intcode[index], ", op:", op)
        if op:
            # input is assumed to be passed to every op, this might not stand true
            index, output = op(index, intcode, input=input)
            
            print("index:", index, "output:", output)
            # zero is falsey, so use None
            if output is not None:
                outputs.append(output)
        else:
            index += 1
        print("new intcode:", intcode)

    if len(outputs) > 1 and any([o != 0 for o in outputs[:-1]]):
        raise Exception(f'Output error: {output_value}')

    diagnostic = outputs[-1]
    return intcode, diagnostic
    
puzzle = [
    3,225,1,225,6,6,1100,1,238,225,104,0,1102,27,28,225,1,113,14,224,1001,224,-34,224,4,224,102,8,223,223,101,7,224,224,1,224,223,223,1102,52,34,224,101,-1768,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1002,187,14,224,1001,224,-126,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,54,74,225,1101,75,66,225,101,20,161,224,101,-54,224,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,6,30,225,2,88,84,224,101,-4884,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1001,214,55,224,1001,224,-89,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1101,34,69,225,1101,45,67,224,101,-112,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,9,81,225,102,81,218,224,101,-7290,224,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1101,84,34,225,1102,94,90,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,677,677,224,102,2,223,223,1005,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,359,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,374,101,1,223,223,108,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,404,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,449,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,464,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,509,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,539,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,554,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,569,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,584,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,599,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,629,101,1,223,223,7,226,226,224,102,2,223,223,1006,224,644,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,659,101,1,223,223,108,677,677,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226
    ]
    

def execute_prog(input):
    return execute(puzzle, input)

print(execute_prog(5))
