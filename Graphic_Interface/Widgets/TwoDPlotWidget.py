# -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore


class TwoDPlotWidget(pg.PlotWidget):

    def __init__(self,parent=None):
        pg.PlotWidget.__init__(self,parent)
        self.mousePressed = False
        self.oldX,self.oldY = 0, 0
        self.ElementSelectionRect = QtGui.QGraphicsRectItem(QtCore.QRectF(0,0, 0, 0))
        self.ElementSelectionRect.setPen(QtGui.QPen(QtGui.QColor(255,255,255)))

    def removeSelectionRect(self):
        if self.ElementSelectionRect in self.items():
            self.removeItem(self.ElementSelectionRect)

    def addSelectionRect(self):
        if self.ElementSelectionRect not in self.items():
            self.addItem(self.ElementSelectionRect)

    def mousePressEvent(self, ev):
        pg.PlotWidget.mousePressEvent(self, ev)
        if ev.button() == QtCore.Qt.LeftButton:
            self.mousePressed = True
            point = self.getPlotItem().getViewBox().mapSceneToView(QtCore.QPointF(ev.x(),ev.y()))
            self.oldX, self.oldY = point.x(),point.y()
            self.ElementSelectionRect.setRect(self.oldX,self.oldY,0,0)
            self.update()

    def __updateSelectionRect(self,ev):
        point = self.getPlotItem().getViewBox().mapSceneToView(QtCore.QPointF(ev.x(),ev.y()))
        x, y = point.x(), point.y()
        #self.oldX,self.oldY, x, y = min(self.oldX,x),min(self.oldY,y),max(self.oldX,x),max(self.oldY,y)
        self.ElementSelectionRect.setRect(self.oldX,self.oldY,x-self.oldX,y - self.oldY)
        print( self.oldX,self.oldY, x, y)

    def mouseReleaseEvent(self, ev):
        pg.PlotWidget.mouseReleaseEvent(self, ev)
        self.mousePressed = False

    def mouseMoveEvent(self, ev):
        pg.PlotWidget.mouseMoveEvent(self,ev)
        if self.mousePressed:
            self.__updateSelectionRect(ev)
            self.update()

