import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt6 import QtCore, QtWidgets

from app.view_models.area_plot_view_model import AreaPlotViewModel
from app.views.base_widget_view import BaseWidgetView


class AreaPlot(BaseWidgetView):
    """Area plot widget for visualizing control surfaces in a separate window."""

    def __init__(self):
        """Initialize the area plot widget."""
        super().__init__()
        self.setObjectName("area_plot")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.view_model = AreaPlotViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self._input_variables = []
        self._output_variables = []
        self._is_updating_controls = False

        self._setup_ui()
        self._retranslate_ui()
        self._populate_controls()
        self._connect_signals()
        self._update_surface()

    def _setup_ui(self):
        self.resize(800, 700)
        self.setWindowTitle("Control Surface")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        system_layout = QtWidgets.QHBoxLayout()
        self.system_label = QtWidgets.QLabel()
        self.system_label.setObjectName("system_label")
        self.name_label = QtWidgets.QLabel()
        self.name_label.setObjectName("name_label")
        system_layout.addWidget(self.system_label)
        system_layout.addWidget(self.name_label)
        system_layout.addStretch()
        main_layout.addLayout(system_layout)

        axes_layout = QtWidgets.QGridLayout()
        axes_layout.setContentsMargins(0, 0, 0, 0)
        axes_layout.setHorizontalSpacing(12)
        axes_layout.setVerticalSpacing(6)

        axes_label = QtWidgets.QLabel()
        axes_label.setText(self.t("AXES"))
        axes_layout.addWidget(axes_label, 0, 0)

        self.x_label = QtWidgets.QLabel()
        self.x_combobox = QtWidgets.QComboBox()
        axes_layout.addWidget(self.x_label, 1, 0)
        axes_layout.addWidget(self.x_combobox, 1, 1)

        self.y_label = QtWidgets.QLabel()
        self.y_combobox = QtWidgets.QComboBox()
        axes_layout.addWidget(self.y_label, 1, 2)
        axes_layout.addWidget(self.y_combobox, 1, 3)

        self.z_label = QtWidgets.QLabel()
        self.z_combobox = QtWidgets.QComboBox()
        axes_layout.addWidget(self.z_label, 1, 4)
        axes_layout.addWidget(self.z_combobox, 1, 5)

        main_layout.addLayout(axes_layout)

        mesh_layout = QtWidgets.QHBoxLayout()
        mesh_layout.setContentsMargins(0, 0, 0, 0)
        mesh_layout.setSpacing(12)
        self.mesh_label = QtWidgets.QLabel()
        mesh_layout.addWidget(self.mesh_label)

        self.x_label_2 = QtWidgets.QLabel()
        self.x_spinbox = QtWidgets.QSpinBox()
        self.x_spinbox.setRange(5, 200)
        self.x_spinbox.setValue(15)
        mesh_layout.addWidget(self.x_label_2)
        mesh_layout.addWidget(self.x_spinbox)

        self.y_label_2 = QtWidgets.QLabel()
        self.y_spinbox = QtWidgets.QSpinBox()
        self.y_spinbox.setRange(5, 200)
        self.y_spinbox.setValue(15)
        mesh_layout.addWidget(self.y_label_2)
        mesh_layout.addWidget(self.y_spinbox)
        mesh_layout.addStretch()
        main_layout.addLayout(mesh_layout)

        reference_layout = QtWidgets.QHBoxLayout()
        self.reference_label = QtWidgets.QLabel()
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setEnabled(False)
        reference_layout.addWidget(self.reference_label)
        reference_layout.addWidget(self.line_edit, 1)
        main_layout.addLayout(reference_layout)

        self.other_inputs_group = QtWidgets.QGroupBox()
        self.other_inputs_group.setObjectName("other_inputs_group")
        self.other_inputs_layout = QtWidgets.QFormLayout(self.other_inputs_group)
        self.other_inputs_layout.setContentsMargins(8, 12, 8, 8)
        self.other_inputs_layout.setSpacing(6)
        self._other_input_widgets = {}
        self.other_inputs_group.hide()
        main_layout.addWidget(self.other_inputs_group)

        self.area_plot_frame = QtWidgets.QFrame()
        self.area_plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.area_plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.area_plot_frame.setObjectName("area_plot_frame")
        self.frame_layout = QtWidgets.QVBoxLayout(self.area_plot_frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)

        self.figure = plt.Figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111, projection="3d")
        self.canvas = FigureCanvas(self.figure)
        self.frame_layout.addWidget(NavigationToolbar(self.canvas, self))
        self.frame_layout.addWidget(self.canvas)

        main_layout.addWidget(self.area_plot_frame, 1)

    def _retranslate_ui(self):
        self.system_label.setText(self.t("SYSTEM"))
        self.mesh_label.setText(self.t("MESH_POINTS"))
        self.x_label.setText(self.t("X"))
        self.y_label.setText(self.t("Y"))
        self.z_label.setText(self.t("Z"))
        self.x_label_2.setText(self.t("X"))
        self.y_label_2.setText(self.t("Y"))
        self.reference_label.setText(self.t("REFERENCE_INPUTS"))
        self.other_inputs_group.setTitle(self.t("OTHER_INPUTS"))
        self.line_edit.setPlaceholderText(self.t("NO_ADDITIONAL_INPUTS"))

    def _connect_signals(self):
        self.x_combobox.currentIndexChanged.connect(self._on_axis_changed)
        self.y_combobox.currentIndexChanged.connect(self._on_axis_changed)
        self.z_combobox.currentIndexChanged.connect(self._on_control_changed)
        self.x_spinbox.valueChanged.connect(self._on_control_changed)
        self.y_spinbox.valueChanged.connect(self._on_control_changed)

        self.view_model.notify_data_changed.connect(self._on_data_changed)

    def _populate_controls(self):
        if not self.view_model or not self.view_model.fuzzy_service:
            return

        self._is_updating_controls = True
        try:
            self._input_variables = self.view_model.get_input_variables()
            self._output_variables = self.view_model.get_output_variables()

            self.x_combobox.clear()
            self.y_combobox.clear()
            for var in self._input_variables:
                name = var.get("name", "")
                if name:
                    self.x_combobox.addItem(name)
                    self.y_combobox.addItem(name)

            self.z_combobox.clear()
            for var in self._output_variables:
                name = var.get("name", "")
                if name:
                    self.z_combobox.addItem(name)

            if self.view_model and self.view_model.fuzzy_service:
                system_name = self.view_model.fuzzy_service.get_system_name()
                self.name_label.setText(system_name)

            if self.x_combobox.count() > 0:
                self.x_combobox.setCurrentIndex(0)
            if self.x_combobox.count() > 1 and self.y_combobox.count() > 1:
                self.y_combobox.setCurrentIndex(1)
            elif self.y_combobox.count() > 0:
                self.y_combobox.setCurrentIndex(0)
            if self.z_combobox.count() > 0:
                self.z_combobox.setCurrentIndex(0)

            self.x_combobox.setEnabled(self.x_combobox.count() > 0)
            self.y_combobox.setEnabled(self.y_combobox.count() > 0)
            self.z_combobox.setEnabled(self.z_combobox.count() > 0)
        finally:
            self._is_updating_controls = False

        self._rebuild_other_inputs_controls()
        self._update_surface()

    def _on_control_changed(self):
        if self._is_updating_controls:
            return
        self._update_surface()

    def _on_axis_changed(self):
        if self._is_updating_controls:
            return

        self._is_updating_controls = True
        try:
            x_name = self.x_combobox.currentText()
            y_name = self.y_combobox.currentText()

            if x_name == y_name and self.y_combobox.count() > 1:
                for idx in range(self.y_combobox.count()):
                    if self.y_combobox.itemText(idx) != x_name:
                        self.y_combobox.setCurrentIndex(idx)
                        y_name = self.y_combobox.itemText(idx)
                        break
        finally:
            self._is_updating_controls = False

        self._rebuild_other_inputs_controls()
        self._update_surface()

    def _rebuild_other_inputs_controls(self):
        while self.other_inputs_layout.count():
            item = self.other_inputs_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        prev_flag = self._is_updating_controls
        self._is_updating_controls = True
        try:
            self._other_input_widgets = {}

            axis_names = {self.x_combobox.currentText(), self.y_combobox.currentText()}

            if not self._input_variables:
                self.other_inputs_group.hide()
                self.line_edit.setText(self.t("NO_ADDITIONAL_INPUTS"))
                return

            has_controls = False
            for var in self._input_variables:
                name = var.get("name", "")
                if not name or name in axis_names:
                    continue

                var_range = var.get("range", [0, 1])
                lower = float(var_range[0]) if len(var_range) > 0 else 0.0
                upper = float(var_range[1]) if len(var_range) > 1 else lower + 1.0
                if lower == upper:
                    upper = lower + 1.0

                spin = QtWidgets.QDoubleSpinBox(self.other_inputs_group)
                spin.setRange(min(lower, upper), max(lower, upper))
                step = (max(lower, upper) - min(lower, upper)) / 100.0
                if step <= 0:
                    step = 0.1
                spin.setSingleStep(step)
                spin.setDecimals(4)
                default_value = (lower + upper) / 2.0
                spin.setValue(default_value)
                spin.valueChanged.connect(self._on_control_changed)

                self.other_inputs_layout.addRow(name, spin)
                self._other_input_widgets[name] = spin
                has_controls = True
        finally:
            self._is_updating_controls = prev_flag

        if has_controls:
            self.other_inputs_group.show()
            reference_text = [
                f"{name} = {format(spin.value(), '.2f')}" for name, spin in self._other_input_widgets.items()
            ]
            self.line_edit.setText(", ".join(reference_text))
        else:
            self.other_inputs_group.hide()
            self.line_edit.setText(self.t("NO_ADDITIONAL_INPUTS"))

    def _update_surface(self):
        if not self.view_model or not self.view_model.fuzzy_service:
            self.ax.clear()
            self.canvas.draw_idle()
            return

        if self.x_combobox.count() == 0 or self.y_combobox.count() == 0 or self.z_combobox.count() == 0:
            self.ax.clear()
            self.canvas.draw_idle()
            return

        if len(self._input_variables) < 2:
            self.ax.clear()
            self.canvas.draw_idle()
            return

        x_var = self.x_combobox.currentText()
        y_var = self.y_combobox.currentText()
        output_var = self.z_combobox.currentText()
        x_points = self.x_spinbox.value()
        y_points = self.y_spinbox.value()

        if not x_var or not y_var or not output_var:
            self.ax.clear()
            self.canvas.draw_idle()
            return

        input_names = {var.get("name", "") for var in self._input_variables}
        output_names = {var.get("name", "") for var in self._output_variables}

        if x_var not in input_names or y_var not in input_names:
            self.ax.clear()
            self.canvas.draw_idle()
            return
        if output_var not in output_names:
            self.ax.clear()
            self.canvas.draw_idle()
            return

        if x_var == y_var and self.x_combobox.count() > 1:
            new_index = (self.y_combobox.currentIndex() + 1) % self.y_combobox.count()
            if self.y_combobox.itemText(new_index) != x_var:
                self._is_updating_controls = True
                self.y_combobox.setCurrentIndex(new_index)
                self._is_updating_controls = False
                y_var = self.y_combobox.currentText()

        overrides = {name: float(spin.value()) for name, spin in self._other_input_widgets.items()}
        surface_data = self.view_model.compute_surface(
            x_var,
            y_var,
            output_var,
            x_points,
            y_points,
            fixed_inputs=overrides,
        )

        if not surface_data:
            self.ax.clear()
            self.line_edit.setText("Error: Could not compute surface")
            self.canvas.draw_idle()
            return

        error = surface_data.get("error")
        if error == "system_not_ready":
            self.ax.clear()
            missing = surface_data.get("missing", [])
            if missing:
                missing_str = ", ".join(missing)
                error_msg = f"System not ready. Missing: {missing_str}"
            else:
                error_msg = self.t("SYSTEM_NOT_READY")
            self.line_edit.setText(error_msg)
            self.canvas.draw_idle()
            return

        success_count = surface_data.get("success_count", 0)
        if success_count == 0:
            self.ax.clear()
            self.line_edit.setText(self.t("NO_VALID_SURFACE"))
            self.canvas.draw_idle()
            return

        X = surface_data["X"]
        Y = surface_data["Y"]
        Z = surface_data["Z"]

        z_min = surface_data.get("z_min")
        z_max = surface_data.get("z_max")

        valid_Z = Z[~np.isnan(Z) & ~np.isinf(Z)]
        if z_min is None or z_max is None or np.isnan(z_min) or np.isnan(z_max):
            if len(valid_Z) > 0:
                z_min = float(np.nanmin(valid_Z))
                z_max = float(np.nanmax(valid_Z))
            else:
                output_var_info = next((var for var in self._output_variables if var.get("name") == output_var), None)
                output_range = output_var_info.get("range", [0, 1]) if output_var_info else [0, 1]
                z_min = float(output_range[0]) if len(output_range) > 0 else 0.0
                z_max = float(output_range[1]) if len(output_range) > 1 else 1.0

        if len(valid_Z) > 0:
            actual_z_min = float(np.nanmin(valid_Z))
            actual_z_max = float(np.nanmax(valid_Z))
            if not (np.isnan(actual_z_min) or np.isnan(actual_z_max)):
                z_min = actual_z_min
                z_max = actual_z_max

        if z_min == z_max or abs(z_max - z_min) < 1e-10:
            if not np.isnan(z_min) and not np.isinf(z_min):
                output_var_info = next((var for var in self._output_variables if var.get("name") == output_var), None)
                output_range = output_var_info.get("range", [0, 1]) if output_var_info else [0, 1]
                output_range_size = abs(output_range[1] - output_range[0]) if len(output_range) >= 2 else 1.0
                offset = max(output_range_size * 0.05, 0.1)
                z_min = z_min - offset
                z_max = z_max + offset
            else:
                output_var_info = next((var for var in self._output_variables if var.get("name") == output_var), None)
                output_range = output_var_info.get("range", [0, 1]) if output_var_info else [0, 1]
                z_min = float(output_range[0]) if len(output_range) > 0 else 0.0
                z_max = float(output_range[1]) if len(output_range) > 1 else 1.0
                if z_min == z_max:
                    z_min -= 0.1
                    z_max += 0.1
        else:
            range_size = abs(z_max - z_min)
            padding = max(range_size * 0.05, 1e-6)
            z_min = z_min - padding
            z_max = z_max + padding

        Z_clean = np.where(np.isnan(Z) | np.isinf(Z), np.nan, Z)

        self.ax.clear()
        try:
            self.ax.plot_surface(
                X, Y, Z_clean, cmap="viridis", edgecolor="none", alpha=0.8, linewidth=0, antialiased=True
            )
            self.ax.set_xlabel(x_var)
            self.ax.set_ylabel(y_var)
            self.ax.set_zlabel(output_var)
            self.ax.set_zlim(z_min, z_max)
        except Exception as e:
            self.ax.clear()
            self.line_edit.setText(f"Error plotting surface: {str(e)}")
            self.canvas.draw_idle()
            return

        reference_text = [f"{name} = {format(spin.value(), '.2f')}" for name, spin in self._other_input_widgets.items()]
        self.line_edit.setText(", ".join(reference_text))

        self.canvas.draw_idle()

    def _on_data_changed(self):
        """Handle data changed signal from view model."""
        self._populate_controls()

    def closeEvent(self, event):
        """Handle window close event to properly clean up resources."""
        self._is_updating_controls = True
        self._disconnect_signals()
        self.view_model.blockSignals(True)
        if self.view_model.event_bus:
            self.view_model.event_bus.unregister_view_model(self.view_model)
        self.canvas.close()
        plt.close(self.figure)
        super().closeEvent(event)

    def _disconnect_signals(self):
        """Disconnect all signal connections."""
        self.x_combobox.currentIndexChanged.disconnect()
        self.y_combobox.currentIndexChanged.disconnect()
        self.z_combobox.currentIndexChanged.disconnect()
        self.x_spinbox.valueChanged.disconnect()
        self.y_spinbox.valueChanged.disconnect()
        for spin in self._other_input_widgets.values():
            spin.valueChanged.disconnect()
