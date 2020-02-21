import unittest

from .puzzle11 import *


class ComputerTest(unittest.TestCase):
    def test_execute(self):
        intcode = (109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101,
                   1006, 101, 0, 99)
        inputs = []
        outputs = Computer(intcode).execute(inputs)
        self.assertSequenceEqual(outputs, intcode)

        intcode = (1102, 34915192, 34915192, 7, 4, 7, 99, 0)
        inputs = []
        outputs = Computer(intcode).execute(inputs)
        self.assertEqual(len(str(outputs[0])), 16)

        intcode = (104, 1125899906842624, 99)
        inputs = []
        outputs = Computer(intcode).execute(inputs)
        self.assertEqual(outputs[0], 1125899906842624)


class MapTest(unittest.TestCase):
    def test_first_seven(self):
        with open('./puzzle11_input.txt') as f:
            intcode = [int(i) for i in f.read().split('\n')[0].split(',')]

        map = Map()

        map.process_outputs((1, 0))
        self.assertEqual([map.current_direction, map.current_tile],
                         [Map.LEFT, (-1, 0)])

        map.process_outputs((0, 0))
        self.assertEqual(map.current_direction, Map.DOWN)
        self.assertEqual(map.current_tile, (-1, -1))

        map.process_outputs((1, 0))
        map.process_outputs((1, 0))
        self.assertEqual(map.current_direction, Map.UP)
        self.assertEqual(map.current_tile, (0, 0))

        map.process_outputs((0, 1))
        map.process_outputs((1, 0))
        map.process_outputs((1, 0))
        self.assertEqual([map.current_direction, map.current_tile],
                         [Map.LEFT, (0, 1)])

        print(map.tiles)

        self.assertEqual(map.count_multipaint_tiles(), 6)

    def xtest(self):
        steps = 1
        while steps <= 7:
            outputs = computer.execute(map.next_inputs())
            map.process_outputs(outputs)
            steps += 1

        self.assertEqual(map.current_direction, Map.LEFT)
        self.assertEqual(map.current_tile, (0, 1))


class RegressionTest(unittest.TestCase):
    def do_instruction(self, instr, start_index, intcode, input,
                       expected_intcode, expected_next_index, expected_output):
        state = ComputerState()
        state, actual_output = instr(state, intcode, inputs=[input])
        self.assertEqual(expected_next_index, state.index)
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(intcode, expected_intcode)

    def test_jump_if_false(self):
        _jump_if_false = jump_if_false(
            param_1_mode=get_immediate, param_2_mode=get_immediate)

        self.do_instruction(
            _jump_if_false,
            start_index=0,
            intcode=[6, 0, 5],
            input=None,
            expected_intcode=[6, 0, 5],
            expected_next_index=5,
            expected_output=None)

        self.do_instruction(
            _jump_if_false,
            start_index=0,
            intcode=[6, 1, 5],
            input=None,
            expected_intcode=[6, 1, 5],
            expected_next_index=3,
            expected_output=None)

    def test_jump_if_true(self):
        _jump_if_true = jump_if_true(
            param_1_mode=get_immediate, param_2_mode=get_immediate)

        self.do_instruction(
            _jump_if_true,
            start_index=0,
            intcode=[5, 1, 5],
            input=None,
            expected_intcode=[5, 1, 5],
            expected_next_index=5,
            expected_output=None)

        self.do_instruction(
            _jump_if_true,
            start_index=0,
            intcode=[5, 0, 5],
            input=None,
            expected_intcode=[5, 0, 5],
            expected_next_index=3,
            expected_output=None)

    def test_less_than(self):
        _less_than = less_than(
            param_1_mode=get_immediate,
            param_2_mode=get_immediate,
            param_3_mode=get_from_pos)

        self.do_instruction(
            _less_than,
            start_index=0,
            intcode=[7, 1, 5, 0],
            input=None,
            expected_intcode=[1, 1, 5, 0],
            expected_next_index=4,
            expected_output=None)

        self.do_instruction(
            _less_than,
            start_index=0,
            intcode=[7, 5, 0, 1],
            input=None,
            expected_intcode=[7, 0, 0, 1],
            expected_next_index=4,
            expected_output=None)

    def test_equals(self):
        _equals = equals(
            param_1_mode=get_immediate,
            param_2_mode=get_immediate,
            param_3_mode=get_from_pos)

        self.do_instruction(
            _equals,
            start_index=0,
            intcode=[8, 5, 5, 2],
            input=None,
            expected_intcode=[8, 5, 1, 2],
            expected_next_index=4,
            expected_output=None)

        self.do_instruction(
            _equals,
            start_index=0,
            intcode=[8, 5, 0, 2],
            input=None,
            expected_intcode=[8, 5, 0, 2],
            expected_next_index=4,
            expected_output=None)

    def test_take_input(self):
        _take_input = take_input(get_from_pos)
        self.do_instruction(
            _take_input,
            start_index=0,
            intcode=[3, 0],
            input=999,
            expected_intcode=[999, 0],
            expected_next_index=2,
            expected_output=None)

    def test_output_op(self):
        _output_op = output_op(get_immediate)
        self.do_instruction(
            _output_op,
            start_index=0,
            intcode=[4, 0],
            input=None,
            expected_intcode=[4, 0],
            expected_next_index=2,
            expected_output=0)
        # diagnostic
        self.do_instruction(
            _output_op,
            start_index=0,
            intcode=[4, 4, 99],
            input=None,
            expected_intcode=[4, 4, 99],
            expected_next_index=2,
            expected_output=4)

        _output_op = output_op(get_from_pos)
        self.do_instruction(
            _output_op,
            start_index=0,
            intcode=[4, 2, 99],
            input=None,
            expected_intcode=[4, 2, 99],
            expected_next_index=2,
            expected_output=99)

