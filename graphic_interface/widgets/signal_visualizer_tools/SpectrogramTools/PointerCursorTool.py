# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from SpectrogramTool import SpectrogramTool


class PointerCursorTool(SpectrogramTool):

    #CONSTANTS
    def __init__(self, widget):
        SpectrogramTool.__init__(self, widget)
        self.pointerCursor = pg.ScatterPlotItem()
        self.widget.viewBox.addItem(self.pointerCursor)
        self.last = {'pos': [0, 0], 'pen': {'color': 'w', 'width': 2}, 'brush': pg.intColor(255, 255), 'symbol': '+',
                     'size': 20}

    def mouseMoveEvent(self, event):
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())
        if x == -1 or y == -1:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            return
        info = self.getFreqTimeAndIntensity(x, y)

        if not self.mousePressed:
            info0 = self.getFreqTimeAndIntensity(self.last['pos'][0], self.last['pos'][1])
            self.detectedData = [("t0", self.timeToStr(round(info0[0], self.DECIMAL_PLACES))),
                                 ("t1", self.timeToStr(round(info[0],self.DECIMAL_PLACES))),
                                 ("dt", self.timeToStr(round(info[0] - info0[0],self.DECIMAL_PLACES)))
                                ]
        else:
            self.detectedData = [("Time", self.timeToStr(round(info[0],self.DECIMAL_PLACES))),
                                 ("Freq", str(round(info[1],self.DECIMAL_PLACES)) + " kHz"),
                                 ("Amp", str(round(info[2],self.DECIMAL_PLACES)) + " dB")
                                ]
        self.widget.setCursor(QCursor(QtCore.Qt.CrossCursor))
        self.detectedDataChanged.emit(self.detectedData)

    def mousePressEvent(self, event):
        self.mousePressed = True
        self.pointerCursor.clear()
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())
        if x == -1 or y == -1:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            return
        self.last = {'pos': [x, y], 'pen': {'color': 'w', 'width': 2}, 'brush': pg.intColor(255, 255), 'symbol': '+',
                     'size': 20}
        self.pointerCursor.addPoints([self.last])
        self.widget.setCursor(QCursor(QtCore.Qt.CrossCursor))

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def dispose(self):
        self.widget.viewBox.removeItem(self.pointerCursor)
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))


