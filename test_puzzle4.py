import unittest

from .puzzle4 import password_is_valid

class Test(unittest.TestCase):
    def test_execute(self):
        expected = [
            (111122, True),

            (1, False),
            (577777, False),
            (122345, True),
            (111111, False),
            # (111111, True),
            (223450, False),
            (123789, False),
            
            (112233, True),
            (123444, False),
            
        ]
        for expect in expected:    
            actual = password_is_valid(expect[0], '109165-576723')
            print(expect, actual)

            self.assertEqual(
                actual,
                expect[1]
            )

