import numpy as np
import pyqtgraph as pg


class ConstantPlot:
    """Support class used to plot constant (Sugeno) plot objects in the main window."""

    def __init__(self, plot_widget, x_data, y_data, constant_value, color):
        """Initialize the constant plot.

        Args:
            plot_widget: The plot widget to display the constant curve.
            x_data: X coordinate data.
            y_data: Y coordinate data.
            constant_value: Constant value parameter.
            color: Color of the plot.
        """
        self.plot_widget = plot_widget
        self.constant_x = x_data
        self.constant_y = y_data
        self.constant_value = constant_value
        self.color = color

        self.constant_plot_line = self.plot_widget.plot(self.constant_x, self.constant_y, pen=self.color)

        self.value_anchor = pg.TargetItem(
            pos=((x_data[0] + x_data[-1]) / 2, self.constant_value),
            size=10,
            symbol="o",
            pen=self.color,
            brush=self.color,
        )
        self.value_anchor.sigPositionChanged.connect(self._value_interaction)

        self.plot_widget.addItem(self.value_anchor)

    def _value_interaction(self):
        """Change the constant value when interacting with the anchor."""
        new_pos = self.value_anchor.pos()
        new_value = np.clip(new_pos.y(), 0.0, 1.0)
        self.constant_value = new_value
        self.constant_y = np.full_like(self.constant_x, new_value)
        self.value_anchor.setPos(self.value_anchor.pos().x(), new_value)
        self._update_plot()

    def _update_plot(self):
        """Update the plot with current data."""
        self.constant_plot_line.setData(self.constant_x, self.constant_y)
