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

        self.plot_color = "CC3"

        SoundLabWidget.__init__(self, **kargs)
        pg.PlotWidget.__init__(self)

        self.getPlotItem().showGrid(True, True)
        self.setClipToView(True)
        self.setDownsampling(auto=True, mode="peak")
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.getPlotItem().hideButtons()

        self.setSelectedTool(Tools.NoTool)
        # self.__selectedTool.detectedDataChanged.connect(self.getInfo)

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

    def load_workspace(self, workspace, forceUpdate=False):
        self.plot_color = workspace.theme.plot_color

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

    def getInfo(self, info1, info2):
       pass

    def graph(self, indexFrom=0, indexTo=-1,morekwargs=None):
        """
        Graphs the one dimensional one_dim_transform of a signal interval on the widget
        :param indexFrom: start value of the signal interval in array data indexes
        :param indexTo: end value of the signal interval in array data indexes
        :return:
        """
        if self.one_dim_transform is not None:
            self.clear()
            (x, y) = self.one_dim_transform.getData(indexFrom, indexTo)
            self.plot(x, y, pen=self.plot_color)
            # self.setRange(xRange = (0,x[len(x) - 1]),yRange = (np.amin(y),0) ,padding=0,update=True)
            self.update()
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
