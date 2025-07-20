import unittest

from app.models.fis_model import FISModel


class AddMFTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()

    def test_1_mf_added_to_input(self) -> None:
        nr_mfs = len(self.model._fis.Inputs[0].MembershipFunctions)
        self.assertEqual(nr_mfs, 0, "Input has MFs upon creation")
        self.model.add_mf("input0", "input")
        self.assertEqual(len(self.model._fis.Inputs[0].MembershipFunctions),
                         nr_mfs + 1, "MF not added to input")

    def test_2_mf_added_to_output(self) -> None:
        nr_mfs = len(self.model._fis.Outputs[0].MembershipFunctions)
        self.assertEqual(nr_mfs, 0, "Output has MFs upon creation")
        self.model.add_mf("output0", "output")
        self.assertEqual(len(self.model._fis.Outputs[0].MembershipFunctions),
                         nr_mfs + 1, "MF not added to output")

    def test_3_mf_name_input(self) -> None:
        self.model.add_mf("input0", "input")
        self.assertEqual(self.model._fis.Inputs[0].MembershipFunctions[0].Name,
                         "mf0", "Wrong name of MF added to input")

    def test_4_mf_parameters_input(self) -> None:
        self.model.add_mf("input0", "input")
        self.assertEqual(self.model._fis.Inputs[0].MembershipFunctions[0]
                         .Parameters, [0, 0.5, 1],
                         "Wrong parameters of MF added to input")

    def test_5_mf_type_input(self) -> None:
        self.model.add_mf("input0", "input")
        self.assertEqual(self.model._fis.Inputs[0].MembershipFunctions[0]
                         .Type, "trimf", "Wrong type of MF added to input")

    def test_6_mf_name_output(self) -> None:
        self.model.add_mf("output0", "output")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0].Name,
                         "mf0", "Wrong name of MF added to output")

    def test_7_mf_parameters_output(self) -> None:
        self.model.add_mf("output0", "output")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0]
                         .Parameters, [0, 0.5, 1],
                         "Wrong parameters of MF added to output")

    def test_8_mf_type_output(self) -> None:
        self.model.add_mf("output0", "output")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0]
                         .Type, "trimf", "Wrong type of MF added to output")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()