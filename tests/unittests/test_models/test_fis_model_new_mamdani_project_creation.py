import unittest

from fuzzylab.mamfis import mamfis

from app.models.fis_model import FISModel


class NewMamdaniModelCreationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = None

    def test_1_new_sugeno_model_created(self) -> None:
        self.model = FISModel(fis_type="mamdani")
        self.assertNotEqual(self.model, None, "No model created")
        self.assertEqual(type(self.model._fis), mamfis, "Wrong model type created")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
