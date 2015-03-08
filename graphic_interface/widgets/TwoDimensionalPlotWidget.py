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

        plot_item = self.getPlotItem()
        view_box = plot_item.getViewBox()
        view_box.mouseDragEvent = lambda ev, axis=0: False

        # variables for rectangular selection manipulation
        self.mousePressed = False
        self.lastPoint = QPoint(0, 0)
        self.oldX, self.oldY = 0, 0
        self.ElementSelectionRect = QtGui.QGraphicsRectItem(QtCore.QRectF(0,0, 0, 0))
        self.ElementSelectionRect.setPen(QtGui.QPen(QtGui.QColor(255,255,255)))

    # region Mouse Events

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
            # update (if necessary) the coordinates of the visual rectangle.
            self.__updateSelectionRect(ev)
            self.update()

    # endregion

    # region Axis Settings

    def setAxisLabel(self, axis_location="bottom", label="", **extra_args):
        """
        Set the label on the x or y axis
        :param axis_location: the location of the axis to set the label. (One of "bottom", "left")
        :param label: The label to set  (str)
        :param extra_args: dict with extra arguments to give to the axis item setLabel.
        :return:
        """
        if axis_location not in ["bottom", "left"]:
            raise ValueError("axis location must one of 'bottom' or 'left'")

        self.getPlotItem().getAxis(axis_location).setLabel(label, **extra_args)

    def setAxisFont(self, axis_location="bottom", font=None):
        """
        Set the font on the x or y axis
        :param axis_location: the location of the axis to set the label. (One of "bottom", "left")
        :param font: The font to set  (QFont)
        :return:
        """
        if axis_location not in ["bottom", "left"]:
            raise ValueError("axis location must one of 'bottom' or 'left'")

        if font is not None:
            self.getPlotItem().getAxis(axis_location).setTickFont(font)

    def showGrid(self, x=True, y=True):
        """
        Set the visibility of grid on the widget
        :param x: The x grid visibility
        :param y: The y grid visibility
        :return:
        """
        self.getPlotItem().showGrid(x=x, y=y)

    # endregion

    # region Selection Rectangle

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

    def __updateSelectionRect(self,ev):
        """
        Update the selection rectangle figure with the information of a new gui
        event like mouse press
        :param ev: The event of the gui system
        """
        point = self.getPlotItem().getViewBox().mapSceneToView(QtCore.QPointF(ev.x(),ev.y()))
        x, y = point.x(), point.y()
        self.ElementSelectionRect.setRect(self.lastPoint.x(), self.lastPoint.y(),
                                          x-self.lastPoint.x(), y - self.lastPoint.y())

    # endregion

    def setRange(self, xRange=(0, 0), yRange=(0, 0)):
        """
        Set the visible range of the widget
        :return:
        """
        self.getPlotItem().setRange(xRange=xRange, yRange=yRange)