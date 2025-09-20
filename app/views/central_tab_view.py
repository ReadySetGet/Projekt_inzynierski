from PyQt6 import QtCore, QtGui, QtWidgets


class CentralTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("centralTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_plot = QtWidgets.QWidget()
        self.fis_plot.setObjectName("fis_plot")

        self.graph_frame = QtWidgets.QFrame(parent=self.fis_plot)
        self.graph_frame.setGeometry(QtCore.QRect(-1, 49, 461, 471))
        self.graph_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.graph_frame.setObjectName("graph_frame")
        self.addTab(self.fis_plot, "")

        self.mf_plot = QtWidgets.QWidget()
        self.mf_plot.setObjectName("mf_plot")

        self.plot_frame = QtWidgets.QFrame(parent=self.mf_plot)
        self.plot_frame.setGeometry(QtCore.QRect(0, 60, 531, 551))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plot_frame.setObjectName("plot_frame")

        self.seperator_line = QtWidgets.QFrame(parent=self.mf_plot)
        self.seperator_line.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperator_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line.setObjectName("seperator_line")

        self.system_name_label = QtWidgets.QLabel(parent=self.mf_plot)
        self.system_name_label.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.system_name_label.setObjectName("system_name_label")
        self.addTab(self.mf_plot, "")

        self.rule_editor = QtWidgets.QWidget()
        self.rule_editor.setObjectName("rule_editor")

        self.table_widget = QtWidgets.QTableWidget(parent=self.rule_editor)
        self.table_widget.setGeometry(QtCore.QRect(20, 100, 431, 491))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)

        self.addTab(self.rule_editor, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fis_plot), _translate("MainWindow", "FIS Plot"))
        self.system_name_label.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.mf_plot), _translate("MainWindow", "MF Editor"))
        self.setTabText(self.indexOf(self.rule_editor), _translate("MainWindow", "Rule Editor"))
