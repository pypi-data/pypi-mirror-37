#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from jhunt.qt.widgets.plot import PlotCanvas

class StatsTab(QWidget):

    def __init__(self, data, parent):
        super().__init__(parent=parent)

        self.tabs = parent

        # See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html

        vbox = QVBoxLayout(self)
        self.plot_canvas = PlotCanvas(data, parent=self, width=5, height=4, dpi=100)
        vbox.addWidget(self.plot_canvas)

        ###################################################

        #proxy_model.dataChanged.connect(plot_canvas.update_figure)
        #proxy_model.rowsInserted.connect(plot_canvas.update_figure)  # TODO
        #proxy_model.rowsRemoved.connect(plot_canvas.update_figure)   # TODO

        # Update the stats plot when the tabs switch to the stats tab
        self.tabs.currentChanged.connect(self.updatePlot)


    def updatePlot(self, index):
        """

        Parameters
        ----------
        index

        Returns
        -------

        """

        # Update the plot whenever the parent tab (i.e. the "stats" tab) is selected as the current tab
        if index == self.tabs.indexOf(self):
            self.plot_canvas.update_figure()

