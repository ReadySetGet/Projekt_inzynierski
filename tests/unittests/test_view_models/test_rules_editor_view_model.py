import pytest
from unittest.mock import Mock

from app.view_models.rules_editor_view_model import RulesEditorViewModel


@pytest.fixture
def rules_editor_view_model(setup_base_view_model_context, mock_fuzzy_service):
    vm = RulesEditorViewModel()
    return vm


def test_rules_editor_view_model_initialization(rules_editor_view_model):
    assert rules_editor_view_model._selected_rule_index == -1
    assert rules_editor_view_model._rules == []
    assert rules_editor_view_model._input_mf_options == []
    assert rules_editor_view_model._output_mf_options == []


def test_rules_editor_view_model_rules_property(rules_editor_view_model):
    assert rules_editor_view_model.rules == []


def test_rules_editor_view_model_selected_rule_index_property(rules_editor_view_model):
    assert rules_editor_view_model.selected_rule_index == -1


def test_rules_editor_view_model_input_mf_options_property(rules_editor_view_model):
    assert rules_editor_view_model.input_mf_options == []


def test_rules_editor_view_model_output_mf_options_property(rules_editor_view_model):
    assert rules_editor_view_model.output_mf_options == []


def test_rules_editor_view_model_update_rules(qtbot, rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    
    with qtbot.waitSignal(rules_editor_view_model.rules_updated, timeout=1000):
        rules_editor_view_model._update_rules()
    
    assert len(rules_editor_view_model._rules) == 1


def test_rules_editor_view_model_update_mf_options(qtbot, rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1"}
    ]
    mock_fuzzy_service.get_output_variables.return_value = [
        {"name": "output1"}
    ]
    mock_fuzzy_service.get_membership_functions.return_value = [
        {"name": "mf1"}
    ]
    
    with qtbot.waitSignal(rules_editor_view_model.input_mf_options_updated, timeout=1000):
        rules_editor_view_model._update_mf_options()
    
    assert len(rules_editor_view_model._input_mf_options) > 0


def test_rules_editor_view_model_select_rule(qtbot, rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    
    with qtbot.waitSignal(rules_editor_view_model.rule_selected, timeout=1000):
        rules_editor_view_model.select_rule(0)
    
    assert rules_editor_view_model._selected_rule_index == 0


def test_rules_editor_view_model_select_rule_invalid_index(rules_editor_view_model):
    rules_editor_view_model.select_rule(10)
    assert rules_editor_view_model._selected_rule_index == -1


def test_rules_editor_view_model_add_rule(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.add_rule.return_value = True
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Placeholder", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    
    result = rules_editor_view_model.add_rule()
    assert result is True
    mock_fuzzy_service.add_rule.assert_called_once()


def test_rules_editor_view_model_delete_rule(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    mock_fuzzy_service.delete_rule.return_value = True
    
    result = rules_editor_view_model.delete_rule(0)
    assert result is True
    mock_fuzzy_service.delete_rule.assert_called_once_with(0)


def test_rules_editor_view_model_delete_rule_invalid_index(rules_editor_view_model):
    result = rules_editor_view_model.delete_rule(10)
    assert result is False


def test_rules_editor_view_model_update_rule(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    mock_fuzzy_service.update_rule.return_value = True
    
    result = rules_editor_view_model.update_rule(0, [1, 1], [1], 0.8, 1, [1, 1])
    assert result is True
    mock_fuzzy_service.update_rule.assert_called_once()


def test_rules_editor_view_model_update_rule_name(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    mock_fuzzy_service._rule_manager = Mock()
    mock_fuzzy_service._rule_manager.update_rule_name.return_value = True
    
    result = rules_editor_view_model.update_rule_name(0, "New Name")
    assert result is True


def test_rules_editor_view_model_update_rule_weight(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    mock_fuzzy_service.update_rule.return_value = True
    
    result = rules_editor_view_model.update_rule_weight(0, 0.8)
    assert result is True


def test_rules_editor_view_model_update_rule_connection(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    mock_fuzzy_service.update_rule.return_value = True
    
    result = rules_editor_view_model.update_rule_connection(0, 0)
    assert result is True


def test_rules_editor_view_model_get_rule_text(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    mock_fuzzy_service.get_rule_text.return_value = "If input1 is mf1 then output1 is mf1"
    
    text = rules_editor_view_model.get_rule_text(0)
    assert "Rule" in text or "input1" in text


def test_rules_editor_view_model_get_selected_rule(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1, "is_mf": [1]}
    ]
    rules_editor_view_model._update_rules()
    rules_editor_view_model.select_rule(0)
    
    rule = rules_editor_view_model.get_selected_rule()
    assert rule is not None
    assert rule["name"] == "Rule 1"


def test_rules_editor_view_model_clear_all_rules(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.clear_all_rules.return_value = True
    mock_fuzzy_service.get_rules.return_value = []
    
    result = rules_editor_view_model.clear_all_rules()
    assert result is True


def test_rules_editor_view_model_add_all_possible_rules(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.add_all_possible_rules.return_value = True
    mock_fuzzy_service.get_rules.return_value = []
    
    result = rules_editor_view_model.add_all_possible_rules()
    assert result is True


def test_rules_editor_view_model_refresh_data(rules_editor_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_rules.return_value = []
    mock_fuzzy_service.get_input_variables.return_value = []
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_membership_functions.return_value = []
    
    rules_editor_view_model.refresh_data()
    assert True

