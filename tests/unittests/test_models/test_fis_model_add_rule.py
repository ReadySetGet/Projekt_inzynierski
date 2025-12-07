import unittest

from app.models.fis_model import FISModel


class AddRuleTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")

    def test_1_rule_added(self) -> None:
        result = self.model.add_rule()
        self.assertEqual(result, 1, "Rule not added correctly")
        self.assertEqual(len(self.model._fis.Rules), 1, "Rule not added to fis")

    def test_2_rule_name(self) -> None:
        self.model.add_rule()
        self.assertEqual(self.model._fis.Rules[0].Name, "rule0", "Wrong name of rule")

    def test_3_rule_antecedent(self) -> None:
        self.model.add_input()
        self.model.add_mf("input1", "input")
        self.model.add_rule()
        self.assertEqual(self.model._fis.Rules[0].Antecedent, [1, 0], "Wrong antecedent of the rule")

    def test_4_rule_consequent(self) -> None:
        self.model.add_output()
        self.model.add_mf("output1", "output")
        self.model.add_rule()
        self.assertEqual(self.model._fis.Rules[0].Consequent, [1, 0], "Wrong consequent of the rule")

    def test_5_rule_weight(self) -> None:
        self.model.add_rule()
        self.assertEqual(self.model._fis.Rules[0].Weight, 1, "Wrong rule weight")

    def test_6_rule_connection(self) -> None:
        self.model.add_rule()
        self.assertEqual(self.model._fis.Rules[0].Connection, 1, "Wrong rule connection")

    def test_7_rule_IS_behaviour_input(self) -> None:
        self.model.add_input()
        self.model.add_mf("input1", "input")
        self.model.add_rule()
        self.assertEqual(
            self.model._fis.Rules[0].IsMFInput,
            [1, 1],
            "Wrong rule input variable to mf mapping behaviour",
        )

    def test_8_rule_IS_behaviour_output(self) -> None:
        self.model.add_output()
        self.model.add_mf("output1", "output")
        self.model.add_rule()
        self.assertEqual(
            self.model._fis.Rules[0].IsMFOutput,
            [1, 1],
            "Wrong rule output variable to mf mapping behaviour",
        )

    def test_9_rule_not_added_without_mfs_input(self) -> None:
        self.model.add_input()
        result = self.model.add_rule()
        self.assertEqual(result, -2, "Rule was incorrectly added - input without MF")

    def test_10_rule_not_added_without_mfs_output(self) -> None:
        self.model.add_output()
        result = self.model.add_rule()
        self.assertEqual(result, -2, "Rule was incorrectly added - output without MF")

    def test_11_all_io_set_to_none(self) -> None:
        result = self.model.add_rule(rule_data=[0, 0, 1, 1])
        self.assertEqual(result, -1, "Rule was incorrectly added - mfs set to None")

    def test_12_is_not_in_sugeno_output(self) -> None:
        model_sugeno = FISModel(fis_type="sugeno")
        model_sugeno.add_input()
        model_sugeno.add_output()
        model_sugeno.add_mf("input0", "input")
        model_sugeno.add_mf("output0", "output", "stala")
        result = model_sugeno.add_rule(is_mf=[1, 0], rule_data=[1, 1, 1, 1])
        self.assertEqual(result, -3, "Rule was incorrectly added - is not set in Sugeno output")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
