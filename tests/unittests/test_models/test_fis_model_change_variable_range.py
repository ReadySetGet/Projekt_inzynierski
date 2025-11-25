import unittest

from app.models.fis_model import FISModel


class ChangeVariableRangeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_input()
        self.model.add_output()
        self.model.add_output()

    def test_1_input_variable_range_changed(self) -> None:
        result = self.model.change_variable_range("input0", "input", [-2, 4])
        self.assertEqual(self.model._fis.Inputs[0].Range, [-2, 4],
                         "Range of input variable not changed")
        self.assertEqual(result, 1, "Wrong return value")

    def test_2_output_variable_range_changed(self) -> None:
        result = self.model.change_variable_range("output0", "output", [-3.09, 5.2])
        self.assertEqual(self.model._fis.Outputs[0].Range, [-3.09, 5.2],
                         "Range of output variable not changed")
        self.assertEqual(result, 1, "Wrong return value")

    def test_3_new_range_too_strict(self) -> None:
        result = self.model.change_variable_range("input0", "input", [-2.001, 4])
        self.assertEqual(result, -2, "Range changed incorrectly")
        result = self.model.change_variable_range("input0", "input",
                                                  [-2.09, 4.015])
        self.assertEqual(result, -2, "Range changed incorrectly")

    def test_4_min_higher_than_max(self) -> None:
        result = self.model.change_variable_range("input0", "input", [10, 4])
        self.assertEqual(result, -1, "Range changed incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()