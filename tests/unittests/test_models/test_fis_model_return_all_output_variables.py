import unittest

from app.models.fis_model import FISModel


class ReturnAllOutputVariablesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")

    def test_1_return_all_output_variables(self) -> None:
        output_vars = self.model.return_all_output_variables()
        self.assertEqual(len(output_vars), 2,
                         "Not all outputs returned")
        self.assertEqual(len(output_vars[0].MembershipFunctions), 1,
                         "Outputs returned without mfs")

    def test_2_no_outputs(self) -> None:
        self.model.delete_output(0)
        self.model.delete_output(0)
        output_vars = self.model.return_all_output_variables()
        self.assertEqual(len(output_vars), 0,
                         "Nonexistent outputs returned")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()
