import unittest

from app.models.fis_model import FISModel


class ChangeDefuzzificationMethodTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()

    def test_1_defuzz_method_changed(self) -> None:
        result = self.model.change_defuzzification_method("mom")
        self.assertEqual(self.model._fis.DefuzzificationMethod, "mom", "Defuzzification method not changed")
        self.assertEqual(result, 1, "Wrong return value")

    def test_2_unavailable_defuzz_method(self) -> None:
        result = self.model.change_defuzzification_method("whatever")
        self.assertEqual(result, -1, "Defuzzification method incorrectly changed")

    def test_3_defuzz_method_incorrect_for_inference_used(self) -> None:
        result = self.model.change_defuzzification_method("wtaver")
        self.assertEqual(result, -1, "Defuzzification method incorrectly changed")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
