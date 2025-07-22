import unittest

from app.models.fis_reader_writer import FISReaderWriter
from app.models.fis_model import FISModel


class DeleteOutputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        model = FISModel()
        model.add_input()
        model.add_input()
        model.add_output()
        model.add_output()

        model.add_mf("input0", "input")
        model.add_mf("input1", "input")
        model.add_mf("output0", "output")
        model.add_mf("output1", "output")

        model.add_rule([1, 1, 1, 1], [1, 1, 1, 1, 0.4, 0])
        model.add_rule([1, 0, 1, 0], [1, 0, 0, 1, 0.3, 1])
        model.add_rule([0, 0, 0, 1], [1, 1, 1, 0, 1, 0])
        self.writer = FISReaderWriter(model)

    def test_1_unsupported_extension(self) -> None:
        result = self.writer.write_fis("./resources/notfisfile.txt")
        self.assertEqual(result, -1, "Unsupported extension wrongly"
                                     "recognized")

    def test_2_no_fis_model_provided(self) -> None:
        self.writer.model = None
        result = self.writer.write_fis("./resources/notexistingfile.fis")
        self.assertEqual(result, -2, "None FISModel saved")

    def test_3_fis_saved_to_file(self) -> None:
        result = self.writer.write_fis("./resources/model.fis")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertNotEqual(self.writer.model, None, "Model not exported")

    def tearDown(self) -> None:
        del self.writer


if __name__ == '__main__':
    unittest.main()
