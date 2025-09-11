import pyqtgraph as pg


class TrianglePlot:

    def __init__(self, plot_widget, x_data, y_data, color, central_x):
        self.plot_widget = plot_widget
        self.tri_x = x_data
        self.tri_y = y_data
        self.color = color
        self.central_x = central_x

        self.triangle_plot_line = self.plot_widget.plot(
            self.tri_x,
            self.tri_y,
            pen=self.color
        )

        self.triangle_central_anchor = pg.TargetItem(
            pos=(self.tri_x[2], self.tri_y[2]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.triangle_central_anchor.sigPositionChanged.connect(self._central_triangle_interaction)

        self.triangle_left_anchor = pg.TargetItem(
            pos=(self.tri_x[1], self.tri_y[1]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.triangle_left_anchor.sigPositionChanged.connect(self._left_triangle_interaction)

        self.triangle_right_anchor = pg.TargetItem(
            pos=(self.tri_x[3], self.tri_y[3]),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.triangle_right_anchor.sigPositionChanged.connect(self._right_triangle_interaction)

        self.position_anchor = pg.TargetItem(
            pos=(self.central_x, 0),
            size=10,
            symbol='s',
            pen=self.color,
            brush=self.color
        )
        self.position_anchor.sigPositionChanged.connect(self._change_position)

        self.plot_widget.addItem(self.triangle_left_anchor)
        self.plot_widget.addItem(self.triangle_right_anchor)
        self.plot_widget.addItem(self.triangle_central_anchor)
        self.plot_widget.addItem(self.position_anchor)

    def _central_triangle_interaction(self):
        if (self.triangle_central_anchor.pos().x() > self.triangle_right_anchor.pos().x()
                or self.triangle_central_anchor.pos().x() < self.triangle_left_anchor.pos().x()):
            self.triangle_central_anchor.setPos(self.tri_x[2], self.tri_y[2])
        else:
            self.triangle_central_anchor.setPos(self.triangle_central_anchor.pos().x(), self.tri_y[2])
            self.tri_x[2] = self.triangle_central_anchor.pos().x()
        self._update_plot()

    def _left_triangle_interaction(self):
        if (self.triangle_left_anchor.pos().x() > self.triangle_central_anchor.pos().x()
                or self.triangle_left_anchor.pos().x() < 0):
            self.triangle_left_anchor.setPos(self.tri_x[1], self.tri_y[1])
        else:
            self.triangle_left_anchor.setPos(self.triangle_left_anchor.pos().x(), self.tri_y[1])
            self.tri_x[1] = self.triangle_left_anchor.pos().x()
        self._update_plot()

    def _right_triangle_interaction(self):
        if (self.triangle_right_anchor.pos().x() < self.triangle_central_anchor.pos().x()
                or self.triangle_right_anchor.pos().x() > 100):
            self.triangle_right_anchor.setPos(self.tri_x[3], self.tri_y[3])
        else:
            self.triangle_right_anchor.setPos(self.triangle_right_anchor.pos().x(), self.tri_y[3])
            self.tri_x[3] = self.triangle_right_anchor.pos().x()
        self._update_plot()

    def _change_position(self):
        if 0 < self.position_anchor.pos().x() < 100:
            dif = self.central_x - self.position_anchor.pos().x()
            self.tri_x = [x - dif for x in self.tri_x]
            self.central_x = self.position_anchor.pos().x()
            self.position_anchor.setPos(self.position_anchor.pos().x(), 0)
            self.triangle_left_anchor.setPos(self.tri_x[1], self.tri_y[1])
            self.triangle_central_anchor.setPos(self.tri_x[2], self.tri_y[2])
            self.triangle_right_anchor.setPos(self.tri_x[3], self.tri_y[3])

        else:
            self.position_anchor.setPos(self.central_x, 0)
        self._update_plot()

    def _update_plot(self):
        self.triangle_plot_line.setData(self.tri_x, self.tri_y)
