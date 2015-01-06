# -*- coding: utf-8 -*-
import numpy
from PyQt4 import QtCore


class Tools:
    """
    Enum for the different tools that can be used on a gui sound lab widget
    """
    ZoomTool, PointerTool, RectangularZoomTool, RectangularEraser, NoTool = range(5)


class SignalVisualizerTool(QtCore.QObject):
    """
    Base class for the tools used in the QSignalVisualizerWidget.
    Encapsulates method for user interaction with the visual controls.
    All the signal_visualizer_tools must manage the gui events
    corresponding to its function
    """

    # region SIGNALS

    # Signal raised when the tool detected data has changed
    # the detected data is send as a list of tuples ("measured_param" , value)
    # it sends a list to keep the order of the atributes
    detectedDataChanged = QtCore.pyqtSignal(list)

    # Signal raised when a tool wants to make a change on the range of visualization
    # of it's widget.
    # raise the limits of the new range x1, x2, y1, y2
    # x1 => start value in x axis
    # x2 => end value in x axis
    # y1 => start value in y axis
    # y2 => end value in y axis
    rangeChanged = QtCore.pyqtSignal(int, int, int, int)

    # Signal raised when a tool made a change on the signal data
    # and the widget must refresh it self
    # raise the limits of the modified range x1, x2 in signal data indexes
    signalChanged = QtCore.pyqtSignal(int, int)

    # endregion

    # CONSTANTS
    # the minimum amount of pixels that would be considered valid for a move
    # action with a mouse cursor. Is used to reduce the unnecessary gui widget refresh
    PIXELS_OF_CURSORS_CHANGES = 5

    # The decimal places to round the numerical meditions made by the tool
    DECIMAL_PLACES = 2

    def __init__(self, widget):
        QtCore.QObject.__init__(self)
        if widget is None:
            raise Exception("Widget can't be None")

        # the widget at which the tool is bounded
        # the tool has the access to the widgets variables to
        # implement the interaction with the widget's signal
        self.widget = widget

        # the signal data detected by the tool
        self.detectedData = []

        self.mousePressed = False

    def dispose(self):
        """
        Method invoked when the tool must be removed from the widget.
        Release all the resources and collateral effects of the tool in the widget
        """
        pass

    def getAmplitudeTimeInfo(self, x, y):
        amplt = numpy.round(y * 100.0 / self.widget.signal.maximumValue, 0)
        time = x * 1.0 / self.widget.signal.samplingRate
        return [time, amplt]

    def getFreqTimeAndIntensity(self,x, y):
        return self.widget.getInfo(x,y)

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates
        in the canvas
        @param indexX:  The signal index
        @return:  the canvas coordinates
        """
        vb = self.widget.getPlotItem().getViewBox()
        maxx = vb.width()
        a, b = self.widget.getPlotItem().viewRange()[0]
        return int(vb.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding
        index in the signal array
        """
        vb = self.widget.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a, b = self.widget.getPlotItem().viewRange()[0]
        return a + int(round((xPixel - minx) * (b - a) * 1. / (maxx - minx), 0))

