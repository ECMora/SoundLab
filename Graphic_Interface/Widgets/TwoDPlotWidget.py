# -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore


class TwoDPlotWidget(pg.PlotWidget):

    def __init__(self,parent=None):
        pg.PlotWidget.__init__(self,parent)
        self.makingElementSelection = True
        self.mousePressed = False
        self.ElementSelectionRect = QtGui.QGraphicsRectItem(QtCore.QRectF(0,0, 0.5, 0.6))
        self.ElementSelectionRect.setPen(QtGui.QPen(QtGui.QColor(255,255,255)))

    def removeSelectionRect(self):
        if self.ElementSelectionRect in self.items():
            self.removeItem(self.ElementSelectionRect)

    def addSelectionRect(self):
        if self.ElementSelectionRect not in self.items():
            self.addItem(self.ElementSelectionRect)

    def mousePressEvent(self, ev):
        pg.PlotWidget.mousePressEvent(self, ev)
        self.mousePressed = True
        if self.makingElementSelection:
            rang = self.viewRect()
            rect = self.rect()
            x, y, w, h = rang.x()+rang.width()*((ev.x()-rect.x())/rect.width()), rang.y()+rang.height()*((ev.y()-rect.y())/rect.height()), 0.5, 0.5
            self.ElementSelectionRect.setRect(x, y, w, h)
            self.update()

    def changeSelectionMode(self,bool):
        self.makingElementSelection = bool
        if bool is False:
            self.ElementSelectionRect = QtGui.QGraphicsRectItem(QtCore.QRectF(0,0, 0, 0))
            self.update()

    def mouseReleaseEvent(self, ev):
        pg.PlotWidget.mouseReleaseEvent(self, ev)
        self.mousePressed = False

    def mouseMoveEvent(self, ev):
        pg.PlotWidget.mouseMoveEvent(self,ev)
        if self.makingElementSelection and self.mousePressed:
            self.update()

