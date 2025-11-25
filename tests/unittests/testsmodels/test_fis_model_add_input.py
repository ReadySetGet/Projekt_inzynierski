import unittest

from app.models.fis_model import FISModel


class AddInputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()

    def test_1_input_added(self) -> None:
        nr_inputs = len(self.model._fis.Inputs)
        self.assertEqual(nr_inputs, 0, "Model has inputs upon creation")
        self.model.add_input()
        self.assertEqual(len(self.model._fis.Inputs), 1, "Input not added")

    def test_2_no_mf(self) -> None:
        self.model.add_input()
        self.assertEqual(
            len(self.model._fis.Inputs[0].MembershipFunctions),
            0,
            "Input added with membership functions",
        )

    def test_3_input_name(self) -> None:
        self.model.add_input()
        self.assertEqual(self.model._fis.Inputs[0].Name, "input0", "Wrong name of added input")

    def test_4_input_range(self) -> None:
        self.model.add_input()
        self.assertEqual(self.model._fis.Inputs[0].Range, [0, 1], "Wrong range of added input")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
