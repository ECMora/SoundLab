# -*- coding: utf-8 -*-
import numpy


class SignalVisualizerTool:
    """
    Base class for the tools used in the QSignalVisualizerWidget.
    Encapsulates method for user interaction with the visual controls.
    All the signal_visualizer_tools must manage the gui events
    corresponding to its function
    """

    # CONSTANTS
    # the minimum amount of pixels that would be considered valid for a move
    #action with a mouse cursor. Is used to reduce the unnecessary gui widget refresh
    PIXELS_OF_CURSORS_CHANGES = 5

    DECIMAL_PLACES = 2

    def __init__(self,widget):
        if widget is None:
            raise Exception("Widget can't be None")
        self.widget = widget
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

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates in the canvas
        @param indexX:  The signal index
        @return:  the canvas coordinates
        """
        vb = self.widget.getPlotItem().getViewBox()
        maxx = vb.width()
        a, b = self.widget.getPlotItem().viewRange()[0]
        return int(vb.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.widget.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a, b = self.widget.getPlotItem().viewRange()[0]
        return a + int(round((xPixel - minx) * (b - a) * 1. / (maxx - minx), 0))

