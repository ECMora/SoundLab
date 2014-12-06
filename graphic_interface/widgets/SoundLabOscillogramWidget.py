from PyQt4 import QtCore
from duetto.widgets.OscillogramWidget import OscillogramWidget
from graphic_interface.widgets.SoundLabWidget import SoundLabWidget
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool


class SoundLabOscillogramWidget(SoundLabWidget, OscillogramWidget):
    # Signal raised when a tool wants to make a change on the range of visualization
    # of it's widget.
    # raise the limits of the new range x1, x2
    # x1 => start value in x axis
    # x2 => end value in x axis
    rangeChanged = QtCore.pyqtSignal(int, int)

    # Signal raised when a tool made a change on the signal data
    # and the widget must refresh it self
    # raise the limits of the modified range x1, x2 in signal data indexes
    signalChanged = QtCore.pyqtSignal(int, int)

    # Signal raised when a tool made a medition and has new data to show
    toolDataDetected = QtCore.pyqtSignal(str)

    def __init__(self):
        OscillogramWidget.__init__(self)
        SoundLabWidget.__init__(self)
        self.changeTool(ZoomTool)
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
        self.setRange(xRange=(x1, x2),
                      yRange=(self.signal.minimumValue, self.signal.maximumValue),
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
        """
        Loads a theme and updates the view according with it.
        :param theme: an instance of OscillogramTheme, the part of the WorkTheme concerning the oscillogram.
        """
        update = False
        # set background color
        self.setBackground(theme.background_color)
        # set grid lines
        self.getPlotItem().showGrid(theme.gridX, theme.gridY)

        # set the color of the plot lines; the lines will be redrawn later if the color changed
        self.plotLine.setPen(theme.plot_color)

        if self.theme is None or self.theme.connectPoints != theme.connectPoints:
            update = True

        # self.minY = -theme.minYOsc * 0.01 * self.signal.minimumValue
        # self.maxY = theme.maxYOsc * 0.01 * self.signal.maximumValue
        # self.setRange(yRange=(self.minY,
        #                       self.maxY),
        #                       padding=0, update=True)

        # keep a copy of the theme
        self.theme = theme.copy()

        # update the widget if needed
        if update:
            rangeX = self.getPlotItem().getViewBox().viewRange()[0]
            self.graph(rangeX[0], rangeX[1])

    def graph(self, indexFrom=0, indexTo=-1):
        morekwargs = dict()
        points = indexTo - indexFrom
        if points < 0: points += len(self.signal)
        if self.theme is not None:
            if not self.theme.connectPoints and points < self.getPlotItem().getViewBox().width():
                morekwargs['symbol'] = 's'
                morekwargs['symbolSize'] = 1
                morekwargs['symbolPen'] = self.theme.plot_color
                morekwargs['pen'] = '0000'
            else:
                morekwargs['pen'] = self.theme.plot_color

        OscillogramWidget.graph(self, indexFrom, indexTo, morekwargs)
        self.setRange(yRange=(self.minY,
                              self.maxY),
                              padding=0)

