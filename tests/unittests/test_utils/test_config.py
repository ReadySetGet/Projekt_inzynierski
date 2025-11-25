import pytest
import configparser
from pathlib import Path
from unittest.mock import patch, mock_open

from app.utils.config import AppConfig


@pytest.fixture
def sample_config_content():
    return """[app]
name = Test App

[window]
width = 1024
height = 768
"""


@pytest.fixture
def temp_config_file(tmp_path, sample_config_content):
    config_file = tmp_path / "config.ini"
    config_file.write_text(sample_config_content)
    return config_file


def test_app_config_initialize(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    assert AppConfig._initialized is True


def test_app_config_get_var(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    value = AppConfig.get_var("app", "name")
    assert value == "Test App"


def test_app_config_get_var_not_initialized():
    AppConfig._initialized = False
    with pytest.raises(RuntimeError, match="AppConfig not initialized"):
        AppConfig.get_var("app", "name")


def test_app_config_set_value(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    AppConfig.set_value("app", "version", "1.0.0")
    value = AppConfig.get_var("app", "version")
    assert value == "1.0.0"


def test_app_config_set_value_new_section(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    AppConfig.set_value("new_section", "key", "value")
    value = AppConfig.get_var("new_section", "key")
    assert value == "value"


def test_app_config_set_value_not_initialized():
    AppConfig._initialized = False
    with pytest.raises(RuntimeError, match="AppConfig not initialized"):
        AppConfig.set_value("app", "key", "value")


def test_app_config_app_name(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    name = AppConfig.app_name()
    assert name == "Test App"


def test_app_config_app_name_fallback():
    AppConfig._initialized = False
    with patch('app.utils.config.CONFIG_PATH', Path("/nonexistent/config.ini")):
        AppConfig.initialize("/nonexistent/config.ini")
        name = AppConfig.app_name()
        assert name == "Default App"


def test_app_config_window_width(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    width = AppConfig.window_width()
    assert width == 1024


def test_app_config_window_width_fallback():
    AppConfig._initialized = False
    with patch('app.utils.config.CONFIG_PATH', Path("/nonexistent/config.ini")):
        AppConfig.initialize("/nonexistent/config.ini")
        width = AppConfig.window_width()
        assert width == 800


def test_app_config_window_height(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    height = AppConfig.window_height()
    assert height == 768


def test_app_config_window_height_fallback():
    AppConfig._initialized = False
    with patch('app.utils.config.CONFIG_PATH', Path("/nonexistent/config.ini")):
        AppConfig.initialize("/nonexistent/config.ini")
        height = AppConfig.window_height()
        assert height == 600


def test_app_config_initialize_idempotent(temp_config_file):
    AppConfig._initialized = False
    AppConfig.initialize(str(temp_config_file))
    first_config = AppConfig._config
    AppConfig.initialize(str(temp_config_file))
    assert AppConfig._config is first_config

