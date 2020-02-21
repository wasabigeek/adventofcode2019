from collections import deque, MutableMapping
import console
from time import sleep


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

 
def build_tile(*args, **kwargs):
    tile_id = kwargs.pop("tile_id")
    
    tile_types = {
        "0": EmptyTile,
        "1": WallTile,
        "2": BlockTile,
        "3": HorizontalPaddleTile,
        "4": BallTile
    }
    
    return tile_types[str(tile_id)](*args, **kwargs)

class BaseTile:
    def __init__(self, *args, **kwargs):
        self.x = kwargs.pop("x")
        self.y = kwargs.pop("y")
    
    @property
    def traversable(self):
        return True
        
class EmptyTile(BaseTile):
    @property
    def symbol(self):
        return ' '
    
class WallTile(BaseTile):
    @property
    def symbol(self):
        return '|'
        
    @property
    def traversable(self):
        return False

class BlockTile(BaseTile):
    @property
    def symbol(self):
        return 'B'
        
    @property
    def traversable(self):
        return False
        
class HorizontalPaddleTile(BaseTile):
    @property
    def symbol(self):
        return 'P'
        
    @property
    def traversable(self):
        return False
    
class BallTile(BaseTile):
    @property
    def symbol(self):
        return 'o'

def process_outputs(outputs):
    score = 0
    tiles = []
    remaining = list(outputs)

    while len(remaining) > 0:
        x, y, tile_id = remaining[:3]
        if x == -1 and y == 0:
            score = tile_id
        else:
            tiles.append(build_tile(x=x, y=y, tile_id=tile_id))

        remaining = remaining[3:]
    tiles = sorted(
        tiles,
        key=lambda t: (t.y, t.x)
    )
    return tiles, score
    
def game_loop(computer, inputs, current_tiles):
    current_tiles = list(current_tiles)
    outputs = computer.execute(inputs)
    new_tiles, score = process_outputs(outputs)

    if len(current_tiles) > 0:
        for tile in new_tiles:
            index = tile_index(current_tiles, tile.x, tile.y)
            current_tiles[index] = tile
    else:
        current_tiles = new_tiles
    
    return current_tiles, score

    
def count_blocks(tiles):
    return len(list(filter(
        lambda t: type(t) == BlockTile,
        tiles
    )))
    
def tile_index(tiles, x, y):
    "finds the index of a tile by x, y coord in a sorted array of tiles"
    board_length = 0
    while True:
        if tiles[board_length].y > 0:
            break
        board_length += 1

    return y * board_length + x
    
def display_board(tiles, score):
    console.clear()
    print("Score:", score, "| Blocks Left:", count_blocks(tiles))
    
    prev_y = 0
    for tile in tiles:      
        if tile.y > prev_y:
            print()
            prev_y = tile.y
        
        print(tile.symbol, end='')
    print(end="\n\n")
    
def find_paddle(tiles):
    return next(filter(lambda t: type(t) == HorizontalPaddleTile, tiles))
    
def find_ball(tiles):
    return next(filter(lambda t: type(t) == BallTile, tiles))
    
def next_move(prev_tiles, tiles):
    LEFT_MOVE = [-1]
    RIGHT_MOVE = [1]
    NO_MOVE = [0]
    
    paddle = find_paddle(tiles)

    prev_ball = find_ball(prev_tiles)
    current_ball = find_ball(tiles)
    
    dx = current_ball.x - prev_ball.x
    dy = current_ball.y - prev_ball.y
    
    # game just started or ball can't move
    if dx == 0 and dy == 0:
        return NO_MOVE
    
    try:
        next_tile = tiles[tile_index(
            tiles,
            current_ball.x + dx,
            current_ball.y + dy
        )]
    # hit the limit of board
    except IndexError:
        return NO_MOVE

    # if right above, the ball will bounce without needing to move
    if current_ball.x == paddle.x and current_ball.y == paddle.y - 1:
        return NO_MOVE
    # try to follow the movement
    elif next_tile.x < paddle.x:
        return LEFT_MOVE
    elif next_tile.x > paddle.x:
        return RIGHT_MOVE

    return NO_MOVE


def do():
    with open('./puzzle13_input.txt') as f:
        intcode = [int(i) for i in f.read().split('\n')[0].split(',')]
        # print(intcode)

    computer = Computer(intcode)
    
    outputs = computer.execute([])
    tiles, _ = process_outputs(outputs)
    
    block_count = len(list(filter(
        lambda t: type(t) == BlockTile,
        tiles
    )))
    print(block_count)
    
def do_b(manual=False):
    with open('./puzzle13_input.txt') as f:
        intcode = [int(i) for i in f.read().split('\n')[0].split(',')]
        intcode[0] = 2

    computer = Computer(intcode)

    tiles, score = game_loop(computer, [], [])
    prev_tiles = list(tiles)
    display_board(tiles, score)

    blocks_left = count_blocks(tiles)
    while blocks_left > 0:
        if manual:
            print("What next? (L: -1, N: 0, R: 1)")
            next_inputs = [int(input("> "))]
            print(inputs)
        else:
            # sleep(0.2)
            next_inputs = next_move(prev_tiles, tiles)

        prev_tiles = list(tiles)
        tiles, new_score = game_loop(computer, next_inputs, tiles)
        if new_score > score:
            score = new_score
        
        blocks_left = count_blocks(tiles)
        # display_board(tiles, score)
    display_board(tiles, score)

do_b()

