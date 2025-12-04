import unittest

from fuzzylab.sugfis import sugfis

from app.models.fis_model import FISModel


class NewSugenoModelCreationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = None

    def test_1_new_sugeno_model_created(self) -> None:
        self.model = FISModel(fis_type="sugeno")
        self.assertNotEqual(self.model, None, "No model created")
        self.assertEqual(type(self.model._fis), sugfis, "Wrong model type created")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
