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
    # the opacity if the grid lines on x and y axis
    GRID_LINE_OPACITY = 150

    # endregion

    def __init__(self):
        SpectrogramWidget.__init__(self)
        SoundLabWidget.__init__(self)

        # region parche para capturar los eventos visuales del control
        # TODO averiguar por que razon no se envian los eventos correctamente al widget
        self.graphics_view.mouseMoveEvent = self.mouseMoveEvent
        self.graphics_view.mouseReleaseEvent = self.mouseReleaseEvent
        self.graphics_view.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.graphics_view.mousePressEvent = self.mousePressEvent
        self.graphics_view.leaveEvent = self.leaveEvent
        self.graphics_view.enterEvent = self.enterEvent
        # endregion

        self.changeTool(SpectrogramZoomTool)

        # the object to compute spectrogram on record mode
        self.recordModeSpectrogram = Spectrogram(NFFT=256, overlap=0)
        self.activeRecordMode = False

        self.workspace = SpectrogramWorkspace()

    # region Tools interaction Implementation

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
    # endregion

    def setRecordMode(self, record_mode_active=True):
        """
        Set the widget prepared for the record process.
        Set default high speed increase values for the spectrogram calculation
        :param record_mode_active: The state of the record mode
        :return:
        """
        if record_mode_active != self.activeRecordMode:
            # if start record mode get the signal
            if not self.activeRecordMode:
                self.recordModeSpectrogram.signal = self.specgramHandler.signal

            spectrogram_handler = self.specgramHandler
            self.specgramHandler = self.recordModeSpectrogram
            self.recordModeSpectrogram = spectrogram_handler

            self.activeRecordMode = not self.activeRecordMode

    # region Theme and Workspace

    def load_theme(self, theme):
        """
        Load the visual components of the workspace
        :param theme:
        :return:
        """
        update = False

        # set background color
        if self.workspace.theme.background_color != theme.background_color:
            self.graphics_view.setBackground(theme.background_color)

        # set grid lines
        if self.workspace.theme.gridX != theme.gridX:
            self.xAxis.setGrid(self.GRID_LINE_OPACITY if theme.gridX else 0)

        if self.workspace.theme.gridY != theme.gridY:
            self.yAxis.setGrid(self.GRID_LINE_OPACITY if theme.gridY else 0)

        # set the state of the histogram and make it note
        # the change so it automatically refreshes the spectrogram
        refrHist = False

        if self.workspace.theme.colorBarState != theme.colorBarState:
            self.histogram.gradient.restoreState(theme.colorBarState)
            refrHist = True
        if self.workspace.theme.histRange != theme.histRange:
            self.histogram.region.setRegion(theme.histRange)
            refrHist = True

        if refrHist:
            self.histogram.region.lineMoved()
            self.histogram.region.lineMoveFinished()

        # returns whether it's necessary to update the widget
        return update

    def load_workspace(self, workspace, forceUpdate=False):
        """
        Loads a workspace and updates the view according with it.
        :param workspace: an instance of SpectrogramWorkspace,
        the part of the Workspace concerning the spectrogram
        """
        # get the current visualizing range (X axis)
        rangeX = self.viewBox.viewRange()[0]
        rangeX = self.specgramHandler.from_spec_to_osc(rangeX[0]), \
                 self.specgramHandler.from_spec_to_osc(rangeX[1])

        # load the workspace and determine if it's necessary to update the widget
        update = False

        # update FFT Size, Window and overlap
        if not self.activeRecordMode:
            # set the FFT size (must also reset the overlap)
            if self.workspace.FFTSize != workspace.FFTSize:
                self.specgramHandler.NFFT = workspace.FFTSize
                update = True

            # set the FFT window
            if self.workspace.FFTWindow != workspace.FFTWindow:
                self.specgramHandler.window = workspace.FFTWindow
                update = True

            # set the FFT overlap (it must be set if the overlap or the FFT size are changed)
            if self.workspace.FFTOverlap != workspace.FFTOverlap or self.workspace.FFTSize != workspace.FFTSize:
                if workspace.FFTOverlap >= 0:
                    self.specgramHandler.set_overlap_ratio(workspace.FFTOverlap)
                else:
                    self.specgramHandler.overlap = workspace.FFTSize - 1

                update = True

        # load the theme
        update = self.load_theme(workspace.theme) or update

        # get a copy of the workspace
        self.workspace = workspace.copy()

        if self.workspace.maxY < 0 or self.workspace.maxY > self.signal.samplingRate / 2.0:
            self.workspace.maxY = self.signal.samplingRate / 2.0

        self.workspace.minY = min(self.workspace.minY, self.signal.samplingRate / 2.0)

        # update the widget if needed (showing the same X axis' range as before)
        if update or forceUpdate:
            self.graph(rangeX[0], rangeX[1])

        # set the y axis' range
        # !!!!!(MUST BE MADE AFTER THE SPECTROGRAM IS COMPUTED BECAUSE THE SPEC MATRIX CHANGE)!!!!!
        minY_index = self.specgramHandler.get_freq_index(self.workspace.minY)
        maxY_index = self.specgramHandler.get_freq_index(self.workspace.maxY)

        minY = 0 if minY_index == -1 else minY_index
        maxY = 0 if maxY_index == -1 else maxY_index
        self.viewBox.setYRange(minY, maxY, padding=0, update=True)
        self.yAxis.setRange(minY, maxY)


    # endregion

    def graph(self, indexFrom=0, indexTo=-1):

        indexTo = indexTo if (indexTo >= 0 and indexTo > indexFrom) else self.signal.length

        SpectrogramWidget.graph(self, indexFrom, indexTo)


    def from_osc_to_spec(self, coord):
        return self.specgramHandler.from_osc_to_spec(coord)

    def from_spec_to_osc(self, coord):
        return self.specgramHandler.from_spec_to_osc(coord)