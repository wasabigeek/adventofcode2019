import unittest
from unittest.mock import Mock

from puzzle15 import *


class MapTest(unittest.TestCase):
    def test_deadend(self):
        map = Map()

        self.assertEqual(
            map.is_deadend((0, 0)),
            False
        )

        map[(1, 0)] = 0
        self.assertEqual(
            map.is_deadend((0, 0)),
            False
        )
        map[(-1, 0)] = 0
        map[(0, 1)] = 0
        # print(map.adjacents((0,0)))
        self.assertEqual(
            map.is_deadend((0, 0)),
            True
        )

class RepairDroidTest(unittest.TestCase):
    def test_position_at(self):
        droid = RepairDroid()
        self.assertEqual(droid.position, (0, 0))
        self.assertEqual(droid._position_at(droid.NORTH), (0, 1))
        self.assertEqual(droid._position_at(droid.SOUTH), (0, -1))
        self.assertEqual(droid._position_at(droid.EAST), (1, 0))
        self.assertEqual(droid._position_at(droid.WEST), (-1, 0))

    def test_find_reverse(self):
        droid = RepairDroid()
        cases = (
            (droid.NORTH, droid.SOUTH),
            (droid.SOUTH, droid.NORTH),
            (droid.EAST, droid.WEST),
            (droid.WEST, droid.EAST),
        )
        for direction, reverse in cases:
            with self.subTest(direction=direction, reverse=reverse):
                self.assertEqual(
                    droid.find_reverse(direction),
                    reverse
                )

    def test_attempt_move(self):
        droid = RepairDroid()

        with self.subTest("Hit a wall"):
            droid._run_program = Mock(return_value=0)
            droid.attempt_move(droid.NORTH)
            self.assertEqual(droid.position, (0, 0))
            self.assertEqual(droid.map.objects, {'(0, 0)': Map.EMPTY, '(0, 1)': Map.WALL})

        with self.subTest("Valid move"):
            droid._run_program = Mock(return_value=1)
            droid.attempt_move(droid.EAST)
            self.assertEqual(droid.position, (1, 0))
            self.assertEqual(
                droid.map.objects,
                {'(0, 0)': Map.EMPTY, '(0, 1)': Map.WALL, '(1, 0)': Map.EMPTY}
            )

        with self.subTest("Found oxygen"):
            droid._run_program = Mock(return_value=2)
            droid.attempt_move(droid.NORTH)
            self.assertEqual(droid.position, (1, 1))
            self.assertEqual(
                droid.map.objects,
                {'(0, 0)': Map.EMPTY, '(0, 1)': Map.WALL, '(1, 0)': Map.EMPTY, '(1, 1)': Map.OXYGEN}
            )


if __name__ == '__main__':
    unittest.main()

