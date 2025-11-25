import json
import os
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from PyQt6.QtWidgets import QApplication

from app.services.theme_manager import ThemeManager


@pytest.fixture
def temp_themes_dir(tmp_path):
    themes_dir = tmp_path / "themes"
    themes_dir.mkdir()
    return themes_dir


@pytest.fixture
def theme_manager(temp_themes_dir):
    return ThemeManager(str(temp_themes_dir))


def test_theme_manager_initialization(theme_manager, temp_themes_dir):
    assert theme_manager.themes_path == str(temp_themes_dir)
    assert theme_manager.current_theme is None
    assert theme_manager.current_palette is None


def test_theme_manager_discover_palettes(theme_manager, temp_themes_dir):
    dark_json = temp_themes_dir / "dark.json"
    light_json = temp_themes_dir / "light.json"
    dark_json.write_text('{"colors": {"primary": "#000000"}}')
    light_json.write_text('{"colors": {"primary": "#ffffff"}}')

    palettes = theme_manager._discover_palettes()
    assert "dark" in palettes
    assert "light" in palettes
    assert palettes["dark"] == str(dark_json)
    assert palettes["light"] == str(light_json)


def test_theme_manager_discover_palettes_no_directory():
    manager = ThemeManager("/nonexistent/path")
    palettes = manager._discover_palettes()
    assert palettes == {}


def test_theme_manager_flatten_dict(theme_manager):
    nested = {"colors": {"primary": "#000000", "secondary": {"light": "#cccccc", "dark": "#333333"}}}
    flattened = theme_manager._flatten_dict(nested)
    assert "colors.primary" in flattened
    assert "colors.secondary.light" in flattened
    assert "colors.secondary.dark" in flattened
    assert flattened["colors.primary"] == "#000000"


def test_theme_manager_available_themes(theme_manager, temp_themes_dir):
    dark_json = temp_themes_dir / "dark.json"
    light_json = temp_themes_dir / "light.json"
    dark_json.write_text("{}")
    light_json.write_text("{}")

    themes = theme_manager.available_themes()
    assert "dark" in themes
    assert "light" in themes


def test_theme_manager_set_theme(theme_manager, temp_themes_dir):
    dark_json = temp_themes_dir / "dark.json"
    dark_json.write_text('{"colors": {"primary": "#000000"}}')

    result = theme_manager.set_theme("dark")
    assert result is True
    assert theme_manager.current_theme == "dark"
    assert theme_manager.current_palette is not None


def test_theme_manager_set_theme_not_found(theme_manager):
    result = theme_manager.set_theme("nonexistent")
    assert result is False
    assert theme_manager.current_theme is None


def test_theme_manager_get_current_theme(theme_manager, temp_themes_dir):
    dark_json = temp_themes_dir / "dark.json"
    dark_json.write_text('{"colors": {"primary": "#000000"}}')

    theme_manager.set_theme("dark")
    assert theme_manager.get_current_theme() == "dark"


def test_theme_manager_load_stylesheet_with_theme(theme_manager, temp_themes_dir):
    dark_json = temp_themes_dir / "dark.json"
    dark_json.write_text('{"colors": {"primary": "#000000"}}')
    qss_file = temp_themes_dir / "style.qss"
    qss_file.write_text("QWidget { background-color: {colors.primary}; }")

    theme_manager.set_theme("dark")
    result = theme_manager.load_stylesheet_with_theme("style.qss")
    assert "{colors.primary}" not in result
    assert "#000000" in result


def test_theme_manager_load_stylesheet_with_theme_absolute_path(theme_manager, temp_themes_dir):
    dark_json = temp_themes_dir / "dark.json"
    dark_json.write_text('{"colors": {"primary": "#000000"}}')
    qss_file = temp_themes_dir / "style.qss"
    qss_file.write_text("QWidget { background-color: {colors.primary}; }")

    theme_manager.set_theme("dark")
    result = theme_manager.load_stylesheet_with_theme(str(qss_file))
    assert "#000000" in result


def test_theme_manager_load_stylesheet_with_theme_not_found(theme_manager):
    result = theme_manager.load_stylesheet_with_theme("nonexistent.qss")
    assert result == ""


def test_theme_manager_load_stylesheet_with_theme_no_palette(theme_manager, temp_themes_dir):
    qss_file = temp_themes_dir / "style.qss"
    qss_file.write_text("QWidget { background-color: red; }")

    result = theme_manager.load_stylesheet_with_theme("style.qss")
    assert result == "QWidget { background-color: red; }"
