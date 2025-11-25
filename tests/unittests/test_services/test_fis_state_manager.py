from unittest.mock import Mock, patch

import pytest

from app.models.fis_model import FISModel
from app.services.fis_state_manager import FISStateManager


@pytest.fixture
def fis_state_manager():
    with patch("app.services.fis_state_manager.FISModel") as mock_fis_model_class:
        mock_fis = Mock()
        mock_fis.Inputs = []
        mock_fis.Outputs = []
        mock_fis.Rules = []
        mock_model = Mock()
        mock_model._fis = mock_fis
        mock_model.add_input = Mock()
        mock_model._fis.Inputs = []
        mock_fis_model_class.return_value = mock_model
        manager = FISStateManager("mamdani")
        manager._fis_model = mock_model
        return manager


def test_fis_state_manager_initialization(fis_state_manager):
    assert fis_state_manager.fis_type == "mamdani"
    assert fis_state_manager.inference_state == "idle"
    assert fis_state_manager.last_inference_results == []
    assert fis_state_manager.last_inference_inputs == []


def test_fis_state_manager_fis_model_property(fis_state_manager):
    assert fis_state_manager.fis_model is not None


def test_fis_state_manager_fis_type_property(fis_state_manager):
    assert fis_state_manager.fis_type == "mamdani"


def test_fis_state_manager_inference_state_property(fis_state_manager):
    assert fis_state_manager.inference_state == "idle"


def test_fis_state_manager_last_inference_results_property(fis_state_manager):
    assert fis_state_manager.last_inference_results == []


def test_fis_state_manager_last_inference_inputs_property(fis_state_manager):
    assert fis_state_manager.last_inference_inputs == []


def test_fis_state_manager_set_selected_input(fis_state_manager):
    fis_state_manager.set_selected_input("input1")
    assert fis_state_manager.selected_input_name == "input1"
    assert fis_state_manager.selected_output_name is None


def test_fis_state_manager_set_selected_output(fis_state_manager):
    fis_state_manager.set_selected_output("output1")
    assert fis_state_manager.selected_output_name == "output1"
    assert fis_state_manager.selected_input_name is None


def test_fis_state_manager_clear_selection(fis_state_manager):
    fis_state_manager.set_selected_input("input1")
    fis_state_manager.clear_selection()
    assert fis_state_manager.selected_input_name is None
    assert fis_state_manager.selected_output_name is None


def test_fis_state_manager_set_inference_state(fis_state_manager):
    fis_state_manager.set_inference_state("calculating")
    assert fis_state_manager.inference_state == "calculating"


def test_fis_state_manager_update_inference_results(fis_state_manager):
    inputs = [0.5, 0.7]
    outputs = [0.6]
    fis_state_manager.update_inference_results(inputs, outputs)
    assert fis_state_manager.last_inference_inputs == inputs
    assert fis_state_manager.last_inference_results == outputs


def test_fis_state_manager_get_selected_variable_info(fis_state_manager):
    fis_state_manager.set_selected_input("input1")
    info = fis_state_manager.get_selected_variable_info()
    assert info["selected_input"] == "input1"
    assert info["selected_output"] is None
    assert info["has_selection"] is True


def test_fis_state_manager_get_selected_variable_info_no_selection(fis_state_manager):
    info = fis_state_manager.get_selected_variable_info()
    assert info["selected_input"] is None
    assert info["selected_output"] is None
    assert info["has_selection"] is False


def test_fis_state_manager_get_system_status(fis_state_manager):
    status = fis_state_manager.get_system_status()
    assert "fis_type" in status
    assert "inference_state" in status
    assert "has_inputs" in status
    assert "has_outputs" in status
    assert "has_rules" in status
    assert "is_ready" in status


def test_fis_state_manager_create_mamdani_fis(fis_state_manager):
    result = fis_state_manager.create_mamdani_fis("test_mamdani")
    assert result is True
    assert fis_state_manager.fis_type == "mamdani"


def test_fis_state_manager_create_sugeno_fis(fis_state_manager):
    result = fis_state_manager.create_sugeno_fis("test_sugeno")
    assert result is True
    assert fis_state_manager.fis_type == "sugeno"


def test_fis_state_manager_switch_to_mamdani(fis_state_manager):
    fis_state_manager._fis_type = "sugeno"
    result = fis_state_manager.switch_to_mamdani()
    assert result is True
    assert fis_state_manager.fis_type == "mamdani"


def test_fis_state_manager_switch_to_sugeno(fis_state_manager):
    fis_state_manager._fis_type = "mamdani"
    result = fis_state_manager.switch_to_sugeno()
    assert result is True
    assert fis_state_manager.fis_type == "sugeno"
