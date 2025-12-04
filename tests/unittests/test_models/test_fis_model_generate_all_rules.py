import unittest

from app.models.fis_model import FISModel


class GenerateAllRulesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_input()
        self.model.add_output()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("input0", "input")
        self.model.add_mf("input0", "input")
        self.model.add_mf("input1", "input")
        self.model.add_mf("input1", "input")
        self.model.add_mf("input1", "input")
        self.model.add_mf("output0", "output")
        self.model.add_mf("output0", "output")
        self.model.add_mf("output0", "output")
        self.model.add_mf("output1", "output")
        self.model.add_mf("output1", "output")
        self.model.add_mf("output1", "output")

    def test_1_is_nr_of_rules_correct_2_inputs(self) -> None:
        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 9, "Wrong nr of rules generated")
        self.assertEqual(result, 1, "Wrong result code returned")

    def test_2_is_nr_of_rules_correct_3_inputs(self) -> None:
        self.model.add_input()
        self.model.add_mf("input2", "input")
        self.model.add_mf("input2", "input")
        self.model.add_mf("input2", "input")
        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 27, "Wrong nr of rules generated")
        self.assertEqual(result, 1, "Wrong result code returned")

    def test_3_is_nr_of_rules_correct_3_outputs(self) -> None:
        self.model.add_output()
        self.model.add_mf("output2", "output")
        self.model.add_mf("output2", "output")
        self.model.add_mf("output2", "output")
        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 9, "Wrong nr of rules generated")
        self.assertEqual(result, 1, "Wrong result code returned")

    def test_4_is_nr_of_rules_correct_some_rules_present(self) -> None:
        self.model.add_rule(None, [2, 3, 2, 3, 1, 1])
        self.model.add_rule(None, [2, 1, 2, 3, 1, 1])
        self.model.add_rule(None, [1, 3, 2, 2, 1, 1])

        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 9, "Wrong nr of rules generated")
        self.assertEqual(result, 1, "Wrong result code returned")

    def test_5_no_output_or_input(self) -> None:
        self.model._fis.Outputs.clear()
        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 0, "Rules incorrectly generated")
        self.assertEqual(result, -1, "Wrong result code returned")

    def test_6_no_mfs(self) -> None:
        self.model._fis.Outputs[0].MembershipFunctions.clear()
        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 0, "Rules incorrectly generated")
        self.assertEqual(result, -2, "Wrong result code returned")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
