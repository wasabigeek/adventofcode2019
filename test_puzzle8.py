import unittest

from .puzzle8 import *

class Test(unittest.TestCase):
    def test_build_layers(self):
        input = "123456789012"
        layers = build_layers(input, width=3, height=2)
        self.assertEqual(
            layers,
            [
                [1,2,3,4,5,6],
                [7, 8, 9, 0, 1, 2]
            ]
        )

    def test_collapse(self):
        layers = build_layers("0222112222120000",  width=2, height=2)
        final = collapse(layers)
        self.assertEqual(
            final,
            [0,1,1,0]
        )

