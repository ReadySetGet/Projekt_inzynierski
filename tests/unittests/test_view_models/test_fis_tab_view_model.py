import pytest
from unittest.mock import Mock

from app.view_models.fis_tab_view_model import FisTabViewModel


@pytest.fixture
def fis_tab_view_model(setup_base_view_model_context, mock_fuzzy_service):
    vm = FisTabViewModel()
    return vm


def test_fis_tab_view_model_initialization(fis_tab_view_model, mock_fuzzy_service):
    assert isinstance(fis_tab_view_model._inputs, list)
    assert isinstance(fis_tab_view_model._outputs, list)


def test_fis_tab_view_model_inputs_property(fis_tab_view_model):
    assert isinstance(fis_tab_view_model.inputs, list)


def test_fis_tab_view_model_outputs_property(fis_tab_view_model):
    assert isinstance(fis_tab_view_model.outputs, list)


def test_fis_tab_view_model_refresh_data(qtbot, fis_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_system_status.return_value = {
        "fis_type": "mamdani",
        "has_inputs": True,
        "has_outputs": True,
        "has_rules": False,
        "is_ready": False,
        "inference_state": "idle"
    }
    mock_fuzzy_service.get_input_variables.return_value = []
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_membership_functions.return_value = []
    mock_fuzzy_service.get_interpolation_points.return_value = 15
    
    with qtbot.waitSignal(fis_tab_view_model.fis_data_updated, timeout=1000):
        fis_tab_view_model.refresh_data()


def test_fis_tab_view_model_get_variables_data_input(fis_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1", "range": [0, 1]}
    ]
    mock_fuzzy_service.get_membership_functions.return_value = []
    
    variables = fis_tab_view_model._get_variables_data("input")
    assert len(variables) == 1
    assert variables[0]["name"] == "input1"


def test_fis_tab_view_model_get_variables_data_output(fis_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_output_variables.return_value = [
        {"name": "output1", "range": [0, 1]}
    ]
    mock_fuzzy_service.get_membership_functions.return_value = []
    
    variables = fis_tab_view_model._get_variables_data("output")
    assert len(variables) == 1
    assert variables[0]["name"] == "output1"


def test_fis_tab_view_model_get_membership_functions_data(fis_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_membership_functions.return_value = [
        {"name": "mf1", "type": "trimf", "parameters": [0, 0.5, 1]}
    ]
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1", "range": [0, 1]}
    ]
    mock_fuzzy_service.get_interpolation_points.return_value = 10
    
    mf_data = fis_tab_view_model._get_membership_functions_data("input1", "input")
    assert len(mf_data) == 1
    assert mf_data[0]["name"] == "mf1"


def test_fis_tab_view_model_generate_plot_data(fis_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_interpolation_points.return_value = 10
    mf = {"type": "trimf", "parameters": [0, 0.5, 1]}
    var_range = [0, 1]
    
    x, y = fis_tab_view_model._generate_plot_data(mf, var_range)
    assert len(x) == 10
    assert len(y) == 10


def test_fis_tab_view_model_calculate_membership_values_trimf(fis_tab_view_model):
    x = [0.0, 0.25, 0.5, 0.75, 1.0]
    mf_type = "trimf"
    parameters = [0.0, 0.5, 1.0]
    
    y = fis_tab_view_model._calculate_membership_values(x, mf_type, parameters)
    assert len(y) == len(x)
    assert y[2] == 1.0


def test_fis_tab_view_model_calculate_membership_values_trapmf(fis_tab_view_model):
    x = [0.0, 0.25, 0.5, 0.75, 1.0]
    mf_type = "trapmf"
    parameters = [0.0, 0.25, 0.75, 1.0]
    
    y = fis_tab_view_model._calculate_membership_values(x, mf_type, parameters)
    assert len(y) == len(x)


def test_fis_tab_view_model_get_system_display_name(fis_tab_view_model):
    fis_tab_view_model._system_info = {"type": "mamdani"}
    assert "Mamdani" in fis_tab_view_model.get_system_display_name()


def test_fis_tab_view_model_get_variable_display_name(fis_tab_view_model):
    var_data = {"name": "input1", "membership_functions": [1, 2, 3]}
    display_name = fis_tab_view_model.get_variable_display_name(var_data)
    assert "input1" in display_name
    assert "3" in display_name

