# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from duetto.audio_signals.audio_signals_stream_readers.FileManager import FileManager
import pyqtgraph as pg
from PyQt4.QtCore import QTimer
from duetto.audio_signals.AudioSignalPlayer import AudioSignalPlayer
from duetto.audio_signals.Synthesizer import Synthesizer
from duetto.audio_signals.AudioSignal import AudioSignal
from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager
from duetto.signal_processing.EditionSignalProcessor import EditionSignalProcessor
from SoundLabOscilogramWidget import SoundLabOscilogramWidget
from SoundLabSpectrogramWidget import SoundLabSpectrogramWidget
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool as OscilogramZoomTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.PointerCursorTool import PointerCursorTool as OscilogramPointerTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.PointerCursorTool import PointerCursorTool as SpectrogramPointerTool
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.RectangularCursorTool import RectangularCursorTool as OscilogramRectangularCursorTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.RectangularCursorTool import RectangularCursorTool as SpectrogramRectangularCursorTool
from graphic_interface.widgets.undo_redo_actions.UndoRedoActions import *


class IntervalCursor:
    """
    """

    def __init__(self, minvalue=0, maxvalue=0):
        self.min = minvalue
        self.max = maxvalue


class QSignalVisualizerWidget(QWidget):
    """
    Widget to visualize a signal in time and frequency domain.
    Provides wrappers for useful signal processing methods.
    """
    # SIGNALS
    # Signal raised when a tool made a medition and has new data to show
    toolDataDetected = QtCore.pyqtSignal(str)

    #CONSTANTS
    #the inverse of the amount of the visible area of the signal that must be
    #visible after make a zooom IN
    ZOOM_STEP = 4

    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent)
        #the two widgets in which are delegated the functions of time and frequency domain
        #representation and visualization.
        self.axesOscilogram = SoundLabOscilogramWidget(**kwargs)
        self.axesSpecgram = SoundLabSpectrogramWidget(**kwargs)

        self.undoRedoManager = UndoRedoManager()
        self.undoRedoManager.actionExec.connect(lambda x: self.graph())

        #sincronization of the change range in the axes
        self.axesSpecgram.rangeChanged.connect(lambda x1, x2: self.axesOscilogram.changeRange(x1, x2))
        self.axesOscilogram.rangeChanged.connect(lambda x1, x2: self.axesSpecgram.changeRange(x1, x2))

        self.axesSpecgram.signalChanged.connect(lambda x1, x2: self.axesOscilogram.updateSignal(x1, x2))
        self.axesOscilogram.signalChanged.connect(lambda x1, x2: self.axesSpecgram.updateSignal(x1, x2))

        #connect the signals for tools data detected
        self.axesOscilogram.toolDataDetected.connect(lambda x: self.toolDataDetected.emit(x))
        self.axesSpecgram.toolDataDetected.connect(lambda x: self.toolDataDetected.emit(x))

        #link the x axis of each widget to visualize the same x grid and ticks
        self.axesSpecgram.xAxis.linkToView(self.axesOscilogram.getViewBox())

        #set the tool zoom as default
        self.setSelectedTool(Tools.ZoomTool)

        #grouping the oscilogram and spectrogram widgets in the control
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.axesOscilogram)
        layout.addWidget(self.axesSpecgram)
        self.setLayout(layout)

        #the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)

        #the zoom cursor
        self.zoomCursor = IntervalCursor(0, 0)

        #current signal to process and visualize
        self.signal = Synthesizer.generateSilence()

        #variables
        self._visibleOscillogram = True
        self._visibleSpectrogram = True
        self._playSpeed = 100

        #the internal variables to show the play line
        #in each widget.
        self.playerLineOsc = pg.InfiniteLine()
        self.playerLineSpec = pg.InfiniteLine()

        self._recordTimer = QTimer(self)
        self._recordTimer.timeout.connect(self.on_newDataRecorded)


    def setSelectedTool(self, tool):
        """
        Change the current selected tool of the widget.
        :param tool: the new tool to set.
        :return:
        """

        #switch for the concrete tools implementations
        if tool == Tools.ZoomTool:
            self.axesOscilogram.changeTool(OscilogramZoomTool)
            self.axesSpecgram.changeTool(SpectrogramZoomTool)

            #Set the connections for the zoom tool sincronization
            self.axesOscilogram.gui_user_tool.zoomRegion.sigRegionChanged.connect(self.updateSpecZoomRegion)
            self.axesSpecgram.gui_user_tool.zoomRegion.sigRegionChanged.connect(self.updateOscZoomRegion)

        elif tool == Tools.PointerTool:
            self.axesOscilogram.changeTool(OscilogramPointerTool)
            self.axesSpecgram.changeTool(SpectrogramPointerTool)

        elif tool == Tools.RectangularZoomTool:
            self.axesOscilogram.changeTool(OscilogramRectangularCursorTool)
            self.axesSpecgram.changeTool(SpectrogramRectangularCursorTool)

        # elif tool == Tools.RectangularEraser:
        #     self.axesSpecgram.changeTool(tool)
        #     self.axesOscilogram.changeTool(tool)
        #update the current selected tool
        self.selectedTool = tool

    def load_Theme(self, theme):
        """
        this method implements the  way in which the control loads the theme
        all the visual options are updated here.
        The method delegates in each control (oscillogram and spectrogram plot widgets)
        the implementation of its respective visual updates.
        """
        self.axesOscilogram.load_Theme(theme.oscillogramTheme)
        self.axesSpecgram.load_Theme(theme.spectrogramTheme)

    def signalName(self):
        """
        Returns the name of the current signal if it has one. A default name is returned
        otherwise.
        :return: string with the name or default name.
        """
        return "" if self.__signal is None else self.__signal.name

    def createContextCursor(self, actions):
        """
        method that add a number of actions to the control's context menu.
        :param actions: List of QAction
        """
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        for act in actions:
            if isinstance(act, QtGui.QAction):
                self.addAction(act)

    #region Zoom Tool Region Management
    #the tool Zoom make changes simultanously in both widgets
    #The sincronization of this tool is made by the update of the interval
    #selected by the tool in the spectrogram when the oscilogram change his interval
    #and viceversa. The methods that

    def updateSpecZoomRegion(self):
        """
        Method that update the zoom region of
        the spectrogram when a change is made
        in the oscilogram zoom tool region
        :return:
        """
        oscilogram_zoom_region = self.axesOscilogram.gui_user_tool.zoomRegion.getRegion()

        # translate the coordinates of the oscilogram zoom region into spectrogram's
        min = self._from_osc_to_spec(oscilogram_zoom_region[0])
        max = self._from_osc_to_spec(oscilogram_zoom_region[1])

        # update spectrogram region
        self.axesSpecgram.gui_user_tool.zoomRegion.setRegion([min, max])

    def updateOscZoomRegion(self):
        """
        Method that update the zoom region of
        the oscilogram when a change is made
        in the spectrogram zoom tool region
        :return:
        """
        spectrogram_zoom_region = self.axesSpecgram.gui_user_tool.zoomRegion.getRegion()

        #translate the coordinates of the spectrogram zoom region into oscilogram's
        min = self._from_spec_to_osc(spectrogram_zoom_region[0]) + self.mainCursor.min
        max = self._from_spec_to_osc(spectrogram_zoom_region[1]) + self.mainCursor.min

        #update oscilogram region
        self.axesOscilogram.gui_user_tool.zoomRegion.setRegion([min, max])

    #endregion

    #region Undo Redo
    def undo(self):
        """
        Undo the last signal processing action.
        :return:
        """
        self.undoRedoManager.undo()

    def redo(self):
        """
        Redo the last signal processing action.
        :return:
        """
        self.undoRedoManager.redo()
    #endregion

    #region Sound
    # manages the reproduction of the signal
    def play(self):
        """
        Start to play the current signal.
        If the signal is been playing nothing is made.
        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.addPlayerLine(start)
        self.signalPlayer.play(start, end, self.playSpeed)

    def switchPlayStatus(self):
        """
        Change the play status from PLAYING into PAUSE
        and vice versa.
        """
        if self.signalPlayer.playStatus == AudioSignalPlayer.PLAYING:
            self.pause()
        elif self.signalPlayer.playStatus == AudioSignalPlayer.PAUSED:
            self.play()

    def stop(self):

        prevStatus = self.signalPlayer.playStatus
        self.signalPlayer.stop()

        if  prevStatus == self.signalPlayer.RECORDING:
            self._recordTimer.stop()
            self.axesOscilogram.mouseZoomEnabled = True
            self.axesSpecgram.mouseZoomEnabled = True
            self.axesOscilogram.setVisible(True)
            self.axesSpecgram.setVisible(True)
            self.graph()
            self.zoomNone()

    def on_newDataRecorded(self):

        self.signalPlayer.readFromStream()

        self.mainCursor.max = len(self.signal.data)
        self.mainCursor.min = max(0,
                                  len(self.signal.data) - 3 * self.signal.samplingRate)

        self.axesOscilogram.graph(self.mainCursor.min, self.mainCursor.max)

        #self.regionChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signal.data))

    def record(self):

        self.axesOscilogram.mouseZoomEnabled = False
        self.axesSpecgram.mouseZoomEnabled = False
        self.axesOscilogram.setVisible(True)
        self.axesSpecgram.setVisible(False)
        try:
            self.signalPlayer.record()
        except:
             self.stop()
        self.__signal = self.signalPlayer.signal
        self.axesOscilogram.signal = self.signalPlayer.signal
        self.axesSpecgram.signal = self.signalPlayer.signal
        updateTime = 15
        self._recordTimer.start(updateTime)
        #self.createPlayerLine(self.mainCursor.min)

    def pause(self):
        """
        Pause the reproduction of the current signal.
        If the signal is paused nothing is made.
        :return:
        """
        self.signalPlayer.pause()

    def addPlayerLine(self, initial_value):
        """
        create the line to show on widgets osc and spec
        when the signal is been played as a way to
        know what section of the signal is been listened.
        The line (two lines, one for each widget)
        is added into every widget and updated
        it's value while the sound is played.
        :param initial_value: the initial value of the line in signal data indexes. (osc coordinates)
        the initial value of where the play start.
        :return:
        """
        if not isinstance(initial_value, int):
            raise Exception("value can't be of type different of int")

        #set the values of the lines for every widget
        self.playerLineOsc.setValue(initial_value)
        self.playerLineSpec.setValue(self._from_osc_to_spec(initial_value))

        #add the lines to the widgets if there aren't
        if self.playerLineOsc not in self.axesOscilogram.getViewBox().addedItems:
            self.axesOscilogram.getViewBox().addItem(self.playerLineOsc)
        if self.playerLineSpec not in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.addItem(self.playerLineSpec)

    def removePlayerLine(self):
        """
        Remove the player lines of the widgets
        is used when the lines shouldn't be visible because the play has ended.
        :return:
        """
        if self.playerLineOsc in self.axesOscilogram.getViewBox().addedItems:
            self.axesOscilogram.getViewBox().removeItem(self.playerLineOsc)
        if self.playerLineSpec in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.removeItem(self.playerLineSpec)

    def notifyPlayingCursor(self, frame):
        #draw the line in the axes
        self.playerLineOsc.setValue(frame)
        self.playerLineSpec.setValue(self._from_osc_to_spec(frame))

    #endregion

    #region Property oscilogram and specgram Visibility
    #update the visualization of the widget to show
    #oscilogram graph, specgram graph or both through the visibility variables
    @property
    def visibleOscilogram(self):
        return self._visibleOscillogram

    @visibleOscilogram.setter
    def visibleOscilogram(self, value):
        self._visibleOscillogram = value
        self.axesOscilogram.setVisible(value)

    @property
    def visibleSpectrogram(self):
        return self._visibleSpectrogram

    @visibleSpectrogram.setter
    def visibleSpectrogram(self, value):
        self._visibleSpectrogram = value
        self.axesSpecgram.setVisible(value)

    @property
    def playSpeed(self):
        return self._playSpeed

    @playSpeed.setter
    def playSpeed(self, value):
        if value <= 0:
            raise Exception("The play speed must be positive.")
        self._playSpeed = value

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, new_signal):
        """
        Modify and update the internal variables that uses the signal.

        :param new_signal: the new AudioSignal
        :raise Exception: If signal is not of type AudioSignal
        """
        if new_signal is None or not isinstance(new_signal, AudioSignal):
            raise Exception("Invalid assignation value. Must be of type AudioSignal")

        self.__signal = new_signal
        #update the main cursor to visualize and process a piece of the signal
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.__signal)

        #update the signal on every widget
        self.axesOscilogram.signal = new_signal
        self.axesSpecgram.signal = new_signal

        #update the variables that manage the signal
        #   the audio signal handler to play options
        self.signalPlayer = AudioSignalPlayer(self.__signal)
        self.signalPlayer.playing.connect(self.notifyPlayingCursor)

        #the edition object that manages cut and paste options
        self.editionSignalProcessor = EditionSignalProcessor(self.__signal)
        self.commonSignalProcessor = CommonSignalProcessor(self.__signal)

        #update the signal int the two widgets that visualize it
        self.axesOscilogram.signal = self.__signal
        self.axesSpecgram.signal = self.__signal

    #endregion

    #region Zoom in,out, none
    def zoomIn(self):
        """
        Make a zoom in to the current visualized region of the signal.
        Change the visualized interval of the signal to a subinterval of the current.
        The new subinterval has the middle index equal to the old one. 
        :return:
        """
        interval_size_removed = (self.mainCursor.max - self.mainCursor.min) / self.ZOOM_STEP

        #update the new visible interval
        if self.mainCursor.max - interval_size_removed > self.mainCursor.min + interval_size_removed:
            self.mainCursor.max -= interval_size_removed
            self.mainCursor.min += interval_size_removed

        self.graph()

    def zoomOut(self):
        """
        Make a zoom out to the current visualized region of the signal.
        Change the visualized interval of the signal to a bigger interval than the current.
        The new subinterval has the middle index equal to the old one.
        :return:
        """
        interval_size_added = self.mainCursor.max - self.mainCursor.min / self.ZOOM_STEP

        #update the max interval limit
        if (self.mainCursor.max + interval_size_added) < len(self.signal):
            self.mainCursor.max += interval_size_added
        else:
            self.mainCursor.max = len(self.signal)

        # update the min interval limit
        if self.mainCursor.min - interval_size_added >= 0:
            self.mainCursor.min -= interval_size_added
        else:
            self.mainCursor.min = 0

        self.graph()

    def zoomNone(self):
        """
        Set the current visible region of the signal to its limits.
        Set to visible the complete signal.
        """
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signal)
        self.graph()

    #endregion

    #region GRAPH
    def graph(self):
        #update the two widgets visualizations
        self.axesSpecgram.graph(indexFrom=self.mainCursor.min, indexTo=self.mainCursor.max)
        self.axesOscilogram.graph(indexFrom=self.mainCursor.min, indexTo=self.mainCursor.max)

    #endregion

    #region Edition CUT,COPY PASTE

    def cut(self):
        """
        Cut the current selected section of the signal for later paste
        in this or another instance of the sound lab.
        If the zoom cursor is active then the its selection is taked.
        else the whole inteval of current visualization is used.
        """
        #get the current signal selection interval
        start, end = self.getIndexFromAndTo()
        self.editionSignalProcessor.cut(start,end)

        #connect the action of cut for update
        #the signal and visualization in the undo and redo
        action = CutAction(self.signal, start, end)
        action.signal_size_changed.connect(self._updateSignal)

        self.undoRedoManager.add(action)
        self._updateSignal(self.editionSignalProcessor.signal)

    def _updateSignal(self,new_signal):
        """
        Update the signal property and the visualization in the widgets.
        Used when a changing size undo redo action is produced.
        :param new_signal: The new signal to visualize
        """
        self.signal = new_signal
        self.graph()

    def copy(self):
        """
        Copy the current selected section of the signal for later paste
        in this or another instance of the sound lab.
        If the zoom cursor is active then the its selection is taked.
        else the whole inteval of current visualization is used.
        """
        # get the current signal selection interval
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(CopyAction(self.signal, start, end))
        self.editionSignalProcessor.copy(start,end)

    def paste(self):
        """
        Paste the previously copied or cutted section
        of a signal stored in clipboard.
        """
        # get the current signal selection interval
        start, end = self.getIndexFromAndTo()

        self.editionSignalProcessor.paste(start)

        # connect the action of paste for update
        # the signal and visualization in the undo and redo
        # because the paste action do not change the signal reference but the size
        action = PasteAction(self.signal, start, end)
        action.signal_size_changed.connect(self._updateSignal)

        self.undoRedoManager.add(action)
        self.graph()

    #endregion

    #region Signal Processing Actions

    def reverse(self):
        """

        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(ReverseAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.reverse)

    def insertWhiteNoise(self, ms=1):
        raise NotImplementedError()

    def insertPinkNoise(self, ms, type, Fc, Fl, Fu):
        raise NotImplementedError()

    def resampling(self, samplingRate):
        self.undoRedoManager.add(ResamplingAction(self.signal, samplingRate))
        self.__signal.resampling(samplingRate)
        self.zoomNone()

    def getIndexFromAndTo(self):
        """
        Returns the interval of the signal that its
        currently analyzed.
        :return: tuple x,y with the start and end of the interval in
                signal array data  indexes.
                If zoom tool is active returns the selection made by the tool.
                the current visualization borders are returned otherwise.
        """
        #get the current visible interval indexes
        indexFrom, indexTo = self.mainCursor.min, self.mainCursor.max

        #if selected tool is Zoom get the selection interval indexes
        axe = self.axesOscilogram if self.visibleOscilogram \
                                  else self.axesSpecgram if self.visibleSpectrogram \
                                  else None

        if self.selectedTool == Tools.ZoomTool and axe is not None:
            zoom_region = axe.gui_user_tool.zoomRegion.getRegion()
            #get the start of the region
            indexFrom = zoom_region[0]

            #set the max limit if the region borders are different
            if zoom_region[1] > zoom_region[0]:
                 indexTo = zoom_region[1]

        return indexFrom, indexTo

    def signalProcessingAction(self, delegate, *args):
        """
        Method that handles the signal processing actions.
        Execute the supplied signal processing method and refresh the widget.
        :param delegate: signal processing action
        :param args: delegate arguments
        :return:
        """
        indexFrom, indexTo = self.getIndexFromAndTo()
        delegate(indexFrom, indexTo, *args)
        self.graph()

    def insertSilence(self, ms=0):
        """
        Insert a silence signal of ms duration in milliseconds.
        If the zoom tool is selected and there is a selection made
        the silence signal would be inserted ni the start of the selection
        otherwise would be inserted at the start of the current
        visualization interval
        :param ms: time in milliseconds of the silence signal to insert
        :return:
        """
        start, end = self.getIndexFromAndTo()

        #add the undo redo action
        self.undoRedoManager.add(
                InsertSilenceAction(self.signal, start, end, ms))

        #generate the silence signal and insert into the signal
        silence_signal = Synthesizer.generateSilence()
        self.signal.insert(silence_signal, start)

    def modulate(self,function="normalize", fade="IN"):
        """

        :param function:
        :param fade:
        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(
                ModulateAction(self.signal, start, end, function, fade))
        self.signalProcessingAction(self.commonSignalProcessor.modulate, function, fade)

    def normalize(self,factor):
        """

        :param factor:
        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(
            NormalizeAction(self.signal, start, end, factor))
        self.signalProcessingAction(self.commonSignalProcessor.normalize, factor)

    def scale(self, factor):
        """

        :param factor:
        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(
            ScaleAction(self.signal, start, end, factor))
        self.signalProcessingAction(self.commonSignalProcessor.scale, factor)

    def silence(self):
        """

        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(SilenceAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.setSilence)

    def filter(self, FCut=0, FLow=0, FUpper=0):
        # self.signalProcessingAction(self.signal.filter, FCut, FLow, FUpper)
        raise NotImplementedError()

    def absoluteValue(self,sign):
        """

        :param sign:
        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(Absolute_ValuesAction(self.signal, start, end,sign))
        self.signalProcessingAction(self.commonSignalProcessor.absoluteValue,sign)

    def changeSign(self):
        """

        :return:
        """
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.add(ChangeSignAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.changeSign)

    #endregion

    #region Open And Save

    def open(self, filename):
        if not filename:
            raise Exception("Invalid filename")

        signal = FileManager().read(filename)
        try:

            #update signal
            self.signal = signal
            self.graph()
        except Exception as ex:
            raise ex

    def save(self, fname):
        """
        Save the current signal into disc.
        :param fname: The path to the file.
        """
        FileManager().write(self.__signal, fname)

    def saveSelectedSectionAsSignal(self, fname):
        """
        Save the signal that is currently selected as a new one
        :param fname: path to save the signal
        """
        #get the interval limits
        indexF, indexTo = self.getIndexFromAndTo()

        signal = self.signal.copy(indexF, indexTo)

        self.__saveSignal(fname, signal)

    #endregion

    def _from_spec_to_osc(self, coord):
        cs = self.axesSpecgram.specgramHandler.NFFT #- self.specgramSettings.visualOverlap
        return int(1.0 * coord * cs - self.axesSpecgram.specgramHandler.NFFT / 2)

    def _from_osc_to_spec(self, coord):
        cs = self.axesSpecgram.specgramHandler.NFFT #- self.axesSpecgram.specgramHandler.visualOverlap
        return 1.0 * (coord - self.mainCursor.min + self.axesSpecgram.specgramHandler.NFFT / 2) / cs
