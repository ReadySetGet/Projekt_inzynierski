import unittest

from app.models.fis_model import FISModel


class UpdateRuleTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")
        self.model.add_rule()
        self.model.add_rule()

    def test_1_rule_weight_updated(self) -> None:
        self.model.update_rule(0, [1, 1], [1, 1, 0.5, 1])
        self.assertEqual(self.model._fis.Rules[0].Weight, 0.5, "Rule weight not updated")

    def test_2_incorrect_new_weight(self) -> None:
        result = self.model.update_rule(0, [1, 1], [1, 1, 2, 1])
        self.assertEqual(result, -2, "Rule incorrectly updated")
        result = self.model.update_rule(0, [1, 1], [1, 1, -1, 1])
        self.assertEqual(result, -2, "Rule incorrectly updated")

    def test_3_rule_connection_updated(self) -> None:
        self.model.update_rule(0, [1, 1], [1, 1, 1, 0])
        self.assertEqual(self.model._fis.Rules[0].Connection, 0, "Rule connection not updated")

    def test_4_rule_IS_behaviour_for_input_updated(self) -> None:
        self.model.update_rule(0, [0, 1], [1, 1, 1, 1])
        self.assertEqual(
            self.model._fis.Rules[0].IsMFInput,
            [0],
            "Rule IS behaviour for input not updated",
        )

    def test_5_rule_IS_behaviour_for_output_updated(self) -> None:
        self.model.update_rule(0, [1, 0], [1, 1, 1, 1])
        self.assertEqual(
            self.model._fis.Rules[0].IsMFOutput,
            [0],
            "Rule IS behaviour for output not updated",
        )

    def test_6_rule_used_mf_updated(self) -> None:
        self.model.add_mf("input0", "input")
        self.model.update_rule(0, [1, 1], [2, 1, 1, 1])
        self.assertEqual(self.model._fis.Rules[0].Antecedent[0], 2, "Rule mf not updated")

    def test_7_data_of_wrong_length_provided(self) -> None:
        result = self.model.update_rule(0, [1, 1, 1], [1, 1, 1, 1])
        self.assertEqual(result, -3, "Rule incorrectly updated")
        result = self.model.update_rule(0, [1, 1], [1, 1, 1])
        self.assertEqual(result, -3, "Rule incorrectly updated")

    def test_8_rule_with_given_idx_does_not_exist(self) -> None:
        result = self.model.update_rule(5, [1, 1], [1, 1, 1, 1])
        self.assertEqual(result, -1, "Rule incorrectly updated")

    def test_9_incorrect_is_not_for_sugeno_output(self) -> None:
        model_sugeno = FISModel(fis_type="sugeno")
        model_sugeno.add_input()
        model_sugeno.add_output()
        model_sugeno.add_mf("input0", "input")
        model_sugeno.add_mf("output0", "output", "stala")
        model_sugeno.add_rule()
        model_sugeno.add_rule()
        result = model_sugeno.update_rule(0, [1, 0], [1, 1, 1, 1])
        self.assertEqual(result, -4, "Rule incorrectly updated")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
