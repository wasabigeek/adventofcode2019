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

class Computer:
    def __init__(self, intcode):
        self.intcode = Intcode(intcode)
        self.state = ComputerState()
        
    @property
    def finished(self):
        return self.state.index >= len(self.intcode)
        
    def execute(self, inputs):
        outputs = []
        while not self.finished:
            op = _get_op(self.intcode[self.state.index])
            
            try:
                if op:
                    self.state, output = op(self.state, self.intcode, inputs=inputs)
        
                    # zero is falsey, so use None
                    if output is not None:
                        outputs.append(output)
                else:
                    self.state.index += 1
            # TODO: refactor as this is anticipated
            # pause the execution if an input is requested but none is provided
            except NoInputsError:
                break

        return outputs


class Map:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT ='right'
    
    BLACK = 0
    WHITE = 1
    
    def __init__(self):
        self.current_tile = (0, 0)
        self.current_direction = Map.UP
        self.tiles = {
            "0": { "0": [Map.BLACK] }
        }
        
    def get_color(self, tile):
        x, y = tile
        try:
            colour = self.tiles[str(y)][str(x)][-1]
        except KeyError:
            colour = Map.BLACK
            
            if str(y) not in self.tiles:
                self.tiles[str(y)] = {}
            self.tiles[str(y)][str(x)] = [colour]
            
        return colour

    def next_inputs(self):
        # get colour of current tile
        x, y = self.current_tile
        try:
            colour = self.tiles[str(y)][str(x)][-1]
        except KeyError:
            colour = Map.BLACK
            
            if str(y) not in self.tiles:
                self.tiles[str(y)] = {}
            self.tiles[str(y)][str(x)] = [colour]
        
        return [colour]
        
    def process_outputs(self, outputs):
        colour, direction = outputs
        
        # paint
        x, y = self.current_tile
        self.get_color(self.current_tile)
        self.tiles[str(y)][str(x)].append(colour)
        
        # TODO: refactor
        # move
        if direction == 0:  # left
            if self.current_direction == Map.UP:
                tile_adjustment = (-1, 0)
                new_direction = Map.LEFT
            elif self.current_direction == Map.DOWN:
                tile_adjustment = (1, 0)
                new_direction = Map.RIGHT
            elif self.current_direction == Map.LEFT:
                tile_adjustment = (0, -1)
                new_direction = Map.DOWN
            elif self.current_direction == Map.RIGHT:
                tile_adjustment = (0, 1)
                new_direction = Map.UP
        elif direction == 1:  # right
            if self.current_direction == Map.UP:
                tile_adjustment = (1, 0)
                new_direction = Map.RIGHT
            elif self.current_direction == Map.DOWN:
                tile_adjustment = (-1, 0)
                new_direction = Map.LEFT
            elif self.current_direction == Map.LEFT:
                tile_adjustment = (0, 1)
                new_direction = Map.UP
            elif self.current_direction == Map.RIGHT:
                tile_adjustment = (0, -1)
                new_direction = Map.DOWN

        cur_x, cur_y = self.current_tile
        x_adj, y_adj = tile_adjustment
        self.current_tile = (
            cur_x + x_adj,
            cur_y + y_adj
        )
        self.current_direction = new_direction
        
    def count_multipaint_tiles(self):
        def counting(tile, paints):
            if len(paints) > 1:
                return 1
            return 0

        count = self.reduce_tiles(0, counting)

        return count
        
    def white_tiles(self):
        def filter_white(tile, paints):
            if paints[-1] == Map.WHITE:
                return [(
                    int(tile[0]),
                    int(tile[1])
                )]
            return []
            
        return self.reduce_tiles([], filter_white)

    # upside down
    def print_white_tiles(self):
        white_tiles = self.white_tiles()
        sorted_tiles = sorted(
            white_tiles,
            key=lambda t: (t[1], t[0])
        )
        print(sorted_tiles)

        prev_tile = None
        # assumes first is a corner
        min_x = sorted_tiles[0][0]
        for tile in sorted_tiles:
            x, y = tile
            # line break
            if prev_tile:
                if prev_tile[1] < y:
                    print()
                    padding = x - min_x
                    print(' ' * padding, end='')

                padding = x - prev_tile[0] - 1
                print(' ' * padding, end='')
                
            print('#', end='')
                
            prev_tile = tile
        
        # return sorted_tiles
        
    def reduce_tiles(self, acc, func):
        for row, row_tiles in self.tiles.items():
            for col, paints in row_tiles.items():
                acc = acc + func((col, row), paints)
                
        return acc


def do():
    with open('./puzzle11_input.txt') as f:
        intcode = [int(i) for i in f.read().split('\n')[0].split(',')]
        # print(intcode)

    computer = Computer(intcode)
    map = Map()
    
    outputs = computer.execute([1])
    while not computer.finished:
        outputs = computer.execute(map.next_inputs())
        map.process_outputs(outputs)
    # print(map.tiles)
    map.print_white_tiles()

do()

