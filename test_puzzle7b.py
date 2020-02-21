import unittest

from .puzzle7b import *

class Test(unittest.TestCase):
    def test_execute_pt2b(self):
        # output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
        amp = Amp(initial_intcode=[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        outputs = amp.execute([7])
        print(amp.index)
        self.assertEqual(outputs, 999)
        
        outputs = Amp(initial_intcode=[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).execute([8])
        self.assertEqual(outputs, 1000)
        
        outputs = Amp(initial_intcode=[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).execute([9])
        self.assertEqual(outputs, 1001)

    def test_calc_thrust(self):
        intcode = (
            3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
        )
        settings = [9,8,7,6,5]
        thrust = calc_thrust(intcode, settings)
        self.assertEqual(thrust, 139629729)
        
        intcode = (
            3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
        )
        settings = [9,7,8,5,6]
        thrust = calc_thrust(intcode, settings)
        self.assertEqual(thrust, 18216)

        
    def xtest_settings_for_max_thrust(self):
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

