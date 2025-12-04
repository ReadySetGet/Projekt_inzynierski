"""Create a widget GUI element responsible for displaying the inputs and outputs.

This module creates a widget GUI element responsible for displaying the inputs
and outputs inside the fis system.

Classes:
    FisTabView: a widget inheriting from QWidget responsible for displaying
        the plots of all the inputs and outputs inside the fis system as well
        as the system name.

Temporarily(?) imports placeholder classes in MembershipFunction and InOutput.
"""

from typing import List, Optional

import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets

from app.view_models.fis_tab_view_model import FisTabViewModel
from app.views.base_tab_view import BaseTabView
from app.views.in_output import InOutput
from app.views.mf import MembershipFunction


def hide_axi(plot):
    """Hide the left and bottom axis of the plot.

    Args:
        plot: the plot which will have its axis removed.
    """
    left_axis = plot.getAxis("left")
    left_axis.hide()
    bottom_axis = plot.getAxis("bottom")
    bottom_axis.hide()


class FisTabView(BaseTabView):
    """Class inheriting from QWidget.

    Displays the inputs and outputs inside fis system as plots.

    Methods:
        __init__(parent): create an instance of MFPropertiesWidget and bind it to
            the parent window.
        remove_plots(): remove every single plot and label from the widget. Clear
            the graphic scene.
        add_input(inp): add a new input to the system, recalculate plot positions,
            redraw plots and labels.
        add_output(out): add a new output to the system, recalculate plot positions,
            redraw plots and labels.
        remove_input(inp): remove an input to the system, recalculate plot positions,
            redraw plots and labels.
        remove_output(out): remove an output to the system, recalculate plot positions,
            redraw plots and labels.

    Attributes:
        membership_functions: membership functions present within the system.
        inputs: fis inputs present within the system.
        outputs: fis outputs present within the system.
        points: list of points to draw lines between in order to show connections.
        plots: list of plots created and displayed by the class.
        labels: list of labels of aforementioned plots.
        middle_height: the middle point of the frame taken as a baseline for plotting.
        gap: the gap between plots.
        colors: table of colours used to differentiate different membership functions.
    """

    # Signals for variable selection
    input_selected = QtCore.pyqtSignal(object)  # Emits selected input InOutput object
    output_selected = QtCore.pyqtSignal(object)  # Emits selected output InOutput object
    selection_cleared = QtCore.pyqtSignal()  # Emits when selection is cleared

    membership_functions = []
    inputs = []
    outputs = []
    points = []
    plots = []
    labels = []
    middle_height = 180
    gap = 160
    colors = [
        "#0027FF",  # Blue
        "#FF0000",  # Red
        "#3D7A00",  # Green
        "#FF2BE7",  # Magenta
        "#FFAE21",  # Orange
        "#2AFF83",  # Light Green
        "#DF79FF",  # Purple
        "#09FF24",  # Bright Green
        "#FF723B",  # Red-Orange
        "#FF6CBA",  # Pink
        "#00FFFF",  # Cyan
        "#FFFF00",  # Yellow
        "#8B4513",  # Brown
        "#FF1493",  # Deep Pink
        "#00FF7F",  # Spring Green
        "#FFD700",  # Gold
        "#DC143C",  # Crimson
        "#32CD32",  # Lime Green
        "#FF4500",  # Orange Red
        "#9370DB",  # Medium Purple
    ]

    def __init__(self, parent=None):
        """Initialize a new class instance.

        Args:
            parent: The parent widget, in this case central tab, to which the widget
                will be attached.
        """
        super().__init__(parent)

        self.view_model = FisTabViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self.view_model.fis_data_updated.connect(self._on_fis_data_updated)

        # Selection state
        self._selected_input: Optional[InOutput] = None
        self._selected_output: Optional[InOutput] = None
        self._plot_to_input_map = {}  # Maps plot widgets to input objects
        self._plot_to_output_map = {}  # Maps plot widgets to output objects

        # Don't set hardcoded background - theme will handle it
        self.setObjectName("fisTab")
        self._setup_ui()
        self._retranslate_ui()

        # Load initial data from view model
        self.view_model.refresh_data()

    def _on_fis_data_updated(self, fis_data: dict):
        """Handle FIS data updates from the view model.

        Args:
            fis_data: Dictionary containing system info, inputs, and outputs
        """
        self.remove_plots()
        self.inputs.clear()
        self.outputs.clear()
        self.membership_functions.clear()

        system_info = fis_data.get("system_info", {})
        self._update_system_display(system_info)

        inputs_data = fis_data.get("inputs", [])
        for input_data in inputs_data:
            input_obj = self._create_inoutput_from_data(input_data)
            if input_obj:
                self.inputs.append(input_obj)

        outputs_data = fis_data.get("outputs", [])
        for output_data in outputs_data:
            output_obj = self._create_inoutput_from_data(output_data)
            if output_obj:
                self.outputs.append(output_obj)

        # Redraw all plots
        self._redraw_all_plots()

    def _create_inoutput_from_data(self, var_data: dict) -> InOutput:
        """Create an InOutput object from view model data.

        Args:
            var_data: Dictionary containing variable data from view model

        Returns:
            InOutput object or None if creation fails
        """
        try:
            var_name = var_data.get("name", "Unknown")
            mfs_data = var_data.get("membership_functions", [])

            mfs = []
            for i, mf_data in enumerate(mfs_data):
                plot_data = mf_data.get("plot_data", ([], []))
                x_data, y_data = plot_data

                if x_data and y_data:
                    mf = MembershipFunction(x=x_data, y=y_data)
                    mfs.append(mf)

            if mfs:
                return InOutput(mfs=mfs, name=var_name)
            else:
                default_mf = MembershipFunction(x=[0, 1], y=[0, 0])
                return InOutput(mfs=[default_mf], name=var_name)

        except Exception:
            return None

    def _update_system_display(self, system_info: dict):
        """Update the system display information.

        Args:
            system_info: Dictionary containing system information
        """
        system_type = system_info.get("type", "mamdani")
        system_type_capitalized = system_type.capitalize()
        self.box_system_label.setText(f"{system_type_capitalized}\nType 1")

    def _redraw_all_plots(self):
        """Redraw all input and output plots."""
        if not self.inputs and not self.outputs:
            return

        if self.inputs:
            input_pos = self._calculate_plot_positions(self.inputs, "input")
            for i in range(len(self.inputs)):
                self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        if self.outputs:
            output_pos = self._calculate_plot_positions(self.outputs, "output")
            for i in range(len(self.outputs)):
                self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

        # Restore selection highlighting after plots are redrawn
        self._restore_selection_highlighting()

    def _restore_selection_highlighting(self):
        """Restore selection highlighting based on fuzzy service state."""
        if not hasattr(self.view_model, "fuzzy_service"):
            return

        fuzzy_service = self.view_model.fuzzy_service
        selected_input_name = fuzzy_service.get_selected_input_name()
        selected_output_name = fuzzy_service.get_selected_output_name()

        self._selected_input = None
        self._selected_output = None

        # Find and restore input selection
        if selected_input_name:
            for input_data in self.inputs:
                if input_data.GetName() == selected_input_name:
                    self._selected_input = input_data
                    break

        # Find and restore output selection
        if selected_output_name:
            for output_data in self.outputs:
                if output_data.GetName() == selected_output_name:
                    self._selected_output = output_data
                    break

        # Apply visual highlighting
        self._update_plot_styling()

    def refresh_selection(self):
        """Manually refresh the selection highlighting."""
        self._restore_selection_highlighting()

    def get_membership_function_color(self, mf_index: int) -> str:
        """Get color for a membership function by index.

        Args:
            mf_index: Index of the membership function

        Returns:
            Color string in hex format
        """
        color_index = mf_index % len(self.colors)
        return self.colors[color_index]

    def get_available_colors(self) -> List[str]:
        """Get list of all available colors for membership functions.

        Returns:
            List of color strings in hex format
        """
        return self.colors.copy()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.system_label = QtWidgets.QLabel(parent=self)
        self.system_label.setGeometry(QtCore.QRect(10, 10, 51, 16))
        self.system_label.setObjectName("system_label")

        self.name_label = QtWidgets.QLabel(parent=self)
        self.name_label.setGeometry(QtCore.QRect(70, 10, 71, 16))
        self.name_label.setObjectName("name_label")

        self.seperator_line = QtWidgets.QFrame(parent=self)
        self.seperator_line.setGeometry(QtCore.QRect(10, 20, 491, 20))
        self.seperator_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line.setObjectName("seperator_line")

        self.graph_frame = QtWidgets.QGraphicsView(parent=self)
        self.graph_frame.setGeometry(QtCore.QRect(10, 60, 490, 510))
        self.graph_frame.setFrameShape(QtWidgets.QGraphicsView.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QGraphicsView.Shadow.Raised)
        # Styling will be applied by theme
        self.graph_frame.setObjectName("graph_frame")

        self.scene = QtWidgets.QGraphicsScene(parent=self.graph_frame)
        self.graph_frame.setScene(self.scene)
        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor("black"))
        self.pen.setWidth(2)

        self.box_system_label = QtWidgets.QLabel(parent=self.graph_frame)
        self.box_system_label.setGeometry(175, 180, 140, 140)
        self.box_system_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.box_system_label.setObjectName("box_system_label")
        self.box_system_label.setWordWrap(True)

        self._apply_initial_box_styling()

        self.remove_plots()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.box_system_label.setText(_translate("Main Window", "Mamdani\nType 1"))
        self.system_label.setText(_translate("MainWindow", "System:"))
        self.name_label.setText(_translate("MainWindow", "FIS System"))

    def _plot_graphs(self, position_y, position_x, data):
        """Plot all the input or output data as graphs and label them.

        Args:
            position_y: the y position where in the window the plot frame
                gets displayed.
            position_x: the x position where in the window the plot frame
                gets displayed.
            data: an In_Output class object representing the data of an input
                or an output.
        """
        in_out_plot = pg.PlotWidget(parent=self.graph_frame)
        mfs = data.GetMfs()
        for i in range(len(mfs)):
            # Cycle through colors if we have more MFs than colors
            color_index = i % len(self.colors)
            color = self.colors[color_index]
            x_data = mfs[i].getX()
            y_data = mfs[i].getY()
            in_out_plot.plot(x_data, y_data, pen=color)
        self.plots.append(in_out_plot)

        # Styling will be applied by theme
        in_out_plot.setGeometry(QtCore.QRect(position_x, position_y, 140, 140))

        # Enable mouse events for click handling
        in_out_plot.scene().sigMouseClicked.connect(lambda event, plot=in_out_plot: self._on_plot_clicked(event, plot))

        # Determine if this is an input or output based on position
        if position_x == 20:  # Input position
            self._plot_to_input_map[in_out_plot] = data
        elif position_x == 330:  # Output position
            self._plot_to_output_map[in_out_plot] = data

        name_label = QtWidgets.QLabel(parent=self.graph_frame)
        name_label.setGeometry(QtCore.QRect(position_x, position_y + 140, 140, 20))
        name_label.setStyleSheet("border: 0px")
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        name_label.setText(f"{data.GetName()} ({len(data.GetMfs())} MFs)")
        self.labels.append(name_label)

        in_out_plot.show()
        name_label.show()
        hide_axi(in_out_plot)

    def _calculate_plot_positions(self, data, side):
        """Calculate the positions in which the plot frames will get displayed.

        Also calculates point coordinates to connect via pen.

        Args:
            data: list of all the inputs or outputs to plot.
            side: whether the data is supposed to get displayed on the 'input' side
                (left) or 'output' side (right).

        Returns:
            returns the list of calculated frame positions.
        """
        positions = []
        x_pos = 0
        if side == "input":
            x_pos = 20
        elif side == "output":
            x_pos = 330
        else:
            return -1

        if len(data) % 2 != 0:
            positions.append(self.middle_height)
            self.points.append([x_pos + self.gap / 2, self.middle_height])
            pair_numb = (len(data) - 1) // 2
            for i in range(1, pair_numb + 1):
                positions.append(self.middle_height - i * self.gap)
                self.points.append([x_pos + self.gap / 2, self.middle_height - i * self.gap])
                positions.append(self.middle_height + i * self.gap)
                self.points.append([x_pos + self.gap / 2, self.middle_height + i * self.gap])

        else:
            pair_numb = (len(data)) // 2
            for i in range(pair_numb):
                positions.append(int(self.middle_height - (i + 0.5) * 160))
                self.points.append(
                    [
                        x_pos + self.gap / 2,
                        int(self.middle_height - (i + 0.5) * self.gap),
                    ]
                )
                positions.append(int(self.middle_height + (i + 0.5) * 160))
                self.points.append(
                    [
                        x_pos + self.gap / 2,
                        int(self.middle_height + (i + 0.5) * self.gap),
                    ]
                )
        return positions

    def _draw_lines(self):
        """Clear the graphic scene and draw lines connecting all the plot frames.

        Lines connect all the plot frames with the system name frame.
        """
        self.scene.clear()
        for point in self.points:
            self.scene.addLine(point[0], point[1], 255, 180, self.pen)

    def _on_plot_clicked(self, event, plot):
        """Handle click events on input/output plots.

        Args:
            event: Mouse click event
            plot: The plot widget that was clicked
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # Check if this is an input plot
            if plot in self._plot_to_input_map:
                input_data = self._plot_to_input_map[plot]
                self._select_input(input_data)
            # Check if this is an output plot
            elif plot in self._plot_to_output_map:
                output_data = self._plot_to_output_map[plot]
                self._select_output(output_data)

    def _select_input(self, input_data: InOutput):
        """Select an input variable.

        Args:
            input_data: The InOutput object representing the input
        """
        self._clear_selection()

        self._selected_input = input_data

        if hasattr(self.view_model, "fuzzy_service"):
            self.view_model.fuzzy_service.set_selected_input(input_data.GetName())

        self._update_plot_styling()

        # Notify data refresh
        if hasattr(self.view_model, "notify_data_changed"):
            self.view_model.notify_data_changed.emit()

        # Emit signal
        self.input_selected.emit(input_data)

    def _select_output(self, output_data: InOutput):
        """Select an output variable.

        Args:
            output_data: The InOutput object representing the output
        """
        self._clear_selection()

        self._selected_output = output_data

        if hasattr(self.view_model, "fuzzy_service"):
            self.view_model.fuzzy_service.set_selected_output(output_data.GetName())

        self._update_plot_styling()

        # Notify data refresh
        if hasattr(self.view_model, "notify_data_changed"):
            self.view_model.notify_data_changed.emit()

        # Emit signal
        self.output_selected.emit(output_data)

    def _clear_selection(self):
        """Clear current selection."""
        self._selected_input = None
        self._selected_output = None

        if hasattr(self.view_model, "fuzzy_service"):
            self.view_model.fuzzy_service.clear_selection()

        self._update_plot_styling()

        # Notify data refresh
        if hasattr(self.view_model, "notify_data_changed"):
            self.view_model.notify_data_changed.emit()

        self.selection_cleared.emit()

    def _update_plot_styling(self):
        """Update the visual styling of plots based on selection state."""
        # Get theme colors
        bg_color = "#E5E8E8"
        border_color = "gray"

        if self.view_model and self.view_model.theme_manager:
            palette = self.view_model.theme_manager.current_palette
            if palette and "colors" in palette:
                colors = palette["colors"]
                bg_color = colors.get("surface", "#E5E8E8")
                border_color = colors.get("border", "gray")

        # Reset all plots to default styling
        default_style = "; ".join(
            [
                f"background-color: {bg_color}",
                f"border: 1px solid {border_color}",
            ]
        )
        for plot in self.plots:
            plot.setStyleSheet(default_style)

        # Highlight selected input
        if self._selected_input:
            for plot, input_data in self._plot_to_input_map.items():
                if input_data == self._selected_input:
                    highlight_style = "; ".join(
                        [
                            f"background-color: {bg_color}",
                            "border: 3px solid #0078D4",
                        ]
                    )
                    plot.setStyleSheet(highlight_style)
                    break

        # Highlight selected output
        if self._selected_output:
            for plot, output_data in self._plot_to_output_map.items():
                if output_data == self._selected_output:
                    highlight_style = "; ".join(
                        [
                            f"background-color: {bg_color}",
                            "border: 3px solid #0078D4",
                        ]
                    )
                    plot.setStyleSheet(highlight_style)
                    break

    def get_selected_input(self) -> Optional[InOutput]:
        """Get the currently selected input.

        Returns:
            Selected input InOutput object or None
        """
        return self._selected_input

    def get_selected_output(self) -> Optional[InOutput]:
        """Get the currently selected output.

        Returns:
            Selected output InOutput object or None
        """
        return self._selected_output

    def _apply_pyqtgraph_theme(self) -> None:
        """Apply the current theme colors to pyqtgraph plots and FIS elements."""
        # Call parent method to handle pyqtgraph plots
        super()._apply_pyqtgraph_theme()

        # Apply theme to FIS-specific elements
        self._apply_fis_theme()

    def _apply_initial_box_styling(self) -> None:
        """Apply initial styling to the system type box."""
        if not hasattr(self, "box_system_label") or self.box_system_label is None:
            return
        self.box_system_label.setStyleSheet(
            "; ".join(
                [
                    "background-color: #ffffff",
                    "border: 2px solid #cccccc",
                    "color: #000000",
                    "font-weight: bold",
                    "font-size: 12pt",
                ]
            )
        )

    def _apply_fis_theme(self) -> None:
        """Apply theme colors to FIS plot elements (graph frame and center box)."""
        if not hasattr(self, "box_system_label") or self.box_system_label is None:
            return

        if not self.view_model or not self.view_model.theme_manager:
            self._apply_initial_box_styling()
            return

        palette = self.view_model.theme_manager.current_palette
        if not palette or "colors" not in palette:
            self._apply_initial_box_styling()
            return

        colors = palette["colors"]
        surface_color = colors.get("surface", "#ffffff")
        border_color = colors.get("border", "#cccccc")
        text_color = colors.get("text", "#000000")

        # Update graph frame background
        if hasattr(self, "graph_frame") and self.graph_frame is not None:
            graph_style = "; ".join(
                [
                    f"background-color: {surface_color}",
                    f"border: 1px solid {border_color}",
                ]
            )
            self.graph_frame.setStyleSheet(graph_style)

        # Update center system label (Mamdani Type 1 box)
        self.box_system_label.setStyleSheet(
            "; ".join(
                [
                    f"background-color: {surface_color}",
                    f"border: 2px solid {border_color}",
                    f"color: {text_color}",
                    "font-weight: bold",
                    "font-size: 12pt",
                ]
            )
        )

        # Update pen color for lines
        if hasattr(self, "pen") and self.pen is not None:
            self.pen.setColor(QtGui.QColor(text_color))

        # Update all plot styling to match theme
        self._update_plot_styling()

    def remove_plots(self):
        """Remove all plots, labels and points from the widget.

        Clear the graphic scene.
        """
        for label in self.labels:
            label.setParent(None)
            label.deleteLater()
        self.labels.clear()
        for plot in self.plots:
            plot.setParent(None)
            plot.deleteLater()
        self.plots.clear()
        self.scene.clear()
        self.points.clear()

        self._plot_to_input_map.clear()
        self._plot_to_output_map.clear()

        self._selected_input = None
        self._selected_output = None

    def add_input(self, inp):
        """Add a new input to the system.

        Calculate new plot positions, redraw plots and labels.

        Args:
            inp: fis input
        """
        self.inputs.append(inp)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

    def add_output(self, out):
        """Add a new output to the system.

        Calculate new plot positions, redraw plots and labels.

        Args:
            out: fis output
        """
        self.outputs.append(out)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

    def remove_input(self, inp):
        """Remove an input from the system.

        Calculate new plot positions, redraw plots and labels.

        Args:
            inp: fis input
        """
        self.inputs.remove(inp)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

    def remove_output(self, out):
        """Remove an output from the system.

        Calculate new plot positions, redraw plots and labels.

        Args:
            out: fis output
        """
        self.outputs.remove(out)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()
