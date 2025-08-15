from PyQt6 import QtCore, QtGui, QtWidgets


class BrowserFrameWidget(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("browserFrane")
        self._setup_ui()

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

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.system_browser_label.setText(_translate("MainWindow", "SYSTEM BROWSER"))
        self.design_browser_label.setText(_translate("MainWindow", "DESIGN BROWSER"))
