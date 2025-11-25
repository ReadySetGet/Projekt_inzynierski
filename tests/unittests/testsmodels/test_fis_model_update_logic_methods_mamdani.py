import unittest

from app.models.fis_model import FISModel


class UpdateLogicMethodsMamdaniTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel(fis_type="mamdani")

    def test_1_and_method_updated(self) -> None:
        result = self.model.update_logic_methods(and_method="prod")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertEqual(self.model._fis.AndMethod, "prod",
                         "And method not updated")

    def test_2_or_method_updated(self) -> None:
        result = self.model.update_logic_methods(or_method="probor")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertEqual(self.model._fis.OrMethod, "probor",
                         "Or method not updated")

    def test_3_imp_method_updated(self) -> None:
        result = self.model.update_logic_methods(imp_method="prod")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertEqual(self.model._fis.ImplicationMethod, "prod",
                         "Implication method not updated")

    def test_4_agg_method_updated(self) -> None:
        result = self.model.update_logic_methods(agg_method="sum")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertEqual(self.model._fis.AggregationMethod, "sum",
                         "Aggregation method not updated")

    def test_5_wrong_method_provided(self) -> None:
        result = self.model.update_logic_methods(agg_method="prod")
        self.assertEqual(result, -1, "Method updated incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()
