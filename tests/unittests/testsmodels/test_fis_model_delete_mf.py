import unittest

from app.models.fis_model import FISModel


class DeleteMFTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FISModel()
        self.model.add_input()
        self.model.add_output()
        self.model.add_mf("input0", "input")
        self.model.add_mf("output0", "output")

    def test_1_input_mf_deleted(self) -> None:
        nr_mfs = len(self.model._fis.Inputs[0].MembershipFunctions)
        self.model.delete_mf("input0", "input", 0)
        self.assertEqual(len(self.model._fis.Inputs[0].MembershipFunctions),
                         nr_mfs - 1, "Input MF not deleted")

    def test_2_input_mf_at_idx_deleted(self) -> None:
        self.model.add_mf("input0", "input")
        nr_mfs = len(self.model._fis.Inputs[0].MembershipFunctions)
        self.model.delete_mf("input0", "input", 0)
        self.assertEqual(len(self.model._fis.Inputs[0].MembershipFunctions),
                         nr_mfs - 1, "Input MF not deleted")
        self.assertEqual(self.model._fis.Inputs[0].MembershipFunctions[0].Name,
                         "mf1", "Input MF at wrong index deleted")

    def test_3_output_mf_deleted(self) -> None:
        nr_mfs = len(self.model._fis.Outputs[0].MembershipFunctions)
        self.model.delete_mf("output0", "output", 0)
        self.assertEqual(len(self.model._fis.Outputs[0].MembershipFunctions),
                         nr_mfs - 1, "Output MF not deleted")

    def test_4_output_mf_at_idx_deleted(self) -> None:
        self.model.add_mf("output0", "output")
        nr_mfs = len(self.model._fis.Outputs[0].MembershipFunctions)
        self.model.delete_mf("output0", "output", 0)
        self.assertEqual(len(self.model._fis.Outputs[0].MembershipFunctions),
                         nr_mfs - 1, "Output MF not deleted")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0].Name,
                         "mf1", "Output MF at wrong index deleted")

    def tearDown(self) -> None:
        del self.model


if __name__ == '__main__':
    unittest.main()