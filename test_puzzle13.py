import unittest

from .puzzle13 import *


class ComputerTest(unittest.TestCase):
    def xtest_execute(self):
        intcode = (109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101,
                   1006, 101, 0, 99)
        inputs = []
        outputs = Computer(intcode).execute(inputs)
        self.assertSequenceEqual(outputs, intcode)
        
    def test_process_outputs(self):
        outputs = (1,2,3,6,5,4)
        tiles, _ = process_outputs(outputs)
        self.assertEqual(len(tiles), 2)

        tile1, tile2 = tiles
        self.assertEqual(type(tile1), HorizontalPaddleTile)
        self.assertEqual((tile1.x, tile1.y), (1, 2))

        self.assertEqual(type(tile2), BallTile)
        self.assertEqual((tile2.x, tile2.y), (6, 5))

