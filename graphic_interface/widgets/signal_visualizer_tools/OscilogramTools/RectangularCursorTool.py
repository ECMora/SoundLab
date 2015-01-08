#  -*- coding: utf-8 -*-
from PyQt4 import QtCore

import numpy
from PyQt4.QtGui import QCursor

from RectROI import RectROI
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class RectangularCursorTool(SignalVisualizerTool):
    """
    Tool that allow to define a rectangle area on the widget and to extract
    parameters from the signal visualized on that area.
    """

    def __init__(self, widget):
        SignalVisualizerTool.__init__(self, widget)

        # dict of data ussefull for the tool
        # TODO must be examinated for possible improvement
        self.last = {'pos': [0, 0]}

        # visual rectangle for the tool
        self.rectangularCursor = RectROI([0, 0], [0, 0], pen=(0, 9), movable=False)

        # the region of the rectangle in points start, end in x and y
        # is used because RectROI do not provide the get size method
        self.rectRegion = {'x': [0, 0], 'y': [0, 0]}

    def mouseMoveEvent(self, event):
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())

        if self.mousePressed:
            if x < self.last['pos'][0]:
                if y < self.last['pos'][1]:
                    self.rectangularCursor.setPos([x, y])
                    self.rectRegion['x'][0] = x
                    self.rectRegion['y'][0] = y
                else:
                    self.rectangularCursor.setPos([x, self.last['pos'][1]])
                    self.rectRegion['x'][0] = x
                    self.rectRegion['y'][0] = self.last['pos'][1]
            elif x >= self.last['pos'][0]:
                if y < self.last['pos'][1]:
                    self.rectangularCursor.setPos([self.last['pos'][0], y])
                    self.rectRegion['x'][0] = self.last['pos'][0]
                    self.rectRegion['y'][0] = y
                else:
                    self.rectangularCursor.setPos(self.last['pos'])
                    self.rectRegion['x'][0] = self.last['pos'][0]
                    self.rectRegion['y'][0] = self.last['pos'][1]
            dx = numpy.abs(self.last['pos'][0] - x)
            dy = numpy.abs(self.last['pos'][1] - y)
            self.rectangularCursor.setSize([dx, dy])
            self.rectRegion['x'][1] = self.rectRegion['x'][0] + dx
            self.rectRegion['y'][1] = self.rectRegion['y'][0] + dy
            amplitude_time_info = self.getAmplitudeTimeInfo(self.rectRegion['x'][0], self.rectRegion['y'][0])
            amplitude_time_info = round(amplitude_time_info[0], self.DECIMAL_PLACES), round(amplitude_time_info[1], self.DECIMAL_PLACES)

            info1 = self.getAmplitudeTimeInfo(self.rectRegion['x'][1], self.rectRegion['y'][1])
            info1 = round(info1[0], self.DECIMAL_PLACES), round(info1[1], self.DECIMAL_PLACES)

            self.rectRegion['y'][0] = amplitude_time_info[1]
            self.rectRegion['y'][1] = info1[1]

            #  clean the detected data for update
            self.detectedData = [("t0", round(amplitude_time_info[0], self.DECIMAL_PLACES)),
                                 ("t1", round(info1[0], self.DECIMAL_PLACES)),
                                 ("dt", round(info1[0] - amplitude_time_info[0], self.DECIMAL_PLACES)),
                                 ("MinAmp(%)",round(amplitude_time_info[1], self.DECIMAL_PLACES)),
                                 ("MaxAmp(%)", round(info1[1], self.DECIMAL_PLACES))
                                ]

        else:
            amplitude_time_info = self.getAmplitudeTimeInfo(x, y)

            if x == -1 or y == -1:
                self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            else:
                self.detectedData = [("Time", round(amplitude_time_info[0],self.DECIMAL_PLACES)),
                                     ("Amp(%)", round(amplitude_time_info[1],self.DECIMAL_PLACES))
                                    ]

        self.detectedDataChanged.emit(self.detectedData)

    def mousePressEvent(self, event):
        self.mousePressed = True
        self.last = {'pos': [self.fromCanvasToClient(event.x()), self.fromCanvasToClientY(event.y())]}
        self.rectangularCursor.setPos(self.last['pos'])
        self.rectangularCursor.setSize([0, 0])

    def mouseDoubleClickEvent(self, event):
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())
        y = numpy.round(y * 100.0 / self.widget.signal.maximumValue, 0)
        if self.mouseInsideRectArea(x, y):
            # make the zoom in the rectangle area
            pass

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def mouseInsideRectArea(self, x, y):
        """
        :param x: Position x in pixels of the widget.
        :param y: Position y in pixels of the widget.
        :return: True if the x,y position is inside the rectangle tool
        selected area, False otherwise.
        """
        return self.rectRegion['x'][1] >= x >= self.rectRegion['x'][0] \
               and self.rectRegion['y'][1] >= y >= self.rectRegion['y'][0]

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.widget.getPlotItem().getViewBox()
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.widget.getPlotItem().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny:
            yPixel = miny

        if yPixel > maxy:
                yPixel = maxy

        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def disable(self):
        self.setRectRegionVisible(False)

    def enable(self):
        self.setRectRegionVisible(True)

    def setRectRegionVisible(self, visibility=False):
        """
        Change the visibility of the tool region rectangle.
        :param visibility: visibility to set the region
        :return:
        """
        if visibility and self.rectangularCursor not in self.widget.items():
            self.widget.addItem(self.rectangularCursor)

        elif not visibility and self.rectangularCursor in self.widget.items():
            self.widget.removeItem(self.rectangularCursor)

