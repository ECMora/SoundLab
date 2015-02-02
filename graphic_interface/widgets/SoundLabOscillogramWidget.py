from PyQt4 import QtCore
from duetto.widgets.OscillogramWidget import OscillogramWidget
from graphic_interface.Settings.Workspace import OscillogramWorkspace
from graphic_interface.widgets.SoundLabWidget import SoundLabWidget
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool


class SoundLabOscillogramWidget(SoundLabWidget, OscillogramWidget):
    """

    """

    # region SIGNALS
    # Signal raised when a tool wants to made a change on the range of visualization
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

    # endregion

    # CONSTANTS
    # the opacity if the grid lines on x and y axis
    GRID_LINE_OPACITY = 150

    def __init__(self):
        OscillogramWidget.__init__(self)
        SoundLabWidget.__init__(self)
        self.changeTool(ZoomTool)

        self.workspace = OscillogramWorkspace()
        self._pointsConnectedOnLastUpdate = False

    # region Tools interaction Implementation
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
    # endregion

    # region Workspace

    def load_workspace(self, workspace, forceUpdate=False):
        """
        Loads a workspace and updates the view according with it.
        :param workspace: an instance of OscillogramWorkspace, the part of the Workspace concerning the oscillogram
        """
        # set the y axis' range
        if self.workspace.maxY != workspace.maxY or \
           self.workspace.minY != workspace.minY:

            minY = -workspace.minY * self.signal.minimumValue / 100.0
            maxY = workspace.maxY * self.signal.maximumValue / 100.0

            self.setRange(yRange=(minY, maxY), padding=0, update=True)
            self.yAxis.setRange(minY, maxY)


        # set background color
        if self.workspace.theme.background_color != workspace.theme.background_color:
            self.setBackground(workspace.theme.background_color)

        # set grid lines
        if self.workspace.theme.gridX != workspace.theme.gridX:
            self.xAxis.setGrid(self.GRID_LINE_OPACITY if workspace.theme.gridX else 0)

        if self.workspace.theme.gridY != workspace.theme.gridY:
            self.yAxis.setGrid(self.GRID_LINE_OPACITY if workspace.theme.gridY else 0)

        # set the color of the plot lines; the lines will be redrawn later if the color changed
        if self.plotLine:
            if self._pointsConnectedOnLastUpdate:
                self.plotLine.setPen(workspace.theme.plot_color)
            else:
                self.plotLine.setSymbolPen(workspace.theme.plot_color)

        # update the widget if needed
        update = forceUpdate or self.workspace.theme.connectPoints != workspace.theme.connectPoints

        # keep a copy of the workspace
        self.workspace = workspace.copy()

        if update:
            rangeX = self.getPlotItem().getViewBox().viewRange()[0]
            self.graph(rangeX[0], rangeX[1])

    # endregion

    def graph(self, indexFrom=0, indexTo=-1, morekwargs=None):
        morekwargs = dict()
        points = indexTo - indexFrom if indexTo - indexFrom > 0 else self.signal.length

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

        # parent graph clears the widget so the tool must be set to enable again
        if self.gui_user_tool is not None:
            self.gui_user_tool.enable()

