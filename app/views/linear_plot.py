import numpy as np
import pyqtgraph as pg


class LinearPlot:
    """Support class used to plot linear (Sugeno) plot objects in the main window."""

    def __init__(self, plot_widget, x_data, y_data, parameters, color):
        """Initialize the linear plot.

        Args:
            plot_widget: The plot widget to display the linear curve.
            x_data: X coordinate data.
            y_data: Y coordinate data.
            parameters: Parameters of the linear function [coeff1, coeff2, ..., constant].
            color: Color of the plot.
        """
        self.plot_widget = plot_widget
        self.linear_x = x_data
        self.linear_y = y_data
        self.parameters = parameters.copy() if isinstance(parameters, list) else parameters
        self.color = color

        self.linear_plot_line = self.plot_widget.plot(self.linear_x, self.linear_y, pen=self.color)

        if len(self.parameters) > 0:
            constant_term = self.parameters[-1]
            center_x = (x_data[0] + x_data[-1]) / 2
            self.value_anchor = pg.TargetItem(
                pos=(center_x, np.clip(constant_term, 0.0, 1.0)),
                size=10,
                symbol="o",
                pen=self.color,
                brush=self.color,
            )
            self.value_anchor.sigPositionChanged.connect(self._value_interaction)
            self.plot_widget.addItem(self.value_anchor)

    def _value_interaction(self):
        """Change the constant term when interacting with the anchor."""
        new_pos = self.value_anchor.pos()
        new_constant = np.clip(new_pos.y(), 0.0, 1.0)
        if len(self.parameters) > 0:
            self.parameters[-1] = new_constant
            self.linear_y = np.full_like(self.linear_x, new_constant)
            self.value_anchor.setPos(self.value_anchor.pos().x(), new_constant)
            self._update_plot()

    def _update_plot(self):
        """Update the plot with current data."""
        self.linear_plot_line.setData(self.linear_x, self.linear_y)
