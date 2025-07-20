import unittest

from app.models.fis_model import FISModel


class AddOutputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()

    def test_1_output_added(self) -> None:
        nr_outputs = len(self.model._fis.Outputs)
        self.assertEqual(nr_outputs, 0, "Model has outputs upon creation")
        self.model.add_output()
        self.assertEqual(len(self.model._fis.Outputs), 1, "Output not added")

    def test_2_no_mf(self) -> None:
        self.model.add_output()
        self.assertEqual(len(self.model._fis.Outputs[0].MembershipFunctions), 0,
                         "Output added with membership functions")

    def test_3_output_name(self) -> None:
        self.model.add_output()
        self.assertEqual(self.model._fis.Outputs[0].Name, "output0",
                         "Wrong name of added output")

    def test_4_output_range(self) -> None:
        self.model.add_output()
        self.assertEqual(self.model._fis.Outputs[0].Range, [0, 1],
                         "Wrong range of added output")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()
