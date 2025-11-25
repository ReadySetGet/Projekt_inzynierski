from unittest.mock import MagicMock, Mock, patch

import pytest
from PyQt6.QtCore import QObject

from app.app_context import AppContext
from app.view_models.base_view_model import BaseViewModel


@pytest.fixture
def mock_context():
    context = Mock(spec=AppContext)
    context.event_bus = Mock()
    context.theme_manager = Mock()
    context.theme_manager.theme_changed = Mock()
    context.fuzzy_service = Mock()
    context.translate_manager = Mock()
    context.translate_manager.t = Mock(return_value="translated")
    return context


@pytest.fixture
def view_model(mock_context):
    with patch.object(BaseViewModel, "_context_provider", return_value=mock_context):
        BaseViewModel.set_context_provider(lambda: mock_context)
        vm = BaseViewModel()
        return vm


def test_base_view_model_initialization(view_model, mock_context):
    assert isinstance(view_model, QObject)
    assert view_model.context == mock_context


def test_base_view_model_context_property(view_model, mock_context):
    assert view_model.context == mock_context


def test_base_view_model_context_provider_not_set():
    BaseViewModel.set_context_provider(None)
    with pytest.raises(RuntimeError, match="No context provider set"):
        BaseViewModel().context


def test_base_view_model_fuzzy_service_property(view_model, mock_context):
    assert view_model.fuzzy_service == mock_context.fuzzy_service


def test_base_view_model_event_bus_property(view_model, mock_context):
    assert view_model.event_bus == mock_context.event_bus


def test_base_view_model_theme_manager_property(view_model, mock_context):
    assert view_model.theme_manager == mock_context.theme_manager


def test_base_view_model_translate_manager_property(view_model, mock_context):
    assert view_model.translate_manager == mock_context.translate_manager


def test_base_view_model_translate_method(view_model, mock_context):
    result = view_model.t("test_key")
    mock_context.translate_manager.t.assert_called_once_with("test_key")
    assert result == "translated"


def test_base_view_model_load_stylesheet_with_theme(view_model, mock_context):
    mock_context.theme_manager.load_stylesheet_with_theme.return_value = "stylesheet_content"
    result = view_model.load_stylesheet_with_theme("test.qss")
    assert result == "stylesheet_content"
    mock_context.theme_manager.load_stylesheet_with_theme.assert_called_once_with("test.qss")


def test_base_view_model_refresh_data(view_model):
    view_model.refresh_data()
    assert True


def test_base_view_model_data_changed_signal(view_model):
    view_model.data_changed.connect(lambda: None)
    view_model.data_changed.emit()


def test_base_view_model_notify_data_changed_signal(view_model):
    view_model.notify_data_changed.connect(lambda: None)
    view_model.notify_data_changed.emit()


def test_base_view_model_theme_changed_signal(view_model):
    view_model.theme_changed.connect(lambda: None)
    view_model.theme_changed.emit()


def test_base_view_model_stylesheet_updated_signal(view_model):
    view_model.stylesheet_updated.connect(lambda x: None)
    view_model.stylesheet_updated.emit("stylesheet")


def test_base_view_model_registers_with_event_bus(mock_context):
    with patch.object(BaseViewModel, "_context_provider", return_value=mock_context):
        BaseViewModel.set_context_provider(lambda: mock_context)
        vm = BaseViewModel()
        mock_context.event_bus.register_view_model.assert_called_once_with(vm)


def test_base_view_model_connects_theme_changed(mock_context):
    with patch.object(BaseViewModel, "_context_provider", return_value=mock_context):
        BaseViewModel.set_context_provider(lambda: mock_context)
        vm = BaseViewModel()
        mock_context.theme_manager.theme_changed.connect.assert_called()


def test_base_view_model_on_theme_changed(view_model):
    view_model._on_theme_changed()
    assert True
