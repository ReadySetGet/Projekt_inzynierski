import unittest

from fuzzylab.sugfis import sugfis

from app.models.fis_model import FISModel


class ConvertInferenceSystemMamdaniToSugenoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model_mamdani = FISModel(fis_type="mamdani")
        self.model_mamdani.add_input()
        self.model_mamdani.add_mf("input0", "input")
        self.model_mamdani.add_output()
        self.model_mamdani.add_mf("output0", "output")
        self.model_mamdani.add_rule([0, 0], [1, 1, 1, 1])

    def test_1_convert_from_mamdani_to_sugeno(self) -> None:
        new_model = self.model_mamdani.convert_inference_system("new_model")
        self.assertNotEqual(new_model, None, "Conversion failed")
        self.assertEqual(new_model._fis.Name, "new_model", "Wrong name")
        self.assertEqual(type(new_model._fis), sugfis, "Wrong type of fis")
        self.assertEqual(new_model._fis.Rules[0].IsMFOutput, [1], "IS NOT not changed")
        self.assertEqual(new_model._fis.Outputs[0].MembershipFunctions[0].Parameters, 0.5, "Wrong parameter conversion")

    def tearDown(self) -> None:
        del self.model_mamdani


if __name__ == "__main__":
    unittest.main()
