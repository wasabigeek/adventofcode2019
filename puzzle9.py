from collections import deque, MutableMapping


class Intcode(MutableMapping):
    def __init__(self, raw_intcode):
        "_intcode should be an iterator"
        self._intcode = self._convert_to_repr(raw_intcode)
        self.lower_index = 0
        self.upper_index = len(raw_intcode) - 1
    
    def _convert_to_repr(self, raw_intcode):
        repr = {}
        for index, code in enumerate(raw_intcode):
            repr[str(index)] = code
            
        return repr
        
    def __getitem__(self, key):
        # TODO: should not allow negatives
        try:
            return self._intcode[str(key)]
        except KeyError:
            # naive check that it's a value key
            index = int(key)
            if index < self.lower_index:
                self.lower_index = index
            if index > self.upper_index:
                self.upper_index = index
            
            return 0

    def __setitem__(self, key, value):
        index = int(key)
        if index < self.lower_index:
            self.lower_index = index
        if index > self.upper_index:
            self.upper_index = index

        _key = str(key)

        self._intcode[_key] = value
    
    def __delitem__(self, key):
        index = int(key)
        if index == self.lower_index:
            self.lower_index += 1
        if index == self.upper_index:
            self.upper_index -= index

        _key = str(key)
        if _key in self._intcode:
            self._intcode.pop(_key)
            
    def __len__(self):
        return self.upper_index + 1 - self.lower_index
        
    def __iter__(self):
        return (
            self[str(i)] for i in range(self.lower_index, self.upper_index + 1)
        )


class ComputerState:
    def __init__(self):
        self.relative_base = 0
        self.index = 0
        
    def __repr__(self):
        return f'{self.__class__.__name__} relative_base={self.relative_base} index={self.index}'

# retrieve position from index, them number from that position
def get_from_pos(index, intcode, relative_base):
    return intcode[index]
def get_immediate(index, intcode, relative_base):
    return index
def get_relative(index, intcode, relative_base):
    return intcode[index] + relative_base


def equals(param_1_mode, param_2_mode, param_3_mode):
    def _equals(state, intcode, inputs=None):
        first_param = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        second_param = intcode[param_2_mode(state.index + 2, intcode, state.relative_base)]
        third_param = param_3_mode(state.index + 3, intcode, state.relative_base)
        if first_param == second_param:
            intcode[third_param] = 1
        else:
            intcode[third_param] = 0
        
        state.index = state.index + 4
        return state, None

    return _equals

def less_than(param_1_mode, param_2_mode, param_3_mode):
    def _less_than(state, intcode, inputs=None):
        first_param = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        second_param = intcode[param_2_mode(state.index + 2, intcode, state.relative_base)]
        third_param = param_3_mode(state.index + 3, intcode, state.relative_base)
        
        if first_param < second_param:
            intcode[third_param] = 1
        else:
            intcode[third_param] = 0
        
        state.index = state.index + 4
        return state, None

    return _less_than

def jump_if_true(param_1_mode, param_2_mode):
    def _jump_if_true(state, intcode, inputs=None):
        first_param = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        if first_param == 0:
            state.index += 3
            return state, None,
        
        state.index = intcode[param_2_mode(state.index + 2, intcode, state.relative_base)]
        return state, None

    return _jump_if_true
    
def jump_if_false(param_1_mode, param_2_mode):
    def _jump_if_false(state, intcode, inputs=None):
        first_param = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        if first_param != 0:
            state.index += 3
            return state, None
        
        state.index = intcode[param_2_mode(state.index + 2, intcode, state.relative_base)]
        return state, None

    return _jump_if_false


class NoInputsError(AttributeError):
    pass
    

# this mutates inputs
def take_input(param_1_mode):
    def _take_input(state, intcode, inputs=None):
        if not inputs:
            raise NoInputsError()
            
        input = inputs.pop(0)
    
        out_index = param_1_mode(state.index + 1, intcode, state.relative_base)
        # print(out_index)
        intcode[out_index] = input
        
        state.index = state.index + 2
        return state, None

    return _take_input

def output_op(param_1_mode):
    def _output_op(state, intcode, inputs=None):
        output_value = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        
        state.index = state.index + 2

        return state, output_value
        
    return _output_op

def add(param_1_mode, param_2_mode, param_3_mode):
    def _add(state, intcode, inputs=None):
        num1 = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        num2 = intcode[param_2_mode(state.index + 2, intcode, state.relative_base)]
        output_index = param_3_mode(state.index + 3, intcode, state.relative_base)
    
        intcode[output_index] = num1 + num2
    
        state.index = state.index + 4
        return state, None
        
    return _add

# warning: mutates intcode
def multiply(param_1_mode, param_2_mode, param_3_mode):
    def _multiply(state, intcode, inputs=None):
        num1 = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        num2 = intcode[param_2_mode(state.index + 2, intcode, state.relative_base)]
        output_index = param_3_mode(state.index + 3, intcode, state.relative_base)
    
        intcode[output_index] = num1 * num2

        state.index = state.index + 4
        return state, None

    return _multiply

def adjust_relative_base(param_1_mode):
    def _func(state, intcode, inputs=None):
        param_1 = intcode[param_1_mode(state.index + 1, intcode, state.relative_base)]
        state.relative_base += param_1
        
        state.index = state.index + 2

        return state, None
        
    return _func

def terminate(state, intcode, inputs=None):
    state.index = len(intcode)
    return state, None

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
        '9': adjust_relative_base
    }
    PARAM_MODES = {
        "0": get_from_pos,
        "1": get_immediate,
        "2": get_relative
    }

    instructor = str(opcode)

    # handle numbers like 13
    if len(instructor) > 1 and instructor[-2] != '0':
        return None
    # 1 params
    elif instructor[-1] in ['3', '4', '9']:
        padding = 3 - len(str(opcode))
        
    # 2 params
    elif instructor[-1] in ['5', '6']:
        padding = 4 - len(str(opcode))

    # 3 params
    elif instructor[-1] in ['1', '2', '7', '8']:
        padding = 5 - len(str(opcode))
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
    intcode = Intcode(_intcode)
    outputs = []
    state = ComputerState()

    is_paused = False
    while state.index < len(intcode) and not is_paused:
        op = _get_op(intcode[state.index])
        # print("current code:", intcode[state.index], ", op:", op, ", inputs:", inputs, state)
        # for i in range(state.index, state.index + 4):
        #     print(intcode[i])
        # print("\n")
        
        if op:
            state, output = op(state, intcode, inputs=inputs)

            # zero is falsey, so use None
            if output is not None:
                outputs.append(output)
        else:
            state.index += 1
        # print("new intcode:", intcode)

    # if len(outputs) > 1 and any([o != 0 for o in outputs[:-1]]):
    #    raise Exception(f'Output error: {outputs}')

    # diagnostic = outputs[-1]
    return intcode, outputs, state.index, is_paused


def do():
    with open('./puzzle9_input.txt') as f:
        intcode = [int(i) for i in f.read().split('\n')[0].split(',')]
        # print(intcode)

    _, outputs, _, _ = execute(intcode, [2])
    print(outputs)
        
do()

