from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy
from duetto.widgets.SpectrogramWidget import SpectrogramWidget
from graphic_interface.widgets.SoundLabWidget import SoundLabWidget
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.PointerCursorTool import PointerCursorTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.RectangularCursorTool import RectangularCursorTool
from signal_visualizer_tools.SpectrogramTools.RectangularCursorTool import \
    RectangularCursorTool as SpecRectangularCursorTool
from signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool
from signal_visualizer_tools.SpectrogramTools.PointerCursorTool import PointerCursorTool as SpecPointerCursorTool


class SoundLabSpectrogramWidget(SoundLabWidget, SpectrogramWidget):
    # Signal raised when a tool wants to make a change on the range of visualization
    #of it's widget.
    #raise the limits of the new range x1, x2
    # x1 => start value in x axis
    # x2 => end value in x axis
    rangeChanged = QtCore.pyqtSignal(int, int)

    # Signal raised when a tool made a change on the signal data
    #and the widget must refresh it self
    #raise the limits of the modified range x1, x2 in signal data indexes
    signalChanged = QtCore.pyqtSignal(int, int)

    # Signal raised when a tool made a medition and has new data to show
    toolDataDetected = QtCore.pyqtSignal(str)

    def __init__(self):
        SpectrogramWidget.__init__(self)
        SoundLabWidget.__init__(self)

        #parche para capturar los eventos visuales del control
        #TODO averiguar por que razon no se envian los eventos correctamente al widget
        self.graphics_view.mouseMoveEvent = self.mouseMoveEvent
        self.graphics_view.mouseReleaseEvent = self.mouseReleaseEvent
        self.graphics_view.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.graphics_view.mousePressEvent = self.mousePressEvent
        self.changeTool(SpectrogramZoomTool)
        self.minY = 0
        self.maxY = 22

    def changeTool(self, new_tool_class):
        SoundLabWidget.changeTool(self,new_tool_class)
        if self.gui_user_tool is not None:
            self.gui_user_tool.rangeChanged.connect(self.changeRangeSignal)
            self.gui_user_tool.signalChanged.connect(self.updateSignalManager)

    def updateSignal(self,x1, x2):
        """
        Update the visible data of the signal.
        :param x1:
        :param x2:
        """
        self.graph(x1, x2)

    def updateSignalManager(self, x1, x2):
        self.updateSignal(x1, x2)
        self.signalChanged.emit(x1, x2)

    def changeRange(self,x1,x2,y1=0,y2=0):
        self.graph(x1, x2)

    def changeRangeSignal(self, x1, x2, y1, y2):
        self.changeRange(x1, x2, y1, y2)
        self.rangeChanged.emit(x1, x2)

    def load_Theme(self, theme):
        self.graphics_view.setBackground(theme.spec_background)
        # self.viewBox.showGrid(theme.spec_GridX,theme.spec_GridY)

        if theme.maxYSpec == -1:
            theme.maxYSpec = self.specgramHandler.freqs[-1]
        YSpec = numpy.searchsorted(self.specgramHandler.freqs, [theme.minYSpec * 1000, theme.maxYSpec * 1000])
        self.minY, self.maxY = YSpec[0], YSpec[1]
        self.viewBox.setYRange(self.minY,
                               self.maxY,
                              padding=0)
        # self.graph()

    def graph(self,indexFrom=0,indexTo=-1):
        SpectrogramWidget.graph(self,indexFrom,indexTo)
        self.viewBox.setYRange(self.minY,
                               self.maxY,
                              padding=0)
