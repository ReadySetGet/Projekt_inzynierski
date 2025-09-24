import unittest

from app.models.fis_model import FISModel


class ReturnAllRulesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_mf("input0", "input")
        self.model.add_output()
        self.model.add_mf("output0", "output")
        self.nr_rules = 10

    def test_1_no_rules(self) -> None:
        rules = self.model.return_all_rules()
        self.assertEqual(len(rules), 0, "Wrong length of rule list")

    def test_2_single_rule(self) -> None:
        result = self.model.add_rule([1, 1], [1, 1, 1, 1])
        self.assertEqual(result, 1, "Issues with rule adding")
        rules = self.model.return_all_rules()
        self.assertEqual(len(rules), 1, "Wrong length of rule list")

    def test_3_multiple_rules(self) -> None:
        for i in range(self.nr_rules):
            result = self.model.add_rule([1, 1], [1, 1, 1, 1])
            self.assertEqual(result, 1, "Issues with rule adding")
        rules = self.model.return_all_rules()
        self.assertEqual(len(rules), self.nr_rules,
                         "Wrong length of rule list")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()
