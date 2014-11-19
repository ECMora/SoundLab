# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import numpy
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from RectROI import RectROI
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class RectangularCursorTool(SignalVisualizerTool):
    def __init__(self, widget):
        SignalVisualizerTool.__init__(self, widget)
        self.last = {'pos': [0,0]}
        self.rectangularCursor = RectROI([0, 0], [0, 0], pen=(0, 9), movable=False)
        self.rectRegion = {'x': [0, 0], 'y': [0, 0]}

    def mouseMoveEvent(self, event):
        self.setRectRegionVisible(True)
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
            info = self.getAmplitudeTimeInfo(self.rectRegion['x'][0], self.rectRegion['y'][0])
            info = round(info[0], self.DECIMAL_PLACES), round(info[1], self.DECIMAL_PLACES)

            info1 = self.getAmplitudeTimeInfo(self.rectRegion['x'][1], self.rectRegion['y'][1])
            info1 = round(info1[0], self.DECIMAL_PLACES), round(info1[1], self.DECIMAL_PLACES)

            self.rectRegion['y'][0] = info[1]
            self.rectRegion['y'][1] = info1[1]

            # clean the detected data for update
            self.detectedData = [("t0", info[0]),
                                 ("t1", info1[0]),
                                 ("dt", info1[0] - info[0]),
                                 ("MaxAmp",info[1]),
                                 ("MinAmp", info1[1])
                                ]

        else:
            info = self.getAmplitudeTimeInfo(x, y)
            info = round(info[0], self.DECIMAL_PLACES), round(info[1], self.DECIMAL_PLACES)

            if x == -1 or y == -1:
                self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            else:
                self.detectedData = [("Time", info[0]),
                                     ("Amp", info[1])
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
            #make the zoom in the rectangle area
            pass

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def mouseInsideRectArea(self, x, y):
        return x <= self.rectRegion['x'][1] and x >= self.rectRegion['x'][0] \
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

    def dispose(self):
        self.setRectRegionVisible(False)

    def setRectRegionVisible(self, value=False):
        if value and self.rectangularCursor not in self.widget.items():
            self.widget.addItem(self.rectangularCursor)
        elif not value and self.rectangularCursor in self.widget.items():
            self.widget.removeItem(self.rectangularCursor)

