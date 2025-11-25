from unittest.mock import Mock

import pytest

from app.view_models.central_tab_view_model import CentralTabViewModel


@pytest.fixture
def central_tab_view_model(setup_base_view_model_context, mock_fuzzy_service):
    vm = CentralTabViewModel()
    vm.set_fuzzy_service(mock_fuzzy_service)
    return vm


def test_central_tab_view_model_initialization(central_tab_view_model):
    assert central_tab_view_model._current_tab == 0
    assert central_tab_view_model._rules == []
    assert central_tab_view_model._system_name == "Placeholder Name"
    assert central_tab_view_model._selected_rule_index == -1


def test_central_tab_view_model_current_tab_property(central_tab_view_model):
    assert central_tab_view_model.current_tab == 0
    central_tab_view_model.current_tab = 1
    assert central_tab_view_model.current_tab == 1


def test_central_tab_view_model_current_tab_setter_emits_signal(qtbot, central_tab_view_model):
    with qtbot.waitSignal(central_tab_view_model.current_tab_changed, timeout=1000):
        central_tab_view_model.current_tab = 2


def test_central_tab_view_model_system_name_property(central_tab_view_model):
    assert central_tab_view_model.system_name == "Placeholder Name"
    central_tab_view_model.system_name = "New Name"
    assert central_tab_view_model.system_name == "New Name"


def test_central_tab_view_model_system_name_setter_emits_signal(qtbot, central_tab_view_model):
    with qtbot.waitSignal(central_tab_view_model.system_name_changed, timeout=1000):
        central_tab_view_model.system_name = "Test System"


def test_central_tab_view_model_rules_property(central_tab_view_model):
    assert central_tab_view_model.rules == []


def test_central_tab_view_model_selected_rule_index_property(central_tab_view_model):
    assert central_tab_view_model.selected_rule_index == -1


def test_central_tab_view_model_set_current_tab(central_tab_view_model):
    central_tab_view_model.set_current_tab(3)
    assert central_tab_view_model.current_tab == 3


def test_central_tab_view_model_select_rule(central_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    central_tab_view_model._update_rules()
    central_tab_view_model.select_rule(0)
    assert central_tab_view_model._selected_rule_index == 0


def test_central_tab_view_model_select_rule_invalid_index(central_tab_view_model):
    central_tab_view_model.select_rule(10)
    assert central_tab_view_model._selected_rule_index == -1


def test_central_tab_view_model_select_rule_emits_signal(qtbot, central_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    central_tab_view_model._update_rules()
    with qtbot.waitSignal(central_tab_view_model.rule_selected, timeout=1000):
        central_tab_view_model.select_rule(0)


def test_central_tab_view_model_update_fis_plot(qtbot, central_tab_view_model):
    with qtbot.waitSignal(central_tab_view_model.fis_plot_updated, timeout=1000):
        central_tab_view_model.update_fis_plot()


def test_central_tab_view_model_update_mf_plot(qtbot, central_tab_view_model):
    with qtbot.waitSignal(central_tab_view_model.mf_plot_updated, timeout=1000):
        central_tab_view_model.update_mf_plot("input1", 0)


def test_central_tab_view_model_set_fuzzy_service(central_tab_view_model, mock_fuzzy_service):
    new_service = Mock()
    new_service.system_changed = Mock()
    new_service.inference_completed = Mock()
    central_tab_view_model.set_fuzzy_service(new_service)
    assert central_tab_view_model._fuzzy_service == new_service


def test_central_tab_view_model_update_rules(central_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1, 0], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1, 1]}
    ]
    central_tab_view_model._update_rules()
    assert len(central_tab_view_model._rules) == 1
    assert central_tab_view_model._rules[0]["name"] == "Rule 1"


def test_central_tab_view_model_update_rules_emits_signal(qtbot, central_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    with qtbot.waitSignal(central_tab_view_model.rules_updated, timeout=1000):
        central_tab_view_model._update_rules()


def test_central_tab_view_model_update_system_name(central_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_system_status.return_value = {"name": "Test FIS"}
    central_tab_view_model._update_system_name()
    assert central_tab_view_model.system_name == "Test FIS"


def test_central_tab_view_model_refresh_data(central_tab_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = []
    mock_fuzzy_service.get_system_status.return_value = {"name": "Test"}
    central_tab_view_model.refresh_data()
    assert True
