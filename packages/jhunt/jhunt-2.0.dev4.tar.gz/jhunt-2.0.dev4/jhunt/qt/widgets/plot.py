#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):
    """This is a Matplotlib QWidget.

    See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """

    def __init__(self, data, parent, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.data = data
        self.date_column_index = data.headers.index("Date")

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        data = np.array(self.data._data)

        try:
            x = data[:, self.date_column_index]
            dti = pd.DatetimeIndex(x)
            s = pd.Series(np.ones(dti.shape), index=dti)

            s.resample('1d').count().plot.bar(color="blue", alpha=0.5, ax=self.axes)

            #s.plot(ax=self.axes)         # TODO
            #s.groupby(s.time).count().plot(ax=self.axes)         # TODO
        except IndexError as e:
            # Happen when data is empty
            pass

        #self.axes.plot(x, y)

    def update_figure(self):
        data = np.array(self.data._data)

        self.axes.cla()

        try:
            x = data[:, self.date_column_index]
            dti = pd.DatetimeIndex(x)
            s = pd.Series(np.ones(dti.shape), index=dti)

            s.resample('1d').count().plot.bar(color="blue", alpha=0.5, ax=self.axes)

            #s.plot(ax=self.axes)         # TODO
            #s.groupby(s.time).count().plot(ax=self.axes)         # TODO
            #self.axes.plot(x, y)
        except IndexError as e:
            # Happen when data is empty
            pass

        self.draw()
