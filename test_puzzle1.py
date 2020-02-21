import unittest

from .puzzle1 import calc_fuel, recursive_calc_fuel

class TestCalcFuel(unittest.TestCase):
    def test_calc(self):
        expected = [
            [12, 2],
            [14, 2],
            [1969, 654],
            [100756, 33583]
        ]
        for expect in expected:
            self.assertEqual(
                calc_fuel(expect[0]),
                expect[1]
            )
            
    def test_recursive_calc_fuel(self):
        expected = [
            [14, 2],
            [1969, 966],
            [100756, 50346]
        ]
        for expect in expected:
            self.assertEqual(
                recursive_calc_fuel(expect[0]),
                expect[1]
            )

