import unittest

from app.models.fis_model import FISModel


class DeleteInputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()

    def test_1_input_deleted(self) -> None:
        nr_inputs = len(self.model._fis.Inputs)
        result = self.model.delete_input(0)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(len(self.model._fis.Inputs), nr_inputs - 1, "Input not deleted")

    def test_2_input_at_idx_deleted(self) -> None:
        self.model.add_input()
        nr_inputs = len(self.model._fis.Inputs)
        self.model.delete_input(0)
        self.assertEqual(len(self.model._fis.Inputs), nr_inputs - 1, "Input not deleted")
        self.assertEqual(self.model._fis.Inputs[0].Name, "input1", "Input at wrong index deleted")

    def test_3_input_with_given_idx_does_not_exist(self) -> None:
        result = self.model.delete_input(5)
        self.assertEqual(result, -1, "Input deleted incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
