import pytest

from app.view_models.top_menu_view_model import TopMenuViewModel


@pytest.fixture
def top_menu_view_model(setup_base_view_model_context, mock_fuzzy_service):
    return TopMenuViewModel()


def test_top_menu_view_model_initialization(top_menu_view_model):
    assert top_menu_view_model._current_tab == 0


def test_top_menu_view_model_current_tab_property(top_menu_view_model):
    assert top_menu_view_model.current_tab == 0
    top_menu_view_model.current_tab = 1
    assert top_menu_view_model.current_tab == 1


def test_top_menu_view_model_current_tab_setter_emits_signal(qtbot, top_menu_view_model):
    with qtbot.waitSignal(top_menu_view_model.current_tab_changed, timeout=1000):
        top_menu_view_model.current_tab = 1


def test_top_menu_view_model_set_current_tab(top_menu_view_model):
    top_menu_view_model.set_current_tab(2)
    assert top_menu_view_model.current_tab == 2


def test_top_menu_view_model_add_input(top_menu_view_model, mock_fuzzy_service):
    initial_count = mock_fuzzy_service.get_input_count()
    top_menu_view_model.add_input()
    mock_fuzzy_service.add_input_variable.assert_called_once_with(f"input{initial_count + 1}", 0.0, 1.0)


def test_top_menu_view_model_delete_input(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_count.return_value = 2
    top_menu_view_model.delete_input()
    mock_fuzzy_service.delete_input_variable.assert_called_once_with(1)


def test_top_menu_view_model_delete_input_when_zero_inputs(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_count.return_value = 0
    top_menu_view_model.delete_input()
    mock_fuzzy_service.delete_input_variable.assert_not_called()


def test_top_menu_view_model_add_output(top_menu_view_model, mock_fuzzy_service):
    initial_count = mock_fuzzy_service.get_output_count()
    top_menu_view_model.add_output()
    mock_fuzzy_service.add_output_variable.assert_called_once_with(f"output{initial_count + 1}", 0.0, 1.0)


def test_top_menu_view_model_delete_output(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_output_count.return_value = 1
    top_menu_view_model.delete_output()
    mock_fuzzy_service.delete_output_variable.assert_called_once_with(0)


def test_top_menu_view_model_delete_output_when_zero_outputs(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_output_count.return_value = 0
    top_menu_view_model.delete_output()
    mock_fuzzy_service.delete_output_variable.assert_not_called()


def test_top_menu_view_model_import_model(top_menu_view_model, mock_fuzzy_service):
    result = top_menu_view_model.import_model("test.fis")
    assert result is True
    mock_fuzzy_service.import_model.assert_called_once_with("test.fis")


def test_top_menu_view_model_export_model(top_menu_view_model, mock_fuzzy_service):
    result = top_menu_view_model.export_model("test.fis")
    assert result is True
    mock_fuzzy_service.export_model.assert_called_once_with("test.fis")


def test_top_menu_view_model_can_delete_input(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_count.return_value = 1
    assert top_menu_view_model.can_delete_input() is True
    mock_fuzzy_service.get_input_count.return_value = 0
    assert top_menu_view_model.can_delete_input() is False


def test_top_menu_view_model_can_delete_output(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_output_count.return_value = 1
    assert top_menu_view_model.can_delete_output() is True
    mock_fuzzy_service.get_output_count.return_value = 0
    assert top_menu_view_model.can_delete_output() is False


def test_top_menu_view_model_get_input_count(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_count.return_value = 3
    assert top_menu_view_model.get_input_count() == 3


def test_top_menu_view_model_get_output_count(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_output_count.return_value = 2
    assert top_menu_view_model.get_output_count() == 2


def test_top_menu_view_model_refresh_data(top_menu_view_model):
    top_menu_view_model.refresh_data()
    assert True


def test_top_menu_view_model_convert_inference_system(top_menu_view_model, mock_fuzzy_service):
    result = top_menu_view_model.convert_inference_system()
    assert result is True
    mock_fuzzy_service.convert_inference_system.assert_called_once()


def test_top_menu_view_model_get_fis_type(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_fis_type.return_value = "sugeno"
    assert top_menu_view_model.get_fis_type() == "sugeno"


def test_top_menu_view_model_get_interpolation_points(top_menu_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_interpolation_points.return_value = 20
    assert top_menu_view_model.get_interpolation_points() == 20


def test_top_menu_view_model_set_interpolation_points(top_menu_view_model, mock_fuzzy_service):
    result = top_menu_view_model.set_interpolation_points(25)
    assert result is True
    mock_fuzzy_service.set_interpolation_points.assert_called_once_with(25)
