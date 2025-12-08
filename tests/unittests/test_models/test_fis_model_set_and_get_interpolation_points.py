import unittest

from app.models.fis_model import FISModel


class SetGetInterpolationPointsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()

    def test_1_default_value_correct(self) -> None:
        self.assertEqual(self.model._interpolation_points_nr, 100, "Problems with default value")

    def test_2_set_interpolation_points_number(self) -> None:
        result = self.model.set_interpolation_points(999)
        self.assertEqual(result, 1, "Problems with return value")
        self.assertEqual(self.model._interpolation_points_nr, 999, "Interpolation points not set")

    def test_3_set_interpolation_points_too_high(self) -> None:
        result = self.model.set_interpolation_points(1001)
        self.assertEqual(result, -1, "Problems with return value")
        self.assertEqual(self.model._interpolation_points_nr, 100, "Interpolation points set incorrectly")

    def test_4_set_interpolation_points_number_too_low(self) -> None:
        result = self.model.set_interpolation_points(3)
        self.assertEqual(result, -1, "Problems with return value")
        self.assertEqual(self.model._interpolation_points_nr, 100, "Interpolation points set incorrectly")

    def test_5_get_interpolation_points_number(self) -> None:
        points = self.model.get_interpolation_points()
        self.assertEqual(points, 100, "Wrong number of interpolation points received")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
