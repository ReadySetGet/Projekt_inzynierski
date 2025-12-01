import unittest

from app.models.fis_model import FISModel


class ChangeMFParametersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel(fis_type="sugeno")
        self.model.add_input()
        self.model.add_mf("input0", "input")
        self.model.add_mf("input1", "input")

    def test_1_mf_parameters_changed(self) -> None:
        result = self.model.change_mf_parameters("input0", "input", 0, [1, 2, 3])
        self.assertEqual(result, 1, "Wrong result value")
        self.assertEqual(
            self.model._fis.Inputs[0].MembershipFunctions[0].Parameters, [1, 2, 3], "Wrong parameters of MF"
        )

    def test_2_mf_parameters_of_wrong_length(self) -> None:
        result = self.model.change_mf_parameters("input0", "input", 0, [1])
        self.assertEqual(result, -3, "Parameters changed incorrectly")

    def test_3_single_parameter_for_constant_sugeno(self) -> None:
        self.model.add_output()
        self.model.add_mf("output0", "output", "stala")
        result = self.model.change_mf_parameters("output0", "output", 0, 1)
        self.assertEqual(result, 1, "Wrong result value")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0].Parameters, 1, "Wrong parameters of mf")

    def test_4_mf_with_given_idx_does_not_exist(self) -> None:
        self.model.add_output()
        self.model.add_mf("output0", "output", "stala")
        result = self.model.change_mf_parameters("output0", "output", 5, 1)
        self.assertEqual(result, -1, "Parameters changed incorrectly")

    def test_5_io_variable_not_found(self) -> None:
        result = self.model.change_mf_parameters("output1", "output", 0, 1)
        self.assertEqual(result, -2, "Parameters changed incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
