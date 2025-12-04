from unittest.mock import Mock

import pytest

from app.services.central_event_bus import CentralEventBus
from app.view_models.base_view_model import BaseViewModel


@pytest.fixture
def event_bus():
    return CentralEventBus()


@pytest.fixture
def mock_view_model():
    vm = Mock(spec=BaseViewModel)
    vm.notify_data_changed = Mock()
    vm.data_changed = Mock()
    return vm


def test_central_event_bus_initialization(event_bus):
    assert len(event_bus._registered_view_models) == 0


def test_central_event_bus_register_view_model(event_bus, mock_view_model):
    event_bus.register_view_model(mock_view_model)
    assert mock_view_model in event_bus._registered_view_models
    mock_view_model.notify_data_changed.connect.assert_called()


def test_central_event_bus_register_view_model_duplicate(event_bus, mock_view_model):
    event_bus.register_view_model(mock_view_model)
    event_bus.register_view_model(mock_view_model)
    assert event_bus._registered_view_models.count(mock_view_model) == 1


def test_central_event_bus_request_data_refresh(event_bus, mock_view_model):
    event_bus.register_view_model(mock_view_model)
    event_bus._request_data_refresh()
    mock_view_model.data_changed.emit.assert_called_once()


def test_central_event_bus_request_data_refresh_multiple(event_bus):
    vm1 = Mock(spec=BaseViewModel)
    vm1.notify_data_changed = Mock()
    vm1.data_changed = Mock()
    vm2 = Mock(spec=BaseViewModel)
    vm2.notify_data_changed = Mock()
    vm2.data_changed = Mock()
    event_bus.register_view_model(vm1)
    event_bus.register_view_model(vm2)
    event_bus._request_data_refresh()
    vm1.data_changed.emit.assert_called_once()
    vm2.data_changed.emit.assert_called_once()


def test_central_event_bus_notify_data_changed_triggers_refresh(event_bus, mock_view_model):
    event_bus.register_view_model(mock_view_model)
    mock_view_model.notify_data_changed.emit()
    mock_view_model.data_changed.emit.assert_called()
