from collections import MutableMapping
from random import shuffle
from time import sleep
import re

from intcode15plus.computer import Computer, Intcode
from utils import read_intcode
# import console


class Map(MutableMapping):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2

    DISPLAY_OBJ = {
        str(WALL): '|',
        str(EMPTY): ' ',
        str(OXYGEN): 'O'
    }

    def __init__(self):
        # this could probably be better done as a tree or graph
        self.objects = {'(0, 0)': 1}
        self.min_x, self.max_x = 0, 0
        self.min_y, self.max_y = 0, 0

    def __getitem__(self, key):
        return self.objects[str(key)]

    def __setitem__(self, key, value):
        self.objects[str(key)] = value
        self.min_x = min(key[0], self.min_x)
        self.max_x = max(key[0], self.max_x)
        self.min_y = min(key[1], self.min_y)
        self.max_y = max(key[1], self.max_y)

    def __delitem__(self, key):
        # edge case: delete changes the min/max
        self.objects.pop(str(key))

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return (
            k for k, _ in self.objects.items()
        )

    def __contains__(self, key):
        return self._key_for(key) in self.objects

    def _key_for(self, key):
        return str(key)

    @classmethod
    def find_reverse(cls, direction):
        backtrack = direction
        if direction % 2 == 0:
            backtrack -= 1
        else:
            backtrack += 1

        return backtrack

    @property
    def oxygenated_positions(self):
        return list(filter(
            lambda x: x[1] == self.OXYGEN,
            self.objects.items()
        ))

    @property
    def oxygen_edges(self):
        # this is a little convoluted because of the data structures >_<
        edges = []
        for position_str, _ in self.oxygenated_positions:
            match = re.compile('\((\d+), (\d+)\)').match(position_str)
            position = (int(match[1]), int(match[2]))
            adjacents = list(map(
                lambda p: p[1],
                self.adjacents(position)
            ))
            edges += list(filter(
                lambda p: p in self and self[p] == self.EMPTY,
                adjacents
            ))
        return edges

    def adjacents(self, position):
        "return direction + position"
        adjustments = (
            (RepairDroid.NORTH, (0, 1)),
            (RepairDroid.SOUTH, (0, -1)),
            (RepairDroid.EAST, (1, 0)),
            (RepairDroid.WEST, (-1, 0)),
        )
        return [
            (
                direction, (adj[0] + position[0], adj[1] + position[1])
            ) for direction, adj in adjustments
        ]

    def is_deadend(self, position):
        return len(list(filter(
            lambda x: (x[1] in self and self[x[1]] == self.WALL),
            self.adjacents(position)
        ))) == 3

    def print(self, droid_position, path):
        # sleep(0.5)
        # console.clear()
        # print(self.min_x, self.max_x, self.min_y, self.max_y)

        for y in range(self.max_y + 1, self.min_y, -1):
            for x in range(self.min_x, self.max_x + 1):
                # print(x, y)
                rep = '.'
                if droid_position == (x, y):
                    rep = "D"
                elif (x, y) == (0, 0):
                    rep = "X"
                elif (x, y) in path:
                    rep = "P"
                elif (x, y) in self:
                    rep = self[(x, y)]
                    rep = self.DISPLAY_OBJ[str(rep)]
                print(rep, end='')
            print()

        # for k in :
        #    print(k, self.objects[k])


class Tile:
    NEW = 0
    PATH = 1
    BLACKLISTED = -1

    def __init__(self, position, object, state=NEW):
        self.position = position
        self.object = object
        self.state = state

    @property
    def adjacent_positions(self):
        "return direction + position"
        adjustments = {
            self.NORTH: (0, 1),
            self.SOUTH: (0, -1),
            self.EAST: (1, 0),
            self.WEST: (-1, 0),
        }
        return list(map(
            lambda k, v: (
                k,
                (v[0] + self.position[0], v[1] + self.position[1])
            ),
            adjustments
        ))


class RepairDroid:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    DIRECTIONS = (NORTH, SOUTH, WEST, EAST)

    def __init__(self, intcode=None):
        self.position = (0, 0)
        if intcode is not None:
            self.program = Computer(Intcode(intcode))
        else:
            self.program = None

        self.map = Map()

    @classmethod
    def find_reverse(cls, direction):
        backtrack = direction
        if direction % 2 == 0:
            backtrack -= 1
        else:
            backtrack += 1

        return backtrack

    def attempt_move(self, direction):
        object_in_path = self._run_program(direction)
        attempted_position = self._position_at(direction)

        self.map[attempted_position] = object_in_path

        if object_in_path == Map.WALL:
            pass
        elif object_in_path == Map.EMPTY:
            self.position = attempted_position
        elif object_in_path == Map.OXYGEN:
            self.position = attempted_position
        else:
            raise Exception(f"Invalid object {object_in_path}")

        return self.position, object_in_path

    def scout_map(self, stop_condition=None):
        # second is reverses
        stack = list(map(
            lambda d: (d, False),
            self.DIRECTIONS
        ))
        path = [self.position]
        prev_command = None
        prev_position = self.position

        while len(stack) > 0:
            next_direction, is_reversing = stack.pop()
            position, object = self.attempt_move(next_direction)

            if object == Map.WALL:
                continue
            elif stop_condition and stop_condition(object):
                break
            else:
                # since droid moves, we need to add the "opposite" movement so the droid eventually backtracks. unless the droid is already backtracking
                # this doesn't work if the droid has already crosses
                if is_reversing:
                    if prev_position in path:
                        path.remove(prev_position)
                else:
                    stack.append((
                        self.find_reverse(next_direction),
                        True
                    ))

                    path.append(position)

                for direction in self.DIRECTIONS:
                    if self._position_at(direction) in self.map:
                        continue
                    stack.append((
                        direction,
                        False
                    ))

                prev_position = position

        self.map.print(droid_position=self.position, path=path)

        return path

    def find_oxygen(self):
        return self.scout_map(stop_condition=lambda object: object == Map.OXYGEN)

    def _run_program(self, direction):
        output =  self.program.execute([direction])
        # print(output)
        object_in_path, *other_outputs = output
        if len(other_outputs) > 0:
            raise Exception(f"Unexpected outputs: {other_outputs}")

        return object_in_path

    def _position_at(self, direction):
        adjustments = {
            self.NORTH: (0, 1),
            self.SOUTH: (0, -1),
            self.EAST: (1, 0),
            self.WEST: (-1, 0),
        }
        return (
            self.position[0] + adjustments[direction][0],
            self.position[1] + adjustments[direction][1],
        )


if __name__ == '__main__':
    ints = read_intcode('./puzzle15_input.txt')
    droid = RepairDroid(intcode=ints)
    droid.scout_map()

