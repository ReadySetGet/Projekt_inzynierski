import numpy as np
import pyqtgraph as pg


class GaussPlot:

    def __init__(self, plot_widget, x_data, y_data, sigma_data, mu_data, color):
        self.plot_widget = plot_widget
        self.gauss_x = x_data
        self.gauss_y = y_data
        self.sigma = sigma_data
        self.mu = mu_data
        self.color = color

        self.gauss_plot_line = self.plot_widget.plot(self.gauss_x, self.gauss_y, pen=self.color)

        self.gauss_left_anchor = pg.TargetItem(
            pos=(self.mu - self.sigma, np.exp(-0.5)),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.gauss_left_anchor.sigPositionChanged.connect(self._left_gauss_interaction)

        self.gauss_right_anchor = pg.TargetItem(
            pos=(self.mu + self.sigma, np.exp(-0.5)),
            size=10,
            symbol='o',
            pen=self.color,
            brush=self.color
        )
        self.gauss_right_anchor.sigPositionChanged.connect(self._right_gauss_interaction)

        self.position_anchor = pg.TargetItem(
            pos=(self.mu, 0),
            size=10,
            symbol='s',
            pen=self.color,
            brush=self.color
        )
        self.position_anchor.sigPositionChanged.connect(self._change_position)

        self.plot_widget.addItem(self.gauss_left_anchor)
        self.plot_widget.addItem(self.gauss_right_anchor)
        self.plot_widget.addItem(self.position_anchor)

    def _left_gauss_interaction(self):
        new_pos = self.gauss_left_anchor.pos()
        new_sigma = abs(new_pos.x() - self.mu)
        if new_sigma > 0 and new_pos.x() < 49:
            self.sigma = new_sigma
        self.gauss_left_anchor.setPos(self.mu - self.sigma, np.exp(-0.5))
        self.gauss_right_anchor.setPos(self.mu + self.sigma, np.exp(-0.5))
        self._update_plot()

    def _right_gauss_interaction(self):
        new_pos = self.gauss_right_anchor.pos()
        new_sigma = abs(new_pos.x() - self.mu)
        if new_sigma > 0 and new_pos.x() > 51:
            self.sigma = new_sigma
        self.gauss_left_anchor.setPos(self.mu - self.sigma, np.exp(-0.5))
        self.gauss_right_anchor.setPos(self.mu + self.sigma, np.exp(-0.5))
        self._update_plot()

    def _change_position(self):
        if 0 < self.position_anchor.pos().x() < 100:
            dif = self.mu - self.position_anchor.pos().x()
            self.gauss_x = np.array([(x - dif) for x in self.gauss_x])
            self.mu = self.position_anchor.pos().x()
            self.position_anchor.setPos(self.position_anchor.pos().x(), 0)
            self.gauss_left_anchor.setPos(self.mu - self.sigma, np.exp(-0.5))
            self.gauss_right_anchor.setPos(self.mu + self.sigma, np.exp(-0.5))
        else:
            self.position_anchor.setPos(self.mu, 0)
        self._update_plot()

    def _update_plot(self):
        self.gauss_y = np.exp(-(1 / 2) * ((self.gauss_x - self.mu) / self.sigma) ** 2)
        self.gauss_plot_line.setData(self.gauss_x, self.gauss_y)
