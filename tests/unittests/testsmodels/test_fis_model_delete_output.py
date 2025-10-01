import unittest

from app.models.fis_model import FISModel


class DeleteOutputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_output()

    def test_1_output_deleted(self) -> None:
        nr_outputs = len(self.model._fis.Outputs)
        self.model.delete_output(0)
        self.assertEqual(
            len(self.model._fis.Outputs), nr_outputs - 1, "Output not deleted"
        )

    def test_2_output_at_idx_deleted(self) -> None:
        self.model.add_output()
        nr_outputs = len(self.model._fis.Outputs)
        self.model.delete_output(0)
        self.assertEqual(
            len(self.model._fis.Outputs), nr_outputs - 1, "Output not deleted"
        )
        self.assertEqual(
            self.model._fis.Outputs[0].Name, "output1", "Output at wrong index deleted"
        )

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
