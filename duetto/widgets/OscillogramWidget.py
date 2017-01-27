# -*- coding: utf-8 -*-
import pyqtgraph as pg
import numpy as np

from duetto.audio_signals import AudioSignal
from Axis import OscXAxis, OscYAxis


class OscillogramWidget(pg.PlotWidget):
    """
    Widget that graph an oscilogram from an audio signal
    """
    # SIGNALS
    # CONSTANTS

    def __init__(self, parent=None, **kargs):
        # definition of the axis for the graph process of the signal
        self.xAxis = OscXAxis(parent, orientation='bottom')
        self.yAxis = OscYAxis(parent, orientation='left')

        # plot widget used to graph the signal
        pg.PlotWidget.__init__(self, axisItems={'bottom': self.xAxis, 'left': self.yAxis})

        self.xAxis.linkToView(self.getPlotItem().getViewBox())
        self.yAxis.linkToView(self.getPlotItem().getViewBox())

        # current signal to visualize
        self.__signal = None
        self.signal = AudioSignal()
        self.default_plot_color = 'CC3'
        self.plotLine = None

        self.getPlotItem().showGrid(True, True)
        self.setClipToView(True)
        self.setDownsampling(auto=True, mode="peak")
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.getPlotItem().hideButtons()

    # region Signal Property

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, signal):
        """
        The property to change the current signal.
        All internal variables are updated to deal with the new signal.
        :param signal: the new Audio Signal to visualize.
        :return:
        """
        if signal is None or not isinstance(signal, AudioSignal):
            raise Exception("Invalid assignation. Must be of type AudioSignal")

        self.__signal = signal

        # update the axis to show the ticks labels properly
        self.xAxis.scale = self.__signal.samplingRate
        self.yAxis.scale = self.__signal.maximumValue / 100.0

        # update the signal interval of visualization in oscilogram
        self.setRange(xRange=(0, signal.length),
                       yRange=(signal.minimumValue, signal.maximumValue),
                       padding=0, update=True)

    # endregion

    def graph(self, indexFrom=0, indexTo=-1, morekwargs=None):
        """
        Graph the oscilogram of the current signal in the provided interval.
        :param indexFrom: Start of the interval in signal data array value.
        :param indexTo: End of the interval in signal data array value.
        :param morekwargs: Additional keyword arguments to pass to plot. Must be a dictionary with str keys.
        """
        if morekwargs is None:
            morekwargs = dict()

        # add my kwargs if not in more kwargs
        kwargs = morekwargs.copy()

        #
        kwargs['clipToView'] = True

        if 'clear' not in kwargs:
            kwargs['clear'] = True
        if 'pen' not in kwargs:
            kwargs['pen'] = self.default_plot_color
        if 'padding' not in kwargs:
            kwargs['padding'] = 0

        # self.clear()
        indexTo = indexTo if (indexTo >= 0 and indexTo > indexFrom) else self.signal.length

        self.setXRange(indexFrom, indexTo, padding=kwargs['padding'])

        self.xAxis.setRange(indexFrom, indexTo)

        self.plotLine = self.plot(np.arange(indexFrom, indexTo), self.signal.data[indexFrom:indexTo], **kwargs)

