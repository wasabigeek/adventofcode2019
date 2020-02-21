import unittest

from .puzzle12 import *


class GravityTest(unittest.TestCase):
    def test_calculate_gravity_from_coords(self):
        coord1 = 5
        coord2 = 3
        gravity = calc_grav_coords(coord1, coord2)
        self.assertEqual(gravity, (-1, 1))

        coord1 = 3
        coord2 = 3
        gravity = calc_grav_coords(coord1, coord2)
        self.assertEqual(gravity, (0, 0))

        coord1 = 3
        coord2 = 5
        gravity = calc_grav_coords(coord1, coord2)
        self.assertEqual(gravity, (1, -1))

        coord1 = -1
        coord2 = 3
        gravity = calc_grav_coords(coord1, coord2)
        self.assertEqual(gravity, (1, -1))

    def test_calculate_gravity_deltas(self):
        delta1, delta2 = calc_grav_deltas(
            Moon(position=(5, 3, 5)), Moon(position=(3, 5, 5)))
        self.assertEqual(delta2, (1, -1, 0))
        self.assertEqual(delta1, (-1, 1, 0))

class UpdateMoonsTest(unittest.TestCase):
    def setUp(self):
        self.moons = (Moon(position=(-1, 0, 2)), Moon(position=(2, -10, -7)), Moon(position=(4, -8, 8)), Moon(position=(3, 5, -1)))

    def test_update_moons(self):
        moon1, moon2, moon3, moon4 = update_moons(self.moons, steps=0)
        self.assertEqual(moon1.position, (-1, 0, 2))

        moon1, moon2, moon3, moon4 = update_moons(self.moons, steps=1)
        self.assertEqual(moon1.position, (2, -1, 1))
        self.assertEqual(moon1.velocity, (3, -1, -1))

        self.assertEqual(moon2.position, (3, -7, -4))
        self.assertEqual(moon2.velocity, (1, 3, 3))
        
        self.assertEqual(moon3.position, (1, -7, 5))
        self.assertEqual(moon3.velocity, (-3, 1, -3))
        
        self.assertEqual(moon4.position, (2, 2, 0))
        self.assertEqual(moon4.velocity, (-1, -3, 1))
        
    def test_2_steps(self):
        moon1, moon2, moon3, moon4 = update_moons(self.moons, steps=2)
        self.assertEqual(moon1.position, (5, -3, -1))
        self.assertEqual(moon1.velocity, (3, -2, -2))

    def test_10_steps(self):
        moon1, moon2, moon3, moon4 = update_moons(self.moons, steps=10)
        self.assertEqual(moon1.position, (2, 1, -3))
        self.assertEqual(moon1.velocity, (-3, -2, 1))
        
        self.assertEqual(
            calculate_energy(self.moons),
            179
        )

class RepeatTest(unittest.TestCase):
    def test_repeat(self):
        moons = (Moon(position=(-1, 0, 2)), Moon(position=(2, -10, -7)), Moon(position=(4, -8, 8)), Moon(position=(3, 5, -1)))
        
        steps = calculate_repeat(moons)
        self.assertEqual(steps, 2772)
        
    def test_repeat_b(self):
        moons = (Moon(position=(-8, -10, 0)), Moon(position=(5, 5, 10)), Moon(position=(2, -7, 3)), Moon(position=(9, -8, -3)))
        
        steps = calculate_repeat(moons)
        self.assertEqual(steps, 4686774924)

