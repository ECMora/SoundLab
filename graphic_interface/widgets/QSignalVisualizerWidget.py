# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
from PyQt4.QtCore import QTimer
from duetto.audio_signals.AudioSignalPlayer import AudioSignalPlayer
from duetto.audio_signals.Synthesizer import Synthesizer
from duetto.audio_signals.AudioSignal import AudioSignal
from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager
from duetto.signal_processing.EditionSignalProcessor import EditionSignalProcessor
from SoundLabOscilogramWidget import SoundLabOscilogramWidget
from SoundLabSpectrogramWidget import SoundLabSpectrogramWidget
from Graphic_Interface.Widgets.signal_visualizer_tools.SignalVisualizerTool import Tools
from Graphic_Interface.Widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool as OscilogramZoomTool
from Graphic_Interface.Widgets.signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool
from Graphic_Interface.Widgets.signal_visualizer_tools.OscilogramTools.PointerCursorTool import PointerCursorTool as OscilogramPointerTool
from Graphic_Interface.Widgets.signal_visualizer_tools.SpectrogramTools.PointerCursorTool import PointerCursorTool as SpectrogramPointerTool
from Graphic_Interface.Widgets.signal_visualizer_tools.OscilogramTools.RectangularCursorTool import RectangularCursorTool as OscilogramRectangularCursorTool
from Graphic_Interface.Widgets.signal_visualizer_tools.SpectrogramTools.RectangularCursorTool import RectangularCursorTool as SpectrogramRectangularCursorTool
from Graphic_Interface.Widgets.undo_redo_actions.UndoRedoActions import *


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

        self._recordTimer = QTimer(self)
        self._recordTimer.timeout.connect(self.on_newDataRecorded)

    def setSelectedTool(self, tool):
        if tool == Tools.ZoomTool:
            self.axesOscilogram.changeTool(OscilogramZoomTool)
            self.axesSpecgram.changeTool(SpectrogramZoomTool)
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
        self.selectedTool = tool

    def updateSpecZoomRegion(self):
        rgn = self.axesOscilogram.gui_user_tool.zoomRegion.getRegion()
        min = self._from_osc_to_spec(rgn[0])
        max = self._from_osc_to_spec(rgn[1])
        self.axesSpecgram.gui_user_tool.zoomRegion.setRegion([min, max])

    def updateOscZoomRegion(self):
        rgn = self.axesSpecgram.gui_user_tool.zoomRegion.getRegion()
        min = self._from_spec_to_osc(rgn[0]) + self.mainCursor.min
        max = self._from_spec_to_osc(rgn[1]) + self.mainCursor.min
        self.axesOscilogram.gui_user_tool.zoomRegion.setRegion([min, max])

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

        if self.signalPlayer.playStatus == self.signalPlayer.RECORDING:

            self._recordTimer.stop()
            print('on stop:' + str(self._recordTimer.isActive()))
            self.axesOscilogram.mouseZoomEnabled = True
            self.axesSpecgram.mouseZoomEnabled = True
            self.axesOscilogram.setVisible(True)
            self.axesSpecgram.setVisible(True)
            self.graph()
            self.zoomNone()
        self.signalPlayer.stop()



    def on_newDataRecorded(self):

        # print('On new data:' + str(self._recordTimer.isActive()))
        self.signalPlayer.readFromStream()

        self.mainCursor.max = len(self.signal.data) - 1
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
        updateTime = 15
        self._recordTimer.start(updateTime)
        #self.createPlayerLine(self.mainCursor.min)

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
    def signal(self, signal):
        """
        Modify and update the internal variables that uses the signal.

        :param signal: the new AudioSignal
        :raise Exception: If signal is not of type AudioSignal
        """
        if signal is None or not isinstance(signal, AudioSignal):
            raise Exception("Invalid assignation value. Must be of type AudioSignal")

        self.__signal = signal
        #update the main cursor to visualize and process a piece of the signal
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.__signal)

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

        #update the widgets with the new signal

    #endregion

    #region Zoom in,out, none
    def zoomIn(self):
        aux = (self.mainCursor.max - self.mainCursor.min) / 4
        if self.mainCursor.max - aux > self.mainCursor.min + aux:
            self.mainCursor.max -= aux
            self.mainCursor.min += aux
        self.graph()

    def zoomOut(self):
        aux = self.mainCursor.max - self.mainCursor.min / 2
        self.mainCursor.max = self.mainCursor.max + aux if (self.mainCursor.max + aux) < len(self.signal) else len(self.signal)
        self.mainCursor.min = self.mainCursor.min - aux if self.mainCursor.min - aux >= 0 else 0
        self.graph()

    def zoomNone(self):
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signal)
        self.graph()

    #endregion

    #region VISUAL EVENTS AND ACTIONS
    def graph(self):
        # perform some heavy calculations
        self.axesSpecgram.graph(indexFrom=self.mainCursor.min, indexTo=self.mainCursor.max)
        self.axesOscilogram.graph(indexFrom=self.mainCursor.min, indexTo=self.mainCursor.max)

    #endregion

    #region Edition CUT,COPY PASTE

    def cut(self):
        start, end = self.getIndexFromAndTo()
        # modify the undo redo action for cut
        self.editionSignalProcessor.cut(start,end)
        self.signal = self.editionSignalProcessor.signal
        self.graph()

    def copy(self):
        start, end = self.getIndexFromAndTo()
        self.editionSignalProcessor.copy(start,end)

    def paste(self):
        start, end = self.getIndexFromAndTo()
        #modify the undo redo action for paste
        self.editionSignalProcessor.paste(start)
        self.signal = self.editionSignalProcessor.signal
        self.graph()

    #endregion

    #region Signal Processing Actions

    def reverse(self):
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.addAction(ReverseAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.reverse)

    def insertWhiteNoise(self, ms=1):
        raise NotImplementedError()
        # if self.signal is not None:
        #     self.signal.generateWhiteNoise(ms, self.zoomCursor.min)
        #     self.updateZoomAndMainCursorFromSignalChangingSizeProcessingAction(ms)

    def updateZoomAndMainCursorFromSignalChangingSizeProcessingAction(self, ms_added):
        self.mainCursor.max += ms_added * self.__signal.samplingRate / 1000
        self.clearZoomCursor()
        self.graph()
        self.axesOscilogram.zoomRegion.setBounds([0, len(self.__signal.data)])
        self.axesSpecgram.zoomRegion.setBounds([0, self._from_osc_to_spec(len(self.__signal.data))])

    def insertPinkNoise(self, ms, type, Fc, Fl, Fu):
        raise NotImplementedError()
        # if self.signal is not None:
        #     self.signal.generateWhiteNoise(ms, self.zoomCursor.min)
        #     self.signal.filter(self.zoomCursor.min, self.zoomCursor.min + ms * self.signal.samplingRate / 1000.0,
        #                        type, Fc, Fl, Fu)
        #     self.updateZoomAndMainCursorFromSignalChangingSizeProcessingAction(ms)

    def resampling(self, samplingRate):
        self.__signal.resampling(samplingRate)
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.__signal.data)
        self.graph()

    def getIndexFromAndTo(self):
        indexFrom, indexTo = self.mainCursor.min, self.mainCursor.max
        axe = self.axesOscilogram if self.visibleOscilogram else self.axesSpecgram if self.visibleSpectrogram else None
        if self.selectedTool == Tools.ZoomTool and axe is not None:
            rgn = axe.gui_user_tool.zoomRegion.getRegion()
            indexFrom, indexTo = rgn[0], rgn[1]
            #the delegate has the responsability of modify just the portion of the signal
            #given by indexFrom:indexTo for an eficient action.
        return indexFrom, indexTo

    def signalProcessingAction(self, delegate, *args):
        indexFrom, indexTo = self.getIndexFromAndTo()
        delegate(indexFrom, indexTo, *args)
        self.graph()

    def insertSilence(self, ms=0):
        indexFrom, indexTo = self.getIndexFromAndTo()
        self.__signal.insertSilence(indexFrom, indexTo, ms)
        self.updateZoomAndMainCursorFromSignalChangingSizeProcessingAction(ms)

    def scale(self, factor, function="normalize", fade="IN"):
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.addAction(
                ScaleAction(self.signal, start, end, factor, function, fade))
        self.signalProcessingAction(self.commonSignalProcessor.scale, factor, function, fade)

    def silence(self):
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.addAction(SilenceAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.setSilence)

    def filter(self, FCut=0, FLow=0, FUpper=0):
        # self.signalProcessingAction(self.signal.filter, FCut, FLow, FUpper)
        raise NotImplementedError()

    def absoluteValue(self,sign):
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.addAction(Absolute_ValuesAction(self.signal, start, end,sign))
        self.signalProcessingAction(self.commonSignalProcessor.absoluteValue,sign)

    def changeSign(self):
        start, end = self.getIndexFromAndTo()
        self.undoRedoManager.addAction(ChangeSignAction(self.signal, start, end))
        self.signalProcessingAction(self.commonSignalProcessor.changeSign)

    #endregion

    def open(self, filename):
        #self.axesOscilogram.sigRangeChanged.disconnect()
        #self.axesSpecgram.viewBox.sigRangeChanged.disconnect()
        #self.undoRedoManager.clearActions() undo redo must be implemented in sound lab not in api

        if not filename:
            raise Exception("Invalid filename")

        signal = WavStreamManager().read(open(filename))

        self.signal = signal

        self.graph()

    def save(self, fname):
        signal_saver = WavStreamManager()
        signal_saver.signal = self.__signal
        signal_saver.save(fname)

    def saveSelectedSectionAsSignal(self, fname):
        """
        Save the signal that is currently selected under the zoom cursor as a new one
        :param fname: path to save the signal
        """
        indexF, indexTo = self.getIndexFromAndTo()
        signal = AudioSignal(samplingRate=self.__signal.samplingRate,
                             bitDepth=self.__signal.bitDepth,
                             channelCount=self.__signal.channelCount,
                             data=self.__signal.data[indexF:indexTo]
        )
        signal_saver = WavStreamManager()
        signal_saver.signal = signal
        signal_saver.save(fname)

    def SaveColorBar(self):
        state = self.axesSpecgram.histogram.item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, self.tr(u"Save Color Bar"),
                                                 filter=self.tr(u"Bar Files") + u"(*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()