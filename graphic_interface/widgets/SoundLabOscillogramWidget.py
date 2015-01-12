from PyQt4 import QtCore
from duetto.widgets.OscillogramWidget import OscillogramWidget
from graphic_interface.Settings.Workspace import OscillogramWorkspace
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
        # self.minY = self.signal.minimumValue if self.signal is not None else -100
        # self.maxY = self.signal.maximumValue if self.signal is not None else 100
        self.workspace = OscillogramWorkspace()
        self._pointsConnectedOnLastUpdate = False

    def changeTool(self, new_tool_class):
        SoundLabWidget.changeTool(self, new_tool_class)
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
        self.graph(x1, x2)

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

    def _load_theme(self, theme):
        update = False
        # set background color
        if self.workspace.theme.background_color != theme.background_color:
            self.setBackground(theme.background_color)

        # set grid lines
        if self.workspace.theme.gridX != theme.gridX or self.workspace.theme.gridY != theme.gridY:
            self.getPlotItem().showGrid(theme.gridX, theme.gridY)

        # set the color of the plot lines; the lines will be redrawn later if the color changed
        if self.plotLine:
            if self._pointsConnectedOnLastUpdate:
                self.plotLine.setPen(theme.plot_color)
            else:
                self.plotLine.setSymbolPen(theme.plot_color)

        if self.workspace.theme is None or self.workspace.theme.connectPoints != theme.connectPoints:
            update = True

        # keep a copy of the theme
        self.workspace.theme = theme.copy()

        # returns whether it's necessary to update the widget
        return update

    def load_Theme(self, theme):
        """
        Loads a theme and updates the view according with it.
        :param theme: an instance of OscillogramTheme, the part of the WorkTheme concerning the oscillogram.
        """
        # load the theme and determine if it's necessary to update the widget
        update = self._load_theme(theme)

        # update the widget if needed
        if update:
            rangeX = self.getPlotItem().getViewBox().viewRange()[0]
            self.graph(rangeX[0], rangeX[1])

    def load_workspace(self, workspace, forceUpdate=False):
        """
        Loads a workspace and updates the view according with it.
        :param workspace: an instance of OscillogramWorkspace, the part of the Workspace concerning the oscillogram
        """
        update = False

        # set the y axis' range
        minY = -workspace.minY * self.signal.minimumValue
        maxY = workspace.maxY * self.signal.maximumValue
        self.setRange(yRange=(minY, maxY), padding=0, update=True)

        # load the theme
        update = self._load_theme(workspace.theme) or update

        # keep a copy of the workspace
        self.workspace = workspace.copy()

        # update the widget if needed
        if update or forceUpdate:
            rangeX = self.getPlotItem().getViewBox().viewRange()[0]
            self.graph(rangeX[0], rangeX[1])

    def graph(self, indexFrom=0, indexTo=-1, morekwargs=None):
        morekwargs = dict()
        points = indexTo - indexFrom
        if points < 0: points += len(self.signal)
        if not self.workspace.theme.connectPoints and points < self.getPlotItem().getViewBox().width():
            morekwargs['symbol'] = 's'
            morekwargs['symbolSize'] = 1
            morekwargs['symbolPen'] = self.workspace.theme.plot_color
            morekwargs['pen'] = '0000'
            self._pointsConnectedOnLastUpdate = False
        else:
            morekwargs['pen'] = self.workspace.theme.plot_color
            self._pointsConnectedOnLastUpdate = True

        OscillogramWidget.graph(self, indexFrom, indexTo, morekwargs)
