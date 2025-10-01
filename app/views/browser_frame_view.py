from PyQt6 import QtCore, QtWidgets

from app.view_models.base_view_model import BaseViewModel
from app.views.base_frame_view import BaseFrameView


class BrowserFrameWidget(BaseFrameView):
    """Browser frame widget for displaying system information."""

    view_model: BaseViewModel

    def __init__(self, view_model: BaseViewModel, parent=None):
        """Initialize the browser frame widget.

        Args:
            view_model: The view model for the browser frame widget.
            parent: The parent widget.
        """
        super().__init__(parent=parent)
        self._view_model = view_model
        self.setObjectName("browserFrane")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName("browserFrame")

        self.system_browser_tree_view = QtWidgets.QTreeView(parent=self)
        self.system_browser_tree_view.setGeometry(QtCore.QRect(0, 300, 301, 341))
        self.system_browser_tree_view.setObjectName("system_browser_tree_view")

        self.system_browser_label = QtWidgets.QLabel(parent=self)
        self.system_browser_label.setGeometry(QtCore.QRect(4, 274, 281, 21))
        self.system_browser_label.setObjectName("system_browser_label")

        self.design_browser_label = QtWidgets.QLabel(parent=self)
        self.design_browser_label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.design_browser_label.setObjectName("design_browser_label")

    def _retranslate_ui(self):
        self.system_browser_label.setText(self.t("SYSTEM BROWSER"))
        self.design_browser_label.setText(self.t("DESIGN BROWSER"))
