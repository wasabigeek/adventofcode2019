import unittest

from .puzzle5 import *


class Test(unittest.TestCase):
    def do_instruction(self, instr, start_index, intcode, input, expected_intcode, expected_next_index, expected_output):
        actual_next, actual_output = instr(start_index, intcode, input=input)
        self.assertEqual(expected_next_index, actual_next)
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(intcode, expected_intcode)

    def xtest_execute_op_3_4(self):
        input = 999
        intcode = [3,0,4,0,99]

        expected_output = [999]
        expected_intcode = [999,0,4,0,99]
        actual_intcode, actual_output = execute(intcode, input)
        self.assertEqual(
            expected_intcode, actual_intcode
        )
        self.assertEqual(
            expected_output, actual_output
        )

    def xtest_execute_param_modes(self):
        input = 999
        intcode = [1002,4,3,4,33]

        expected_output = []
        expected_intcode = [1002,4,3,4,99]
        actual_intcode, actual_output = execute(intcode, input)
        self.assertEqual(
            expected_intcode, actual_intcode
        )
        self.assertEqual(
            expected_output, actual_output
        )

    def xtest_pt_1(self):
        puzzle = [
        3,225,1,225,6,6,1100,1,238,225,104,0,1102,27,28,225,1,113,14,224,1001,224,-34,224,4,224,102,8,223,223,101,7,224,224,1,224,223,223,1102,52,34,224,101,-1768,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1002,187,14,224,1001,224,-126,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,54,74,225,1101,75,66,225,101,20,161,224,101,-54,224,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,6,30,225,2,88,84,224,101,-4884,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1001,214,55,224,1001,224,-89,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1101,34,69,225,1101,45,67,224,101,-112,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,9,81,225,102,81,218,224,101,-7290,224,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1101,84,34,225,1102,94,90,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,677,677,224,102,2,223,223,1005,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,359,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,374,101,1,223,223,108,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,404,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,449,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,464,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,509,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,539,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,554,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,569,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,584,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,599,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,629,101,1,223,223,7,226,226,224,102,2,223,223,1006,224,644,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,659,101,1,223,223,108,677,677,224,102,2,223,223,1005,224,674,1001,223,1,223,4,223,99,226
        ]
        
        _, outputs = execute(puzzle, 1)
        self.assertEqual(outputs, [16348437])
    
    def test_execute_pt2(self):
        # 1 if equals 8 else zero
        _, outputs = execute([3,9,8,9,10,9,4,9,99,-1,8], 1)
        self.assertEqual(outputs, 0)
        
        _, outputs = execute([3,3,1108,-1,8,3,4,3,99], 1)
        self.assertEqual(outputs, 0)
        
        _, outputs = execute([3,9,8,9,10,9,4,9,99,-1,8], 8)
        self.assertEqual(outputs, 1)
        
        _, outputs = execute([3,3,1108,-1,8,3,4,3,99], 8)
        self.assertEqual(outputs, 1)
        
    def test_execute_pt2aa(self):
        # 1 if less than 8, else 0
        _, outputs = execute([3,9,7,9,10,9,4,9,99,-1,8], 1)
        self.assertEqual(outputs, 1)
        
        _, outputs = execute([3,9,7,9,10,9,4,9,99,-1,8], 9)
        self.assertEqual(outputs, 0)
        
        _, outputs = execute([3,3,1107,-1,8,3,4,3,99], 7)
        self.assertEqual(outputs, 1)
        
        _, outputs = execute([3,3,1107,-1,8,3,4,3,99], 9)
        self.assertEqual(outputs, 0)
        
        # one if input is non-zero
        _, outputs = execute([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 9)
        self.assertEqual(outputs, 1)
    
        _, outputs = execute([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0)
        self.assertEqual(outputs, 0)
        
        _, outputs = execute([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0)
        self.assertEqual(outputs, 0)
        
        _, outputs = execute([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], -55)
        self.assertEqual(outputs, 1)
        
    def test_execute_pt2b(self):
        # output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
        _, outputs = execute([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7)
        self.assertEqual(outputs, 999)
        
        _, outputs = execute([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8)
        self.assertEqual(outputs, 1000)
        
        _, outputs = execute([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9)
        self.assertEqual(outputs, 1001)


    def xtest_execute_negative(self):
        input = 999
        intcode = [1101,100,-1,4,0]

        expected_output = []
        expected_intcode = [1101,100,-1,4,99]
        actual_intcode, actual_output = execute(intcode, input)
        self.assertEqual(
            expected_intcode, actual_intcode
        )
        self.assertEqual(
            expected_output, actual_output
        )

    def test_take_input(self):
        self.do_instruction(
            take_input,
            start_index=0,
            intcode=[3, 0],
            input=999,
            expected_intcode=[999, 0], expected_next_index=2, expected_output=None)

        
    def test_output_op(self):
        _output_op = output_op(get_immediate)
        self.do_instruction(
            _output_op,
            start_index=0,
            intcode=[4, 0],
            input=None,
            expected_intcode=[4, 0], expected_next_index=2, expected_output=0)
        # diagnostic
        self.do_instruction(
            _output_op,
            start_index=0,
            intcode=[4, 4, 99],
            input=None,
            expected_intcode=[4, 4, 99], expected_next_index=2, expected_output=4)
            
        _output_op = output_op(get_from_pos)
        self.do_instruction(
            _output_op,
            start_index=0,
            intcode=[4, 2, 99],
            input=None,
            expected_intcode=[4, 2, 99], expected_next_index=2, expected_output=99)
        

    def test_jump_if_false(self):
        _jump_if_false = jump_if_false(param_1_mode=get_immediate, param_2_mode=get_immediate)
        
        intcode = [6, 0, 5]
        expected_intcode = [6, 0, 5]
        expected_next = 5
        expected_output = None
        
        actual_next, actual_output = _jump_if_false(0, intcode)
        self.assertEqual(expected_next, actual_next)
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(intcode, expected_intcode)
        
        intcode = [6, 1, 5]
        expected_intcode = [6, 1, 5]
        expected_next = 3
        expected_output = None
        
        actual_next, actual_output = _jump_if_false(0, intcode)
        self.assertEqual(expected_next, actual_next)
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(intcode, expected_intcode)
    
    def xtest_jump_if_true(self):
        _jump_if_true = jump_if_true(param_1_mode=get_immediate, param_2_mode=get_immediate)

        self.do_instruction(
            _jump_if_true,
            start_index=0,
            intcode=[5, 1, 5],
            input=None,
            expected_intcode=[5, 1, 5], expected_next_index=5, expected_output=None)
            
        self.do_instruction(
            _jump_if_true,
            start_index=0,
            intcode=[5, 0, 5],
            input=None,
            expected_intcode=[5, 0, 5], expected_next_index=3, expected_output=None)

    def xtest_less_than(self):
        _less_than = less_than(param_1_mode=get_immediate, param_2_mode=get_immediate)

        self.do_instruction(
            _less_than,
            start_index=0,
            intcode=[7, 1, 5, 0],
            input=None,
            expected_intcode=[1, 1, 5, 0], expected_next_index=4, expected_output=None)
            
        self.do_instruction(
            _less_than,
            start_index=0,
            intcode=[7, 5, 0, 1],
            input=None,
            expected_intcode=[7, 0, 0, 1], expected_next_index=4, expected_output=None)
        
    def xtest_equals(self):
        _equals = equals(param_1_mode=get_immediate, param_2_mode=get_immediate)

        self.do_instruction(
            _equals,
            start_index=0,
            intcode=[8, 5, 5, 2],
            input=None,
            expected_intcode=[8, 5, 1, 2], expected_next_index=4, expected_output=None)
            
        self.do_instruction(
            _equals,
            start_index=0,
            intcode=[8, 5, 0, 2],
            input=None,
            expected_intcode=[8, 5, 0, 2], expected_next_index=4, expected_output=None)
