import pyqtgraph as pg


class TrapezoidPlot:
    """Support class used to plot trapezoid plot objects in the main window.

    The class requires central window plot widget in order to display its data.
    """

    def __init__(self, plot_widget, x_data, y_data, color, central_x):
        """Initialize the trapezoid plot.

        Args:
            plot_widget: The plot widget to display the trapezoid curve.
            x_data: X coordinate data.
            y_data: Y coordinate data.
            color: Color of the plot.
            central_x: Central x position.
        """
        self.plot_widget = plot_widget
        self.trap_x = x_data
        self.trap_y = y_data
        self.color = color
        self.central_x = central_x

        self.trapezoid_plot_line = self.plot_widget.plot(self.trap_x, self.trap_y, pen=self.color)

        self.trapezoid_left_down_anchor = pg.TargetItem(
            pos=(self.trap_x[1], self.trap_y[1]),
            size=10,
            symbol="o",
            pen=self.color,
            brush=self.color,
        )
        self.trapezoid_left_down_anchor.sigPositionChanged.connect(self._left_down_trap_interaction)

        self.trapezoid_left_up_anchor = pg.TargetItem(
            pos=(self.trap_x[2], self.trap_y[2]),
            size=10,
            symbol="o",
            pen=self.color,
            brush=self.color,
        )
        self.trapezoid_left_up_anchor.sigPositionChanged.connect(self._left_up_trap_interaction)

        self.trapezoid_right_up_anchor = pg.TargetItem(
            pos=(self.trap_x[3], self.trap_y[3]),
            size=10,
            symbol="o",
            pen=self.color,
            brush=self.color,
        )
        self.trapezoid_right_up_anchor.sigPositionChanged.connect(self._right_up_trap_interaction)

        self.trapezoid_right_down_anchor = pg.TargetItem(
            pos=(self.trap_x[4], self.trap_y[4]),
            size=10,
            symbol="o",
            pen=self.color,
            brush=self.color,
        )
        self.trapezoid_right_down_anchor.sigPositionChanged.connect(self._right_down_trap_interaction)

        self.position_anchor = pg.TargetItem(
            pos=(self.central_x, 0),
            size=10,
            symbol="s",
            pen=self.color,
            brush=self.color,
        )
        self.position_anchor.sigPositionChanged.connect(self._change_position)

        self.plot_widget.addItem(self.trapezoid_right_up_anchor)
        self.plot_widget.addItem(self.trapezoid_left_up_anchor)
        self.plot_widget.addItem(self.trapezoid_left_down_anchor)
        self.plot_widget.addItem(self.trapezoid_right_down_anchor)
        self.plot_widget.addItem(self.position_anchor)

    def _left_down_trap_interaction(self):
        """Change the shape by moving the bottom left point of the plot.

        The anchor cannot be moved beyond 0 and the position of top left anchor.
        """
        if (
            self.trapezoid_left_down_anchor.pos().x() < 0
            or self.trapezoid_left_down_anchor.pos().x() > self.trapezoid_left_up_anchor.pos().x()
        ):
            self.trapezoid_left_down_anchor.setPos(self.trap_x[1], self.trap_y[1])
        else:
            self.trapezoid_left_down_anchor.setPos(self.trapezoid_left_down_anchor.pos().x(), self.trap_y[1])
            self.trap_x[1] = self.trapezoid_left_down_anchor.pos().x()
        self._update_plot()

    def _left_up_trap_interaction(self):
        """Change the shape by moving the top left point of the plot.

        The anchor cannot be moved beyond the positions of bottom left anchor
        and top right anchor.
        """
        if (
            self.trapezoid_left_up_anchor.pos().x() < self.trapezoid_left_down_anchor.pos().x()
            or self.trapezoid_left_up_anchor.pos().x() > self.trapezoid_right_up_anchor.pos().x()
        ):
            self.trapezoid_left_up_anchor.setPos(self.trap_x[2], self.trap_y[2])
        else:
            self.trapezoid_left_up_anchor.setPos(self.trapezoid_left_up_anchor.pos().x(), self.trap_y[2])
            self.trap_x[2] = self.trapezoid_left_up_anchor.pos().x()
        self._update_plot()

    def _right_up_trap_interaction(self):
        """Change the shape by moving the top right point of the plot.

        The anchor cannot be moved beyond the positions of top left anchor
        and bottom right anchor.
        """
        if (
            self.trapezoid_right_up_anchor.pos().x() < self.trapezoid_left_up_anchor.pos().x()
            or self.trapezoid_right_up_anchor.pos().x() > self.trapezoid_right_down_anchor.pos().x()
        ):
            self.trapezoid_right_up_anchor.setPos(self.trap_x[3], self.trap_y[3])
        else:
            self.trapezoid_right_up_anchor.setPos(self.trapezoid_right_up_anchor.pos().x(), self.trap_y[3])
            self.trap_x[3] = self.trapezoid_right_up_anchor.pos().x()
        self._update_plot()

    def _right_down_trap_interaction(self):
        """Change the shape by moving the bottom right point of the plot.

        The anchor cannot be moved beyond the positions of top right anchor and 100.
        """
        if (
            self.trapezoid_right_down_anchor.pos().x() < self.trapezoid_right_up_anchor.pos().x()
            or self.trapezoid_right_down_anchor.pos().x() > 100
        ):
            self.trapezoid_right_down_anchor.setPos(self.trap_x[4], self.trap_y[4])
        else:
            self.trapezoid_right_down_anchor.setPos(self.trapezoid_right_down_anchor.pos().x(), self.trap_y[4])
            self.trap_x[4] = self.trapezoid_right_down_anchor.pos().x()
        self._update_plot()

    def _change_position(self):
        """Change the position of the entire plot.

        The position anchor has to be between 0 and 100.
        """
        if 0 < self.position_anchor.pos().x() < 100:
            dif = self.central_x - self.position_anchor.pos().x()
            self.trap_x = [x - dif for x in self.trap_x]
            self.central_x = self.position_anchor.pos().x()
            self.position_anchor.setPos(self.position_anchor.pos().x(), 0)
            self.trapezoid_left_down_anchor.setPos(self.trap_x[1], self.trap_y[1])
            self.trapezoid_left_up_anchor.setPos(self.trap_x[2], self.trap_y[2])
            self.trapezoid_right_up_anchor.setPos(self.trap_x[3], self.trap_y[3])
            self.trapezoid_right_down_anchor.setPos(self.trap_x[4], self.trap_y[4])

        else:
            self.position_anchor.setPos(self.central_x, 0)
        self._update_plot()

    def _update_plot(self):
        self.trapezoid_plot_line.setData(self.trap_x, self.trap_y)
