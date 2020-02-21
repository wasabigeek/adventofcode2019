import unittest

from .puzzle2 import execute

class Test(unittest.TestCase):
    def test_execute(self):
        expected = [
            ([1,0,0,0,99], [2,0,0,0,99]),
            ([2,3,0,3,99], [2,3,0,6,99]),
            ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
            ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])   
        ]
        for expect in expected:
            self.assertEqual(
                execute(expect[0]),
                expect[1]
            )

