# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import pyqtgraph as pg
from PyQt4.QtGui import QCursor
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class NoTool(SignalVisualizerTool):

    def __init__(self,widget):
        SignalVisualizerTool.__init__(self, widget)

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass