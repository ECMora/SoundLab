from PyQt4 import QtCore
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.Spectrogram import Spectrogram
from graphic_interface.Settings.Workspace import SpectrogramWorkspace
import numpy
from duetto.widgets.SpectrogramWidget import SpectrogramWidget
from graphic_interface.widgets.SoundLabWidget import SoundLabWidget
from signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool


class SoundLabSpectrogramWidget(SoundLabWidget, SpectrogramWidget):

    # region SIGNALS
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

    # endregion

    # region CONSTANTS

    # Value of the axis lines opacity
    AXIS_LINES_OPACITY = 255

    # endregion

    def __init__(self):
        SpectrogramWidget.__init__(self)
        SoundLabWidget.__init__(self)

        # parche para capturar los eventos visuales del control
        # TODO averiguar por que razon no se envian los eventos correctamente al widget
        self.graphics_view.mouseMoveEvent = self.mouseMoveEvent
        self.graphics_view.mouseReleaseEvent = self.mouseReleaseEvent
        self.graphics_view.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.graphics_view.mousePressEvent = self.mousePressEvent
        self.graphics_view.leaveEvent = self.leaveEvent
        self.graphics_view.enterEvent = self.enterEvent

        self.changeTool(SpectrogramZoomTool)

        self.workspace = None
        self._load_workspace(SpectrogramWorkspace())

        self.minY = 0
        self.maxY = 256

    def changeTool(self, new_tool_class):
        SoundLabWidget.changeTool(self,new_tool_class)
        if self.gui_user_tool is not None:
            self.gui_user_tool.rangeChanged.connect(self.changeRangeSignal)
            self.gui_user_tool.signalChanged.connect(self.updateSignalManager)

    def updateSignal(self, x1, x2):
        """
        Update the visible data of the signal.
        :param x1:
        :param x2:
        """
        self.graph(x1, x2)

    def updateSignalManager(self, x1, x2):
        self.updateSignal(x1, x2)
        self.signalChanged.emit(x1, x2)

    def changeRange(self, x1, x2, y1=0, y2=0):
        self.graph(x1, x2)

    def changeRangeSignal(self, x1, x2, y1, y2):
        self.changeRange(x1, x2, y1, y2)
        self.rangeChanged.emit(x1, x2)

    # region Theme and Workspace
    # TODO Improve and refactor the theme code. must keep simplicity and minimality
    def _load_theme(self, theme, keepCopy=True):
        update = False

        noTheme = self.workspace is None or (not hasattr(self.workspace, 'theme')) or self.workspace.theme is None






        # set background color
        if noTheme or self.workspace.theme.background_color != theme.background_color:
            self.graphics_view.setBackground(theme.background_color)

        # set grid lines
        if noTheme or self.workspace.theme.gridX != theme.gridX:
            self.xAxis.setGrid(88 if theme.gridX else 0)
        if noTheme or self.workspace.theme.gridY != theme.gridY:
            self.yAxis.setGrid(88 if theme.gridY else 0)

        # set the state of the histogram and make it note the change so it automatically refreshes the spectrogram
        refrHist = False
        if noTheme or self.workspace.theme.colorBarState != theme.colorBarState:
            self.histogram.item.gradient.restoreState(theme.colorBarState)
            refrHist = True
        if noTheme or self.workspace.theme.histRange != theme.histRange:
            self.histogram.item.region.setRegion(theme.histRange)
            refrHist = True
        if refrHist:
            self.histogram.item.region.lineMoved()
            self.histogram.item.region.lineMoveFinished()

        if keepCopy:
            if self.workspace is None:
                self.workspace = SpectrogramWorkspace()
            self.workspace.theme = theme.copy()

        # returns whether it's necessary to update the widget
        return update

    def load_Theme(self, theme):
        """
        Loads a theme and updates the view according with it.
        :param theme: an instance of SpectrogramTheme, the part of the WorkTheme concerning the spectrogram.
        """
        # load the theme and determine if it's necessary to update the widget
        update = self._load_theme(theme)

        # update the widget if needed
        if update:
            rangeX = self.viewBox.viewRange()[0]
            rangeX = self.specgramHandler.from_spec_to_osc(rangeX[0]), self.specgramHandler.from_spec_to_osc(rangeX[1])
            self.graph(rangeX[0], rangeX[1])

    def _load_workspace(self, workspace):
        update = False
        noWorkspace = not hasattr(self, 'workspace') or self.workspace is None

        # set the FFT size (must also reset the overlap)
        if noWorkspace or self.workspace.FFTSize != workspace.FFTSize:
            self.specgramHandler.NFFT = workspace.FFTSize
            update = True

        # set the FFT window
        if noWorkspace or self.workspace.FFTWindow != workspace.FFTWindow:
            self.specgramHandler.window = workspace.FFTWindow
            update = True

        # set the FFT overlap (it must be set if the overlap or the FFT size are changed)
        if noWorkspace or self.workspace.FFTOverlap != workspace.FFTOverlap or self.workspace.FFTSize != workspace.FFTSize:
            if workspace.FFTOverlap >= 0:
                self.specgramHandler.set_overlap_ratio(workspace.FFTOverlap)
            else:
                self.specgramHandler.overlap = workspace.FFTSize - 1
            update = True

        # load the theme
        update = self._load_theme(workspace.theme, keepCopy=False) or update

        # keep a copy of the workspace
        self.workspace = workspace.copy()

        # returns whether it's necessary to update the widget
        return update

    def load_workspace(self, workspace, forceUpdate=False):
        """
        Loads a workspace and updates the view according with it.
        :param workspace: an instance of SpectrogramWorkspace, the part of the Workspace concerning the spectrogram
        """
        # get the current visualizing range (X axis)
        rangeX = self.viewBox.viewRange()[0]
        rangeX = self.specgramHandler.from_spec_to_osc(rangeX[0]), self.specgramHandler.from_spec_to_osc(rangeX[1])

        # load the workspace and determine if it's necessary to update the widget
        update = self._load_workspace(workspace)

        # update the widget if needed (showing the same X axis' range as before)
        if update or forceUpdate:
            self.graph(rangeX[0], rangeX[1])


        # set the y axis' range (must be made after the spectrogram is computed)
        minY = self.specgramHandler.get_freq_index(workspace.minY)
        maxY = self.specgramHandler.get_freq_index(workspace.maxY)
        self.viewBox.setYRange(minY, maxY, padding=0, update=True)
        # I had to do the following to make the spectrogram update right after changing minY or maxY
        self.histogram.item.region.lineMoved()
        self.histogram.item.region.lineMoveFinished()

    # endregion

    def graph(self, indexFrom=0, indexTo=-1):

        indexTo = indexTo if (indexTo >= 0 and indexTo > indexFrom) else self.signal.length

        SpectrogramWidget.graph(self, indexFrom, indexTo)

    def from_osc_to_spec(self, coord):
        return self.specgramHandler.from_osc_to_spec(coord)

    def from_spec_to_osc(self, coord):
        return self.specgramHandler.from_spec_to_osc(coord)