# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from graphic_interface.widgets.signal_visualizer_tools import SignalVisualizerTool


class RectangularEraserTool(SignalVisualizerTool):
    def __init__(self, widget):
        SignalVisualizerTool.__init__(self, widget)

        self.mousePressed = False
        self.zoomRegion = pg.LinearRegionItem([0, 0])

    def mouseMoveEvent(self, event):
        # self.widget.getPlotItem().mouseMoveEvent(event)
        rgn = self.zoomRegion.getRegion()
        minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
        if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                        abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
            self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
        elif self.mouseInsideZoomArea(event.x()):
            if self.mousePressed:
                self.widget.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
            else:
                self.widget.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        pg.PlotWidget.mouseMoveEvent(self.widget, event)
        self.widget.update()

    def mousePressEvent(self, event):
        self.mousePressed = True
        if self.zoomRegion not in self.widget.items():
            self.zoomRegion.setRegion([self.fromCanvasToClient(event.x()), self.fromCanvasToClient(event.x())])
            self.setZoomRegionVisible(True)

        else:
            rgn = self.zoomRegion.getRegion()
            minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
            if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                            abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
                self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
            elif not self.mouseInsideZoomArea(event.x()):
                x = self.fromCanvasToClient(event.x())
                self.zoomRegion.setRegion([x, x])
                # self.update()
            else:
                self.widget.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
        pg.PlotWidget.mousePressEvent(self.widget, event)

    def mouseDoubleClickEvent(self, event):
        pg.PlotWidget.mouseDoubleClickEvent(self.widget, event)
        # if self.mouseInsideZoomArea(event.x()) and self.makeZoom and callable(self.makeZoom):
        #     rgn = self.zoomRegion.getRegion()
        #     if rgn[0] == rgn[1]:
        #         return
        #     self.rangeChanged.emit()
        #     self.zoomRegion.setRegion([rgn[0], rgn[0]])

    def mouseReleaseEvent(self, event):
        self.mousePressed = False
        pg.PlotWidget.mouseReleaseEvent(self.widget, event)
        rgn = self.zoomRegion.getRegion()
        minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
        if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                        abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
            self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
        elif self.mouseInsideZoomArea(event.x()):
            self.widget.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def dispose(self):
        pass

