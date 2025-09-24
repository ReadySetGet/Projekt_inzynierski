import unittest

from app.models.fis_model import FISModel


class ReturnSystemNameTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_1_return_system_name_set(self) -> None:
        self.model = FISModel(fis_name="name")
        name = self.model.return_system_name()
        self.assertEqual(name, "name", "Wrong name returned")

    def test_1_return_system_name_default(self) -> None:
        self.model = FISModel()
        name = self.model.return_system_name()
        self.assertEqual(name, "fis", "Wrong name returned")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()
