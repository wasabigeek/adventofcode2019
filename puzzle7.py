from collections import deque


# retrieve position from index, them number from that position
def get_from_pos(index, intcode):
    return intcode[intcode[index]]
def get_immediate(index, intcode):
    return intcode[index]


def equals(param_1_mode, param_2_mode):
    def _equals(start_index, intcode, inputs=None):
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
    def _less_than(start_index, intcode, inputs=None):
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
    def _jump_if_true(start_index, intcode, inputs=None):
        first_param = param_1_mode(start_index + 1, intcode)
        if first_param == 0:
            return start_index + 3, None
        
        new_index = param_2_mode(start_index + 2, intcode)
        return new_index, None

    return _jump_if_true
    
def jump_if_false(param_1_mode, param_2_mode):
    def _jump_if_false(start_index, intcode, inputs=None):
        first_param = param_1_mode(start_index + 1, intcode)
        if first_param != 0:
            return start_index + 3, None
        
        new_index = param_2_mode(start_index + 2, intcode)
        return new_index, None

    return _jump_if_false

# TODO: support param mode
def take_input(start_index, intcode, inputs=None):
    if inputs is None:
        raise AttributeError()
        
    input = inputs.pop(0)

    out_index = get_immediate(start_index + 1, intcode)
    # print(out_index)
    intcode[out_index] = input
    
    next_index = start_index + 2
    return next_index, None
    

def output_op(param_1_mode):
    def _output_op(start_index, intcode, inputs=None):
        output_value = param_1_mode(start_index + 1, intcode)
        
        next_index = start_index + 2

        return next_index, output_value
        
    return _output_op

def add(param_1_mode, param_2_mode):
    def _add(start_index, intcode, inputs=None):
        num1 = param_1_mode(start_index + 1, intcode)
        num2 = param_2_mode(start_index + 2, intcode)
        output_index = intcode[start_index + 3]
    
        intcode[output_index] = num1 + num2
    
        next_index = start_index + 4
        return next_index, None
        
    return _add

# warning: mutates intcode
def multiply(param_1_mode, param_2_mode):
    def _multiply(start_index, intcode, inputs=None):
        num1 = param_1_mode(start_index + 1, intcode)
        num2 = param_2_mode(start_index + 2, intcode)
        output_index = intcode[start_index + 3]
    
        intcode[output_index] = num1 * num2
    
        next_index = start_index + 4
        return next_index, None

    return _multiply
    
def terminate(_, intcode, inputs=None):
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


def execute(_intcode, inputs):
    intcode = list(_intcode)
    index = 0
    outputs = []

    while index < len(intcode):
        op = _get_op(intcode[index])
        # print("current code:", intcode[index], ", op:", op)
        if op:
            # input is assumed to be passed to every op, this might not stand true
            index, output = op(index, intcode, inputs=inputs)
            
            # print("index:", index, "output:", output)
            # zero is falsey, so use None
            if output is not None:
                outputs.append(output)
        else:
            index += 1
        # print("new intcode:", intcode)

    if len(outputs) > 1 and any([o != 0 for o in outputs[:-1]]):
        raise Exception(f'Output error: {output_value}')

    diagnostic = outputs[-1]
    return intcode, diagnostic


def calc_thrust(_intcode, settings):
    intcode = list(_intcode)
    output = 0
    for setting in settings:
        _, output = execute(intcode, inputs=[setting, output])

    return output


def possible_settings(all_settings=[], current_set=list()):
    numbers = [0, 1, 2, 3, 4]
    
    if len(current_set) == 5:
        all_settings.append(current_set)
        return

    possibilities = set(numbers) - set(current_set)
    for pos in possibilities:
        possible_settings(all_settings, list(current_set) + [pos])

    return all_settings
    

# print(possible_settings())  

def settings_for_max_thrust(intcode):
    max_settings = []
    max_output = 0
    
    for settings in possible_settings():
        output = calc_thrust(intcode, list(settings))
        
        if output > max_output:
            max_output = output
            max_settings = list(settings)
    
    print(max_settings, max_output)
    return max_settings
        
        
thruster_intcode = (
    3,8,1001,8,10,8,105,1,0,0,21,46,67,88,101,126,207,288,369,450,99999,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99
)
    
# print(settings_for_max_thrust(thruster_intcode))       

