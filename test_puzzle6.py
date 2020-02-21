import unittest

from .puzzle6 import *

class Test(unittest.TestCase):
    def xtest_count_orbits(self):
        map = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L"
        ]
        checksum = count_orbits(map, "D")
        self.assertEqual(
            checksum,
            3
        )
        
        # unordered
        map = [
            "COM)B",
            "C)D",
            "B)C",
        ]
        checksum = count_orbits(map, "D")
        self.assertEqual(
            checksum,
            3
        )
    
    def test_sum_orbits(self):
        map = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L"
        ]
        checksum = sum_orbits(map)
        self.assertEqual(
            checksum,
            42
        )
        
    def test_transfers_to(self):
        map = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
            "K)YOU",
            "I)SAN",
        ]
        _, santa, you = build_tree(map)
        # print(santa, you)
        self.assertEqual(
            santa.transfers_to(you),
            4
        )

