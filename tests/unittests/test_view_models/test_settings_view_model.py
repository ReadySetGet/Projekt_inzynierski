from unittest.mock import Mock

import pytest

from app.view_models.settings_view_model import SettingsViewModel


@pytest.fixture
def settings_view_model(setup_base_view_model_context, mock_theme_manager, mock_translate_manager):
    vm = SettingsViewModel()
    return vm


def test_settings_view_model_initialization(settings_view_model):
    assert settings_view_model is not None


def test_settings_view_model_get_available_themes(settings_view_model, mock_theme_manager):
    mock_theme_manager.available_themes.return_value = ["dark", "light"]
    themes = settings_view_model.get_available_themes()
    assert "dark" in themes
    assert "light" in themes


def test_settings_view_model_get_available_languages(settings_view_model, mock_translate_manager):
    mock_translate_manager.available_languages.return_value = ["en", "pl"]
    languages = settings_view_model.get_available_languages()
    assert "en" in languages
    assert "pl" in languages


def test_settings_view_model_get_current_theme(settings_view_model, mock_theme_manager):
    mock_theme_manager.get_current_theme.return_value = "dark"
    assert settings_view_model.get_current_theme() == "dark"


def test_settings_view_model_get_current_theme_none(settings_view_model, mock_theme_manager):
    mock_theme_manager.get_current_theme.return_value = None
    assert settings_view_model.get_current_theme() == ""


def test_settings_view_model_get_current_language(settings_view_model, mock_translate_manager):
    mock_translate_manager.current_language = "en"
    assert settings_view_model.get_current_language() == "en"


def test_settings_view_model_set_theme(settings_view_model, mock_theme_manager, mock_app_context):
    mock_theme_manager.set_theme.return_value = True
    mock_app_context.config = Mock()
    mock_app_context.config.set_value = Mock()

    result = settings_view_model.set_theme("dark")
    assert result is True
    mock_theme_manager.set_theme.assert_called_once_with("dark")


def test_settings_view_model_set_theme_failure(settings_view_model, mock_theme_manager):
    mock_theme_manager.set_theme.return_value = False

    result = settings_view_model.set_theme("nonexistent")
    assert result is False


def test_settings_view_model_set_language(settings_view_model, mock_translate_manager, mock_app_context):
    mock_translate_manager.set_language.return_value = True
    mock_app_context.config = Mock()
    mock_app_context.config.set_value = Mock()

    result = settings_view_model.set_language("pl")
    assert result is True
    mock_translate_manager.set_language.assert_called_once_with("pl")


def test_settings_view_model_set_language_failure(settings_view_model, mock_translate_manager):
    mock_translate_manager.set_language.return_value = False

    result = settings_view_model.set_language("nonexistent")
    assert result is False


def test_settings_view_model_on_theme_changed_internal(qtbot, settings_view_model, mock_theme_manager):
    mock_theme_manager.get_current_theme.return_value = "light"

    with qtbot.waitSignal(settings_view_model.current_theme_changed, timeout=1000):
        settings_view_model._on_theme_changed_internal()


def test_settings_view_model_on_language_changed_internal(qtbot, settings_view_model, mock_translate_manager):
    mock_translate_manager.current_language = "pl"

    with qtbot.waitSignal(settings_view_model.current_language_changed, timeout=1000):
        settings_view_model._on_language_changed_internal()


def test_settings_view_model_refresh_data(qtbot, settings_view_model, mock_theme_manager, mock_translate_manager):
    mock_theme_manager.available_themes.return_value = ["dark", "light"]
    mock_theme_manager.get_current_theme.return_value = "dark"
    mock_translate_manager.available_languages.return_value = ["en", "pl"]
    mock_translate_manager.current_language = "en"

    signals_received = []

    def on_theme_list():
        signals_received.append("theme_list")

    def on_lang_list():
        signals_received.append("lang_list")

    def on_theme():
        signals_received.append("theme")

    def on_lang():
        signals_received.append("lang")

    settings_view_model.theme_list_changed.connect(on_theme_list)
    settings_view_model.language_list_changed.connect(on_lang_list)
    settings_view_model.current_theme_changed.connect(on_theme)
    settings_view_model.current_language_changed.connect(on_lang)

    settings_view_model.refresh_data()

    qtbot.wait(100)
    assert len(signals_received) >= 2
