import numpy as np
import pyqtgraph as pg


class BellPlot:

    def __init__(self, plot_widget, x_data, y_data, a_data, b_data, c_data, color):
        self.plot_widget = plot_widget
        self.bell_x = x_data
        self.bell_y = y_data
        self.a = a_data
        self.b = b_data
        self.c = c_data
        self.color = color
        self.b_height = 0.8

        self.bell_plot_line = self.plot_widget.plot(self.bell_x, self.bell_y, pen=self.color)

        self.left_a_anchor = pg.TargetItem(
            pos=(self.c - self.a, 0.5),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.left_a_anchor.sigPositionChanged.connect(self._interaction_left_a)

        self.right_a_anchor = pg.TargetItem(
            pos=(self.c + self.a, 0.5),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.right_a_anchor.sigPositionChanged.connect(self._interaction_right_a)

        right_b_x_coordinate = self.c + self.a * 0.25 ** (1 / (2 * self.b))
        self.right_b_anchor = pg.TargetItem(
            pos=(right_b_x_coordinate, self.b_height),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.right_b_anchor.sigPositionChanged.connect(self._update_b)

        left_b_x_coordinate = self.c - self.a * 0.25 ** (1 / (2 * self.b))
        self.left_b_anchor = pg.TargetItem(
            pos=(left_b_x_coordinate, self.b_height),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.left_b_anchor.sigPositionChanged.connect(self._update_b)

        self.position_anchor = pg.TargetItem(
            pos=(self.c, 0),
            size=10,
            symbol='s',
            pen=self.color,
            brush=self.color
        )
        self.position_anchor.sigPositionChanged.connect(self._change_position)

        self.plot_widget.addItem(self.left_a_anchor)
        self.plot_widget.addItem(self.right_a_anchor)
        self.plot_widget.addItem(self.left_b_anchor)
        self.plot_widget.addItem(self.right_b_anchor)
        self.plot_widget.addItem(self.position_anchor)

    def _interaction_left_a(self):
        new_pos = self.left_a_anchor.pos()
        new_a = abs(new_pos.x() - self.c)
        if self.c - 2.5 > new_pos.x() > 0:
            self.a = new_a
        self._update_plot()

    def _interaction_right_a(self):
        new_pos = self.right_a_anchor.pos()
        new_a = abs(new_pos.x() - self.c)
        if self.c + 2.5 < new_pos.x() < 100:
            self.a = new_a
        self._update_plot()

    def _update_b(self, item):
        new_pos = item.pos()
        new_x = new_pos.x()

        try:
            if (self.left_a_anchor.pos().x() < self.left_b_anchor.pos().x() < self.c - 2.5
                    and self.right_a_anchor.pos().x() > self.right_b_anchor.pos().x() > self.c + 2.5):
                new_b = np.log(1 / self.b_height - 1) / (2 * np.log(abs((new_x - self.c) / self.a)))
                self.b = max(0.1, new_b)
        except (ZeroDivisionError, ValueError):
            pass

        self._update_plot()

    def _change_position(self):
        if 0 < self.position_anchor.pos().x() < 100:
            dif = self.c - self.position_anchor.pos().x()
            self.bell_x = np.array([(x - dif) for x in self.bell_x])
            self.c = self.position_anchor.pos().x()
            self.position_anchor.setPos(self.position_anchor.pos().x(), 0)
            self.left_a_anchor.setPos(self.c - self.a, 0.5)
            self.right_a_anchor.setPos(self.c + self.a, 0.5)
            self.left_b_anchor.setPos(self.c - self.a * 0.25 ** (1 / (2 * self.b)), self.b_height)
            self.right_b_anchor.setPos(self.c + self.a * 0.25 ** (1 / (2 * self.b)), self.b_height)
        else:
            self.position_anchor.setPos(self.c, 0)
        self._update_plot()

    def _update_plot(self):
        self.left_a_anchor.setPos(self.c - self.a, 0.5)
        self.right_a_anchor.setPos(self.c + self.a, 0.5)

        right_b_x_coordinate = self.c + self.a * 0.25 ** (1 / (2 * self.b))
        left_b_x_coordinate = self.c - self.a * 0.25 ** (1 / (2 * self.b))

        self.right_b_anchor.setPos(right_b_x_coordinate, self.b_height)
        self.left_b_anchor.setPos(left_b_x_coordinate, self.b_height)

        self.bell_y = 1 / (1 + np.abs((self.bell_x - self.c) / self.a) ** (2 * self.b))
        self.bell_plot_line.setData(self.bell_x, self.bell_y)
