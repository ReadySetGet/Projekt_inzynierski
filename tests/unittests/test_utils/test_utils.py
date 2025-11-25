from pathlib import Path
from unittest.mock import patch

import pytest

from app.utils.utils import load_stylesheet


@patch("app.utils.utils.VIEWS_DIR")
def test_load_stylesheet(mock_views_dir, tmp_path):
    mock_views_dir.__truediv__ = lambda self, other: tmp_path / other
    stylesheet_file = tmp_path / "test.qss"
    stylesheet_file.write_text("QWidget { background-color: red; }")

    result = load_stylesheet("test.qss")
    assert result == "QWidget { background-color: red; }"


@patch("app.utils.utils.VIEWS_DIR")
def test_load_stylesheet_file_not_found(mock_views_dir):
    mock_views_dir.__truediv__ = lambda self, other: Path("/nonexistent") / other

    with pytest.raises(FileNotFoundError):
        load_stylesheet("nonexistent.qss")
