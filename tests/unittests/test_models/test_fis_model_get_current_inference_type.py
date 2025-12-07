import unittest

import fuzzylab as fl

from app.models.fis_model import FISModel


class GetCurrentInferenceTypeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_1_correct_inference_type_mamdani(self) -> None:
        self.model = FISModel(fis_type="mamdani")
        fis_type = self.model.get_current_inference_type()
        self.assertEqual(fis_type, fl.mamfis, "Wrong type returned")

    def test_2_correct_inference_type_sugeno(self) -> None:
        self.model = FISModel(fis_type="sugeno")
        fis_type = self.model.get_current_inference_type()
        self.assertEqual(fis_type, fl.sugfis, "Wrong type returned")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
