# -*- coding: utf-8 -*-
from PyQt4.QtCore import QPoint
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore


class TwoDPlotWidget(pg.PlotWidget):
    """
    Widget to display a two dimensional graph
    based on elements with (x,y) coordinates.
    The widget allow to select a rectangular region of elements
    by their coordinates
    """

    def __init__(self,parent=None):
        pg.PlotWidget.__init__(self, parent)

        #variables for rectangular selection manipulation
        self.mousePressed = False
        self.lastPoint = QPoint(0, 0)
        self.oldX, self.oldY = 0, 0
        self.ElementSelectionRect = QtGui.QGraphicsRectItem(QtCore.QRectF(0,0, 0, 0))
        self.ElementSelectionRect.setPen(QtGui.QPen(QtGui.QColor(255,255,255)))

    def removeSelectionRect(self):
        """
        Removes (if exist) the visual rectangle of the widget.
        """
        if self.ElementSelectionRect in self.items():
            self.removeItem(self.ElementSelectionRect)

    def addSelectionRect(self):
        """
        Adds a visual rectangle in the widget to select elements
        """
        if self.ElementSelectionRect not in self.items():
            self.addItem(self.ElementSelectionRect)

    def mousePressEvent(self, ev):
        pg.PlotWidget.mousePressEvent(self, ev)
        if ev.button() == QtCore.Qt.LeftButton:
            self.mousePressed = True
            # get the local graph coordinate point from
            # the pixel where the cursor was pressed
            # update last point
            self.lastPoint = self.getPlotItem().getViewBox().mapSceneToView(QtCore.QPointF(ev.x(),ev.y()))
            self.ElementSelectionRect.setRect(self.lastPoint.x(),self.lastPoint.y(),0,0)
            self.update()

    def __updateSelectionRect(self,ev):
        """
        Update the selection rectangle figure with the information of a new gui
        event like mouse press
        :param ev: The event of the gui system
        """
        point = self.getPlotItem().getViewBox().mapSceneToView(QtCore.QPointF(ev.x(),ev.y()))
        x, y = point.x(), point.y()
        #self.oldX,self.oldY, x, y = minThresholdLabel(self.oldX,x),minThresholdLabel(self.oldY,y),maxThresholdLabel(self.oldX,x),maxThresholdLabel(self.oldY,y)
        self.ElementSelectionRect.setRect(self.lastPoint.x(),self.lastPoint.y(),x-self.lastPoint.x(),y - self.lastPoint.y())

    def mouseReleaseEvent(self, ev):
        """
        Widget response for a mouse release event.
        :param ev:
        """
        pg.PlotWidget.mouseReleaseEvent(self, ev)
        self.mousePressed = False

    def mouseMoveEvent(self, ev):
        pg.PlotWidget.mouseMoveEvent(self,ev)
        if self.mousePressed:
            #update (if necessary) the coordinates of the visual rectangle.
            self.__updateSelectionRect(ev)
            self.update()

