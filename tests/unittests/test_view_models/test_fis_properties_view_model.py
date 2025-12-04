from unittest.mock import Mock

import pytest

from app.view_models.fis_properties_view_model import FisPropertiesViewModel


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


@pytest.fixture
def fis_properties_view_model(setup_base_view_model_context, mock_fuzzy_service, mock_fis_model):
    vm = FisPropertiesViewModel()
    mock_fuzzy_service.get_fis_model.return_value = mock_fis_model
    mock_fis_model._fis.Inputs = []
    mock_fis_model._fis.Outputs = []
    return vm


def test_fis_properties_view_model_initialization(fis_properties_view_model):
    assert fis_properties_view_model._system_name == "fis"
    assert fis_properties_view_model._system_type == "mamfis"
    assert fis_properties_view_model._selected_variable is None


def test_fis_properties_view_model_system_name_property(fis_properties_view_model):
    assert fis_properties_view_model.system_name == "fis"
    fis_properties_view_model.system_name = "new_name"
    assert fis_properties_view_model.system_name == "new_name"


def test_fis_properties_view_model_system_name_setter_emits_signal(qtbot, fis_properties_view_model):
    with qtbot.waitSignal(fis_properties_view_model.system_name_changed, timeout=1000):
        fis_properties_view_model.system_name = "Test System"


def test_fis_properties_view_model_system_type_property(fis_properties_view_model):
    assert fis_properties_view_model.system_type == "mamfis"
    fis_properties_view_model.system_type = "sugfis"
    assert fis_properties_view_model.system_type == "sugfis"


def test_fis_properties_view_model_system_type_setter_emits_signal(qtbot, fis_properties_view_model):
    with qtbot.waitSignal(fis_properties_view_model.system_type_changed, timeout=1000):
        fis_properties_view_model.system_type = "sugfis"


def test_fis_properties_view_model_inputs_property(fis_properties_view_model, mock_fis_model):
    input_var = create_mock_input_variable("input1", [0, 1], 2)
    mock_fis_model._fis.Inputs = [input_var]

    inputs = fis_properties_view_model.inputs
    assert len(inputs) == 1
    assert inputs[0]["name"] == "input1"
    assert inputs[0]["mf_count"] == 2


def test_fis_properties_view_model_outputs_property(fis_properties_view_model, mock_fis_model):
    output_var = create_mock_output_variable("output1", [0, 1], 3)
    mock_fis_model._fis.Outputs = [output_var]

    outputs = fis_properties_view_model.outputs
    assert len(outputs) == 1
    assert outputs[0]["name"] == "output1"
    assert outputs[0]["mf_count"] == 3


def test_fis_properties_view_model_add_input(fis_properties_view_model, mock_fuzzy_service, mock_fis_model):
    input_var = create_mock_input_variable("input1", [0, 1], 0)
    mock_fis_model._fis.Inputs = [input_var]
    mock_fuzzy_service.get_input_count.return_value = 1
    mock_fuzzy_service.add_input_variable.return_value = True

    fis_properties_view_model.add_input()
    mock_fuzzy_service.add_input_variable.assert_called_once()


def test_fis_properties_view_model_delete_input(fis_properties_view_model, mock_fis_model):
    input_var = create_mock_input_variable("input1", [0, 1], 0)
    mock_fis_model._fis.Inputs = [input_var]
    mock_fis_model.delete_input.return_value = 1

    fis_properties_view_model.delete_input(0)
    mock_fis_model.delete_input.assert_called_once_with(0)


def test_fis_properties_view_model_add_output(fis_properties_view_model, mock_fuzzy_service, mock_fis_model):
    output_var = create_mock_output_variable("output1", [0, 1], 0)
    mock_fis_model._fis.Outputs = [output_var]
    mock_fuzzy_service.get_output_count.return_value = 1
    mock_fuzzy_service.add_output_variable.return_value = True

    fis_properties_view_model.add_output()
    mock_fuzzy_service.add_output_variable.assert_called_once()


def test_fis_properties_view_model_delete_output(fis_properties_view_model, mock_fis_model):
    output_var = create_mock_output_variable("output1", [0, 1], 0)
    mock_fis_model._fis.Outputs = [output_var]
    mock_fis_model.delete_output.return_value = 1

    fis_properties_view_model.delete_output(0)
    mock_fis_model.delete_output.assert_called_once_with(0)


def test_fis_properties_view_model_select_variable(qtbot, fis_properties_view_model):
    with qtbot.waitSignal(fis_properties_view_model.variable_selected, timeout=1000):
        fis_properties_view_model.select_variable("input1", "input")
    assert fis_properties_view_model._selected_variable == "input1"
    assert fis_properties_view_model._selected_variable_type == "input"


def test_fis_properties_view_model_get_variable_info(fis_properties_view_model, mock_fis_model):
    input_var = create_mock_input_variable("input1", [0, 1], 2)
    mock_fis_model._fis.Inputs = [input_var]

    info = fis_properties_view_model.get_variable_info("input1", "input")
    assert info is not None
    assert info["name"] == "input1"
    assert info["mf_count"] == 2


def test_fis_properties_view_model_get_variable_info_not_found(fis_properties_view_model, mock_fis_model):
    mock_fis_model._fis.Inputs = []

    info = fis_properties_view_model.get_variable_info("nonexistent", "input")
    assert info is None


def test_fis_properties_view_model_update_variable_range(fis_properties_view_model, mock_fis_model):
    input_var = create_mock_input_variable("input1", [0, 1], 0)
    mock_fis_model._fis.Inputs = [input_var]

    result = fis_properties_view_model.update_variable_range("input1", "input", [0, 10])
    assert result is True
    assert input_var.Range == [0, 10]


def test_fis_properties_view_model_refresh_data(fis_properties_view_model, mock_fis_model):
    mock_fis_model._fis.Name = "Test FIS"
    fis_properties_view_model.refresh_data()
    assert True


def test_fis_properties_view_model_convert_inference_system(fis_properties_view_model, mock_fuzzy_service):
    mock_fuzzy_service.convert_inference_system.return_value = True
    result = fis_properties_view_model.convert_inference_system()
    assert result is True


def test_fis_properties_view_model_get_fis_type_display(fis_properties_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_fis_type.return_value = "mamdani"
    assert fis_properties_view_model.get_fis_type_display() == "Mamdani"

    mock_fuzzy_service.get_fis_type.return_value = "sugeno"
    assert fis_properties_view_model.get_fis_type_display() == "Sugeno"


def test_fis_properties_view_model_get_defuzzification_method(fis_properties_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_defuzzification_method.return_value = "centroid"
    assert fis_properties_view_model.get_defuzzification_method() == "centroid"


def test_fis_properties_view_model_set_defuzzification_method(fis_properties_view_model, mock_fuzzy_service):
    mock_fuzzy_service.set_defuzzification_method.return_value = True
    result = fis_properties_view_model.set_defuzzification_method("centroid")
    assert result is True


def test_fis_properties_view_model_get_available_defuzzification_methods_mamdani(
    fis_properties_view_model, mock_fuzzy_service
):
    mock_fuzzy_service.get_fis_type.return_value = "mamdani"
    methods = fis_properties_view_model.get_available_defuzzification_methods()
    assert "centroid" in methods
    assert "wtaver" not in methods


def test_fis_properties_view_model_get_available_defuzzification_methods_sugeno(
    fis_properties_view_model, mock_fuzzy_service
):
    mock_fuzzy_service.get_fis_type.return_value = "sugeno"
    methods = fis_properties_view_model.get_available_defuzzification_methods()
    assert "wtaver" in methods
    assert "centroid" not in methods
