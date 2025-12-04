from unittest.mock import Mock

import pytest
from PyQt6.QtWidgets import QWidget

from app.utils.shortcut_manager import ShortcutManager


@pytest.fixture
def parent_widget(qt_application):
    return QWidget()


@pytest.fixture
def shortcut_manager(parent_widget):
    return ShortcutManager(parent_widget)


def test_shortcut_manager_initialization(shortcut_manager, parent_widget):
    assert shortcut_manager.parent == parent_widget
    assert len(shortcut_manager._shortcuts) == 0
    assert len(shortcut_manager._actions) == 0


def test_shortcut_manager_register_shortcut(shortcut_manager):
    action = Mock()
    result = shortcut_manager.register_shortcut("Ctrl+S", action)
    assert result is True
    assert "Ctrl+S" in shortcut_manager._shortcuts
    assert "Ctrl+S" in shortcut_manager._actions


def test_shortcut_manager_register_shortcut_conflict(shortcut_manager):
    action1 = Mock()
    action2 = Mock()
    shortcut_manager.register_shortcut("Ctrl+S", action1)
    result = shortcut_manager.register_shortcut("Ctrl+S", action2)
    assert result is False
    assert shortcut_manager._actions["Ctrl+S"] == action1


def test_shortcut_manager_update_shortcut(shortcut_manager):
    action = Mock()
    shortcut_manager.register_shortcut("Ctrl+S", action)
    result = shortcut_manager.update_shortcut("Ctrl+S", "Ctrl+Shift+S")
    assert result is True
    assert "Ctrl+S" not in shortcut_manager._shortcuts
    assert "Ctrl+Shift+S" in shortcut_manager._shortcuts
    assert shortcut_manager._actions["Ctrl+Shift+S"] == action


def test_shortcut_manager_update_shortcut_not_found(shortcut_manager):
    result = shortcut_manager.update_shortcut("Ctrl+S", "Ctrl+Shift+S")
    assert result is False


def test_shortcut_manager_update_shortcut_conflict(shortcut_manager):
    action1 = Mock()
    action2 = Mock()
    shortcut_manager.register_shortcut("Ctrl+S", action1)
    shortcut_manager.register_shortcut("Ctrl+Shift+S", action2)
    result = shortcut_manager.update_shortcut("Ctrl+S", "Ctrl+Shift+S")
    assert result is False


def test_shortcut_manager_remove_shortcut(shortcut_manager):
    action = Mock()
    shortcut_manager.register_shortcut("Ctrl+S", action)
    result = shortcut_manager.remove_shortcut("Ctrl+S")
    assert result is True
    assert "Ctrl+S" not in shortcut_manager._shortcuts
    assert "Ctrl+S" not in shortcut_manager._actions


def test_shortcut_manager_remove_shortcut_not_found(shortcut_manager):
    result = shortcut_manager.remove_shortcut("Ctrl+S")
    assert result is False


def test_shortcut_manager_list_shortcuts(shortcut_manager):
    action1 = Mock()
    action2 = Mock()
    shortcut_manager.register_shortcut("Ctrl+S", action1)
    shortcut_manager.register_shortcut("Ctrl+O", action2)
    shortcuts = shortcut_manager.list_shortcuts()
    assert len(shortcuts) == 2
    assert ("Ctrl+S", action1) in shortcuts
    assert ("Ctrl+O", action2) in shortcuts


def test_shortcut_manager_has_conflict(shortcut_manager):
    action = Mock()
    assert shortcut_manager.has_conflict("Ctrl+S") is False
    shortcut_manager.register_shortcut("Ctrl+S", action)
    assert shortcut_manager.has_conflict("Ctrl+S") is True


def test_shortcut_manager_clear(shortcut_manager):
    action1 = Mock()
    action2 = Mock()
    shortcut_manager.register_shortcut("Ctrl+S", action1)
    shortcut_manager.register_shortcut("Ctrl+O", action2)
    shortcut_manager.clear()
    assert len(shortcut_manager._shortcuts) == 0
    assert len(shortcut_manager._actions) == 0
