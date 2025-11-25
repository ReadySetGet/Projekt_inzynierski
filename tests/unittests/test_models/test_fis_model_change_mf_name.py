import unittest

from app.models.fis_model import FISModel


class ChangeMFNameTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_output()
        self.model.add_mf("output0", "output")
        self.model.add_mf("output1", "output")

    def test_1_mf_name_changed(self) -> None:
        result = self.model.change_mf_name("output0", "output", 0, "newname")
        self.assertEqual(result, 1, "Wrong result value")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0].Name, "newname", "Wrong name of MF")

    def test_2_mf_name_too_long(self) -> None:
        long_name = ""
        for _ in range(101):
            long_name += "a"
        result = self.model.change_mf_name("output0", "output", 0, long_name)
        self.assertEqual(result, -3, "Name changed incorrectly")

    def tearDown(self) -> None:
        del self.model


if __name__ == "__main__":
    unittest.main()
