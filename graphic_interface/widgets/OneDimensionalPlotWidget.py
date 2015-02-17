# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from duetto.audio_signals import AudioSignal
from duetto.dimensional_transformations.one_dimensional_transforms.OneDimensionalTransform import *
from graphic_interface.widgets.SoundLabWidget import SoundLabWidget
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool as OneDimZoomTool
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.PointerCursorTool import PointerCursorTool as OneDimPointerTool
from graphic_interface.widgets.signal_visualizer_tools.NoTool import NoTool
import pyqtgraph as pg

class OneDimPlotWidget(SoundLabWidget,pg.PlotWidget):
    """
    Plots a one dimensional transformation of a signal
    """

    # Signal raised when a tool made a medition and has new data to show
    toolDataDetected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None,**kargs):
        # set the one dimensional one_dim_transform currently applied to the signal
        self.__one_dim_transform = None
        self._minY = 0
        self._maxY = 0
        self._lines = True

        self.plot_color = "CC3"

        SoundLabWidget.__init__(self, **kargs)
        pg.PlotWidget.__init__(self)

        self.getPlotItem().showGrid(True, True)
        self.setClipToView(True)
        self.setDownsampling(auto=True, mode="peak")
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.getPlotItem().hideButtons()
        self.setRange(xRange=(0, 10),
                       yRange=(0, 10),
                       padding=0, update=True)

        self.setSelectedTool(Tools.NoTool)
        # self.__selectedTool.detectedDataChanged.connect(self.getInfo)

    #region Lines Property

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value):
        self._lines = value

    #endregion

    # region Signal Property

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, signal):
        """
        The property to change the current signal.
        :param signal: the new Audio Signal to process.
        :return:
        """
        if signal is None or not isinstance(signal, AudioSignal):
            raise Exception("Invalid assignation. Must be of type AudioSignal")

        self.__signal = signal

    # endregion

    #region MinY, MaxY Properties

    @property
    def minY(self):
        return self._minY

    @minY.setter
    def minY(self, value):
        self._minY = value

    @property
    def maxY(self):
        return self._maxY

    @maxY.setter
    def maxY(self, value):
        self._maxY = value

    #endregion

    def load_workspace(self, workspace, forceUpdate=False):
        self.plot_color = workspace.oneDimensionalWorkspace.theme.plot_color

    # region Property Transform
    # the signal and the one_dim_transform update is made on the window
    # that controls this widget to avoid redefine the signal property of the widget

    @property
    def one_dim_transform(self):
        return self.__one_dim_transform

    @one_dim_transform.setter
    def one_dim_transform(self, transform):
        """
        Change the current one dim transformation
        visualized by the widget
        :return:
        """
        if not isinstance(transform, OneDimensionalTransform):
            raise Exception("Invalid type. one_dim_transform must be of type OneDimensionalTransform")

        self.__one_dim_transform = transform

        self.__one_dim_transform.signal = self.signal

    # endregion

    def graph(self, indexFrom=0, indexTo=-1,labels=None, morekwargs=None):
        """
        Graphs the one dimensional one_dim_transform of a signal interval on the widget
        :param indexFrom: start value of the signal interval in array data indexes
        :param indexTo: end value of the signal interval in array data indexes
        :return:
        """
        if self.one_dim_transform is not None:

            self.clear()
            (x, y) = self.one_dim_transform.getData(indexFrom, indexTo)

            # plotting function according connecting lines between points or not
            if self.lines:
                self.plot(x, y, pen=self.plot_color, clear=True)
            else:
                self.plot(x, y, pen=None, symbol='s', symbolSize=1, symbolPen=self.plot_color, clear=True)

            # setting the range desired
            self.setXRange(0, x[len(x) - 1], padding=0)
            self.setYRange(self.minY, self.maxY, padding=0)
            self.getPlotItem().getAxis(u'bottom').setRange(0, x[len(x) - 1])
            self.getPlotItem().getAxis(u'left').setRange(self.minY, self.maxY)

            # getting and setting the axis labels
            xLabel = unicode(self.tr(labels[u'X']))
            yLabel = unicode(self.tr(labels[u'Y']))
            self.getPlotItem().setLabel(axis='bottom',text=xLabel)
            self.getPlotItem().setLabel(axis='left', text=yLabel)

            self.show()

    # region Tools interaction Implementation
    def changeTool(self, new_tool_class):
        SoundLabWidget.changeTool(self, new_tool_class)

    def setSelectedTool(self, tool):
        """
        Change the current selected tool of the widget.
        :param tool: the new tool to set.
        :return:
        """
        # switch for the concrete tools implementations
        if tool == Tools.ZoomTool:
            self.changeTool(OneDimZoomTool)

        elif tool == Tools.PointerTool:
            self.changeTool(OneDimPointerTool)


        elif tool == Tools.NoTool:
            self.changeTool(NoTool)

        self.__selectedTool = tool
