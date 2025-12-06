import unittest

from app.models.fis_model import FISModel


class ReturnAllInputVariablesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_input()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")

    def test_1_return_all_input_variables(self) -> None:
        input_vars = self.model.return_all_input_variables()
        self.assertEqual(len(input_vars), 2, "Not all inputs returned")
        self.assertEqual(len(input_vars[0].MembershipFunctions), 1, "Inputs returned without mfs")

    def test_2_no_inputs(self) -> None:
        self.model.delete_input(0)
        self.model.delete_input(0)
        input_vars = self.model.return_all_input_variables()
        self.assertEqual(len(input_vars), 0, "Nonexistent inputs returned")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
