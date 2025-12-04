from typing import Callable, Dict, List, Optional, Tuple

from PyQt6 import QtCore
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget


class ShortcutManager:
    """Manages keyboard shortcuts for a given QWidget parent.

    Allows dynamic registration, removal, updating, and listing of shortcuts.
    Includes conflict detection and runtime management.
    """

    def __init__(self, parent: QWidget):
        """Initialize the ShortcutManager.

        Args:
            parent (QWidget): The parent widget to which shortcuts are attached.
        """
        self.parent = parent
        self._shortcuts: Dict[str, QShortcut] = {}
        self._actions: Dict[str, Callable] = {}

    def register_shortcut(self, key_sequence: str, action: Callable, description: Optional[str] = None) -> bool:
        """Register a new shortcut.

        Args:
            key_sequence (str): The key sequence (e.g., 'Ctrl+H').
            action (Callable): The function to call when triggered.
            description (str, optional): Description for the shortcut.

        Returns:
            bool: True if registered, False if conflict.
        """
        if key_sequence in self._shortcuts:
            return False  # Conflict
        shortcut = QShortcut(QKeySequence(key_sequence), self.parent)
        shortcut.setContext(QtCore.Qt.ShortcutContext.WindowShortcut)
        shortcut.activated.connect(action)
        self._shortcuts[key_sequence] = shortcut
        self._actions[key_sequence] = action
        return True

    def update_shortcut(self, old_key_sequence: str, new_key_sequence: str) -> bool:
        """Update an existing shortcut to a new key sequence.

        Args:
            old_key_sequence (str): The current key sequence.
            new_key_sequence (str): The new key sequence to assign.

        Returns:
            bool: True if successful, False if conflict or not found.
        """
        if old_key_sequence not in self._shortcuts or new_key_sequence in self._shortcuts:
            return False
        action = self._actions[old_key_sequence]
        self.remove_shortcut(old_key_sequence)
        return self.register_shortcut(new_key_sequence, action)

    def remove_shortcut(self, key_sequence: str) -> bool:
        """Remove a shortcut by its key sequence.

        Args:
            key_sequence (str): The key sequence to remove.

        Returns:
            bool: True if removed, False if not found.
        """
        shortcut = self._shortcuts.pop(key_sequence, None)
        self._actions.pop(key_sequence, None)
        if shortcut:
            shortcut.activated.disconnect()
            shortcut.setParent(None)
            return True
        return False

    def list_shortcuts(self) -> List[Tuple[str, Callable]]:
        """List all registered shortcuts as (key_sequence, action) tuples.

        Returns:
            List[Tuple[str, Callable]]: List of registered shortcuts.
        """
        return list(self._actions.items())

    def has_conflict(self, key_sequence: str) -> bool:
        """Check if a key sequence is already registered.

        Args:
            key_sequence (str): The key sequence to check.

        Returns:
            bool: True if conflict exists, False otherwise.
        """
        return key_sequence in self._shortcuts

    def clear(self):
        """Remove all shortcuts managed by this manager."""
        for key in list(self._shortcuts.keys()):
            self.remove_shortcut(key)
