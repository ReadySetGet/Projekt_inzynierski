import unittest

from app.models.fis_model import FISModel


class DeleteOutputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_output()

    def test_1_output_deleted(self) -> None:
        nr_outputs = len(self.model._fis.Outputs)
        result = self.model.delete_output(0)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(len(self.model._fis.Outputs), nr_outputs - 1, "Output not deleted")

    def test_2_output_at_idx_deleted(self) -> None:
        self.model.add_output()
        nr_outputs = len(self.model._fis.Outputs)
        self.model.delete_output(0)
        self.assertEqual(len(self.model._fis.Outputs), nr_outputs - 1, "Output not deleted")
        self.assertEqual(self.model._fis.Outputs[0].Name, "output1", "Output at wrong index deleted")

    def test_3_output_with_given_idx_does_not_exist(self) -> None:
        result = self.model.delete_output(5)
        self.assertEqual(result, -1, "Output deleted incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
