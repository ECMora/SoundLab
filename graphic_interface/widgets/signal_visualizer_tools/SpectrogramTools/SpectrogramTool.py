# -*- coding: utf-8 -*-
import numpy

from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class SpectrogramTool(SignalVisualizerTool):

    # SIGNALS

    # CONSTANTS

    def __init__(self,widget):
        SignalVisualizerTool.__init__(self,widget)

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates in the canvas
        """
        maxx = self.widget.viewBox.width()
        a, b = self.widget.viewBox.viewRange()[0]
        return int(self.widget.viewBox.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        minx = self.widget.viewBox.x()
        maxx = self.widget.viewBox.width() + minx
        a, b = self.widget.viewBox.viewRange()[0]
        if xPixel < minx or xPixel > maxx:
            return -1
        return a + int(round((xPixel - minx) * (b - a) * 1. / (maxx - minx), 0))

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.widget.viewBox
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.widget.viewBox.viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny:
            yPixel = miny

        if yPixel > maxy:
            yPixel = maxy

        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def timeToStr(self, time):
        unit = 's'
        if time < 1:
            time *= 1000
            unit = 'ms'
        elif time > 60:
            time /= 60
            unit = 'm'
            if time > 60:
                time /= 60
                unit = 'h'
        return unicode(numpy.round(time, 1)) + unit