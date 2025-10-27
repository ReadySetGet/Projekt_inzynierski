import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6 import QtCore, QtWidgets

from app.views.base_widget_view import BaseWidgetView

"""Import necessary for project=3D to be available in matplotlib"""
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

# from mpl_toolkits.mplot3d import Axes3D  # Unused import


def fun(x, y):
    """Placeholder function implemented to showcase the 3D plot."""
    return x**2 + y


class AreaPlot(BaseWidgetView):
    """Class used to display area plot widget.

    It does not have a Parent attribute as to be displayed in a separate window.
    """

    def __init__(self):
        """Initialize the area plot widget."""
        super().__init__()
        self.setObjectName("area_plot")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.resize(650, 629)
        self.setWindowTitle("Area Plot")

        """Setting up plot area for the 3D plot.

        We set up a frame which serves as an area for our Vertical Box Layout.
        The class uses matplotlib PyQT integration in order to be able to
        embed matplotlib cavas in the layout.
        """
        self.area_plot_frame = QtWidgets.QFrame(parent=self)
        self.area_plot_frame.setGeometry(QtCore.QRect(10, 170, 621, 401))
        self.area_plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.area_plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.area_plot_frame.setObjectName("area_plot_frame")

        self.frame_layout = QtWidgets.QVBoxLayout(self.area_plot_frame)

        """Example placeholder data""" ""
        x = y = np.arange(0.0, 100.0, 5)
        X, Y = np.meshgrid(x, y)
        zs = np.array(fun(np.ravel(X), np.ravel(Y)))
        Z = zs.reshape(X.shape)
        mfs = ["Mf1", "Mf2"]

        fig = plt.Figure(figsize=(1500, 1500))

        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z)
        ax.set_xlabel("MF 1")
        ax.set_ylabel("MF 2")
        ax.set_zlabel("Input")

        canvas = FigureCanvas(fig)

        self.frame_layout.addWidget(NavigationToolbar(canvas, self))
        self.frame_layout.addWidget(canvas)

        self.system_label = QtWidgets.QLabel(parent=self)
        self.system_label.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.system_label.setObjectName("system_label")

        self.name_label = QtWidgets.QLabel(parent=self)
        self.name_label.setGeometry(QtCore.QRect(80, 10, 55, 16))
        self.name_label.setObjectName("name_label")

        self.line = QtWidgets.QFrame(parent=self)
        self.line.setGeometry(QtCore.QRect(10, 20, 621, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")

        self.axes_label = QtWidgets.QLabel(parent=self)
        self.axes_label.setGeometry(QtCore.QRect(10, 40, 55, 21))
        self.axes_label.setObjectName("axes_label")

        """ComboBox is QT name for dropdown widgets."""
        self.x_combobox = QtWidgets.QComboBox(parent=self)
        self.x_combobox.setGeometry(QtCore.QRect(120, 40, 121, 22))
        self.x_combobox.setObjectName("x_combobox")
        self.x_combobox.addItems(mfs)

        self.x_label = QtWidgets.QLabel(parent=self)
        self.x_label.setGeometry(QtCore.QRect(100, 40, 16, 21))
        self.x_label.setObjectName("x_label")

        self.y_label = QtWidgets.QLabel(parent=self)
        self.y_label.setGeometry(QtCore.QRect(280, 40, 21, 21))
        self.y_label.setObjectName("y_label")

        self.y_combobox = QtWidgets.QComboBox(parent=self)
        self.y_combobox.setGeometry(QtCore.QRect(300, 40, 121, 22))
        self.y_combobox.setObjectName("y_combobox")
        self.y_combobox.addItems(mfs)

        self.z_combobox = QtWidgets.QComboBox(parent=self)
        self.z_combobox.setGeometry(QtCore.QRect(470, 40, 121, 22))
        self.z_combobox.setObjectName("z_combobox")
        self.z_combobox.addItem("Variable 1")
        self.z_combobox.addItem("Variable 2")

        self.z_label = QtWidgets.QLabel(parent=self)
        self.z_label.setGeometry(QtCore.QRect(450, 40, 21, 21))
        self.z_label.setObjectName("z_label")

        self.mesh_label = QtWidgets.QLabel(parent=self)
        self.mesh_label.setGeometry(QtCore.QRect(10, 80, 81, 21))
        self.mesh_label.setObjectName("mesh_label")

        self.x_label_2 = QtWidgets.QLabel(parent=self)
        self.x_label_2.setGeometry(QtCore.QRect(100, 80, 16, 21))
        self.x_label_2.setObjectName("x_label_2")

        self.x_spinbox = QtWidgets.QSpinBox(parent=self)
        self.x_spinbox.setGeometry(QtCore.QRect(120, 80, 121, 22))
        self.x_spinbox.setProperty("value", 15)
        self.x_spinbox.setObjectName("x_spinbox")

        self.y_label_2 = QtWidgets.QLabel(parent=self)
        self.y_label_2.setGeometry(QtCore.QRect(280, 80, 16, 21))
        self.y_label_2.setObjectName("y_label_2")

        self.y_spinbox = QtWidgets.QSpinBox(parent=self)
        self.y_spinbox.setGeometry(QtCore.QRect(300, 80, 121, 22))
        self.y_spinbox.setProperty("value", 15)
        self.y_spinbox.setObjectName("y_spinbox")

        self.reference_label = QtWidgets.QLabel(parent=self)
        self.reference_label.setGeometry(QtCore.QRect(10, 120, 101, 31))
        self.reference_label.setObjectName("reference_label")

        self.line_edit = QtWidgets.QLineEdit(parent=self)
        self.line_edit.setEnabled(False)
        self.line_edit.setGeometry(QtCore.QRect(120, 121, 113, 31))
        self.line_edit.setObjectName("line_edit")

    def _retranslate_ui(self):
        self.system_label.setText(self.t("SYSTEM"))
        self.name_label.setText(self.t("NAME"))
        self.axes_label.setText(self.t("AXES"))
        self.x_label.setText(self.t("X"))
        self.y_label.setText(self.t("Y"))
        self.z_label.setText(self.t("Z"))
        self.mesh_label.setText(self.t("MESH_POINTS"))
        self.x_label_2.setText(self.t("X"))
        self.y_label_2.setText(self.t("Y"))
        self.reference_label.setText(self.t("REFERENCE_INPUTS"))
