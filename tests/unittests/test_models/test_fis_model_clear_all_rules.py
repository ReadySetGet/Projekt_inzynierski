import unittest

from app.models.fis_model import FISModel


class ClearAllRulesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")
        for _ in range(10):  # nr of rules to be cleared
            self.model.add_rule()

    def test_1_all_rules_deleted(self) -> None:
        self.model.clear_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 0, "Not all rules deleted")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
