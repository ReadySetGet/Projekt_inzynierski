import pytest

from app.services.translate_manager import TranslateManager


@pytest.fixture
def temp_locales_dir(tmp_path):
    locales_dir = tmp_path / "locales"
    locales_dir.mkdir()
    en_dir = locales_dir / "en"
    en_dir.mkdir()
    pl_dir = locales_dir / "pl"
    pl_dir.mkdir()
    return locales_dir


@pytest.fixture
def translate_manager(temp_locales_dir):
    en_json = temp_locales_dir / "en" / "app.json"
    en_json.write_text('{"hello": "Hello", "world": "World"}')
    return TranslateManager(str(temp_locales_dir), "en")


def test_translate_manager_initialization(translate_manager, temp_locales_dir):
    assert translate_manager.locales_path == str(temp_locales_dir)
    assert translate_manager.current_language == "en"
    assert "hello" in translate_manager.translations


def test_translate_manager_available_languages(translate_manager, temp_locales_dir):
    pl_json = temp_locales_dir / "pl" / "app.json"
    pl_json.write_text('{"hello": "Witaj"}')

    languages = translate_manager.available_languages()
    assert "en" in languages
    assert "pl" in languages


def test_translate_manager_load_language(translate_manager, temp_locales_dir):
    pl_json = temp_locales_dir / "pl" / "app.json"
    pl_json.write_text('{"hello": "Witaj", "world": "Świat"}')

    result = translate_manager.load_language("pl")
    assert result is True
    assert translate_manager.current_language == "pl"
    assert translate_manager.translations["hello"] == "Witaj"


def test_translate_manager_load_language_not_found(translate_manager):
    result = translate_manager.load_language("fr")
    assert result is False


def test_translate_manager_set_language(translate_manager, temp_locales_dir):
    pl_json = temp_locales_dir / "pl" / "app.json"
    pl_json.write_text('{"hello": "Witaj"}')

    result = translate_manager.set_language("pl")
    assert result is True
    assert translate_manager.current_language == "pl"


def test_translate_manager_translate(translate_manager):
    result = translate_manager.t("hello")
    assert result == "Hello"


def test_translate_manager_translate_key_not_found(translate_manager):
    result = translate_manager.t("nonexistent_key")
    assert result == "nonexistent_key"


def test_translate_manager_language_changed_signal(qtbot, translate_manager, temp_locales_dir):
    pl_json = temp_locales_dir / "pl" / "app.json"
    pl_json.write_text('{"hello": "Witaj"}')

    with qtbot.waitSignal(translate_manager.language_changed, timeout=1000):
        translate_manager.set_language("pl")
