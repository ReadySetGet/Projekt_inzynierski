import unittest

from app.models.fis_model import FISModel


class ReturnAllInputVariablesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_input()
        self.model.add_output()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")
        self.model.add_mf("output0", "output")

    def test_1_return_all_mfs_of_input_variable(self) -> None:
        input_mfs = self.model.return_all_mfs_of_io_variable("input0", "input")
        self.assertEqual(len(input_mfs), 2, "Not all mfs returned")

    def test_2_return_all_mfs_of_output_variable(self) -> None:
        output_mfs = self.model.return_all_mfs_of_io_variable("output0", "output")
        self.assertEqual(len(output_mfs), 2, "Not all mfs returned")

    def test_3_no_mfs(self) -> None:
        input_mfs = self.model.return_all_mfs_of_io_variable("input1", "input")
        self.assertEqual(len(input_mfs), 0, "Nonexistent mfs returned")

    def test_4_nonexistent_variable(self) -> None:
        input_mfs = self.model.return_all_mfs_of_io_variable("input2", "input")
        self.assertEqual(input_mfs, None, "Nonexistent variable found")

    def test_5_nonexistent_variable_type(self) -> None:
        input_mfs = self.model.return_all_mfs_of_io_variable("input0", "tak")
        self.assertEqual(input_mfs, None, "Nonexistent variable type found")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
