import unittest

from .puzzle10 import *

class Test(unittest.TestCase):
    def test_in_los(self):
        start = (0, 0)
        chart = (
            '###',
            '.#.',
            '#.#',
        )
        asteroids = get_asteroids(chart)

        target = (2, 0)
        self.assertFalse(in_los(asteroids, start, target))

        target = (1, 0)
        self.assertTrue(in_los(asteroids, start, target))
        
        target = (1, 1)
        self.assertTrue(in_los(asteroids, start, target))
        
        target = (2, 2)
        self.assertFalse(in_los(asteroids, start, target))
        
        start = (2, 2)
        target = (0, 0)
        self.assertFalse(in_los(asteroids, start, target))
        target = (1, 0)
        self.assertTrue(in_los(asteroids, start, target))
        

        chart = (
            "#.........",
            "...A......",
            "...B..a...",
            ".EDCG....a",
            "..F.c.b...",
            ".....c....",
            "..efd.c.gb",
            ".......c..",
            "....f...c.",
            "...e..d..c",
        )
        asteroids = get_asteroids(chart)
        start = (0, 0)
        visibles = [
            (3, 1), (3, 2), (1, 3), (2, 3), (3, 3), (4, 3), (2, 4)
        ]
        for target in visibles:
            self.assertTrue(in_los(asteroids, start, target))

        blocked = [
            (6, 2), (9, 3), (6, 4), (9, 6),
            (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
        ]
        for target in blocked:
            self.assertFalse(in_los(asteroids, start, target))

        chart = (
            ".7..7",
            ".....",
            "67775",
            "....7",
            "...87",
        )
        asteroids = get_asteroids(chart)
        start = (3, 4)
        target = (3, 2)
        self.assertTrue(in_los(asteroids, start, target))

    def test_count_visibles(self):
        chart = (
            ".7..7",
            ".....",
            "67775",
            "....7",
            "...87",
        )
        asteroids = get_asteroids(chart)

        for row, values in enumerate(chart):
            for column, _ in enumerate(values):
                if chart[row][column] != '.':
                    expected = int(chart[row][column])

                    count = count_visibles(asteroids, (column, row))
                    print((column, row), expected, count)
                    self.assertEqual(count, expected)
        
        chart = (
            "......#.#.",
            "#..#.#....",
            "..#######.",
            ".#.#.###..",
            ".#..#.....",
            "..#....#.#",
            "#..#....#.",
            ".##.#..###",
            "##...#..#.",
            ".#....####"","
        )
        asteroids = get_asteroids(chart)
        count = count_visibles(asteroids, (5, 8))
        self.assertEqual(count, 33)
        
        chart = (
            ".#..#..###",
            "####.###.#",
            "....###.#.",
            "..###.##.#",
            "##.##.#.#.",
            "....###..#",
            "..#.#..#.#",
            "#..#.#.###",
            ".##...##.#",
            ".....#.#..",
        )
        asteroids = get_asteroids(chart)
        count = count_visibles(asteroids, (6, 3))
        self.assertEqual(count, 41)
        
    def test_get_asteroids(self):
        chart = (
            '.##',
            '.#.',
            '#.#',
        )

        positions = get_asteroids(chart)
        self.assertEqual(
            positions,
            [
                (1, 0), (2, 0), (1, 1), (0, 2), (2, 2)
            ]
        )

    def test_get_best_pos(self):
        chart = (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##",
        )

        pos = get_best_pos(chart)
        self.assertEqual(
            pos,
            (3, 4)
        )
        
        chart = (
            "......#.#.",
            "#..#.#....",
            "..#######.",
            ".#.#.###..",
            ".#..#.....",
            "..#....#.#",
            "#..#....#.",
            ".##.#..###",
            "##...#..#.",
            ".#....####"","
        )
        pos = get_best_pos(chart)
        self.assertEqual(
            pos,
            (5, 8)
        )
        
        chart = (
            "#.#...#.#.",
            ".###....#.",
            ".#....#...",
            "##.#.#.#.#",
            "....#.#.#.",
            ".##..###.#",
            "..#...##..",
            "..##....##",
            "......#...",
            ".####.###.",
        )
        pos = get_best_pos(chart)
        self.assertEqual(
            pos,
            (1, 2)
        )
        
        chart = (
            ".#..#..###",
            "####.###.#",
            "....###.#.",
            "..###.##.#",
            "##.##.#.#.",
            "....###..#",
            "..#.#..#.#",
            "#..#.#.###",
            ".##...##.#",
            ".....#.#..",
        )
        pos = get_best_pos(chart)
        self.assertEqual(
            pos,
            (6, 3)
        )
    
    def xtest_get_best_pos2(self):
        chart = (
            ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##",
        )

        pos = get_best_pos(chart)
        self.assertEqual(
            pos,
            (11, 13)
        )
        
    def test_vaporisation_order(self):
        chart = (
            "#",
            "X",
            "#",
        )

        order = vaporisation_order(chart)
        self.assertEqual(
            order,
            [(0,0),(0,2)]
        )
        
    def test_vaporisation_order1(self):
        chart = (
            ".#....#####...#..",
            "##...##.#####..##",
            "##...#...#.#####.",
            "..#.....X...###..",
            "..#.#.....#....##",
        )
        
        pos = get_best_pos(chart)
        self.assertEqual(pos, (8,3))
        order = vaporisation_order(chart)
        self.assertEqual(
            order[:3],
            [(8,1),(9,0),(9,1)]
        )
        self.assertEqual(
            order[-3:],
            [(16, 1),(13, 3),(14, 3)]
        )
        
    def test_vaporisation_order_2(self):
        chart = (
            ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##",
        )
        
        pos = get_best_pos(chart)
        order = vaporisation_order(chart)
        self.assertEqual(
            order[:3],
            [(11,12),(12,1),(12,2)]
        )
        self.assertEqual(order[9], (12,8))
        self.assertEqual(order[19], (16,0))
        self.assertEqual(order[199], (8,2))
        self.assertEqual(order[200], (10,9))
        self.assertEqual(order[298], (11,1))
        
