import unittest

from app.models.fis_model import FISModel


class ChangeMFTypeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_output()
        self.model.add_mf("output0", "output")

    def test_1_mf_type_changed(self) -> None:
        result = self.model.change_mf_type("output0", "output", 0, "gaussowska")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            self.model._fis.Outputs[0].MembershipFunctions[0].Type,
            "gaussmf",
            "Wrong type of MF",
        )

    def test_2_mf_parameters_adequate_to_type(self) -> None:
        self.model.change_mf_type("output0", "output", 0, "gaussowska")
        self.assertEqual(
            self.model._fis.Outputs[0].MembershipFunctions[0].Parameters,
            [0.3196, 1.2467],
            "Wrong MF parameters",
        )

    def test_3_mf_with_given_idx_does_not_exist(self) -> None:
        result = self.model.change_mf_type("output0", "output", 5, "gaussowska")
        self.assertEqual(result, -1, "Type changed incorrectly")

    def test_4_io_variable_not_found(self) -> None:
        result = self.model.change_mf_type("output2", "output", 0, "gaussowska")
        self.assertEqual(result, -2, "Type changed incorrectly")

    def test_5_wrong_mf_type(self) -> None:
        result = self.model.change_mf_type("output0", "output", 0, "jakaś")
        self.assertEqual(result, -3, "Type changed incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
