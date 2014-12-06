# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class ZoomTool(SignalVisualizerTool):

    def __init__(self,widget):
        SignalVisualizerTool.__init__(self, widget)
        self.zoomRegion = pg.LinearRegionItem([0, 0])

    def mouseMoveEvent(self, event):
        """
        Process the mouse move event
        :param event:
        :return:
        """
        pg.PlotWidget.mouseMoveEvent(self.widget, event)

        # get the region selected by the tool in pixels
        rgn = self.zoomRegion.getRegion()

        # transform the selected region in logical widget graph coordinates
        minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])

        if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
               abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:

            self.widget.setCursor(QCursor(QtCore.Qt.SizeHorCursor))

            t0 = round(rgn[0] * 1.0 / self.widget.signal.samplingRate,self.DECIMAL_PLACES)
            t1 = round(rgn[1] * 1.0 / self.widget.signal.samplingRate,self.DECIMAL_PLACES)
            dt = round(t1 - t0, self.DECIMAL_PLACES)
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
        if self.mouseInsideZoomArea(event.x()):
            rgn = self.zoomRegion.getRegion()
            if rgn[0] == rgn[1]:
                return
            self.rangeChanged.emit(int(rgn[0]), int(rgn[1]),0,0)
            self.zoomRegion.setRegion([rgn[0], rgn[0]])

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

    def mouseInsideZoomArea(self, xPixel):
        xIndex = self.fromCanvasToClient(xPixel)
        rgn = self.zoomRegion.getRegion()
        return rgn[0] <= xIndex <= rgn[1]

    def setZoomRegionVisible(self, value=False):
        """
        Change the visibility of the tool region.
        :param visibility: visibility to set the region
        :return:
        """
        if value and self.zoomRegion not in self.widget.items():
            self.widget.addItem(self.zoomRegion)

        elif not value and self.zoomRegion in self.widget.items():
            self.widget.removeItem(self.zoomRegion)

    def dispose(self):
        self.setZoomRegionVisible(False)
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))