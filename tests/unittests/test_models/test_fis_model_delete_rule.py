import unittest

from app.models.fis_model import FISModel


class DeleteRuleTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")
        self.model.add_rule()

    def test_1_rule_deleted(self) -> None:
        nr_rules = len(self.model._fis.Rules)
        result = self.model.delete_rule(0)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(len(self.model._fis.Rules), nr_rules - 1, "Rule not deleted")

    def test_2_rule_at_idx_deleted(self) -> None:
        self.model.add_rule()
        nr_rules = len(self.model._fis.Rules)
        self.model.delete_rule(0)
        self.assertEqual(len(self.model._fis.Rules), nr_rules - 1, "Rule not deleted")
        self.assertEqual(self.model._fis.Rules[0].Name, "rule1", "Rule at wrong index deleted")

    def test_3_rule_at_given_idx_does_not_exist(self) -> None:
        result = self.model.delete_rule(5)
        self.assertEqual(result, -1, "Rule deleted incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
