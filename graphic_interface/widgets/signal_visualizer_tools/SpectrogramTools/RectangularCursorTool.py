# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import numpy
from PyQt4.QtGui import QCursor
from SpectrogramTool import SpectrogramTool
from Graphic_Interface.Widgets.signal_visualizer_tools.OscilogramTools.RectROI import RectROI


class RectangularCursorTool(SpectrogramTool):
    def __init__(self, widget):
        SpectrogramTool.__init__(self, widget)
        self.last = {'pos': [0,0]}
        self.rectangularCursor = RectROI([0, 0], [0, 0], pen=(0, 9), movable=False)
        self.widget.viewBox.addItem(self.rectangularCursor)
        self.rectRegion = {'x': [0, 0], 'y': [0, 0]}
        self.detectedData = []

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
            info = self.getFreqTimeAndIntensity(self.rectRegion['x'][0], self.rectRegion['y'][0])
            info1 = self.getFreqTimeAndIntensity(self.rectRegion['x'][1], self.rectRegion['y'][1])
            self.rectRegion['y'][0] = info[1]
            self.rectRegion['y'][1] = info1[1]
            self.detectedData = [("t0", self.timeToStr(round(info[0], self.DECIMAL_PLACES))),
                                 ("t1", self.timeToStr(round(info1[0], self.DECIMAL_PLACES))),
                                 ("dt", self.timeToStr(round(info1[0] - info[0],self.DECIMAL_PLACES))),
                                 ("MinFreq", round(info[1],self.DECIMAL_PLACES)),
                                 ("MaxFreq", round(info1[1],self.DECIMAL_PLACES)),
                                 ("dF", round(info1[1] - info[1],self.DECIMAL_PLACES))
                                ]
        else:
            info = self.getFreqTimeAndIntensity(x, y)
            if x == -1 or y == -1:
                self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            else:
                self.detectedData = [("Time", self.timeToStr(round(info[0],self.DECIMAL_PLACES))),
                                     ("Freq", round(info[1],self.DECIMAL_PLACES)),
                                     ("Amp", round(info[2],self.DECIMAL_PLACES))
                                    ]
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.detectedDataChanged.emit(self.detectedData)

    def mousePressEvent(self, event):
        self.mousePressed = True
        self.last = {'pos': [self.fromCanvasToClient(event.x()), self.fromCanvasToClientY(event.y())]}
        self.rectangularCursor.setPos(self.last['pos'])
        self.rectangularCursor.setSize([0, 0])

    def mouseDoubleClickEvent(self, event):
        x = self.fromCanvasToClient(event.x())
        y = numpy.round(self.parent().specgramSettings.freqs[self.fromCanvasToClientY(event.y())] * 1.0 / 1000, 1)
        if self.mouseInsideRectArea(x, y):
            #make the zomm self.makeZoomRect(specCoords=True)
            pass

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def mouseInsideRectArea(self, x, y):
        return x <= self.rectRegion['x'][1] and x >= self.rectRegion['x'][0] \
               and self.rectRegion['y'][1] >= y >= self.rectRegion['y'][0]

    def dispose(self):
        self.widget.viewBox.removeItem(self.rectangularCursor)

