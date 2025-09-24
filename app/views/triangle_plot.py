"""Add an interactive triangle plot element to the plot widget.

    Classes:
        TrianglePlot: a class responsible for plotting an interacting plot to a given pyqtgraph plot widget element.
"""
import pyqtgraph as pg


class TrianglePlot:
    """Class representing a Triangle plot.
        Allows user interaction via pyqtgraph TargetItem elements in order to change shape and position of the plot.

        Methods:
            __init__(pq.PlotWidget(), list[float], list[float], string):
                create an instance of TrianglePlot.

        Parameters:
            plot_widget: an instance of pq.PlotWidget() to which the plot will be added
            x_data: list of the points on the x axi
            y_data: list of the points on the y axi
            color:  a hexadecimal string representing the colour of the plot

    """
    def __init__(self, plot_widget, x_data, y_data, color):
        self.plot_widget = plot_widget
        self.tri_x = x_data
        self.tri_y = y_data
        self.color = color

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

        self.plot_widget.addItem(self.triangle_left_anchor)
        self.plot_widget.addItem(self.triangle_right_anchor)
        self.plot_widget.addItem(self.triangle_central_anchor)

    def _central_triangle_interaction(self) -> None:
        """Move the central anchor of the plot. Disallows moving beyond right anchor and the left anchor."""
        if (self.triangle_central_anchor.pos().x() > self.triangle_right_anchor.pos().x()
                or self.triangle_central_anchor.pos().x() < self.triangle_left_anchor.pos().x()):
            self.triangle_central_anchor.setPos(self.tri_x[2], self.tri_y[2])
        else:
            self.triangle_central_anchor.setPos(self.triangle_central_anchor.pos().x(), self.tri_y[2])
            self.tri_x[2] = self.triangle_central_anchor.pos().x()
        self._update_plot()

    def _left_triangle_interaction(self) -> None:
        """Move the left anchor of the plot. Disallows moving beyond central anchor and 0."""
        if (self.triangle_left_anchor.pos().x() > self.triangle_central_anchor.pos().x()
                or self.triangle_left_anchor.pos().x() < 0):
            self.triangle_left_anchor.setPos(self.tri_x[1], self.tri_y[1])
        else:
            self.triangle_left_anchor.setPos(self.triangle_left_anchor.pos().x(), self.tri_y[1])
            self.tri_x[1] = self.triangle_left_anchor.pos().x()
        self._update_plot()

    def _right_triangle_interaction(self) -> None:
        """Move the right anchor of the plot. Disallows moving beyond central anchor and 100."""
        if (self.triangle_right_anchor.pos().x() < self.triangle_central_anchor.pos().x()
                or self.triangle_right_anchor.pos().x() > 100):
            self.triangle_right_anchor.setPos(self.tri_x[3], self.tri_y[3])
        else:
            self.triangle_right_anchor.setPos(self.triangle_right_anchor.pos().x(), self.tri_y[3])
            self.tri_x[3] = self.triangle_right_anchor.pos().x()
        self._update_plot()

    def _update_plot(self) -> None:
        """Updates the plot"""
        self.triangle_plot_line.setData(self.tri_x, self.tri_y)