import unittest

from fuzzylab.mamfis import mamfis

from app.models.fis_model import FISModel


class ConvertInferenceSystemSugenoToMamdaniTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model_sugeno = FISModel(fis_type="sugeno")
        self.model_sugeno.add_input()
        self.model_sugeno.add_mf("input0", "input")
        self.model_sugeno.add_output()
        self.model_sugeno.add_mf("output0", "output", "stala")
        self.model_sugeno.add_rule([0, 1], [1, 1, 1, 1])

    def test_1_convert_from_sugeno_to_mamdani(self) -> None:
        new_model = self.model_sugeno.convert_inference_system("new_model")
        self.assertNotEqual(new_model, None, "Conversion failed")
        self.assertEqual(new_model._fis.Name, "new_model", "Wrong name")
        self.assertEqual(type(new_model._fis), mamfis, "Wrong type of fis")

    def tearDown(self) -> None:
        del self.model_sugeno


if __name__ == "__main__":
    unittest.main()
