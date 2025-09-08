import pyqtgraph as pg


class TrapezoidPlot:

    def __init__(self, plot_widget, x_data, y_data, color):
        self.plot_widget = plot_widget
        self.trap_x = x_data
        self.trap_y = y_data
        self.color = color

        self.trapezoid_plot_line = self.plot_widget.plot(
            self.trap_x,
            self.trap_y,
            pen=self.color
        )

        self.trapezoid_left_down_anchor = pg.TargetItem(
            pos=(self.trap_x[1], self.trap_y[1]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.trapezoid_left_down_anchor.sigPositionChanged.connect(self._left_down_trap_interaction)

        self.trapezoid_left_up_anchor = pg.TargetItem(
            pos=(self.trap_x[2], self.trap_y[2]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.trapezoid_left_up_anchor.sigPositionChanged.connect(self._left_up_trap_interaction)

        self.trapezoid_right_up_anchor = pg.TargetItem(
            pos=(self.trap_x[3], self.trap_y[3]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.trapezoid_right_up_anchor.sigPositionChanged.connect(self._right_up_trap_interaction)

        self.trapezoid_right_down_anchor = pg.TargetItem(
            pos=(self.trap_x[4], self.trap_y[4]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )

        self.trapezoid_right_down_anchor.sigPositionChanged.connect(self._right_down_trap_interaction)

        self.plot_widget.addItem(self.trapezoid_right_up_anchor)
        self.plot_widget.addItem(self.trapezoid_left_up_anchor)
        self.plot_widget.addItem(self.trapezoid_left_down_anchor)
        self.plot_widget.addItem(self.trapezoid_right_down_anchor)

    def _left_down_trap_interaction(self):
        if (self.trapezoid_left_down_anchor.pos().x() < 0
                or self.trapezoid_left_down_anchor.pos().x() > self.trapezoid_left_up_anchor.pos().x()):
            self.trapezoid_left_down_anchor.setPos(self.trap_x[1], self.trap_y[1])
        else:
            self.trapezoid_left_down_anchor.setPos(self.trapezoid_left_down_anchor.pos().x(), self.trap_y[1])
            self.trap_x[1] = self.trapezoid_left_down_anchor.pos().x()
        self._update_plot()

    def _left_up_trap_interaction(self):
        if (self.trapezoid_left_up_anchor.pos().x() < self.trapezoid_left_down_anchor.pos().x()
                or self.trapezoid_left_up_anchor.pos().x() > self.trapezoid_right_up_anchor.pos().x()):
            self.trapezoid_left_up_anchor.setPos(self.trap_x[2], self.trap_y[2])
        else:
            self.trapezoid_left_up_anchor.setPos(self.trapezoid_left_up_anchor.pos().x(), self.trap_y[2])
            self.trap_x[2] = self.trapezoid_left_up_anchor.pos().x()
        self._update_plot()

    def _right_up_trap_interaction(self):
        if (self.trapezoid_right_up_anchor.pos().x() < self.trapezoid_left_up_anchor.pos().x()
                or self.trapezoid_right_up_anchor.pos().x() > self.trapezoid_right_down_anchor.pos().x()):
            self.trapezoid_right_up_anchor.setPos(self.trap_x[3], self.trap_y[3])
        else:
            self.trapezoid_right_up_anchor.setPos(self.trapezoid_right_up_anchor.pos().x(), self.trap_y[3])
            self.trap_x[3] = self.trapezoid_right_up_anchor.pos().x()
        self._update_plot()

    def _right_down_trap_interaction(self):
        if (self.trapezoid_right_down_anchor.pos().x() < self.trapezoid_right_up_anchor.pos().x()
                or self.trapezoid_right_down_anchor.pos().x() > 100):
            self.trapezoid_right_down_anchor.setPos(self.trap_x[4], self.trap_y[4])
        else:
            self.trapezoid_right_down_anchor.setPos(self.trapezoid_right_down_anchor.pos().x(), self.trap_y[4])
            self.trap_x[4] = self.trapezoid_right_down_anchor.pos().x()
        self._update_plot()

    def _update_plot(self):
        self.trapezoid_plot_line.setData(self.trap_x, self.trap_y)
