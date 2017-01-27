# -*- coding: utf-8 -*-
from PyQt4 import QtGui

import pyqtgraph as pg
from pyqtgraph.widgets.HistogramLUTWidget import HistogramLUTWidget
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox

from duetto.audio_signals import AudioSignal
from HorizontalHistogram import HorizontalHistogramWidget
from Axis import SpecYAxis, OscXAxis
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.Spectrogram import Spectrogram


class SpectrogramWidget(QtGui.QWidget):
    """
    Widget that visualize and interacts with a spectrogram graph
    of an audio signal.
    """
    # SIGNALS

    # CONSTANTS
    # Value of the axis lines opacity
    AXIS_LINES_OPACITY = 255

    # Max amount of columns to show on the visual widget.
    MAX_SPECGRAM_COLUMNS = 800

    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__(self)
        # variable that handles the manipulation of the spectrogram
        # create, recompute etc
        self.specgramHandler = Spectrogram()

        # create the histogram widget
        self.imageItem = ImageItem()
        self.__histogram = HorizontalHistogramWidget()
        self.__histogram.item.setImageItem(self.imageItem)

        # internal vieBox for image graph
        self.viewBox = ViewBox()
        self.viewBox.addItem(self.imageItem)
        self.viewBox.setMouseEnabled(x=False, y=False)
        self.viewBox.setMenuEnabled(False)
        self.viewBox.setAspectLocked(False)

        # set the X and Y axis for the graph
        self.xAxis = OscXAxis(self, orientation='bottom')
        self.yAxis = SpecYAxis(self, orientation='left')

        self.xAxis.linkToView(self.viewBox)
        self.yAxis.linkToView(self.viewBox)

        self.xAxis.setGrid(self.AXIS_LINES_OPACITY)
        self.yAxis.setGrid(self.AXIS_LINES_OPACITY)

        # adjust the graph zone in the control
        horizontal_histogram = kwargs["horizontal_histogram"] if "horizontal_histogram" in kwargs else True
        visible_histogram = kwargs["visible_histogram"] if "visible_histogram" in kwargs else False
        self.__updateLayout(histogramHorizontal=(horizontal_histogram if visible_histogram else None))

    def __updateLayout(self,histogramHorizontal=None):
        """
        Updates the layout of the widget to change the histogram
        position (horizontal-vertical) and visibility
        :param histogramHorizontal: None if invisible, true if horizontal
        false if vertical
        :return:
        """
        # graph_control_layout

        self.graphics_view = pg.GraphicsView()

        # set the layout of the graphics view internal
        # that contains the axis and the view box to graph the spectrogram
        graphics_view_grid_layout = QtGui.QGraphicsGridLayout()
        graphics_view_grid_layout.setContentsMargins(0, 0, 0, 0)
        graphics_view_grid_layout.setHorizontalSpacing(0)
        graphics_view_grid_layout.setVerticalSpacing(0)

        graphics_view_grid_layout.addItem(self.xAxis, 1, 1)
        graphics_view_grid_layout.addItem(self.yAxis, 0, 0)
        graphics_view_grid_layout.addItem(self.viewBox, 0, 1)

        self.graphics_view.centralWidget.setLayout(graphics_view_grid_layout)
        layout = QtGui.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphics_view, 0, 0)
        # add the elements in row,col

        if histogramHorizontal is not None:
            row = 1 if histogramHorizontal else 0
            col = 1 - row
            self.__histogram = HorizontalHistogramWidget() if histogramHorizontal else\
                               HistogramLUTWidget()
            self.__histogram.item.gradient.loadPreset('thermal')
            self.__histogram.item.setImageItem(self.imageItem)
            layout.addWidget(self.histogram,row,col)

        self.setLayout(layout)

    # region Signal Property
    @property
    def signal(self):
        return self.specgramHandler.signal

    @signal.setter
    def signal(self, signal):
        if signal is None or not isinstance(signal, AudioSignal):
            raise ValueError("Invalid assignation. Must be of type AudioSignal")

        self.specgramHandler.signal = signal

        max_columns = max(self.viewBox.width(), self.MAX_SPECGRAM_COLUMNS)

        self.specgramHandler.recomputeSpectrogram(maxCol=max_columns)
        # updating the axis scales
        self.xAxis.scale = self.specgramHandler.signal.samplingRate

        # updating the frequencies present in the signal
        # samplingRate/2 by Nyquist theorem. After update the spectrogram handler
        # there is an array in the specgramHandler with the freqs returned by the specgram
        # freqs is an array with the values of the frequency of each row of the specgram matriz
        self.yAxis.frequencies = self.specgramHandler.freqs

    # endregion

    # region Histogram Prop
    @property
    def histogram(self):
        """
        Histogram widget with the values of the image.
        interacts with the image graph to change its color,
        threshold etc. Allow to visualize it outside the spectrogram widget
        :return:
        """
        return self.__histogram
    # endregion

    def getInfo(self,x,y):
        """
        Gets the values at x, y in the spectrogram
        :param x: the time position in rows of the spectrogram matriz
        :param y: the freq position in columns of the spectrogram matriz
        :return: a tuple with (time, freq, intensity)
        """
        return self.specgramHandler.getInfo(x,y)

    def graph(self, indexFrom=0, indexTo=-1, padding=0):

        indexTo = indexTo if (indexTo >= 0 and indexTo > indexFrom) else self.signal.length

        # avoid to set the max columns too high that the spectrogram cant be computed
        # and do not consume more resources that necessary
        # show at most as many columns as pixels in the widget's width
        max_columns = max(self.viewBox.width(), self.MAX_SPECGRAM_COLUMNS)

        self.specgramHandler.recomputeSpectrogram(indexFrom, indexTo, max_columns)
        self.yAxis.frequencies = self.specgramHandler.freqs

        # set the new spectrogram image computed
        self.imageItem.setImage(self.specgramHandler.matriz)
        self.viewBox.setRange(xRange=(self.specgramHandler.from_osc_to_spec(indexFrom),
                                      self.specgramHandler.from_osc_to_spec(indexTo-1)), padding=padding)

        # update the histogram colors of the spectrogram
        self.histogram.item.region.lineMoved()
        self.histogram.item.region.lineMoveFinished()
        self.xAxis.setRange(indexFrom, indexTo)

        self.update()

