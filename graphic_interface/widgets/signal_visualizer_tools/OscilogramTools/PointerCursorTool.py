# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class PointerCursorTool(SignalVisualizerTool):
    """
    Tool that allow to get information about a point x,y
    in the widget graph visualization.
    """

    #CONSTANTS
    def __init__(self, widget):
        SignalVisualizerTool.__init__(self, widget)
        self.pointerCursor = pg.ScatterPlotItem()
        self.widget.addItem(self.pointerCursor)

        # dict of data usefull for the tool
        # TODO must be examinated for possible improvement
        self.last = {'pos': [0, 0], 'pen': {'color': 'w', 'width': 2}, 'brush': pg.intColor(255, 255), 'symbol': '+',
                     'size': 20}

    def mouseMoveEvent(self, event):
        """
        Process the
        :param event:
        :return:
        """

        # get the logical coordinates of the widget's graph from the pixels
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())

        # get the information measured by the tool
        info = self.getAmplitudeTimeInfo(x, y)
        info0 = round(info[0], self.DECIMAL_PLACES), round(info[1], self.DECIMAL_PLACES)

        # check if the cursor is outside the widget graph
        if x == -1 or y == -1:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            return

        self.widget.setCursor(QCursor(QtCore.Qt.CrossCursor))

        # set the detected data for update
        if not self.mousePressed:
            info = self.getAmplitudeTimeInfo(self.last['pos'][0], self.last['pos'][1])
            info0 = round(info0[0], self.DECIMAL_PLACES), round(info0[1], self.DECIMAL_PLACES)
            self.detectedData = [("Amp(%)", round(info[1], self.DECIMAL_PLACES)),
                                 ("t0", round(info0[0],self.DECIMAL_PLACES)),
                                 ("t1", round(info[0],self.DECIMAL_PLACES)),
                                 ("dt", round(info[0] - info0[0],self.DECIMAL_PLACES))
                                ]
        else:
            self.detectedData = [("Amp(%)", round(info[1], self.DECIMAL_PLACES)),
                                 ("Time", round(info[0],self.DECIMAL_PLACES))
                                ]

        # raise the signal of detection data
        self.detectedDataChanged.emit(self.detectedData)

    def mousePressEvent(self, event):
        """
        Process the mouse press event with the pointer cursor tool.
        """
        # update the mouse press state
        self.mousePressed = True

        # clear previous point selection of the widget
        self.pointerCursor.clear()

        # get the coordinates of the widget signal from the x,y pixels
        x = self.fromCanvasToClient(event.x())
        y = self.fromCanvasToClientY(event.y())

        # check if the logical coordinates are outside the visible area
        if x == -1 or y == -1:
            self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            return

        # update the tool data
        self.last = {'pos': [x, y], 'pen': {'color': 'w', 'width': 2}, 'brush': pg.intColor(255, 255), 'symbol': '+',
                     'size': 20}

        self.pointerCursor.addPoints([self.last])

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        # update the mouse press state
        self.mousePressed = False

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        :param yPixel: the y component of the pixel in the widget
        :return: the logical coordinate of the widget's graph if yPixel is inside the graph,
                -1 otherwise
        """

        # get the view ox of the widget to get the size
        widget_viewbox = self.widget.getPlotItem().getViewBox()

        # get the limits of the interval in pixels
        min_y_pixels = widget_viewbox.y()
        max_y_pixels = widget_viewbox.height() + min_y_pixels

        # get the visible logical interval limits in y axis of the widget
        min_y_amplitude, max_y_amplitude = self.widget.getPlotItem().viewRange()[1]

        # set the yPixel of units in entire widget
        # to units inside the range of pixels of the widget
        yPixel = max_y_pixels - yPixel

        # check if yPixel is inside the widget graph
        if yPixel < min_y_pixels or yPixel > max_y_pixels:
            return -1

        return min_y_amplitude + int(round((yPixel - min_y_pixels) * (max_y_amplitude - min_y_amplitude) * 1. / (max_y_pixels - min_y_pixels), 0))

    def dispose(self):
        """
        Release the resources asociated with the tool.
        :return:
        """
        # remove the item of pointer on the widget and the cursor shape
        self.widget.removeItem(self.pointerCursor)
        self.widget.setCursor(QCursor(QtCore.Qt.ArrowCursor))

