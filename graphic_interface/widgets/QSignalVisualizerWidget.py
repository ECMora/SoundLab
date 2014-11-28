# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
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

        #the internal variables to show the play line
        self.playerLineOsc = pg.InfiniteLine()
        self.playerLineSpec = pg.InfiniteLine()

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

    def _from_spec_to_osc(self, coord):
        cs = self.axesSpecgram.specgramHandler.NFFT #- self.specgramSettings.visualOverlap
        return int(1.0 * coord * cs - self.axesSpecgram.specgramHandler.NFFT / 2)

    def _from_osc_to_spec(self, coord):
        cs = self.axesSpecgram.specgramHandler.NFFT #- self.axesSpecgram.specgramHandler.visualOverlap
        return 1.0 * (coord - self.mainCursor.min + self.axesSpecgram.specgramHandler.NFFT / 2) / cs

    def load_Theme(self, theme):
        """
        this method implements the  way in which the control load the theme
        all the visual options are updated here.
        The method delegate in each control (oscilogram plot widget and spectrogram)
        the implementation of its respective visual updates.
        """
        self.axesOscilogram.load_Theme(theme)
        self.axesSpecgram.load_Theme(theme)

    def signalName(self):
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

    #region Undo Redo
    def undo(self):
        self.undoRedoManager.undo()

    def redo(self):
        self.undoRedoManager.redo()
    #endregion

    #region Sound
    # manages the reproduction of the signal
    def play(self):
        self.createPlayerLine(0)
        self.signalPlayer.play()

    def switchPlayStatus(self):
        """
        Change the play status from PLAYING into PAUSE
        and viceversa
        """
        if self.signalPlayer.playStatus == AudioSignalPlayer.PLAYING:
            self.pause()
        elif self.signalPlayer.playStatus == AudioSignalPlayer.PAUSED:
            self.play()

    def stop(self):
        self.removePlayerLine()
        self.signalPlayer.stop()

    def record(self):
        pass

    def pause(self):
        self.signalPlayer.pause()

    def createPlayerLine(self, value):
        if not isinstance(value, int):
            return
        #creates the player cursor to display the signal playing speed
        self.playerLineOsc.setValue(value)
        self.playerLineSpec.setValue(self._from_osc_to_spec(value))
        if self.playerLineOsc not in self.axesOscilogram.getPlotItem().getViewBox().addedItems:
            self.axesOscilogram.getPlotItem().getViewBox().addItem(self.playerLineOsc)
        if self.playerLineSpec not in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.addItem(self.playerLineSpec)

    def removePlayerLine(self):
        if self.playerLineOsc in self.axesOscilogram.getPlotItem().getViewBox().addedItems:
            self.axesOscilogram.getPlotItem().getViewBox().removeItem(self.playerLineOsc)
        if self.playerLineSpec in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.removeItem(self.playerLineSpec)

    def notifyPlayingCursor(self, frame):
        #draw the line in the axes
        self.playerLineOsc.setValue(frame)
        self.playerLineSpec.setValue(self._from_osc_to_spec(frame))
        if self.signalPlayer.playStatus == self.signalPlayer.STOPPED:
            self.removePlayerLine()

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
        self.__signal.resampling(samplingRate)
        self.zoomNone()

    def getIndexFromAndTo(self):
        """
        Returns the interval of the signal that its
        currently analized.
        :return: tuple x,y with the start and end of the interval in
                signal array data  indexes.
                If zoom tool is active returns the selection made by the tool.
                the current visualizating borders are returned otherwise.
        """
        #get the current visible interval indexes
        indexFrom, indexTo = self.mainCursor.min, self.mainCursor.max

        #if selected tool is Zoom get the selection interval indexes
        axe = self.axesOscilogram if self.visibleOscilogram \
                                  else self.axesSpecgram if self.visibleSpectrogram \
                                  else None

        if self.selectedTool == Tools.ZoomTool and axe is not None:
            rgn = axe.gui_user_tool.zoomRegion.getRegion()
            indexFrom, indexTo = rgn[0], rgn[1]

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
        pass

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

    def open(self, filename):
        #self.axesOscilogram.sigRangeChanged.disconnect()
        #self.axesSpecgram.viewBox.sigRangeChanged.disconnect()
        #self.undoRedoManager.clear() undo redo must be implemented in sound lab not in api

        if not filename:
            raise Exception("Invalid filename")

        #open the signal with the correct Stream Manager. (only wav by now)
        signal = WavStreamManager().read(open(filename))

        #update signal
        self.signal = signal
        self.graph()

    def save(self, fname):
        """
        Save the current signal into disc.
        :param fname: The path to the file.
        """
        signal_saver = WavStreamManager()
        signal_saver.signal = self.signal
        signal_saver.save(fname)

    def saveSelectedSectionAsSignal(self, fname):
        """
        Save the signal that is currently selected under the zoom cursor as a new one
        :param fname: path to save the signal
        """
        #get the interval limits
        indexF, indexTo = self.getIndexFromAndTo()

        signal = self.signal.copy(indexF, indexTo)

        #save the signal section
        signal_saver = WavStreamManager()
        signal_saver.signal = signal
        signal_saver.write(fname)

    def SaveColorBar(self):
        state = self.axesSpecgram.histogram.item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, self.tr(u"Save Color Bar"),
                                                 filter=self.tr(u"Bar Files") + u"(*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()