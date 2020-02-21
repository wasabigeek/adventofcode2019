import unittest

from .puzzle3 import execute, execute_shortest, is_between

class Test(unittest.TestCase):
    def xtest_execute(self):
        expected = [
            (
                # intersects [(158, -12), (146, 46), (155, 4), (155, 11)]
                ['R75','D30','R83','U83','L12','D49','R71','U7','L72'], ['U62','R66','U55','R34','D71','R55','D58','R83'],
                159
            ),
            (
                ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
                'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','),
                135
            ),
            #(
            #    ['R5'], ['R7'], 2
            #)
        ]
        for expect in expected:
            self.assertEqual(
                execute(expect[0], expect[1]),
                expect[2]
            )
            
    def xtest_is_between(self):
        expected = [
            ([2,1,3], True),
            ([2,3,1], True),
            ([1,2,3], False),
            ([2,1,-3], False),
            ([-2,1,3], False),
            ([1,1,3], True),
        ]
        for expect in expected:
            print(expect, is_between(*expect[0]))
            self.assertEqual(
                is_between(*expect[0]),
                expect[1]
            )

    def test_execute_shortest(self):
        expected = [
            # ('R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','), 'U62,R66,U55,R34,D71,R55,D58,R83'.split(','), 610),
            (
                ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
                'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','),
                410
            )
        ]
        for expect in expected:
            self.assertEqual(
                execute_shortest(expect[0], expect[1]),
                expect[2]
            )

