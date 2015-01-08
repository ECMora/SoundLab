# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from SpectrogramTool import SpectrogramTool


class PointerCursorTool(SpectrogramTool):

    # CONSTANTS

    def __init__(self, widget):
        SpectrogramTool.__init__(self, widget)
        self.pointerCursor = pg.ScatterPlotItem()
        self.last = {'pos': [0, 0], 'pen': {'color': 'w', 'width': 2}, 'brush': pg.intColor(255, 255), 'symbol': '+',
                     'size': 20}

    def mouseMoveEvent(self, event):
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())
        if x == -1 or y == -1:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            return
        info = self.widget.specgramHandler.getInfo(x, y)

        if not self.mousePressed:
            info0 = self.widget.specgramHandler.getInfo(*self.last['pos'])
            self.detectedData = [("Amp(dB)", round(info[2], self.DECIMAL_PLACES)),
                                 ("t0", round(info0[0], self.DECIMAL_PLACES)),
                                 ("t1", round(info[0], self.DECIMAL_PLACES)),
                                 ("dt", round(info[0] - info0[0], self.DECIMAL_PLACES))
                                ]
        else:
            self.detectedData = [("Amp(dB)", round(info[2], self.DECIMAL_PLACES)),
                                 ("Time",  round(info[0],self.DECIMAL_PLACES)),
                                 ("Freq(kHz)", round(info[1],self.DECIMAL_PLACES))
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

    def disable(self):
        self.widget.viewBox.removeItem(self.pointerCursor)
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def enable(self):
        self.widget.viewBox.addItem(self.pointerCursor)



