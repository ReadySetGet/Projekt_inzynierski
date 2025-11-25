import pytest

from app.view_models.editor_tab_view_model import EditorTabViewModel


@pytest.fixture
def editor_tab_view_model(setup_base_view_model_context, mock_fuzzy_service):
    return EditorTabViewModel()


def test_editor_tab_view_model_initialization(editor_tab_view_model):
    assert editor_tab_view_model._current_tab == 0


def test_editor_tab_view_model_current_tab_property(editor_tab_view_model):
    assert editor_tab_view_model.current_tab == 0
    editor_tab_view_model.current_tab = 1
    assert editor_tab_view_model.current_tab == 1


def test_editor_tab_view_model_current_tab_setter_emits_signal(qtbot, editor_tab_view_model):
    with qtbot.waitSignal(editor_tab_view_model.current_tab_changed, timeout=1000):
        editor_tab_view_model.current_tab = 2


def test_editor_tab_view_model_set_current_tab(editor_tab_view_model):
    editor_tab_view_model.set_current_tab(3)
    assert editor_tab_view_model.current_tab == 3


def test_editor_tab_view_model_update_fis_properties_tab(qtbot, editor_tab_view_model):
    with qtbot.waitSignal(editor_tab_view_model.fis_properties_updated, timeout=1000):
        editor_tab_view_model.update_fis_properties_tab()


def test_editor_tab_view_model_update_mf_properties_tab(qtbot, editor_tab_view_model):
    with qtbot.waitSignal(editor_tab_view_model.mf_properties_updated, timeout=1000):
        editor_tab_view_model.update_mf_properties_tab()


def test_editor_tab_view_model_update_rule_properties_tab(qtbot, editor_tab_view_model):
    with qtbot.waitSignal(editor_tab_view_model.rule_properties_updated, timeout=1000):
        editor_tab_view_model.update_rule_properties_tab()


def test_editor_tab_view_model_update_all_tabs(qtbot, editor_tab_view_model, mock_fuzzy_service):
    signals_received = []

    def on_fis_updated():
        signals_received.append("fis")

    def on_mf_updated():
        signals_received.append("mf")

    def on_rule_updated():
        signals_received.append("rule")

    editor_tab_view_model.fis_properties_updated.connect(on_fis_updated)
    editor_tab_view_model.mf_properties_updated.connect(on_mf_updated)
    editor_tab_view_model.rule_properties_updated.connect(on_rule_updated)

    editor_tab_view_model._update_all_tabs()

    qtbot.wait(100)
    assert "fis" in signals_received
    assert "mf" in signals_received
    assert "rule" in signals_received


def test_editor_tab_view_model_refresh_data(editor_tab_view_model, mock_fuzzy_service):
    editor_tab_view_model.refresh_data()
    assert True


def test_editor_tab_view_model_refresh_all_tabs(editor_tab_view_model, mock_fuzzy_service):
    editor_tab_view_model.refresh_all_tabs()
    assert True


def test_editor_tab_view_model_get_selected_variable_info_input(editor_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_selected_input_name.return_value = "input1"
    mock_fuzzy_service.get_selected_input_data.return_value = {"name": "input1", "range": [0, 1]}
    mock_fuzzy_service.get_selected_output_name.return_value = None

    info = editor_tab_view_model.get_selected_variable_info()
    assert info is not None
    assert info["name"] == "input1"
    assert info["type"] == "input"


def test_editor_tab_view_model_get_selected_variable_info_output(editor_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_selected_input_name.return_value = None
    mock_fuzzy_service.get_selected_output_name.return_value = "output1"
    mock_fuzzy_service.get_selected_output_data.return_value = {"name": "output1", "range": [0, 1]}

    info = editor_tab_view_model.get_selected_variable_info()
    assert info is not None
    assert info["name"] == "output1"
    assert info["type"] == "output"


def test_editor_tab_view_model_get_selected_variable_info_none(editor_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_selected_input_name.return_value = None
    mock_fuzzy_service.get_selected_output_name.return_value = None

    info = editor_tab_view_model.get_selected_variable_info()
    assert info is None


def test_editor_tab_view_model_get_selected_variable_info_no_service(editor_tab_view_model):
    editor_tab_view_model._fuzzy_service = None
    info = editor_tab_view_model.get_selected_variable_info()
    assert info is None
