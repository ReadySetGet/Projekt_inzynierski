from unittest.mock import Mock

import numpy as np
import pytest

from app.view_models.area_plot_view_model import AreaPlotViewModel


@pytest.fixture
def area_plot_view_model(setup_base_view_model_context, mock_fuzzy_service):
    vm = AreaPlotViewModel()
    return vm


def test_area_plot_view_model_initialization(area_plot_view_model):
    assert area_plot_view_model is not None


def test_area_plot_view_model_refresh_data(qtbot, area_plot_view_model):
    with qtbot.waitSignal(area_plot_view_model.notify_data_changed, timeout=1000):
        area_plot_view_model.refresh_data()


def test_area_plot_view_model_get_input_variables(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [{"name": "input1", "range": [0, 1]}]

    inputs = area_plot_view_model.get_input_variables()
    assert len(inputs) == 1
    assert inputs[0]["name"] == "input1"


def test_area_plot_view_model_get_output_variables(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_output_variables.return_value = [{"name": "output1", "range": [0, 1]}]

    outputs = area_plot_view_model.get_output_variables()
    assert len(outputs) == 1
    assert outputs[0]["name"] == "output1"


def test_area_plot_view_model_compute_surface_success(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1", "range": [0, 1]},
        {"name": "input2", "range": [0, 1]},
    ]
    mock_fuzzy_service.get_output_variables.return_value = [{"name": "output1", "range": [0, 1]}]
    mock_fuzzy_service.is_system_ready.return_value = True
    mock_fuzzy_service.get_membership_functions.return_value = [
        {"name": "mf1", "type": "trimf", "parameters": [0, 0.5, 1]}
    ]
    mock_fuzzy_service.perform_inference.return_value = ([0.5], True)

    result = area_plot_view_model.compute_surface("input1", "input2", "output1", 5, 5)
    assert result is not None
    assert "X" in result
    assert "Y" in result
    assert "Z" in result


def test_area_plot_view_model_compute_surface_not_ready(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1", "range": [0, 1]},
        {"name": "input2", "range": [0, 1]},
    ]
    mock_fuzzy_service.get_output_variables.return_value = [{"name": "output1", "range": [0, 1]}]
    mock_fuzzy_service.is_system_ready.return_value = False
    mock_fuzzy_service.get_rule_count.return_value = 0

    result = area_plot_view_model.compute_surface("input1", "input2", "output1", 5, 5)
    assert result is not None
    assert result.get("error") == "system_not_ready"


def test_area_plot_view_model_compute_surface_insufficient_inputs(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [{"name": "input1", "range": [0, 1]}]
    mock_fuzzy_service.get_output_variables.return_value = [{"name": "output1", "range": [0, 1]}]

    result = area_plot_view_model.compute_surface("input1", "input2", "output1", 5, 5)
    assert result is None


def test_area_plot_view_model_compute_surface_no_outputs(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1", "range": [0, 1]},
        {"name": "input2", "range": [0, 1]},
    ]
    mock_fuzzy_service.get_output_variables.return_value = []

    result = area_plot_view_model.compute_surface("input1", "input2", "output1", 5, 5)
    assert result is None


def test_area_plot_view_model_get_mf_center_value_trimf(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_membership_functions.return_value = [{"type": "trimf", "parameters": [0, 0.5, 1]}]

    center = area_plot_view_model._get_mf_center_value("input1", [0, 1])
    assert center == 0.5


def test_area_plot_view_model_get_mf_center_value_trapmf(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_membership_functions.return_value = [{"type": "trapmf", "parameters": [0, 0.25, 0.75, 1]}]

    center = area_plot_view_model._get_mf_center_value("input1", [0, 1])
    assert center == 0.5


def test_area_plot_view_model_get_mf_center_value_gaussmf(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_membership_functions.return_value = [{"type": "gaussmf", "parameters": [0.1, 0.5]}]

    center = area_plot_view_model._get_mf_center_value("input1", [0, 1])
    assert center == 0.5


def test_area_plot_view_model_get_mf_center_value_gbellmf(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_membership_functions.return_value = [{"type": "gbellmf", "parameters": [0.1, 2, 0.5]}]

    center = area_plot_view_model._get_mf_center_value("input1", [0, 1])
    assert center == 0.5


def test_area_plot_view_model_get_mf_center_value_no_mfs(area_plot_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_membership_functions.return_value = []

    center = area_plot_view_model._get_mf_center_value("input1", [0, 1])
    assert center == 0.5
