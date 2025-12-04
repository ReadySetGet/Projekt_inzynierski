import unittest

from app.models.fis_reader_writer import FISReaderWriter


class DeleteOutputTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = FISReaderWriter()

    def test_1_unsupported_extension(self) -> None:
        result = self.reader.read_fis("./resources/notfisfile.txt")
        self.assertEqual(result, -1, "Unsupported extension wronglyrecognized")

    def test_2_file_not_exists(self) -> None:
        result = self.reader.read_fis("./resources/notexistingfile.fis")
        self.assertEqual(result, -2, "File somehow found")

    def test_3_fis_loaded_to_model(self) -> None:
        result = self.reader.read_fis("./resources/model.fis")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertNotEqual(self.reader.model, None, "Model not imported")

    def test_4_poorly_formatted_file(self) -> None:
        result = self.reader.read_fis("./resources/model_bad_formatting.fis")
        self.assertEqual(result, -3, "Problems with file import - possible structural errors")

    def tearDown(self) -> None:
        del self.reader


if __name__ == "__main__":
    unittest.main()
