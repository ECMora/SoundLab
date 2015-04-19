# -*- coding: utf-8 -*-
import os
import pyqtgraph as pg
from PyQt4 import QtGui
from duetto.audio_signals import openSignal
from PyQt4.QtCore import QTimer, Qt
from duetto.audio_signals.AudioSignal import AudioSignal
from duetto.audio_signals.AudioSignalPlayer import AudioSignalPlayer
from duetto.audio_signals.audio_signals_stream_readers.FileManager import FileManager
from SoundLabOscillogramWidget import SoundLabOscillogramWidget
from SoundLabSpectrogramWidget import SoundLabSpectrogramWidget
from duetto.signal_processing.filter_signal_processors.FilterSignalProcessor import FilterSignalProcessor
from graphic_interface.widgets.signal_visualizer_tools import *
from graphic_interface.widgets.undo_redo_actions.UndoRedoActions import *


class IntervalCursor:
    def __init__(self, minvalue=0, maxvalue=0):
        self.min = minvalue
        self.max = maxvalue


class QSignalVisualizerWidget(QtGui.QWidget):
    """
    Widget to visualize a signal in time and frequency domain.
    Provides wrappers for useful signal processing methods.
    """

    #  region SIGNALS
    #  Signal raised when a tool made a measurement and has new data to show
    toolDataDetected = QtCore.pyqtSignal(str)

    # signal raised when there is a signal interval selected (commonly by zoom tool)
    # raise the limits of the interval in signal data array coordinates
    signalIntervalSelected = QtCore.pyqtSignal(int, int)

    # signal raised when the name of the signal is changed by code
    # raise the new name
    signalNameChanged = pyqtSignal(str)

    # endregion

    # region CONSTANTS

    # The inverse of the amount of the visible area of the signal that must be
    # visible after make a zoom IN
    ZOOM_STEP = 4

    # The step of move for the scroll bar. Each scroll bar step when moved is equal
    # to the length of the signal divided by SCROLL_BAR_STEP
    SCROLL_BAR_STEP = 10

    # endregion

    # region Initialize

    def __init__(self, parent=None, signal=None, **kwargs):
        QtGui.QWidget.__init__(self, parent)

        #  !!! THE ORDER OF VARIABLES INITIALIZATION IS RELEVANT !!!
        #  the two widgets in which are delegated the functions of time and
        #  frequency domain representation and visualization.
        self.axesOscilogram = SoundLabOscillogramWidget(**kwargs)
        self.axesSpecgram = SoundLabSpectrogramWidget(**kwargs)
        self.scrollBar = QtGui.QScrollBar(Qt.Horizontal, parent=self)

        #  the internal variables to show the play line
        #  in each widget.
        self.signalPlayer = None
        self._playSpeed = 100
        self.playerLineOsc = pg.InfiniteLine()
        self.playerLineSpec = pg.InfiniteLine()

        # the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)

        self.undoRedoManager = UndoRedoManager()
        self.undoRedoManager.actionExec.connect(lambda x: self.graph())

        # set the tool zoom as default
        self.__selectedTool = Tools.NoTool

        #  synchronization of the change range in the axes
        self.axesSpecgram.rangeChanged.connect(lambda x1, x2: self.update_widget_range(self.axesOscilogram, x1, x2))
        self.axesOscilogram.rangeChanged.connect(lambda x1, x2: self.update_widget_range(self.axesSpecgram, x1, x2))

        self.axesSpecgram.signalChanged.connect(lambda x1, x2: self.axesOscilogram.updateSignal(x1, x2))
        self.axesOscilogram.signalChanged.connect(lambda x1, x2: self.axesSpecgram.updateSignal(x1, x2))

        # variable to avoid multiple recursion calls to update limits of spec and osc widgets
        self.zoom_update_in_progress = False

        #  connect the signals for tools data detected
        self.axesOscilogram.toolDataDetected.connect(lambda x: self.toolDataDetected.emit(x))
        self.axesSpecgram.toolDataDetected.connect(lambda x: self.toolDataDetected.emit(x))

        #  link the x axis of each widget to visualize the same x grid and ticks
        self.axesSpecgram.xAxis.linkToView(self.axesOscilogram.getViewBox())

        # creating the scrollbar
        self.horizontalScrollBar = QtGui.QScrollBar()
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.valueChanged.connect(self.scrollBarRangeChanged)

        self.editionSignalProcessor = None
        self.commonSignalProcessor = None

        # current signal to initialize
        self._signal = None
        self.signal = signal if signal is not None else Synthesizer.generateSilence(duration=1)

        self.setSelectedTool(Tools.ZoomTool)

        self.configure_widget_layout()

        #  variables for visualization
        self._visibleOscillogram = True
        self._visibleSpectrogram = True

        self._recordTimer = QTimer(self)
        self._recordTimer.timeout.connect(self.on_newDataRecorded)

        # signal file path to save and read the signals from files.
        # None if signal was not loaded from file
        self.__signalFilePath = None

        self.graph()

    def configure_widget_layout(self):
        """
        Set some initial state configurations of the widget layout
        :return:
        """
        #  grouping the oscilogram and spectrogram widgets in the control
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.axesOscilogram)
        layout.addWidget(self.axesSpecgram)
        layout.addWidget(self.horizontalScrollBar)

        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        layout.setStretch(2, 1)
        self.setLayout(layout)

    # endregion

    # region Scroll Bar

    def scrollBarRangeChanged(self, start):
        """
        Invoked when the scrollbar is moved
        param start: the start of the range
        """
        self.mainCursor.min = start
        self.mainCursor.max = start + self.horizontalScrollBar.pageStep()
        self.graph()

    def updateScrollbar(self):
        """
        This method updates the values of the scrollbar
        """
        self.horizontalScrollBar.blockSignals(True)

        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(self.signal.length - (self.mainCursor.max - self.mainCursor.min))
        self.horizontalScrollBar.setValue(self.mainCursor.min)
        self.horizontalScrollBar.setPageStep(self.mainCursor.max - self.mainCursor.min)
        self.horizontalScrollBar.setSingleStep((self.mainCursor.max - self.mainCursor.min) / self.SCROLL_BAR_STEP)

        # if zoom tool is selected update its limits here because
        # this is where all change range operations finish it's processing
        self.updateZoomRegionsLimits()

        self.horizontalScrollBar.blockSignals(False)

    # endregion

    # region Widgets synchronization

    def update_widget_range(self, widget, x1, x2):
        """
        Update the rancge of visibility of the oscilogram or spectrogram
        widgets.
        :param widget: The widget type to update. axesOscilogram or axesSpectrogram
        :param x1: the start limit of the new visible interval in signal data array indexes
        :param x2: the end limit of the new visible interval in signal data array indexes
        :return:
        """
        widget.changeRange(x1, x2)
        self.mainCursor.min, self.mainCursor.max = x1, x2
        self.updateScrollbar()

    # endregion

    #  region Zoom Tool Region Management
    #  the tool Zoom make changes simultanously in both widgets
    #  The synchronization of this tool is made by the update of the interval
    #  selected by the tool in the spectrogram when the oscilogram change his interval
    #  and vice versa.

    def updateZoomRegionsLimits(self):
        """
        Set the limits of the zoom regions if the zoom tool is selected
        :return:
        """
        if self.selectedTool != Tools.ZoomTool:
            return

        min_limit, max_limit = self.mainCursor.min, self.mainCursor.max
        # set the limits of the zoom regions to the length of the signal
        self.axesOscilogram.gui_user_tool.zoomRegion.setBounds((min_limit, max_limit))

        rgn = self.axesOscilogram.gui_user_tool.zoomRegion.getRegion()
        # if the zoom region is the complete interval of visualization
        # clear the zoom tool region
        if rgn == (min_limit, max_limit):
            self.axesOscilogram.gui_user_tool.zoomRegion.setRegion((min_limit, min_limit))

        # do not update the spectrogram cursors directly because the oscilogram
        # zoom region setBounds raise the signal of changed if have to and then
        # the spec zoom region would be updated by the connections made
        self.updateSpecZoomRegion()

    def updateSpecZoomRegion(self):
        """
        Method that update the zoom region of
        the spectrogram when a change is made
        in the oscilogram zoom tool region
        :return:
        """
        self.updateZoomRegion(True)

    def updateOscZoomRegion(self):
        """
        Method that update the zoom region of
        the oscilogram when a change is made
        in the spectrogram zoom tool region
        :return:
        """
        self.updateZoomRegion(False)

    def updateZoomRegion(self, oscilogram_update=True):
        """
        Update the region of zoom in the widget. After a zoom region change on one of the
        visualization graphs zoom regions (Oscilogram or Spectrogram). Update the other widget's zoom region
        :param oscilogram_update: if the update was made in the oscilogram zoom region
        :return:
        """
        # to avoid multiple recursive calls at this method because
        # the signal raised by the zoom region widgets of osc and spec widgets
        if self.zoom_update_in_progress:
            return

        # avoid multiples recursion calls when update the zoom regions in widgets
        self.zoom_update_in_progress = True

        oscilogram_zoom_region = self.axesOscilogram.gui_user_tool.zoomRegion.getRegion()
        spectrogram_zoom_region = self.axesSpecgram.gui_user_tool.zoomRegion.getRegion()

        #  the translation of spectrograms coords into oscilogram coords
        spec_region_coords_in_osc = self.from_spec_to_osc(spectrogram_zoom_region[0]),\
                                 self.from_spec_to_osc(spectrogram_zoom_region[1])

        #  rename for easy code
        osc_min_x, osc_max_x = oscilogram_zoom_region[0], oscilogram_zoom_region[1]

        #  rename for easy code
        spec_min_x, spec_max_x = spec_region_coords_in_osc[0], spec_region_coords_in_osc[1]

        min_x_spec = self.from_osc_to_spec(osc_max_x)
        max_x_spec = self.from_osc_to_spec(osc_min_x)

        if abs(osc_max_x - spec_max_x) > 1 or abs(osc_min_x - spec_min_x) > 1:
            if oscilogram_update and (min_x_spec != spec_min_x or max_x_spec != spec_max_x):
                self.axesSpecgram.gui_user_tool.zoomRegion.setRegion([min_x_spec, max_x_spec])
                self.signalIntervalSelected.emit(osc_min_x, osc_max_x)

            elif not oscilogram_update and (spec_min_x != osc_min_x or spec_max_x != osc_max_x):
                self.axesOscilogram.gui_user_tool.zoomRegion.setRegion([spec_min_x, spec_max_x])
                self.signalIntervalSelected.emit(spec_min_x, spec_max_x)

        self.zoom_update_in_progress = False

    #  endregion

    #  region Undo Redo

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

    # endregion

    # region Sound

    def change_volume(self, volume):
        """
        Change the volume of play for the signal.
        :param volume: int [0, 100] of the volume in %
        :return:
        """
        self.signalPlayer.volume = volume

    def setPlayLoopEnabled(self, enabled):
        """
        Define the play loop as enable or disabled
        :param enabled: boolean. True to enable play in loop false otherwise.
        :return:
        """
        self.signalPlayer.playLoop = enabled

    def play(self):
        """
        Start to play the current signal.
        If the signal is been playing nothing is made.
        :raise: UnavailableAudioDeviceException if play fails because the selected
        Audio Device is unavailable.
        """
        start, end = self.selectedRegion
        self.add_player_line(start, end)
        self.signalPlayer.play(start, end, self.playSpeed)

    def switchPlayStatus(self):
        """
        Change the play status from PLAYING into PAUSE
        and vice versa.
        """
        if self.signalPlayer.playStatus == AudioSignalPlayer.PLAYING or \
           self.signalPlayer.playStatus == AudioSignalPlayer.RECORDING:

            self.pause()

        elif self.signalPlayer.playStatus == AudioSignalPlayer.PAUSED or \
             self.signalPlayer.playStatus == AudioSignalPlayer.STOPPED:

            self.play()

    def stop(self):
        """
        Stops the reproduction or record of the current signal
        :return:
        """
        prevStatus = self.signalPlayer.playStatus

        # stopping the player
        self.signalPlayer.stop()
        self.remove_player_line()

        #  if the previous status was RECORDING then we have
        #  to stop the licence_checker_timer and draw the new signal on both controls.
        if prevStatus == self.signalPlayer.RECORDING:
            self.axesSpecgram.setRecordMode(False)

            self._recordTimer.stop()
            self.visibleOscilogram = True
            self.visibleSpectrogram = True
            self.zoomNone()

    def on_newDataRecorded(self):
        """
        This interval_function is called when on every tick count of the record timer
        to update the oscillogram with the new data recorded.
        """
        #  the player read from the record stream
        self.signalPlayer.readFromStream()

        # update the current view interval of the recording signal
        if self.signal.length > 0:

            self.mainCursor.max = self.signal.length
            # draw the last signal second
            self.mainCursor.min = max(0, self.signal.length - self.signal.samplingRate)
            self.graph()

    def record(self, newSignal=False):
        """
        Start to record a new signal.
        If the signal is been playing nothing is made.
        :raise: UnavailableAudioDeviceException if play fails because the selected
        Audio Device is unavailable.
        """
        if newSignal:
            self.signal = AudioSignal(self.signal.samplingRate, self.signal.bitDepth, self.signal.channelCount)

        #  Here we try to record. In case of any IO device exception
        #  stop recording immediately.
        try:
            self.axesSpecgram.setRecordMode(True)
            self.signalPlayer.record()
            # add a undo redo action to save the state of signal edited.
            # reserved to future use the implementation
            # of the redo action for return to the previous one before record
            action = RecordAction(self._signal)
            self.undoRedoManager.add(action)

        except Exception as ex:
            self.stop()
            self.signal = Synthesizer.generateSilence(samplingRate=self.signal.samplingRate,
                                                      bitDepth=self.signal.bitDepth, duration=1)
            self.graph()
            print(ex.message)
            raise ex

        #  update oscillogram time (ms) interval for drawing the recorded section
        updateTime = 15

        #  starting the update record licence_checker_timer
        self._recordTimer.start(updateTime)
        #  self.createPlayerLine(self.mainCursor.minThresholdLa  bel)

    def pause(self):
        """
        Pause the reproduction of the current signal.
        If the signal is paused nothing is made.
        """
        self.signalPlayer.pause()

    def add_player_line(self, initial_value, end_value):
        """
        create the line to show on widgets osc and spec when the signal is been played
        as a way to know what section of the signal is been listened.
        The line (two lines, one for each widget) is added into every widget
        and updated it's value while the sound is played.
        :param initial_value: the initial value of the line in signal data indexes.
        (osc coordinates) the initial value of where the play start.
        :return:
        """
        if not isinstance(initial_value, int):
            raise Exception("value can't be of type different of int")

        self.playerLineEnd = end_value
        #  set the values of the lines for every widget
        self.playerLineOsc.setValue(initial_value)
        self.playerLineSpec.setValue(self.from_osc_to_spec(initial_value))

        #  add the lines to the widgets if there aren't
        if self.playerLineOsc not in self.axesOscilogram.getViewBox().addedItems:
            self.axesOscilogram.getViewBox().addItem(self.playerLineOsc)

        if self.playerLineSpec not in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.addItem(self.playerLineSpec)

    def remove_player_line(self):
        """
        Remove the player lines of the widgets
        is used when the lines shouldn't be visible because the play has ended.
        :return:
        """
        if self.playerLineOsc in self.axesOscilogram.getViewBox().addedItems:
            self.axesOscilogram.getViewBox().removeItem(self.playerLineOsc)
        if self.playerLineSpec in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.removeItem(self.playerLineSpec)

    def update_playing_line(self, frame):
        """
        Updates the value of the player line
        with the latest play position.
        :param frame:
        :return:
        """
        # draw the line in the axes
        if frame < self.playerLineEnd:
            self.playerLineOsc.setValue(frame)
            self.playerLineSpec.setValue(self.from_osc_to_spec(frame))

    #  endregion

    #  region Properties

    @property
    def signalName(self):
        """
        Returns the name of the current signal if it has one.
        An empty string is returned if there is no signal.
        :return: string with the name or default name.
        """
        return "" if self._signal is None else self._signal.name

    @signalName.setter
    def signalName(self, name):
        if name != self._signal.name:
            action = SignalNameChangeAction(self._signal, name)
            action.signalNameChanged.connect(lambda name: self.signalNameChanged.emit(name))

            self.undoRedoManager.add(action)
            self._signal.name = name

    # region Audio Devices

    @property
    def audioOutputDevice(self):
        """
        :return: The selected output audio device to record signals
        """
        return self.signalPlayer.outputDevice

    @audioOutputDevice.setter
    def audioOutputDevice(self, value):
        """
        Set the new selected output audio device to record signals
        :param value: the new output audioDevice
        """
        self.signalPlayer.outputDevice = value

    @property
    def audioInputDevice(self):
        return self.signalPlayer.inputDevice

    @audioInputDevice.setter
    def audioInputDevice(self, value):
        self.signalPlayer.inputDevice = value
    # endregion

    @property
    def selectedTool(self):
        """
        The type (Enum) of the selected tool currently used on the widget
        :return:
        """
        return self.__selectedTool

    @property
    def signalFilePath(self):
        """
        Signal file path to save and read the signals from files.
        None if signal was not loaded from file
        :return:
        """
        return self.__signalFilePath

    @signalFilePath.setter
    def signalFilePath(self, value):
        """
        Set the signal file path to save and read the signals from files.
        :return:
        """
        self.__signalFilePath = value

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
        """
        Change the visibility of the specgram widget.
        :param value: Bolean with the new visibility
        :return:
        """
        self._visibleSpectrogram = value
        self.axesSpecgram.setVisible(value)
        # update graph to avoid the pyqtgraph
        # widget error that do not update the axis grid lines

    @property
    def playSpeed(self):
        return self._playSpeed

    @playSpeed.setter
    def playSpeed(self, value):
        if not 0 <= value <= 100:
            raise Exception("The play speed must be positive.")
        self._playSpeed = value

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        """
        Modify and update the internal variables that uses the signal.

        :param new_signal: the new AudioSignal
        :raise Exception: If signal is not of type AudioSignal
        """
        if new_signal is None or not isinstance(new_signal, AudioSignal):
            raise Exception("Invalid assignation value. Must be of type AudioSignal")

        self._signal = new_signal

        #  update the main cursor to visualize and process a piece of the signal
        self.mainCursor.min = 0
        self.mainCursor.max = new_signal.length

        #  update the signal on every widget
        self.axesOscilogram.signal = new_signal
        self.axesSpecgram.signal = new_signal

        # update workspace values for the widgets
        self.axesSpecgram.workspace.maxY = 0
        self.axesSpecgram.workspace.maxY = new_signal.samplingRate / 2.0

        # update the zoom regions limit if zoom tool is selected
        self.updateZoomRegionsLimits()

        #  update the variables that manage the signal
        #  the audio signal handler to play options
        if self.signalPlayer is not None and (self.signalPlayer.playStatus == self.signalPlayer.RECORDING \
           or self.signalPlayer.playStatus == self.signalPlayer.PLAYING):
                self.stop()

        self.signalPlayer = AudioSignalPlayer(self._signal)
        self.signalPlayer.playing.connect(self.update_playing_line)
        self.signalPlayer.playingDone.connect(self.remove_player_line)

        #  the edition object that manages cut and paste options
        self.editionSignalProcessor = EditionSignalProcessor(self._signal)
        self.commonSignalProcessor = CommonSignalProcessor(self._signal)

        #  clean the previous actions to get the initial state with the new signal
        self.undoRedoManager.clear()

        self.updateScrollbar()
    
    @property
    def selectedRegion(self):
        """
        Returns the interval of the signal that its
        currently analyzed.
        :return: tuple x,y with the start and end of the interval in
                signal array data  indexes.
                If zoom tool is active returns the selection made by the tool.
                the current visualization borders are returned otherwise.
        """
        #  get the current visible interval indexes
        index_from, index_to = self.mainCursor.min, self.mainCursor.max
        index_from_zoom, index_to_zoom = index_from, index_to

        #  if selected tool is Zoom get the selection interval indexes
        if self.selectedTool == Tools.ZoomTool:
            if self.visibleOscilogram:
                index_from_zoom, index_to_zoom = self.axesOscilogram.gui_user_tool.zoomRegion.getRegion()

            elif self.visibleSpectrogram:
                spec_rgn = self.axesSpecgram.gui_user_tool.zoomRegion.getRegion()
                index_from_zoom, index_to_zoom = self.from_spec_to_osc(spec_rgn[0]), self.from_spec_to_osc(spec_rgn[1])

            index_from_zoom, index_to_zoom = max(index_from, index_from_zoom), min(index_to, index_to_zoom)

            index_from = index_from_zoom if index_from < index_from_zoom else index_from

            index_to = index_to_zoom if index_to_zoom < index_to else index_to

        return int(index_from), int(index_to)

    @property
    def histogram(self):
        """
        Histogram widget with the values of the spectrogram image.
        interacts with the spectrogram image graph to change its color,
        threshold etc.
        :return:
        """
        return self.axesSpecgram.histogram
    #  endregion

    #  region Zoom in,out, none

    def zoomIn(self):
        """
        Make a zoom in to the current visualized region of the signal.
        Change the visualized interval of the signal to a subinterval of the current.
        The new subinterval has the middle index equal to the old one. 
        :return:
        """
        interval_size_removed = (self.mainCursor.max - self.mainCursor.min) / self.ZOOM_STEP

        # update the new visible interval
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
        interval_size_added = (self.mainCursor.max - self.mainCursor.min) / self.ZOOM_STEP

        # update the max interval limit
        if (self.mainCursor.max + interval_size_added) < self.signal.length:
            self.mainCursor.max += interval_size_added
        else:
            self.mainCursor.max = self.signal.length

        #  update the min interval limit
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
        self.mainCursor.max = self.signal.length
        self.graph()

    #  endregion

    # region GRAPH

    def graph(self):
        """
        Update the two widgets visualizations
        """
        # ensure that the region to graph is inside the signal limits
        self.mainCursor.max = min(self.mainCursor.max, self.signal.length)
        self.mainCursor.min = max(self.mainCursor.min, 0)
        if self.mainCursor.min > self.mainCursor.max:
            self.zoomNone()

        self.axesOscilogram.graph(indexFrom=self.mainCursor.min, indexTo=self.mainCursor.max)
        self.axesSpecgram.graph(indexFrom=self.mainCursor.min, indexTo=self.mainCursor.max)

        self.updateScrollbar()

        # update the coordinates of zoom
        if self.selectedTool == Tools.ZoomTool:
            self.updateZoomRegion(oscilogram_update=True)

    #  endregion

    #  region Edition CUT,COPY PASTE

    def cut(self):
        """
        Cut the current selected section of the signal for later paste
        in this or another instance of the sound lab.
        If the zoom cursor is active then the its selection is taken.
        else the whole inteval of current visualization is used.
        """
        # get the current signal selection interval
        start, end = self.selectedRegion
        self.editionSignalProcessor.cut(start, end)
        self.undoRedoManager.add(CutAction(self.signal, start, end))
        self.graph()

    def _updateSignal(self, new_signal):
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
        #  get the current signal selection interval
        start, end = self.selectedRegion
        self.editionSignalProcessor.copy(start, end)
        self.undoRedoManager.add(CopyAction(self.signal, start, end))

    def paste(self):
        """
        Paste the previously copied or cutted section
        of a signal stored in clipboard.
        """
        #  get the current signal selection interval
        start, end = self.selectedRegion
        self.editionSignalProcessor.paste(start)
        self.undoRedoManager.add(PasteAction(self.signal, start, end))
        self.graph()

    #  endregion

    #  region Signal Processing Actions

    def reverse(self):
        """

        :return:
        """
        start, end = self.selectedRegion
        self.undoRedoManager.add(ReverseAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.reverse)

    def resampling(self, samplingRate):
        self.undoRedoManager.add(ResamplingAction(self.signal, samplingRate))
        self._signal.resampling(samplingRate)
        self.zoomNone()

    def signalProcessingAction(self, delegate, *args):
        """
        Method that handles the signal processing actions.
        Execute the supplied signal processing method and refresh the widget.
        :param delegate: signal processing action
        :param args: delegate arguments
        :return:
        """
        index_from, index_to = self.selectedRegion
        delegate(index_from, index_to, *args)
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
        self.__insertSignal(InsertSilenceAction, ms)

    def insertWhiteNoise(self, ms=1):
        """
        Insert a white noise signal of ms duration in milliseconds.
        If the zoom tool is selected and there is a selection made
        the silence signal would be inserted ni the start of the selection
        otherwise would be inserted at the start of the current
        visualization interval
        :param ms: time in milliseconds of the silence signal to insert
        :return:
        """
        self.__insertSignal(InsertWhiteNoiseAction,ms)

    def __insertSignal(self, undo_action, ms=0):
        """
        Helper method to encapsulate and factorize the code of insert signals
        into the current one.
        :param undo_action: the undo redo action according to the desired
        signal to insert.
        :param ms:
        :return:
        """
        start, end = self.selectedRegion

        #  connect the action for update because the undo of the insert action
        #  is cut and cut change the size of the signal
        action = undo_action(self.signal, start, ms)
        action.signal_size_changed.connect(self._updateSignal)

        #  add the undo redo action
        self.undoRedoManager.add(action)

        #  do the insert action
        action.redo()

        self.graph()

    def modulate(self,function="normalize", fade="IN"):
        """

        :param function:
        :param fade:
        :return:
        """
        start, end = self.selectedRegion

        self.undoRedoManager.add(ModulateAction(self.signal, start, end, function, fade))

        self.signalProcessingAction(self.commonSignalProcessor.modulate, function, fade)

    def normalize(self,factor):
        """

        :param factor:
        :return:
        """
        start, end = self.selectedRegion
        self.undoRedoManager.add(NormalizeAction(self.signal, start, end, factor))
        self.signalProcessingAction(self.commonSignalProcessor.normalize, factor)

    def scale(self, factor):
        """

        :param factor:
        :return:
        """
        start, end = self.selectedRegion
        self.undoRedoManager.add(ScaleAction(self.signal, start, end, factor))
        self.signalProcessingAction(self.commonSignalProcessor.scale, factor)

    def silence(self):
        """

        :return:
        """
        start, end = self.selectedRegion
        self.undoRedoManager.add(SilenceAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.setSilence)

    def filter(self, filter_method):
        """
        Method that filter the selected section
        of the signal with the filter_method supplied.
        The section filtered is the visible range of the signal or the
        selected by the zoom cursor if there is a selection made.
        :param filter_method: The filter method used
        :return:
        """
        if filter_method is None or not isinstance(filter_method, FilterSignalProcessor):
            raise Exception("Invalid filter object.")

        # get the interval limits
        start, end = self.selectedRegion
        filter_method.signal = self.signal
        self.undoRedoManager.add(FilterAction(self.signal, start, end, filter_method))

        # execute the filter and refresh
        filter_method.filter(start, end)
        self.graph()

    def absoluteValue(self,sign):
        """

        :param sign:
        :return:
        """
        start, end = self.selectedRegion
        self.undoRedoManager.add(Absolute_ValuesAction(self.signal, start, end,sign))
        self.signalProcessingAction(self.commonSignalProcessor.absoluteValue,sign)

    def changeSign(self):
        """

        :return:
        """
        start, end = self.selectedRegion
        self.undoRedoManager.add(ChangeSignAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.changeSign)

    #  endregion

    #  region Open And Save

    def open(self, filename):
        if not filename:
            raise Exception("Invalid filename")

        if not os.path.exists(filename):
            raise Exception("Invalid path in file system.")

        try:
            signal = openSignal(filename)
            self.__signalFilePath = filename

            # update signal
            self.signal = signal
            self.graph()

        except Exception as ex:
            raise ex

    def save(self, fname=None):
        """
        Save the current signal into disc.
        :param fname: The path to the file.
        """
        fname = self.signalFilePath if fname is None else fname
        if fname:
            FileManager().write(self._signal, fname)

    def saveSelectedSectionAsSignal(self, fname):
        """
        Save the signal that is currently selected as a new one
        :param fname: path to save the signal
        """
        # get the interval limits
        indexF, index_to = self.selectedRegion

        try:
            signal = self.signal.copy(indexF, index_to)
            FileManager().write(signal, fname)

        except Exception as ex:
            raise ex

    #  endregion

    # region WorkSpace

    @property
    def oscilogramWorkSpace(self):
        """
        :return: the workspace of the oscilogram signal widget
        """
        return self.axesOscilogram.workspace

    @property
    def spectrogramWorkSpace(self):
        """
        :return: the workspace of the spectrogram signal widget
        """
        return self.axesSpecgram.workspace

    def load_workspace(self, workspace, forceUpdate=False):
        """
        Loads a workspace containing all the settings of the oscillogram and spectrogram
        (amongst others) and updates as
        needed
        :param workspace: the workspace to load
        :param forceUpdate: whether to update even if there were no changes to the workspace
        """
        self.axesSpecgram.load_workspace(workspace.spectrogramWorkspace, forceUpdate)
        self.axesOscilogram.load_workspace(workspace.oscillogramWorkspace, forceUpdate)

    # endregion

    def setSelectedTool(self, tool):
        """
        Change the current selected tool of the widget.
        :param tool: the new tool to set.
        :return:
        """

        # switch for the concrete tools implementations
        if tool == Tools.ZoomTool:
            self.axesOscilogram.changeTool(OscilogramZoomTool)
            self.axesSpecgram.changeTool(SpectrogramZoomTool)

            #  Set the connections for the zoom tool synchronization
            self.axesOscilogram.gui_user_tool.zoomRegion.sigRegionChanged.connect(self.updateSpecZoomRegion)
            self.axesSpecgram.gui_user_tool.zoomRegion.sigRegionChanged.connect(self.updateOscZoomRegion)

            # set the limits of the zoom regions to the length of the signal
            self.updateZoomRegionsLimits()

        elif tool == Tools.PointerTool:
            self.axesOscilogram.changeTool(OscilogramPointerTool)
            self.axesSpecgram.changeTool(SpectrogramPointerTool)

        elif tool == Tools.RectangularZoomTool:
            self.axesOscilogram.changeTool(OscilogramRectangularCursorTool)
            self.axesSpecgram.changeTool(SpectrogramRectangularCursorTool)

        elif tool == Tools.NoTool:
            self.axesOscilogram.changeTool(NoTool)
            self.axesSpecgram.changeTool(NoTool)

        self.__selectedTool = tool

    def createContextCursor(self, actions):
        """
        method that add a number of actions to the control's context menu.
        :param actions: List of QAction
        """
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        for act in actions:
            if isinstance(act, QtGui.QAction):
                self.addAction(act)

    def from_osc_to_spec(self, x):
        return self.axesSpecgram.from_osc_to_spec(x)

    def from_spec_to_osc(self, x):
        return self.axesSpecgram.from_spec_to_osc(x)

    def get_freq_index(self, freq):
        return self.axesSpecgram.get_freq_index(freq)