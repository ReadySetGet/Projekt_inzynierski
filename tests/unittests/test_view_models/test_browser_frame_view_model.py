from unittest.mock import Mock

import pytest

from app.view_models.browser_frame_view_model import BrowserFrameViewModel


@pytest.fixture
def browser_frame_view_model(setup_base_view_model_context, mock_fuzzy_service):
    vm = BrowserFrameViewModel()
    return vm


def test_browser_frame_view_model_initialization(browser_frame_view_model):
    assert browser_frame_view_model._system_items == []
    assert browser_frame_view_model._design_items == []


def test_browser_frame_view_model_system_items_property(browser_frame_view_model):
    assert browser_frame_view_model.system_items == []


def test_browser_frame_view_model_design_items_property(browser_frame_view_model):
    assert browser_frame_view_model.design_items == []


def test_browser_frame_view_model_get_system_items(browser_frame_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [
        {"name": "input1", "range": [0, 1], "membership_functions": []}
    ]
    mock_fuzzy_service.get_output_variables.return_value = [
        {"name": "output1", "range": [0, 1], "membership_functions": []}
    ]
    mock_fuzzy_service.get_rules.return_value = []

    items = browser_frame_view_model._get_system_items()
    assert len(items) == 2
    assert items[0]["type"] == "input"
    assert items[1]["type"] == "output"


def test_browser_frame_view_model_get_system_items_with_rules(browser_frame_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = []
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_rules.return_value = [
        {"name": "Rule 1", "antecedent": [1], "consequent": [1], "weight": 1.0, "connection": 1}
    ]

    items = browser_frame_view_model._get_system_items()
    assert len(items) == 1
    assert items[0]["type"] == "rule"


def test_browser_frame_view_model_get_design_items(browser_frame_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = [{"name": "input1", "range": [0, 1]}]
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_membership_functions.return_value = [
        {"name": "mf1", "type": "trimf", "parameters": [0, 0.5, 1]}
    ]

    items = browser_frame_view_model._get_design_items()
    assert len(items) == 1
    assert items[0]["type"] == "input_mf"


def test_browser_frame_view_model_select_system_item(qtbot, browser_frame_view_model):
    item_data = {"type": "input", "name": "input1"}
    with qtbot.waitSignal(browser_frame_view_model.system_item_selected, timeout=1000):
        browser_frame_view_model.select_system_item("input1", item_data)


def test_browser_frame_view_model_select_design_item(qtbot, browser_frame_view_model):
    item_data = {"type": "input_mf", "name": "mf1"}
    with qtbot.waitSignal(browser_frame_view_model.design_item_selected, timeout=1000):
        browser_frame_view_model.select_design_item("mf1", item_data)


def test_browser_frame_view_model_refresh_data(qtbot, browser_frame_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = []
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_rules.return_value = []
    mock_fuzzy_service.get_membership_functions.return_value = []

    with qtbot.waitSignal(browser_frame_view_model.system_browser_updated, timeout=1000):
        browser_frame_view_model.refresh_data()


def test_browser_frame_view_model_refresh_browser(browser_frame_view_model, mock_fuzzy_service):
    mock_fuzzy_service.get_input_variables.return_value = []
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_rules.return_value = []
    mock_fuzzy_service.get_membership_functions.return_value = []

    browser_frame_view_model.refresh_browser()
    assert True


def test_browser_frame_view_model_update_browser_data_emits_signals(
    qtbot, browser_frame_view_model, mock_fuzzy_service
):
    mock_fuzzy_service.get_input_variables.return_value = []
    mock_fuzzy_service.get_output_variables.return_value = []
    mock_fuzzy_service.get_rules.return_value = []
    mock_fuzzy_service.get_membership_functions.return_value = []

    with qtbot.waitSignal(browser_frame_view_model.design_browser_updated, timeout=1000):
        browser_frame_view_model._update_browser_data()
