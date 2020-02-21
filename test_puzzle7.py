import unittest

from .puzzle7 import *

class Test(unittest.TestCase):
    def test_calc_thrust(self):
        intcode = (
            3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
        )
        settings = [4,3,2,1,0]
        thrust = calc_thrust(intcode, settings)
        self.assertEqual(thrust, 43210)
        
        intcode = (
            3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
        )
        settings = [0,1,2,3,4]
        thrust = calc_thrust(intcode, settings)
        self.assertEqual(thrust, 54321)
        
        intcode = (
            3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
        )
        settings = [1,0,4,3,2]
        thrust = calc_thrust(intcode, settings)
        self.assertEqual(thrust, 65210)
        
    def test_settings_for_max_thrust(self):
        intcode = (
            3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
        )
        settings = settings_for_max_thrust(intcode)
        self.assertEqual(settings, [4,3,2,1,0])
        
        intcode = (
            3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
        )
        
        settings = settings_for_max_thrust(intcode)
        self.assertEqual(settings, [0,1,2,3,4])
        
        intcode = (
            3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
        )
        
        settings = settings_for_max_thrust(intcode)
        self.assertEqual(settings, [1,0,4,3,2])

