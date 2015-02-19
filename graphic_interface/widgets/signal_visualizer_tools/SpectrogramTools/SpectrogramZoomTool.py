# -*- coding: utf-8 -*-
from PyQt4 import QtCore,QtGui
import numpy
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from SpectrogramTool import SpectrogramTool


class SpectrogramZoomTool(SpectrogramTool):

    def __init__(self, widget):
        SpectrogramTool.__init__(self,widget)
        self.zoomRegion = pg.LinearRegionItem([0, 0])

    def mouseMoveEvent(self, event):
        pg.GraphicsView.mouseMoveEvent(self.widget.graphics_view, event)
        rgn = self.zoomRegion.getRegion()
        minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
        if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                        abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
            self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
            t0 = round(rgn[0] * 1.0 / self.widget.signal.samplingRate, self.DECIMAL_PLACES)
            t1 = round(rgn[1] * 1.0 / self.widget.signal.samplingRate,self.DECIMAL_PLACES)
            dt = t0 - t1
            self.detectedData = [("t0", t0),
                                 ("t1", t1),
                                 ("dt", dt)
            ]
            self.detectedDataChanged.emit(self.detectedData)

        elif self.mouseInsideZoomArea(event.x()):
            cursor = QtCore.Qt.ClosedHandCursor if self.mousePressed else QtCore.Qt.OpenHandCursor
            self.widget.setCursor(QCursor(cursor))

        else:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def mousePressEvent(self, event):
        self.mousePressed = True
        rgn = self.zoomRegion.getRegion()
        minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
        if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                        abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
            self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
        elif not self.mouseInsideZoomArea(event.x()):
            x = self.fromCanvasToClient(event.x())
            self.zoomRegion.setRegion([x, x])
        else:
            self.widget.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
        pg.GraphicsView.mousePressEvent(self.widget.graphics_view, event)

    def mouseDoubleClickEvent(self, event):
        pg.GraphicsView.mouseDoubleClickEvent(self.widget.graphics_view, event)
        if self.mouseInsideZoomArea(event.x()):
            rgn = self.zoomRegion.getRegion()
            if rgn[0] == rgn[1]:
                return
            indexFrom = int(self.widget.from_spec_to_osc(rgn[0]))
            indexTo = int(self.widget.from_spec_to_osc(rgn[1]))
            self.rangeChanged.emit(indexFrom, indexTo, 0, 0)

    def mouseReleaseEvent(self, event):
        self.mousePressed = False
        pg.GraphicsView.mouseReleaseEvent(self.widget.graphics_view, event)
        rgn = self.zoomRegion.getRegion()
        minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
        if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                        abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
            self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
        elif self.mouseInsideZoomArea(event.x()):
            self.widget.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        #interval Changed

    def mouseInsideZoomArea(self, xPixel):
        xIndex = self.fromCanvasToClient(xPixel)
        rgn = self.zoomRegion.getRegion()
        return rgn[0] <= xIndex <= rgn[1]

    def disable(self):
        self.widget.viewBox.removeItem(self.zoomRegion)
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def enable(self):
        self.widget.viewBox.addItem(self.zoomRegion)