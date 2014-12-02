from PyQt4 import QtCore
from duetto.widgets.OscillogramWidget import OscillogramWidget
from Graphic_Interface.Widgets.SoundLabWidget import SoundLabWidget
from Graphic_Interface.Widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool


class SoundLabOscilogramWidget(SoundLabWidget,OscillogramWidget):
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
        OscillogramWidget.__init__(self)
        SoundLabWidget.__init__(self)
        self.changeTool(ZoomTool)
        self.osc_color = "CC3"
        self.minY = self.signal.minimumValue if self.signal is not None else -100
        self.maxY = self.signal.maximumValue if self.signal is not None else 100

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
        self.graph(x1,x2)

    def updateSignalManager(self, x1, x2):
        self.updateSignal(x1, x2)
        self.signalChanged.emit(x1, x2)

    def changeRange(self,x1,x2,y1=0,y2=0):
        """
        Change the range of visualization of the signal
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        """
        self.setRange(xRange=(x1,x2),
                      yRange=(self.signal.minimumValue,self.signal.maximumValue),
                      padding=0)

    def changeRangeSignal(self, x1, x2, y1, y2):
        """
        Manage the range changed signal from tools.
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        """
        self.changeRange(x1, x2, y1, y2)
        self.rangeChanged.emit(x1, x2)

    def load_Theme(self, theme):
        update = False
        self.setBackground(theme.osc_background)
        self.getPlotItem().showGrid(theme.osc_GridX, theme.osc_GridY)
        if self.osc_color != theme.osc_plot:
            update = True
            self.osc_color = theme.osc_plot
        self.minY = -theme.minYOsc * 0.01 * self.signal.minimumValue
        self.maxY = theme.maxYOsc * 0.01 * self.signal.maximumValue
        self.setRange(yRange=(self.minY,
                              self.maxY),
                              padding=0, update=True)
        if update:
            self.graph()

    def graph(self, indexFrom=0, indexTo=-1):
        OscillogramWidget.graph(self,indexFrom,indexTo)
        self.setRange(yRange=(self.minY,
                              self.maxY),
                              padding=0)

