from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pyqtgraph as pg
from PyQt6 import QtCore, QtWidgets

from app.view_models.rule_interference_view_model import RuleInterferenceViewModel
from app.views.base_tab_view import BaseTabView


def hide_axes(plot: pg.PlotWidget) -> None:
    """Hide the left and bottom axes of a plot widget."""
    left_axis = plot.getAxis("left")
    if left_axis:
        left_axis.hide()
    bottom_axis = plot.getAxis("bottom")
    if bottom_axis:
        bottom_axis.hide()


class RuleInterferenceTabWidget(BaseTabView):
    """Rule interference tab showing live data sourced from the fuzzy service."""

    def __init__(self, parent=None, status_bar=None):
        """Create the rule interference tab widget."""
        super().__init__(parent=parent)
        pg.setConfigOption("background", "w")
        self.setObjectName("interferenceTab")
        self.status_bar = status_bar

        self.view_model = RuleInterferenceViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self._current_inputs: List[float] = []
        self._current_outputs: List[float] = []

        self._slider_resolution = 1000
        self._updating_controls = False
        self._input_sliders: List[QtWidgets.QSlider] = []
        self._input_value_labels: List[QtWidgets.QLabel] = []
        self._input_ranges: List[Tuple[float, float]] = []
        self._latest_payload: Dict[str, Any] = {"inputs": [], "rules": [], "outputs": []}

        self._setup_ui()
        self._connect_view_model_signals()
        self._retranslate_ui()
        self._update_system_name()
        self.view_model.refresh_data()

    # ------------------------------------------------------------------ #
    # UI setup                                                           #
    # ------------------------------------------------------------------ #
    def _setup_ui(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        self.system_label = QtWidgets.QLabel(parent=self)
        self.system_label.setObjectName("system_label")
        header_layout.addWidget(self.system_label)

        self.name_label = QtWidgets.QLabel(parent=self)
        self.name_label.setObjectName("name_label")
        header_layout.addWidget(self.name_label)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        separator = QtWidgets.QFrame(parent=self)
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        input_row = QtWidgets.QHBoxLayout()
        input_row.setContentsMargins(0, 0, 0, 0)
        input_row.setSpacing(8)

        self.input_values_label = QtWidgets.QLabel(parent=self)
        self.input_values_label.setObjectName("input_values_label")
        input_row.addWidget(self.input_values_label)

        self.input_values_edit = QtWidgets.QLineEdit(parent=self)
        self.input_values_edit.setObjectName("input_values_edit")
        self.input_values_edit.setFixedWidth(220)
        self.input_values_edit.textChanged.connect(self._update_from_editor_field)
        input_row.addWidget(self.input_values_edit)
        input_row.addStretch()

        main_layout.addLayout(input_row)

        self.inputs_summary_layout = QtWidgets.QHBoxLayout()
        self.inputs_summary_layout.setContentsMargins(0, 0, 0, 0)
        self.inputs_summary_layout.setSpacing(24)
        self._input_label_stretch = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.inputs_summary_layout.addItem(self._input_label_stretch)
        main_layout.addLayout(self.inputs_summary_layout)

        self.rules_scroll_area = QtWidgets.QScrollArea(parent=self)
        self.rules_scroll_area.setWidgetResizable(True)
        self.rules_container = QtWidgets.QWidget(parent=self.rules_scroll_area)
        self.rules_layout = QtWidgets.QVBoxLayout(self.rules_container)
        self.rules_layout.setContentsMargins(0, 0, 0, 0)
        self.rules_layout.setSpacing(16)

        # Aggregated output section (inserted after rule rows)
        self.aggregated_section = QtWidgets.QWidget(parent=self.rules_container)
        aggregated_layout = QtWidgets.QVBoxLayout(self.aggregated_section)
        aggregated_layout.setContentsMargins(0, 0, 0, 0)
        aggregated_layout.setSpacing(8)

        self.output_label = QtWidgets.QLabel(parent=self.aggregated_section)
        self.output_label.setObjectName("output_label")
        aggregated_layout.addWidget(self.output_label)

        self.result_plot = pg.PlotWidget(parent=self.aggregated_section)
        self.result_plot.setMinimumHeight(180)
        hide_axes(self.result_plot)
        aggregated_layout.addWidget(self.result_plot)

        self.rules_scroll_area.setWidget(self.rules_container)
        main_layout.addWidget(self.rules_scroll_area, stretch=3)

        self.sliders_layout = QtWidgets.QHBoxLayout()
        self.sliders_layout.setContentsMargins(0, 0, 0, 0)
        self.sliders_layout.setSpacing(16)
        self._slider_stretch = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.sliders_layout.addItem(self._slider_stretch)
        main_layout.addLayout(self.sliders_layout)

    def _retranslate_ui(self) -> None:
        self.system_label.setText(self.t("SYSTEM"))
        self.input_values_label.setText(self.t("INPUT_VALUES"))
        self.output_label.setText("Output = --")
        self.input_values_edit.setPlaceholderText("0.0, 0.0")

    def _update_system_name(self) -> None:
        try:
            system_name = self.view_model.fuzzy_service.get_system_name()
        except Exception:
            system_name = self.t("PLACEHOLDER")
        self.name_label.setText(system_name or self.t("PLACEHOLDER"))

    # ------------------------------------------------------------------ #
    # View model connections                                             #
    # ------------------------------------------------------------------ #
    def _connect_view_model_signals(self) -> None:
        self.view_model.inputs_updated.connect(self._on_data_changed)
        self.view_model.outputs_updated.connect(self._on_data_changed)
        self.view_model.rules_updated.connect(self._on_data_changed)
        self.view_model.inference_updated.connect(self._on_data_changed)
        self.view_model.status_message.connect(self._show_status_message)

    # ------------------------------------------------------------------ #
    # Slots                                                              #
    # ------------------------------------------------------------------ #
    def _on_data_changed(self, *_args) -> None:
        self._refresh_visualization()

    # ------------------------------------------------------------------ #
    # Data-driven UI updates                                             #
    # ------------------------------------------------------------------ #
    def _refresh_visualization(self) -> None:
        payload = self.view_model.build_visualization_payload()
        self._latest_payload = payload

        inputs_payload = payload.get("inputs", [])
        outputs_payload = payload.get("outputs", [])

        self._ensure_input_controls(len(inputs_payload))
        self._input_ranges = [
            tuple(info.get("range", [0, 1])) if info.get("range") else (0, 1) for info in inputs_payload
        ]
        self._current_inputs = [info.get("value") for info in inputs_payload]
        self._current_outputs = [info.get("value") for info in outputs_payload]

        self._update_input_text()
        self._update_input_labels_text(inputs_payload)
        self._update_input_controls_from_values()

        self._rebuild_rule_rows(payload.get("rules", []))
        self._update_aggregated_output(outputs_payload)

    def _update_input_controls_from_values(self) -> None:
        self._updating_controls = True
        try:
            for idx, slider in enumerate(self._input_sliders):
                slider.blockSignals(True)
                if idx < len(self._current_inputs) and idx < len(self._input_ranges):
                    value = self._current_inputs[idx]
                    if value is not None:
                        range_min, range_max = self._input_ranges[idx]
                        slider.setRange(0, self._slider_resolution)
                        slider.setValue(self._value_to_slider(value, range_min, range_max))
                slider.blockSignals(False)
        finally:
            self._updating_controls = False

    def _update_input_labels_text(self, inputs_payload: List[Dict[str, Any]] | None = None) -> None:
        if inputs_payload is None:
            inputs_payload = self._latest_payload.get("inputs", [])

        for idx, label in enumerate(self._input_value_labels):
            if idx < len(inputs_payload):
                var_info = inputs_payload[idx]
                var_name = var_info.get("name", f"Input {idx + 1}")
                value = var_info.get("value")
                if value is None:
                    label.setText(f"{var_name} = --")
                else:
                    formatted_value = format(value, ".2f")
                    label.setText(f"{var_name} = {formatted_value}")
            else:
                label.setText("")

    def _update_input_text(self) -> None:
        if not self._current_inputs:
            self._updating_controls = True
            self.input_values_edit.clear()
            self._updating_controls = False
            return
        values_text = ", ".join(format(value, ".2f") for value in self._current_inputs if value is not None)
        self._updating_controls = True
        self.input_values_edit.setText(values_text)
        self._updating_controls = False

    def _ensure_input_controls(self, count: int) -> None:
        current = len(self._input_sliders)
        if current < count:
            for _ in range(current, count):
                label = QtWidgets.QLabel(parent=self)
                label.setMinimumWidth(140)
                self.inputs_summary_layout.insertWidget(self.inputs_summary_layout.count() - 1, label)
                self._input_value_labels.append(label)

                slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, parent=self)
                slider.setRange(0, self._slider_resolution)
                slider.setMinimumWidth(160)
                slider.valueChanged.connect(self._update_from_sliders)
                self.sliders_layout.insertWidget(self.sliders_layout.count() - 1, slider)
                self._input_sliders.append(slider)
        elif current > count:
            for _ in range(current - count):
                slider = self._input_sliders.pop()
                slider.blockSignals(True)
                self.sliders_layout.removeWidget(slider)
                slider.deleteLater()

                label = self._input_value_labels.pop()
                self.inputs_summary_layout.removeWidget(label)
                label.deleteLater()

    def _rebuild_rule_rows(self, rules_payload: List[Dict[str, Any]]) -> None:
        self._clear_layout(self.rules_layout)

        # Temporarily remove aggregated section before rebuilding rules
        # Remove existing rule widgets while leaving the aggregated section intact.
        self._remove_rule_widgets()

        if not rules_payload:
            empty_label = QtWidgets.QLabel(self.t("NO_RULES_DEFINED") if hasattr(self, "t") else "No rules defined.")
            empty_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.rules_layout.addWidget(empty_label)

        else:
            for rule in rules_payload:
                title_label = QtWidgets.QLabel(rule.get("display", "Rule"))
                title_label.setStyleSheet("font-weight: bold;")
                self.rules_layout.addWidget(title_label)

                row_widget = QtWidgets.QWidget(parent=self.rules_container)
                row_layout = QtWidgets.QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setSpacing(12)

                inputs = rule.get("inputs", [])
                if inputs:
                    for input_vis in inputs:
                        plot = pg.PlotWidget()
                        plot.setMinimumSize(140, 110)
                        self._render_input_condition_plot(plot, input_vis)
                        row_layout.addWidget(plot)
                else:
                    placeholder = QtWidgets.QLabel(self.t("NO_INPUT_CONDITIONS") if hasattr(self, "t") else "No inputs")
                    placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    row_layout.addWidget(placeholder)

                connection_label = QtWidgets.QLabel(rule.get("connection_label", ""))
                connection_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                connection_label.setMinimumWidth(70)
                row_layout.addWidget(connection_label)

                outputs = rule.get("outputs", [])
                if outputs:
                    for output_vis in outputs:
                        plot = pg.PlotWidget()
                        plot.setMinimumSize(140, 110)
                        self._render_output_condition_plot(plot, output_vis)
                        row_layout.addWidget(plot)
                else:
                    placeholder = QtWidgets.QLabel(self.t("NO_OUTPUT") if hasattr(self, "t") else "No outputs")
                    placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    row_layout.addWidget(placeholder)

                row_layout.addStretch()
                self.rules_layout.addWidget(row_widget)

        # Insert aggregated section after rule rows (second element overall)
        self.rules_layout.insertWidget(self._aggregated_index(), self.aggregated_section)

    def _render_input_condition_plot(self, plot_widget: pg.PlotWidget, data: Dict[str, Any]) -> None:
        plot_widget.clear()
        hide_axes(plot_widget)

        x = data.get("curve_x", [])
        y = data.get("curve_y", [])
        value = data.get("value")
        membership = data.get("membership")

        if x and y:
            base_pen = pg.mkPen("#888888", width=1, style=QtCore.Qt.PenStyle.DashLine)
            plot_widget.plot(x, y, pen=base_pen)
            brush = pg.mkBrush(55, 115, 255, 80)
            active_pen = pg.mkPen("#3773FF", width=2)
            plot_widget.plot(x, y, pen=active_pen)
            plot_widget.plot(x, y, pen=None, brush=brush, fillLevel=0.0)

        if value is not None:
            vert_pen = pg.mkPen("#FF8C00", width=2)
            plot_widget.addItem(pg.InfiniteLine(pos=value, angle=90, pen=vert_pen))

        if membership is not None:
            horiz_pen = pg.mkPen("#CC0000", width=2, style=QtCore.Qt.PenStyle.DashLine)
            plot_widget.addItem(pg.InfiniteLine(pos=membership, angle=0, pen=horiz_pen))

    def _render_output_condition_plot(self, plot_widget: pg.PlotWidget, data: Dict[str, Any]) -> None:
        plot_widget.clear()
        hide_axes(plot_widget)

        x = data.get("curve_x", [])
        base_y = data.get("curve_y", [])
        clipped_y = data.get("clipped_curve_y", [])

        if x and base_y:
            base_pen = pg.mkPen("#888888", width=1, style=QtCore.Qt.PenStyle.DashLine)
            plot_widget.plot(x, base_y, pen=base_pen)

        if x and clipped_y:
            brush = pg.mkBrush(55, 115, 255, 80)
            active_pen = pg.mkPen("#3773FF", width=2)
            plot_widget.plot(x, clipped_y, pen=active_pen)
            plot_widget.plot(x, clipped_y, pen=None, brush=brush, fillLevel=0.0)

    def _update_aggregated_output(self, outputs_payload: List[Dict[str, Any]]) -> None:
        self.result_plot.clear()
        hide_axes(self.result_plot)

        if not outputs_payload:
            self.output_label.setText("Output = --")
            return

        output = outputs_payload[0]
        x = output.get("curve_x", [])
        y = output.get("curve_y", [])
        value = output.get("value")
        name = output.get("variable_name", "Output")

        if x and y:
            pen = pg.mkPen("#3773FF", width=2)
            brush = pg.mkBrush(55, 115, 255, 80)
            self.result_plot.plot(x, y, pen=pen)
            self.result_plot.plot(x, y, pen=None, brush=brush, fillLevel=0.0)

        if value is not None:
            line = pg.InfiniteLine(pos=value, angle=90, pen=pg.mkPen("#D62728", width=2))
            self.result_plot.addItem(line)
            formatted_value = format(value, ".2f")
            self.output_label.setText(f"{name} = {formatted_value}")
        else:
            self.output_label.setText(f"{name} = --")

    # ------------------------------------------------------------------ #
    # Interaction handlers                                               #
    # ------------------------------------------------------------------ #
    def _update_from_sliders(self) -> None:
        if self._updating_controls or not self._input_sliders:
            return

        new_values: List[float] = []
        for idx, slider in enumerate(self._input_sliders):
            if idx >= len(self._input_ranges):
                continue
            range_min, range_max = self._input_ranges[idx]
            slider_value = slider.value()
            value = self._slider_to_value(slider_value, range_min, range_max)
            new_values.append(value)

        if self.view_model.set_input_values(new_values):
            self._show_status_message("Updated inference inputs via sliders.")

    def _update_from_editor_field(self) -> None:
        if self._updating_controls or not self._input_ranges:
            return

        raw = self.input_values_edit.text()
        if not raw:
            return

        fragments = [part.strip() for part in raw.replace(";", ",").split(",") if part.strip()]
        if not fragments:
            return

        current_values = self.view_model.current_input_values
        if not current_values:
            current_values = [self._clamp_value(0, rng) for rng in self._input_ranges]

        for idx, fragment in enumerate(fragments):
            if idx >= len(self._input_ranges):
                break
            try:
                value = float(fragment)
            except ValueError:
                continue
            value = self._clamp_value(value, self._input_ranges[idx])
            if idx < len(current_values):
                current_values[idx] = value

        if self.view_model.set_input_values(current_values):
            self._show_status_message("Updated inference inputs via editor.")

    # ------------------------------------------------------------------ #
    # Utility helpers                                                    #
    # ------------------------------------------------------------------ #
    def _slider_to_value(self, slider_value: int, range_min: float, range_max: float) -> float:
        span = range_max - range_min
        if span <= 0:
            return range_min
        ratio = slider_value / self._slider_resolution
        return range_min + ratio * span

    def _value_to_slider(self, value: float, range_min: float, range_max: float) -> int:
        span = range_max - range_min
        if span <= 0:
            return 0
        ratio = (value - range_min) / span
        ratio = max(0.0, min(1.0, ratio))
        return int(round(ratio * self._slider_resolution))

    def _clamp_value(self, value: float, range_pair: Tuple[float, float]) -> float:
        range_min, range_max = range_pair
        if range_max < range_min:
            range_min, range_max = range_max, range_min
        return max(range_min, min(range_max, value))

    def _show_status_message(self, message: str) -> None:
        if self.status_bar and message:
            self.status_bar.showMessage(message)

    def _clear_layout(self, layout: QtWidgets.QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
        layout.invalidate()

    def _remove_rule_widgets(self) -> None:
        """Remove existing rule widgets while keeping the aggregated section alive."""
        while self.rules_layout.count():
            item = self.rules_layout.takeAt(0)
            widget = item.widget()
            if widget and widget is not self.aggregated_section:
                widget.deleteLater()
            elif widget is self.aggregated_section:
                # Keep reference for later re-insertion.
                self.aggregated_section.setParent(self.rules_container)

    def _aggregated_index(self) -> int:
        """Return the index where the aggregated section should be inserted."""
        return min(1, self.rules_layout.count())
