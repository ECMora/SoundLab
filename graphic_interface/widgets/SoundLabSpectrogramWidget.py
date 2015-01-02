from PyQt4 import QtCore
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.Spectrogram import Spectrogram
from duetto.widgets.SpectrogramWidget import SpectrogramWidget
from graphic_interface.Settings.Workspace import SpectrogramWorkspace

from graphic_interface.widgets.SoundLabWidget import SoundLabWidget
from signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool


class SoundLabSpectrogramWidget(SoundLabWidget, SpectrogramWidget):
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
        SpectrogramWidget.__init__(self)
        SoundLabWidget.__init__(self)

        # parche para capturar los eventos visuales del control
        # TODO averiguar por que razon no se envian los eventos correctamente al widget
        self.graphics_view.mouseMoveEvent = self.mouseMoveEvent
        self.graphics_view.mouseReleaseEvent = self.mouseReleaseEvent
        self.graphics_view.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.graphics_view.mousePressEvent = self.mousePressEvent
        self.changeTool(SpectrogramZoomTool)
        self.workspace = None
        self._load_workspace(SpectrogramWorkspace())

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

    def _load_theme(self, theme):
        update = False

        # set background color
        self.graphics_view.setBackground(theme.background_color)
        # set grid lines
        self.xAxis.setGrid(88 if theme.gridX else 0)
        self.yAxis.setGrid(88 if theme.gridY else 0)

        # set the state of the histogram and make it note the change so it automatically refreshes the spectrogram
        self.histogram.item.gradient.restoreState(theme.colorBarState)
        self.histogram.item.region.setRegion(theme.histRange)
        self.histogram.item.region.lineMoved()
        self.histogram.item.region.lineMoveFinished()

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
        noWorkspace = self.workspace is None

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
        update = update or self._load_theme(workspace.theme)

        # keep a copy of the workspace
        self.workspace = workspace.copy()

        # returns whether it's necessary to update the widget
        return update

    def load_workspace(self, workspace):
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
        if update:
            self.graph(rangeX[0], rangeX[1])

        # set the y axis' range (must be made after the spectrogram is computed)
        minY = self.specgramHandler.get_freq_index(workspace.minY)
        maxY = self.specgramHandler.get_freq_index(workspace.maxY)
        self.viewBox.setYRange(minY, maxY, padding=0)

    def graph(self, indexFrom=0, indexTo=-1):
        if indexTo < 0:
            indexTo += len(self.signal)
        if indexTo < indexFrom:
            indexTo = len(self.signal)
        self.specgramHandler.recomputeSpectrogram(indexFrom, indexTo,
                                                  self.viewBox.width() if self.workspace.FFTOverlap < 0 else None)

        # set the new spectrogram image computed
        self.imageItem.setImage(self.specgramHandler.matriz)
        self.viewBox.setRange(xRange=(self.specgramHandler.from_osc_to_spec(indexFrom),
                                      self.specgramHandler.from_osc_to_spec(indexTo-1)), padding=0)

        # update the histogram colors of the spectrogram
        self.histogram.item.region.lineMoved()
        self.histogram.item.region.lineMoveFinished()

    def from_osc_to_spec(self,coord):
        return self.specgramHandler.from_osc_to_spec(coord)

    def from_spec_to_osc(self,coord):
        return self.specgramHandler.from_spec_to_osc(coord)