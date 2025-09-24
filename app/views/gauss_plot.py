"""Add an interactive gauss plot element to the plot widget.

    Classes:
        GaussPlot: a class responsible for plotting an interacting plot to a given pyqtgraph plot widget element.
"""
import numpy as np
import pyqtgraph as pg


class GaussPlot:
    """Class representing a Triangle plot.
         Allows user interaction via pyqtgraph TargetItem elements in order to change shape and position of the plot.

         Methods:
             __init__(pq.PlotWidget(), list[float], list[float], float, float string):
                 create an instance of TrianglePlot.

         Parameters:
             plot_widget: an instance of pq.PlotWidget() to which the plot will be added
             x_data: list of the points on the x axi
             y_data: list of the points on the y axi
             sigma_data: the standard deviation
             mu_data: the median point of the plot
             color:  a hexadecimal string representing the colour of the plot

     """
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

        self.plot_widget.addItem(self.gauss_left_anchor)
        self.plot_widget.addItem(self.gauss_right_anchor)

    def _left_gauss_interaction(self) -> None:
        """Change the shape of the plot by interacting via the left anchor, update the new sigma."""
        new_pos = self.gauss_left_anchor.pos()
        new_sigma = abs(new_pos.x() - self.mu)
        if new_sigma > 0 and new_pos.x() < 49:
            self.sigma = new_sigma
        self.gauss_left_anchor.setPos(self.mu - self.sigma, np.exp(-0.5))
        self.gauss_right_anchor.setPos(self.mu + self.sigma, np.exp(-0.5))
        self._update_plot()

    def _right_gauss_interaction(self) -> None:
        """Change the shape of the plot by interacting via the left anchor, update the right sigma."""
        new_pos = self.gauss_right_anchor.pos()
        new_sigma = abs(new_pos.x() - self.mu)
        if new_sigma > 0 and new_pos.x() > 51:
            self.sigma = new_sigma
        self.gauss_left_anchor.setPos(self.mu - self.sigma, np.exp(-0.5))
        self.gauss_right_anchor.setPos(self.mu + self.sigma, np.exp(-0.5))
        self._update_plot()

    def _update_plot(self) -> None:
        """Calculate new list of y points. Update the plot."""
        self.gauss_y = np.exp(-(1 / 2) * ((self.gauss_x - self.mu) / self.sigma) ** 2)
        self.gauss_plot_line.setData(self.gauss_x, self.gauss_y)
