from typing import List, Optional, Protocol


class Command(Protocol):
    """Protocol for undo/redo commands. Must implement do() and undo()."""

    def do(self) -> None:
        """Execute the command."""
        ...

    def undo(self) -> None:
        """Undo the command."""
        ...

    description: Optional[str]


class UndoRedoStack:
    """Generic undo/redo stack using the command pattern.

    Supports push, undo, redo, clear, and can_undo/can_redo.
    Each command must implement do() and undo() methods.
    """

    def __init__(self):
        """Initialize the undo/redo stack."""
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    def push(self, command: Command) -> None:
        """Push a new command and execute it. Clears redo stack.

        Args:
            command (Command): The command to execute and add to the undo stack.
        """
        command.do()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        """Undo the last command."""
        if self.can_undo():
            command = self._undo_stack.pop()
            command.undo()
            self._redo_stack.append(command)

    def redo(self) -> None:
        """Redo the last undone command."""
        if self.can_redo():
            command = self._redo_stack.pop()
            command.do()
            self._undo_stack.append(command)

    def can_undo(self) -> bool:
        """Return True if there is something to undo.

        Returns:
            bool: True if undo is possible, False otherwise.
        """
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        """Return True if there is something to redo.

        Returns:
            bool: True if redo is possible, False otherwise.
        """
        return bool(self._redo_stack)

    def clear(self) -> None:
        """Clear both undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def undo_description(self) -> Optional[str]:
        """Return the description of the next undo command, if any.

        Returns:
            Optional[str]: Description of the next undo command, or None.
        """
        if self.can_undo():
            return getattr(self._undo_stack[-1], "description", None)
        return None

    def redo_description(self) -> Optional[str]:
        """Return the description of the next redo command, if any.

        Returns:
            Optional[str]: Description of the next redo command, or None.
        """
        if self.can_redo():
            return getattr(self._redo_stack[-1], "description", None)
        return None
