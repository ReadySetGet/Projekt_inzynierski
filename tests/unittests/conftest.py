from unittest.mock import MagicMock, Mock, patch

import pytest
from PyQt6 import QtWidgets

from app.app_context import AppContext
from app.services.central_event_bus import CentralEventBus
from app.services.fuzzy_calculation_service import FuzzyCalculationService
from app.services.theme_manager import ThemeManager
from app.services.translate_manager import TranslateManager


@pytest.fixture
def qt_application():
    if QtWidgets.QApplication.instance() is None:
        app = QtWidgets.QApplication([])
        yield app
        app.quit()
    else:
        yield QtWidgets.QApplication.instance()


@pytest.fixture
def mock_fuzzy_service():
    service = Mock(spec=FuzzyCalculationService)
    service.get_input_count = Mock(return_value=2)
    service.get_output_count = Mock(return_value=1)
    service.add_input_variable = Mock(return_value=True)
    service.delete_input_variable = Mock(return_value=True)
    service.add_output_variable = Mock(return_value=True)
    service.delete_output_variable = Mock(return_value=True)
    service.import_model = Mock(return_value=True)
    service.export_model = Mock(return_value=True)
    service.convert_inference_system = Mock(return_value=True)
    service.get_fis_type = Mock(return_value="mamdani")
    service.get_interpolation_points = Mock(return_value=15)
    service.set_interpolation_points = Mock(return_value=True)
    service.get_system_status = Mock(
        return_value={
            "fis_type": "mamdani",
            "inference_state": "idle",
            "has_inputs": True,
            "has_outputs": True,
            "has_rules": False,
            "is_ready": False,
            "name": "test_fis",
        }
    )
    service.get_fis_model = Mock(return_value=Mock())
    service.get_input_variables = Mock(
        return_value=[{"name": "input1", "range": [0, 1]}, {"name": "input2", "range": [0, 1]}]
    )
    service.get_output_variables = Mock(return_value=[{"name": "output1", "range": [0, 1]}])
    sample_mfs = [
        {"name": "low", "type": "trimf", "parameters": [0.0, 0.0, 0.5]},
        {"name": "high", "type": "trimf", "parameters": [0.5, 1.0, 1.0]},
    ]
    service.get_membership_functions = Mock(return_value=sample_mfs)
    service.get_rules = Mock(return_value=[])
    service.get_defuzzification_method = Mock(return_value="centroid")
    service.set_defuzzification_method = Mock(return_value=True)
    service.get_selected_input_name = Mock(return_value="input1")
    service.get_selected_output_name = Mock(return_value=None)
    sample_variable_data = {
        "name": "input1",
        "range": [0, 1],
        "membership_functions": sample_mfs,
    }
    service.get_selected_input_data = Mock(return_value=sample_variable_data)
    service.get_selected_output_data = Mock(return_value=None)
    service.is_system_ready = Mock(return_value=True)
    service.validate_inputs = Mock(return_value=(True, None))
    service.perform_inference = Mock(return_value=([0.5], True))
    service.system_changed = Mock()
    service.inference_completed = Mock()
    return service


@pytest.fixture
def mock_event_bus():
    bus = Mock(spec=CentralEventBus)
    bus.register_view_model = Mock()
    bus.data_refresh_requested = Mock()
    return bus


@pytest.fixture
def mock_theme_manager():
    manager = Mock(spec=ThemeManager)
    manager.theme_changed = Mock()
    manager.load_stylesheet_with_theme = Mock(return_value="stylesheet_content")
    manager.set_theme = Mock(return_value=True)
    manager.get_current_theme = Mock(return_value="dark")
    manager.available_themes = Mock(return_value=["dark", "light"])
    manager.current_theme = "dark"
    manager.current_palette = {}
    return manager


@pytest.fixture
def mock_translate_manager():
    manager = Mock(spec=TranslateManager)
    manager.t = Mock(side_effect=lambda key: f"translated_{key}")
    manager.language_changed = Mock()
    manager.current_language = "en"
    manager.translations = {"test_key": "test_value"}
    manager.available_languages = Mock(return_value=["en", "pl"])
    manager.load_language = Mock(return_value=True)
    manager.set_language = Mock(return_value=True)
    return manager


@pytest.fixture
def mock_app_context(mock_fuzzy_service, mock_event_bus, mock_theme_manager, mock_translate_manager):
    context = Mock(spec=AppContext)
    context.fuzzy_service = mock_fuzzy_service
    context.event_bus = mock_event_bus
    context.theme_manager = mock_theme_manager
    context.translate_manager = mock_translate_manager
    context.config = Mock()
    return context


@pytest.fixture
def setup_base_view_model_context(mock_app_context):
    from app.view_models.base_view_model import BaseViewModel

    BaseViewModel.set_context_provider(lambda: mock_app_context)
    yield mock_app_context
    BaseViewModel.set_context_provider(None)


@pytest.fixture(autouse=True)
def _auto_setup_base_view_model_context(setup_base_view_model_context):
    """Ensure every test has BaseViewModel context configured."""
    yield setup_base_view_model_context


@pytest.fixture
def mock_fis_model():
    model = Mock()
    model._fis = Mock()
    model._fis.Inputs = []
    model._fis.Outputs = []
    model._fis.Rules = []
    model._fis.Name = "test_fis"
    model.add_input = Mock(return_value=1)
    model.add_output = Mock(return_value=1)
    model.delete_input = Mock(return_value=1)
    model.delete_output = Mock(return_value=1)
    model.add_mf = Mock(return_value=1)
    model.delete_mf = Mock(return_value=1)
    model.clear_all_rules = Mock()
    return model


def create_mock_input_variable(name="input1", range_values=[0, 1], mf_count=0):
    var = Mock()
    var.Name = name
    var.Range = range_values
    var.MembershipFunctions = [Mock() for _ in range(mf_count)]
    for i, mf in enumerate(var.MembershipFunctions):
        mf.Name = f"mf_{i}"
        mf.Type = "trimf"
        mf.Parameters = [0, 0.5, 1]
    return var


def create_mock_output_variable(name="output1", range_values=[0, 1], mf_count=0):
    var = Mock()
    var.Name = name
    var.Range = range_values
    var.MembershipFunctions = [Mock() for _ in range(mf_count)]
    for i, mf in enumerate(var.MembershipFunctions):
        mf.Name = f"mf_{i}"
        mf.Type = "trimf"
        mf.Parameters = [0, 0.5, 1]
    return var


def create_mock_rule(antecedent=[1, 1], consequent=[1], weight=1.0, connection=1):
    rule = Mock()
    rule.Antecedent = antecedent
    rule.Consequent = consequent
    rule.Weight = weight
    rule.Connection = connection
    return rule
