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

        self.systemBrowserTreeView = QtWidgets.QTreeView(parent=self)
        self.systemBrowserTreeView.setGeometry(QtCore.QRect(0, 300, 301, 341))
        self.systemBrowserTreeView.setObjectName("systemBrowserTreeView")

        self.systemBrowserLabel = QtWidgets.QLabel(parent=self)
        self.systemBrowserLabel.setGeometry(QtCore.QRect(4, 274, 281, 21))
        self.systemBrowserLabel.setObjectName("systemBrowserLabel")

        self.designBrowserLabel = QtWidgets.QLabel(parent=self)
        self.designBrowserLabel.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.designBrowserLabel.setObjectName("designBrowserLabel")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.systemBrowserLabel.setText(_translate("MainWindow", "SYSTEM BROWSER"))
        self.designBrowserLabel.setText(_translate("MainWindow", "DESIGN BROWSER"))
