# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from Graphic_Interface.Widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class PointerCursorTool(SignalVisualizerTool):

    #CONSTANTS
    def __init__(self, widget):
        SignalVisualizerTool.__init__(self, widget)
        self.pointerCursor = pg.ScatterPlotItem()
        self.widget.addItem(self.pointerCursor)
        self.last = {'pos': [0, 0], 'pen': {'color': 'w', 'width': 2}, 'brush': pg.intColor(255, 255), 'symbol': '+',
                     'size': 20}

    def mouseMoveEvent(self, event):

        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())
        info = self.getAmplitudeTimeInfo(x, y)
        info0 = round(info[0], self.DECIMAL_PLACES), round(info[1], self.DECIMAL_PLACES)
        if x == -1 or y == -1:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            return
        #clean the detected data for update

        if not self.mousePressed:
            info = self.getAmplitudeTimeInfo(self.last['pos'][0], self.last['pos'][1])
            info0 = round(info0[0], self.DECIMAL_PLACES), round(info0[1], self.DECIMAL_PLACES)
            self.detectedData = [("t0", round(info0[0],self.DECIMAL_PLACES)),
                                 ("t1", round(info[0],self.DECIMAL_PLACES)),
                                 ("dt", round(info[0] - info0[0],self.DECIMAL_PLACES)),
                                 ("Amp",round(info[1],self.DECIMAL_PLACES))
                                ]


        else:
            self.detectedData = [("Time", round(info[0],self.DECIMAL_PLACES)),
                                 ("Amp", round(info[1], self.DECIMAL_PLACES))
                                ]
        self.detectedDataChanged.emit(self.detectedData)

        self.widget.setCursor(QCursor(QtCore.Qt.CrossCursor))

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

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.widget.getPlotItem().getViewBox()
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.widget.getPlotItem().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny or yPixel > maxy:
            self.pointerCursor.clear()
            if not self.mousePressed:
                self.pointerCursor.addPoints([self.last])
            return -1

        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def dispose(self):
        self.widget.removeItem(self.pointerCursor)
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

