from datetime import datetime
from PyQt4.QtCore import pyqtSignal,QRect, Qt, QRectF,QTimer
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import matplotlib.mlab as mlab
from pyqtgraph.Point import Point
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector, DetectionType
from Duetto_Core.Segmentation.Elements.Element import Element
from Duetto_Core.SignalProcessors.CommonSignalProcessor import CommonSignalProcessor
from Duetto_Core.SignalProcessors.FilterSignalProcessor import *
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
from Duetto_Core.SignalProcessors.EditionSignalProcessor import EditionSignalProcessor

from Duetto_Core.SpecgramSettings import SpecgramSettings
from DuettoPlotWidget import DuettoPlotWidget
from Graphic_Interface.UndoRedoActions import UndoRedoManager, FilterAction
from Graphic_Interface.Widgets.DuettoImageWidget import DuettoImageWidget
from Graphic_Interface.Widgets.Tools import Tools


BACK_COLOR = "gray"


class OscXAxis(pg.AxisItem):
    def __init__(self,parent,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.parent = parent
        self.setLabel(text="Time (s)")
        font = QFont(self.font)
        font.setPointSize(8)
        self.setTickFont(font)

    def tickStrings(self, values, scale, spacing):
        strns = []
        delta = spacing/self.parent.signalProcessor.signal.samplingRate
        a = max(-(int(np.log10(delta))-1),0)
        a = min(a,4)
        s = "{:."+str(a)+"f}"
        for x in values:
            strns.append(s.format(x*1.0/self.parent.signalProcessor.signal.samplingRate))
        return strns

    def tickValues(self,minVal, maxVal, size):
        minVal = self.parent.mainCursor.min
        maxVal = self.parent.mainCursor.max
        spacing = self.tickSpacing(minVal,maxVal,size)[0][0]
        values = []
        temp = minVal
        while(temp < maxVal):
            values.append(temp)
            temp += spacing
        return [(spacing,values)]

    def tickSpacing(self, minVal, maxVal, size):
        minVal = self.parent.mainCursor.min
        maxVal = self.parent.mainCursor.max
        return [(max((maxVal-minVal)/(10.0*self.parent.signalProcessor.signal.samplingRate),0.0001)*self.parent.signalProcessor.signal.samplingRate,0)]

class OscYAxis(pg.AxisItem):
    def __init__(self,parent,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.parent = parent
        self.setLabel(text="Amplitude (%)")
        font = QFont(self.font)
        font.setPointSize(8)
        self.setTickFont(font)

    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            strns.append("{:.0f}".format(x*100.0/self.parent.signalProcessor.signal.getMaximumValueAllowed()))
        return strns


class QSignalVisualizerWidget(QWidget):
    """Class to represent the QSignalVisualizerWidget widget"""
    playing = pyqtSignal(int)
    rangeChanged = pyqtSignal(int, int, int)
    _doRefresh = pyqtSignal(bool, bool, bool, bool)
    rangeAmplitudeChanged = pyqtSignal(int, int)
    rangeFrequencyChanged = pyqtSignal(int, int)

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.histogram = pg.HistogramLUTWidget()
        self._Z = np.array([[0]])
        self.osc_gridx = True
        self.osc_gridy = True
        self.spec_gridx = True
        self.spec_gridy = True
        self.osc_color = QColor(255, 255, 255)
        self.axisXOsc = OscXAxis(self,orientation = 'bottom')
        self.axisXOsc.enableAutoSIPrefix(False)
        self.axisYOsc = OscYAxis(self,orientation = 'left')
        self.axesOscilogram = DuettoPlotWidget(parent=self,axisItems={'bottom': self.axisXOsc,'left':self.axisYOsc})
        self.axesOscilogram.setClipToView(True)
        self.axesOscilogram.setDownsampling(auto=True,mode="peak")
        self.osc_background = "000"
        self.spec_background = "000"
        self.undoRedoManager = UndoRedoManager(self)
        self.minYOsc = -100
        self.maxYOsc =  100
        self.minYSpc = 0
        self.maxYSpc = 100
        self.lines = True

        self.envelopeCurve = pg.PlotCurveItem(np.array([0]),pen=pg.mkPen(self.osc_color,width=1),shadowPen=pg.mkPen(QtGui.QColor(255,0,0),width=3))
        self.axesOscilogram.addItem(self.envelopeCurve)
        self.envelopeFactor = 2 #factor to expand the envelope for best visualization


        self.axesOscilogram.setMouseEnabled(x=False, y=False)
        self.axesOscilogram.getPlotItem().hideButtons()
        self.axesOscilogram.show()
        self.axesOscilogram.setRange(QRect(0,0,1,1))
        self.axesSpecgram = DuettoImageWidget(parent=self)

        self.axesSpecgram.show()

        self.axesOscilogram.IntervalOscChanged.connect(self.updateSpecZoomRegion)
        self.axesSpecgram.IntervalSpecChanged.connect(self.updateOscZoomRegion)
        self.axesOscilogram.PointerCursorPressed.connect(self.axesSpecgram.clearPointerCursor)
        self.axesSpecgram.PointerCursorPressed.connect(self.axesOscilogram.clearPointerCursor)
        self.axesOscilogram.RectangularCursorPressed.connect(self.axesSpecgram.clearRectangularCursor)
        self.axesSpecgram.RectangularCursorPressed.connect(self.axesOscilogram.clearRectangularCursor)
        self.axesSpecgram.applyFilter.connect(self.applyFilterSpec)
        #self.axesOscilogram.NewRectangularRegion.connect(self.applyRectabgularCursorOsc)
        #self.axesSpecgram.NewRectangularRegion.connect(self.applyRectangularCursorSpec)
        layout = QVBoxLayout()
        layout.addWidget(self.axesOscilogram)
        layout.addWidget(self.axesSpecgram)
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        self.mousePressed = False
        self.movingCursorZoom = False
        self.lastX = 0
        self.lastRefreshPoint = False
        #the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)
        #the zoom cursor
        self.zoomCursor = IntervalCursor(0, 0)
        self.axesOscilogram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
        self.axesSpecgram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
        #self.setLayout(layout)
        self.axesOscilogram.makeZoom = self.makeZoom  # metodo a ejecutar si se produce un zoom
        self.axesOscilogram.makeZoomRect = self.makeZoomRect
        self.axesSpecgram.makeZoom = self.makeZoom
        self.axesSpecgram.makeZoomRect = self.makeZoomRect
        self.zoomStep = 1
        self.visualChanges = False
        self._visibleOscillogram = False
        self._visibleSpectrogram = False
        self.axesOscilogram.setMenuEnabled(False)
        self.axesSpecgram.viewBox.setMenuEnabled(False)

        self.clear()

        self.signalProcessor = SignalProcessor()
        self.editionSignalProcessor = EditionSignalProcessor()
        self.specgramSettings = SpecgramSettings()
        self.cursors = []
        self.cursorsmarkers = []  # the rectangles for the visualizations of cursors
        self.visibleCursors = True
        self.Elements = []  # list of elements detected in oscilogram each element contains the object it self and the extra data for visualize it
        self.visibleElements = True

        self.colorbar = None
        self.playerSpeed = 100
        self.playerLineOsc = pg.InfiniteLine()
        self.playerLineSpec = pg.InfiniteLine()
        self.elements_detector = OneDimensionalElementsDetector()

        self._playDelta = 1
        self._playerLineTimer = QTimer(self)
        self._playerLineTimer.timeout.connect(lambda: self.notifyPlayingCursor(int(self.playerLineOsc.value() + self._playDelta)))

        self._lastRecordRefresh = datetime.now()
        self._recordRefreshRate = 5

        self._doRefresh.connect(self._refresh)
        self.playing.connect(self.notifyPlayingCursor)

        self._pivot = self.zoomCursor.min

    def setSelectedTool(self,tool):
        self.axesSpecgram.changeSelectedTool(tool)
        self.axesOscilogram.changeSelectedTool(tool)

    def load_Theme(self,theme):
        """
        this method implements the  way in wich the controls load the theme
        all changes made by the theme are made in this place
        """
        self.osc_background = theme.osc_background
        self.osc_color = theme.osc_plot
        self.osc_gridx = theme.osc_GridX
        self.osc_gridy = theme.osc_GridY
        self.spec_background = theme.spec_background
        self.envelopeCurve.setPen(pg.mkPen(self.osc_color,width=1))
        self.envelopeCurve.setShadowPen(pg.mkPen(QtGui.QColor(255,0,0),width=3))


    def createContextCursor(self,actions):
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        for act in actions:
            self.addAction(act)

    def applyFilterSpec(self,indexF,indexT,FreqLow,FreqUp):
        filter = FilterSignalProcessor(self.signalProcessor.signal)
        start = int(self._from_spec_to_osc(indexF))
        end = int(self._from_spec_to_osc(indexT))
        self.undoRedoManager.addAction(FilterAction(self.signalProcessor.signal,start,end,FILTER_TYPE.BAND_STOP, 0, FreqLow, FreqUp))
        filter.filter(indexFrom = start,indexTo = end,filterType = FILTER_TYPE.BAND_STOP,Fl=FreqLow,Fu=FreqUp)
        self.visualChanges = True
        self.refresh()

    def updateSpecZoomRegion(self,a,b):
        min = self._from_osc_to_spec(a)
        max = self._from_osc_to_spec(b)
        self.axesSpecgram.emitIntervalSpecChanged = False
        self.axesSpecgram.zoomRegion.setRegion([min, max])
        self.axesSpecgram.emitIntervalSpecChanged = True
        self.stop()


    def updateOscZoomRegion(self,a,b):
        min = self._from_spec_to_osc(a) + self.mainCursor.min
        max = self._from_spec_to_osc(b) + self.mainCursor.min
        self.axesOscilogram.setZoomRegionVisible(True)
        self.axesOscilogram.emitIntervalOscChanged = False
        self.axesOscilogram.zoomRegion.setRegion([min, max])
        self.axesOscilogram.emitIntervalOscChanged = True
        self.stop()

	#region Sound

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Left:
            shift = max(1, (self.mainCursor.max - self.mainCursor.min) / 1000.0)
            if QKeyEvent.modifiers() & Qt.ControlModifier:
                shift *= 10
            if QKeyEvent.modifiers() & Qt.ShiftModifier:
                if self.zoomCursor.max > self._pivot:
                    self.zoomCursor.max = max(self.zoomCursor.max - shift, self._pivot)
                else:
                    self.zoomCursor.min -= shift
            else:
                self.zoomCursor.shift(-shift)
            self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
        elif QKeyEvent.key() == Qt.Key_Right:
            shift = max(1, (self.mainCursor.max - self.mainCursor.min) / 1000.0)
            if QKeyEvent.modifiers() & Qt.ControlModifier:
                shift *= 10
            if QKeyEvent.modifiers() & Qt.ShiftModifier:
                if self.zoomCursor.min < self._pivot:
                    self.zoomCursor.min = min(self.zoomCursor.min + shift, self._pivot)
                else:
                    self.zoomCursor.max += shift
            else:
                self.zoomCursor.shift(shift)
            self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
        elif QKeyEvent.key() == Qt.Key_Space:
            self.switchPlayStatus()
        elif QKeyEvent.key() == Qt.Key_Shift:
            self._pivot = self.zoomCursor.min

    def changePlayStatus(self):
        if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PAUSED or \
           self.signalProcessor.signal.playStatus == self.signalProcessor.signal.STOPPED:
            self.play()
        elif self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING:
            self.pause()

    def play(self):
        if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PAUSED:
            self.signalProcessor.signal.play()
            self.createPlayerLine(self.playerLineOsc.value())
            return

        if self.zoomCursor.min > 0 and self.zoomCursor.max > 0:
            if self.zoomCursor.max - self.zoomCursor.min > self.signalProcessor.signal.samplingRate / 100.0:
                self.signalProcessor.signal.play(self.zoomCursor.min, self.zoomCursor.max, self.playerSpeed)
            else:
                self.signalProcessor.signal.play(self.zoomCursor.min, self.mainCursor.max, self.playerSpeed)
            self.createPlayerLine(self.zoomCursor.min)
        else:
            self.signalProcessor.signal.play(self.mainCursor.min, self.mainCursor.max, self.playerSpeed)
            self.createPlayerLine(self.mainCursor.min)

    def switchPlayStatus(self):
        if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING:
            self.pause()
        else:
            self.play()

    def stop(self):
        prevStatus = self.signalProcessor.signal.playStatus
        self.signalProcessor.signal.stop()
        self.removePlayerLine()
        if prevStatus == AudioSignal.RECORDING:
            self.axesOscilogram.mouseZoomEnabled = True
            self.axesSpecgram.mouseZoomEnabled = True
            self.visibleSpectrogram = True
            self.axesOscilogram.setVisible(self.visibleOscilogram)
            self.axesSpecgram.setVisible(self.visibleSpectrogram)
            self.visualChanges = True
            self.refresh(updateSpectrogram=True)
            self.zoomNone()
            self.axesOscilogram.zoomRegion.setBounds([self.mainCursor.min,self.mainCursor.max])
            self.axesSpecgram.zoomRegion.setBounds([0,self._from_osc_to_spec(self.mainCursor.max)])

    def record(self):
        self.axesOscilogram.mouseZoomEnabled = False
        self.axesSpecgram.mouseZoomEnabled = False
        self.axesOscilogram.setVisible(True)
        self.axesSpecgram.setVisible(False)
        self.signalProcessor.signal.record()
        #self.createPlayerLine(self.mainCursor.min)

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

        updateTime =  41 #41ms=1/24s
        self._playDelta = self.signalProcessor.signal.samplingRate*self.playerSpeed/100*updateTime/1000
        self._playerLineTimer.start(updateTime)




    def removePlayerLine(self):
        self._playerLineTimer.stop()
        if self.playerLineOsc in self.axesOscilogram.getPlotItem().getViewBox().addedItems:
            self.axesOscilogram.getPlotItem().getViewBox().removeItem(self.playerLineOsc)
        if self.playerLineSpec in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.removeItem(self.playerLineSpec)


    def pause(self):
        self._playerLineTimer.stop()
        self.signalProcessor.signal.pause()


    def notifyPlayingCursor(self, frame):
        #if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING:
            #draw the line in the axes
        self.playerLineOsc.setValue(frame)
        self.playerLineSpec.setValue(self._from_osc_to_spec(frame))
        if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.STOPPED:
            self.removePlayerLine()
            #if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.RECORDING:
            #    size = len(self.signalProcessor.signal.data)
            #    self.mainCursor.min, self.mainCursor.max = 5 * size / 10, 9 * size / 10
            #    self.visualChanges = True
            #    self.refresh()
            #    self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))


    #endregion

    #region Property oscilogram and specgram Visibility

    def _getVisibleOscilogram(self):
        return self._visibleOscillogram

    def _setVisibleOscilogram(self, value):
        self.visualChanges = True
        self._visibleOscillogram = value
        self.axesOscilogram.setVisible(value)

    visibleOscilogram = property(_getVisibleOscilogram, _setVisibleOscilogram)

    def _getVisibleSpectrogram(self):
        return self._visibleSpectrogram

    def _setVisibleSpectrogram(self, value):
        self.visualChanges = True
        self._visibleSpectrogram = value
        self.axesSpecgram.setVisible(value)

    visibleSpectrogram = property(_getVisibleSpectrogram, _setVisibleSpectrogram)
    #endregion

    #region VISUAL EVENTS AND ACTIONS
    def updatezoomcursor(self):
        #actualiza los cursores de zoom segun el area seleccionada por el usuario
        range = self.axesOscilogram.zoomRegion.getRegion()
        self.zoomCursor.min, self.zoomCursor.max = int(range[0]), int(range[1])
        #self.emit(SIGNAL("IntervalChanged"))


    def dropEvent(self, event):
        data = event.mimeData().data()
        file = QtCore.QFile()
        file.setFileName("local.wav")
        file.write(data)
        file.close()
        event.accept()
        self.open("local.wav")

    def deselectZoomRegion(self):
        self.clearZoomCursor()
        self.visualChanges = True
        self.refresh(dataChanged=False)

    def _oscRangeChanged(self, window, viewRange):
        if not isinstance(viewRange, list):
            return
        [left, right] = viewRange[0]
        if (left, right) == (self.mainCursor.min, self.mainCursor.max):
            return
        self.changeRange(left, right, updateOscillogram=False)

    def _specRangeChanged(self, b):
        [left, right] = self.axesSpecgram.viewBox.viewRange()[0]
        (left, right) = self._from_spec_to_osc(left), self._from_spec_to_osc(right)
        if (left, right) == (self.mainCursor.min, self.mainCursor.max):
            return
        self.changeRange(left, right, updateSpectrogram=False)

    def _from_spec_to_osc(self, coord):
        cs = self.specgramSettings.NFFT - self.specgramSettings.visualOverlap
        return int(1.0 * coord * cs - self.specgramSettings.NFFT / 2)

    def _from_osc_to_spec(self, coord):
        cs = self.specgramSettings.NFFT - self.specgramSettings.visualOverlap
        return 1.0 * (coord - self.mainCursor.min + self.specgramSettings.NFFT / 2) / cs

    def zoomOut(self):
        if not self.signalProcessor.signal.opened():
            return
        aux = max((self.mainCursor.max - self.mainCursor.min), 4 * self.zoomStep) / (2 * self.zoomStep)
        if self.mainCursor.max + aux < len(self.signalProcessor.signal.data):
            self.mainCursor.max += aux
        else:
            self.mainCursor.max = len(self.signalProcessor.signal.data)

        if self.mainCursor.min - aux >= 0:
            self.mainCursor.min -= aux
        else:
            self.mainCursor.min = 0
        self.visualChanges = True
        self.refresh(dataChanged=False)
        self.axesOscilogram.clearPointerCursor()
        self.axesOscilogram.clearRectangularCursor()
        self.axesSpecgram.clearPointerCursor()
        self.axesSpecgram.clearRectangularCursor()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))
        self.zoomCursor.max = self.zoomCursor.min
        self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
        self.axesSpecgram.zoomRegion.setRegion([0,0])

    def undo(self):
        self.undoRedoManager.undo()

    def redo(self):
        self.undoRedoManager.redo()

    def makeZoomRect(self, specCoords = False):
        if specCoords:
            self.makeZoom(self.axesSpecgram.rectRegion['x'][0],self.axesSpecgram.rectRegion['x'][1], specCoords=True)
            self.minYSpc = self.axesSpecgram.rectRegion['y'][0]
            self.maxYSpc = self.axesSpecgram.rectRegion['y'][1]
            self.refresh(dataChanged=False, updateOscillogram=True, updateSpectrogram=True)
            self.rangeFrequencyChanged.emit(self.minYSpc,self.maxYSpc)
        else:
            self.makeZoom(self.axesOscilogram.rectRegion['x'][0],self.axesOscilogram.rectRegion['x'][1], specCoords=False)
            self.minYOsc = self.axesOscilogram.rectRegion['y'][0]
            self.maxYOsc = self.axesOscilogram.rectRegion['y'][1]
            self.refresh(dataChanged=False, updateOscillogram=True, updateSpectrogram=True)
            self.rangeAmplitudeChanged.emit(self.minYOsc,self.maxYOsc)

    def zoomIn(self):

        if self.axesSpecgram.selectedTool == Tools.RectangularCursor:
            if self.axesSpecgram.mouseReleased:
               self.makeZoomRect(specCoords=True)
            else: self.makeZoomRect()
            return

        elif not self.signalProcessor.signal.opened():
            return
        aux = (self.mainCursor.max - self.mainCursor.min) / (4 * self.zoomStep)
        if self.mainCursor.max - aux > self.mainCursor.min + aux:
            self.mainCursor.max -= aux
            self.mainCursor.min += aux
        self.visualChanges = True
        self.refresh(dataChanged=False)
        self.axesOscilogram.clearPointerCursor()
        self.axesOscilogram.clearRectangularCursor()
        self.axesSpecgram.clearRectangularCursor()
        self.axesSpecgram.clearPointerCursor()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))
        self.zoomCursor.max = self.zoomCursor.min
        self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
        self.axesSpecgram.zoomRegion.setRegion([0,0])

    def zoomNone(self):
        if not self.signalProcessor.signal.opened():
            return
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        self.clearZoomCursor()
        self.visualChanges = True
        self.refresh(dataChanged=False)
        self.axesOscilogram.clearPointerCursor()
        self.axesSpecgram.clearRectangularCursor()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def makeZoom(self, _min, _max, specCoords=False):
        if not self.signalProcessor.signal.opened() or _min == _max:
            return
        if specCoords:
            _min = self._from_spec_to_osc(_min)
            _max = self._from_spec_to_osc(_max)
        self.changeRange(_min, _max)
        self.zoomCursor.max = self.zoomCursor.min
        self.axesOscilogram.emitIntervalOscChanged = False
        self.axesSpecgram.emitIntervalSpecChanged = False
        self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
        self.axesSpecgram.zoomRegion.setRegion([0,0])
        self.axesOscilogram.emitIntervalOscChanged = True
        self.axesSpecgram.emitIntervalSpecChanged = True


    def changeRange(self, left, right, emit=True, updateOscillogram=True, updateSpectrogram=True):
        self.mainCursor.min, self.mainCursor.max = left, right
        self.visualChanges = True
        self.refresh(dataChanged=False, updateOscillogram=updateOscillogram, updateSpectrogram=updateSpectrogram)
        if emit:
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def on_newDataRecorded(self, frame_count):
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        self.mainCursor.min = max(0, len(self.signalProcessor.signal.data) - 3*self.signalProcessor.signal.samplingRate)
        self.visualChanges = True
        #print(self.signalProcessor.signal.data.size)
        self.refresh(updateSpectrogram=False)
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    SPECGRAM_COMPLEX_SIDE = "onesided"

    TICK_INTERVAL_MS = 10

    def refreshAxes(self):
        bounds = self.axisXOsc.mapRectFromParent(self.axisXOsc.geometry())
        points = list(map(self.axisXOsc.mapToDevice, (bounds.topLeft(), bounds.topRight())))
        spc,vals = self.axisXOsc.tickValues(self.axisXOsc.range[0], self.axisXOsc.range[1], Point(points[1] - points[0]).length())[0]
        strgs = self.axisXOsc.tickStrings(vals,1,spc)
        self.axisXOsc.setTicks([zip(vals,strgs)])
        self.axesSpecgram.xAxis.setTicks(self.axisXOsc._tickLevels)

    def zoomY(self,ymin,ymax):
        self.axesSpecgram.viewBox.setRange()
        self.axesSpecgram.getView().setRange()

    def computeSpecgramSettings(self,overlap=None):
        """
        Computes the specgram settings for a specified overlap
        """
        overlap = overlap if overlap is not None else int(self.specgramSettings.NFFT*self.specgramSettings.overlap/100.)

        #print(self.signalProcessor.signal._padded)
        if self.signalProcessor.signal._padded:
            smin = self.mainCursor.min - self.specgramSettings.NFFT + 4096
            smax = self.mainCursor.max + self.specgramSettings.NFFT + 4096
            data = self.signalProcessor.signal._data[smin: smax]
        else:
            smin = self.mainCursor.min - self.specgramSettings.NFFT
            smax = self.mainCursor.max + self.specgramSettings.NFFT
            pre, post = np.zeros(max(-smin, 0)), np.zeros(max(smax - len(self.signalProcessor.signal.data), 0))
            data = np.concatenate((pre, self.signalProcessor.signal.data[max(smin, 0): min(smax, len(self.signalProcessor.signal.data))], post))

        self.specgramSettings.Pxx, self.specgramSettings.freqs, self.specgramSettings.bins = mlab.specgram(
            data, self.specgramSettings.NFFT, Fs=self.signalProcessor.signal.samplingRate,
            detrend=mlab.detrend_none, window=self.specgramSettings.window, noverlap=overlap,
            sides=self.SPECGRAM_COMPLEX_SIDE)

    def refresh(self, dataChanged=True, updateOscillogram=True, updateSpectrogram=True, partial=True):
        # perform some heavy calculations
        self.mainCursor.max = min(self.mainCursor.max,len(self.signalProcessor.signal.data))
        width = False if not self.visibleSpectrogram else self.axesSpecgram.viewBox.width()
        if self.visibleSpectrogram and updateSpectrogram and self.signalProcessor.signal \
           and self.signalProcessor.signal.opened() and self.signalProcessor.signal.playStatus != AudioSignal.RECORDING\
           and self.mainCursor.max > self.mainCursor.min and width:
            normOverlap = self.specgramSettings.overlap / 100.0
            if normOverlap < 0:
                normOverlap = 1 - 1.0 * (self.mainCursor.max-self.mainCursor.min) / (self.specgramSettings.NFFT * width)
            self.specgramSettings.visualOverlap = int(self.specgramSettings.NFFT * normOverlap)
            self.computeSpecgramSettings(self.specgramSettings.visualOverlap)

            #self.specgramSettings.visualOverlap *= 100.0/self.specgramSettings.NFFT
            temp = np.amax(self.specgramSettings.Pxx)
            if temp == 0:
                temp = 1.0
            self._Z = 10. * np.log10(self.specgramSettings.Pxx/temp)
            #self._Z = np.flipud(self._Z)
            Zfin = np.isfinite(self._Z)
            if np.any(Zfin):
                m = self._Z[Zfin].min()
                self._Z[np.isneginf(self._Z)] = m
            else:
                self._Z[self._Z < -100] = -100
        # do actual refresh
        self._doRefresh.emit(dataChanged, updateOscillogram, updateSpectrogram, partial)

    def _refresh(self, dataChanged, updateOscillogram, updateSpectrogram, partial):

        if not self.visualChanges:
            return

        self.axesOscilogram.setRange(xRange=(self.mainCursor.min, self.mainCursor.max),
                                     yRange=(self.minYOsc*0.01*self.signalProcessor.signal.getMaximumValueAllowed(),
                                             self.maxYOsc*0.01*self.signalProcessor.signal.getMaximumValueAllowed()),
                                     padding=0,update = True)

        if (self.visibleOscilogram or self.signalProcessor.signal.playStatus == AudioSignal.RECORDING) \
           and updateOscillogram and self.signalProcessor.signal and self.signalProcessor.signal.opened()\
           and self.mainCursor.max > self.mainCursor.min:
            self.mainCursor.min = int(self.mainCursor.min)
            self.mainCursor.max = int(self.mainCursor.max)
            if self.lines or self.axesOscilogram.width() < self.mainCursor.max - self.mainCursor.min:
                if partial:
                    self.axesOscilogram.plot(np.arange(self.mainCursor.min,self.mainCursor.max),self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max], clear=True, pen = self.osc_color , clipToView=True)
                elif dataChanged or self.lastRefreshPoint:
                    self.axesOscilogram.plot(self.signalProcessor.signal.data, clear=True, pen = self.osc_color , clipToView=True)
                    self.lastRefreshPoint = False
            else:
                self.axesOscilogram.plot(np.arange(self.mainCursor.min,self.mainCursor.max),self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max], clear=True, pen = None, symbol = 's', symbolSize = 1,symbolPen = self.osc_color, clipToView=True)
                self.lastRefreshPoint = True

            self.axesOscilogram.getPlotItem().showGrid(x=self.osc_gridx, y=self.osc_gridy)
            self.axesOscilogram.setBackground(self.osc_background)

        if self.visibleSpectrogram and updateSpectrogram and self.signalProcessor.signal \
           and self.signalProcessor.signal.opened() and self.signalProcessor.signal.playStatus != AudioSignal.RECORDING\
           and self.mainCursor.max > self.mainCursor.min:

            YSpec = np.searchsorted(self.specgramSettings.freqs, [self.minYSpc*1000, self.maxYSpc*1000])

            self.axesSpecgram.imageItem.setImage(np.transpose(self._Z))

            self.axesSpecgram.viewBox.setRange(xRange=(self._from_osc_to_spec(self.mainCursor.min),
                                                       self._from_osc_to_spec(self.mainCursor.max)),
                                               yRange=(YSpec[0], YSpec[1]), padding=0)
            self.updateSpecZoomRegion(self.zoomCursor.min, self.zoomCursor.max)

            self.updateSpectrogramColors()
            self.axesSpecgram.setBackground(self.spec_background)
            self.axesSpecgram.showGrid(x=self.spec_gridx, y=self.spec_gridy)
            self.updateSpecZoomRegion(self.zoomCursor.min, self.zoomCursor.max)

        self.refreshAxes()
        self.visualChanges = False
        if self.visibleElements:
            self.drawElements()

        gem = self.parent().geometry()
        self.parent().resize(gem.width()/3, gem.height())
        self.parent().resize(gem.width(), gem.height())


    def updateSpectrogramColors(self):
        self.histogram.item.region.lineMoved()
        self.histogram.item.region.lineMoveFinished()

    def cursorZoomTransform(self, cursorIndex):
        return cursorIndex - self.mainCursor.min

    def changeElementsVisibility(self,visible,element_type=Element.Figures,oscilogramItems=True):
        #change the visibility of the visual items in items
        #that objects must be previously added into oscilogram or specgram widgets
        iterable = self.Elements
        if not oscilogramItems:
            aux = [x.twoDimensionalElements for x in self.Elements]
            iterable = []
            for list in aux:
                iterable.extend(list)
        for e in iterable:
            if element_type is Element.Figures:
                for x in e.visual_figures:
                    x[1] = visible
            elif element_type is Element.Text:
                for x in e.visual_text:
                    x[1] = visible
            elif element_type is Element.Locations:
                for x in e.visual_locations:
                    x[1] = visible
            elif element_type is Element.PeakFreqs:
                for x in e.visual_peaksfreqs:
                    x[1] = visible
        self.drawElements()


    def drawElements(self,oscilogramItems=None):
        # if oscilogramItems = None its updated the oscilogram and spectrogram widgets
        osc = oscilogramItems is None or oscilogramItems
        spec = oscilogramItems is None or not oscilogramItems

        if(self.visibleOscilogram and osc):
            for i in range(len(self.Elements)):
                if self.Elements[i].visible:
                    for item, visible in self.Elements[i].visualwidgets():
                        if not visible:
                            self.axesOscilogram.removeItem(item)
                        else:
                            if(not item in self.axesOscilogram.items() and visible):
                                self.axesOscilogram.addItem(item)
                else:
                    for item, visible  in self.Elements[i].visualwidgets():
                        self.axesOscilogram.removeItem(item)
            self.axesOscilogram.update()

        if(self.visibleSpectrogram and spec):
            for i in range(len(self.Elements)):
                for j in range(len(self.Elements[i].twoDimensionalElements)):
                    if self.Elements[i].twoDimensionalElements[j].visible:
                        for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            if not visible:
                                self.axesSpecgram.viewBox.removeItem(item)
                            else:
                                if(not item in self.axesSpecgram.items() and visible):
                                    self.axesSpecgram.viewBox.addItem(item)
                    else:
                        for item, visible  in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            self.axesSpecgram.viewBox.removeItem(item)

            self.axesSpecgram.update()

    def clear(self):
        self.colorbar = None

    def clearZoomCursor(self):
        self.zoomCursor.min, self.zoomCursor.max = 0, 0
        self.axesOscilogram.zoomRegion.setRegion([0, 0])
        self.axesSpecgram.zoomRegion.setRegion([0, 0])


    #endregion

    #region SIGNAL PROCESSING

    #region Edition CUT,COPY PASTE
    def cut(self):
        if(len(self.signalProcessor.signal.data)>0 and self.signalProcessor.signal.opened()):
            self.editionSignalProcessor.cut(self.zoomCursor.min, self.zoomCursor.max)
            self.mainCursor.max -= self.zoomCursor.max - self.zoomCursor.min
            self.visualChanges = True
            if (self.mainCursor.max < 1):
                self.zoomOut()
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))
            self.refresh()

    def copy(self):
        if(len(self.signalProcessor.signal.data)>0and self.signalProcessor.signal.opened()):
            return self.editionSignalProcessor.copy(self.zoomCursor.min, self.zoomCursor.max)

    def paste(self):
        if(self.signalProcessor.signal.opened):
            self.editionSignalProcessor.paste(self.editionSignalProcessor.clipboard, self.zoomCursor.min)
            self.mainCursor.max += len(self.editionSignalProcessor.clipboard)
            self.visualChanges = True
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))
            self.refresh()
    #endregion

    def reverse(self):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).reverse)

    def insertWhiteNoise(self,ms=1):
        if(self.signalProcessor.signal is not None):
            self.signalProcessor.signal.generateWhiteNoise(ms,self.zoomCursor.min)
            self.visualChanges=True
            self.refresh()

    def insertPinkNoise(self,ms,type, Fc,Fl,Fu):
        if(self.signalProcessor.signal is not None):
            self.signalProcessor.signal.generateWhiteNoise(ms,self.zoomCursor.min)
            f = FilterSignalProcessor(self.signalProcessor.signal)
            f.filter(self.zoomCursor.min,self.zoomCursor.min+ms*self.signalProcessor.signal.samplingRate/1000.0,type,Fc,Fl,Fu)
            self.visualChanges=True
            self.refresh()

    def resampling(self,samplingRate):
        self.signalProcessor.signal.resampling(samplingRate)
        self.visualChanges = True
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        self.maxYSpc = self.signalProcessor.signal.samplingRate
        self.refresh()

    def envelope(self):
        #add cofig dialog and plot the envelope
        indexFrom, indexTo = self.getIndexFromAndTo()
        self.envelopeCurve.setData(self.getTransformedEnvelope(envelope(self.signalProcessor.signal.data[indexFrom:indexTo],decay=self.signalProcessor.signal.samplingRate/1000)))
        self.setEnvelopeVisibility(True)

    def getTransformedEnvelope(self,array):
        self.envelopeFactor = (2.0**(self.signalProcessor.signal.bitDepth)*self.maxYOsc/100)/array[np.argmax(array)]
        return (self.envelopeFactor*array-2**(self.signalProcessor.signal.bitDepth-1)*self.maxYOsc/100)

    def setEnvelopeVisibility(self,bool):
        inaxes = self.envelopeCurve in self.axesOscilogram.items()
        if bool and not inaxes:
            self.axesOscilogram.addItem(self.envelopeCurve)
        elif not bool and inaxes:
            self.axesOscilogram.removeItem(self.envelopeCurve)
        self.axesOscilogram.update()



    def getIndexFromAndTo(self):
        indexFrom, indexTo = self.mainCursor.min, self.mainCursor.max
        if self.zoomCursor.min > 0 and self.zoomCursor.max > 0 and self.zoomCursor.max > self.zoomCursor.min:
            indexFrom, indexTo = self.zoomCursor.min, self.zoomCursor.max
            #the delegate has the responsability of modify just the portion of the signal
            #given by indexFrom:indexTo for an eficient action.
        return indexFrom, indexTo

    def signalProcessingAction(self, delegate, *args):
        indexFrom, indexTo = self.getIndexFromAndTo()
        delegate(indexFrom, indexTo, *args)
        self.clearZoomCursor()
        self.visualChanges = True
        self.refresh()

    def insertSilence(self, ms=0):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).insertSilence, ms)

    def scale(self, factor, function="normalize", fade="IN"):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).scale,factor,function,fade)

    def silence(self):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).setSilence)


    def filter(self, filterType=FILTER_TYPE().LOW_PASS, FCut=0, FLow=0, FUpper=0):
        self.signalProcessingAction(FilterSignalProcessor(self.signalProcessor.signal). \
                                        filter, filterType, FCut, FLow, FUpper)

    def normalize(self):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).normalize)

    def absoluteValue(self,sign):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).absoluteValue,sign)

    def changeSign(self):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).changeSign)


    #endregion

    #region DETECTION

    def cleanVisibleCursors(self,oscilogram=True,specgram=True):
        if(oscilogram):
            for elem in self.Elements:
                for item, visible in elem.visualwidgets():
                    if(visible):
                        self.axesOscilogram.removeItem(item)
        if(specgram):
            for elem in self.Elements:
                for elem2 in elem.twoDimensionalElements:
                    for item, visible in elem2.visualwidgets():
                        if(visible):
                            self.axesSpecgram.viewBox.removeItem(item)

    def clearCursors(self,oscilogram=True,specgram=True):
        self.cleanVisibleCursors(oscilogram=True,specgram=True)
        self.Elements = [] if oscilogram and specgram else self.Elements

    def selectElement(self,number=-1):
        if len(self.Elements) > number and number >= 0:
            f,t = self.Elements[number].indexFrom,self.Elements[number].indexTo
            self.axesOscilogram.selectElement(f,t,pg.mkBrush(QtGui.QColor(255, 255, 255, 150)))
            if f < self.mainCursor.min or t > self.mainCursor.max:
                sizeInterval = self.mainCursor.max-self.mainCursor.min
                self.mainCursor.min = max(0,(f+t-sizeInterval)/2)
                self.mainCursor.max = min(self.mainCursor.min + sizeInterval,len(self.signalProcessor.signal.data))
                self.visualChanges= True
                self.refresh()
        else:
            self.axesOscilogram.selectElement(0,0)

    def detectElements(self,threshold=20, decay=1, minSize=0, detectionsettings=None,softfactor=5, merge_factor=50,threshold2=0, threshold_spectral=95, pxx=[], freqs=[], bins=[], minsize_spectral=(0, 0),location= None, progress=None,findSpectralSublements = True):
        self.clearCursors()
        self.elements_detector.detect(self.signalProcessor.signal,0,len(self.signalProcessor.signal.data),threshold= threshold,detectionsettings=detectionsettings,decay=decay,minSize= minSize,softfactor= softfactor,merge_factor= merge_factor,secondThreshold=threshold2,threshold_spectral=threshold_spectral,
                                      minsize_spectral = minsize_spectral,location=location,progress=progress,findSpectralSublements = findSpectralSublements, specgramSettings= self.specgramSettings)

        if detectionsettings is None or detectionsettings.detectiontype == DetectionType.Envelope_Abs_Decay_Averaged or detectionsettings.detectiontype == DetectionType.Envelope_Rms:
            self.envelopeCurve.setData(self.getTransformedEnvelope(self.elements_detector.envelope))
            self.setEnvelopeVisibility(True)
            self.axesOscilogram.threshold.setValue(self.elements_detector.getThreshold())
        else:
            self.setEnvelopeVisibility(False)

        self.axesOscilogram.setVisibleThreshold(True)

        for c in self.elements_detector.elements():
            self.Elements.append(c)# the elment the space for the span selector and the text
        #incorporar deteccion en espectrograma
        if findSpectralSublements:
            self.drawElements()
        else:
            self.drawElements(oscilogramItems=True)


    #endregion

    #region SAVE AND OPEN

    def openNew(self, samplingRate=1, bitDepth=8, duration=1, whiteNoise=False):
        self.open(None, samplingRate, bitDepth, duration, whiteNoise)

    def open(self, filename, samplingRate=1, bitDepth=8, duration=1, whiteNoise=False):
        #self.axesOscilogram.sigRangeChanged.disconnect()
        #self.axesSpecgram.viewBox.sigRangeChanged.disconnect()
        self.clear()
        self.undoRedoManager.clearActions()
        if self.signalProcessor.signal:
            self.stop()

        if filename:
            self.signalProcessor.signal = WavFileSignal(filename)
        else:
            self.signalProcessor.signal = WavFileSignal(samplingRate=samplingRate, duration=duration, bitDepth=bitDepth,
                                                        whiteNoise=whiteNoise)
        if self.signalProcessor.signal.bitDepth > 16:
            self.signalProcessor.signal.data = self.signalProcessor.signal.data*(2.0**15)/self.signalProcessor.signal.getMaximumValueAllowed()
            self.signalProcessor.signal.data = self.signalProcessor.signal.data.astype('int16')
            self.signalProcessor.signal.bitDepth = 16
        self.cursors = []

        self.editionSignalProcessor = EditionSignalProcessor(self.signalProcessor.signal)
        #self.signalProcessor.signal.setTickInterval(self.TICK_INTERVAL_MS)
        #self.signalProcessor.signal.timer.timeout.connect(self.notifyPlayingCursor)

        if isinstance(self.signalProcessor.signal, WavFileSignal):
            self.loadUserData(self.signalProcessor.signal.userData)
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        self.specgramSettings.threshold = 50
        if self.visibleOscilogram:
            self.axesOscilogram.clear()
            self.axesOscilogram.zoomRegion.setBounds([self.mainCursor.min, self.mainCursor.max])
            self.axesOscilogram.setRange(QRect(0, -2 ** (self.signalProcessor.signal.bitDepth-1),
                                               self.mainCursor.max-self.mainCursor.min,
                                               2 ** self.signalProcessor.signal.bitDepth), padding=0)
            self.axesOscilogram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
            self.signalProcessor.signal.play_finished = self.removePlayerLine
        self.visualChanges = True
        self.maxYSpc = self.signalProcessor.signal.samplingRate/2000
        self.minYSpc = 0
        self.refresh()

        #self.zoomNone()
        self.axesSpecgram.zoomRegion.setBounds([0,self._from_osc_to_spec(self.mainCursor.max)])
        self.axesOscilogram.getPlotItem().getViewBox().sigRangeChangedManually.connect(self._oscRangeChanged)
        self.axesSpecgram.viewBox.sigRangeChangedManually.connect(self._specRangeChanged)
        self.signalProcessor.signal.recordNotifier = self.on_newDataRecorded#self.newDataRecorded.emit
        self.signalProcessor.signal.playNotifier = self.playing.emit
        self.rangeChanged.emit(0, len(self.signalProcessor.signal.data), len(self.signalProcessor.signal.data))
        self.axesOscilogram.changeSelectedTool(Tools.Zoom)
        self.axesSpecgram.changeSelectedTool(Tools.Zoom)
        self.axesOscilogram.zoomRegion.setRegion([0,0])
        self.axesSpecgram.zoomRegion.setRegion([0,0])


    def save(self, fname):
        chunk = self.cursorsData()
        self.signalProcessor.signal.save(fname, chunk)

    def saveSelected(self,fname):
        indexF,indexTo = self.getIndexFromAndTo()
        chunk = self.cursorsData()
        signal = WavFileSignal(samplingRate=self.signalProcessor.signal.samplingRate,whiteNoise=False)
        signal.data = self.signalProcessor.signal.data[indexF:indexTo]
        signal.save(fname,chunk)


    def cursorsData(self):
        cursData = PointerCursor().intToByteArray(len(self.cursors))
        for x in self.cursors:
            if isinstance(x, PointerCursor):
                cursData.extend(bytearray([0, 0]))  # pcur ---> pointer cursor
            if isinstance(x, IntervalCursor):
                cursData.extend(bytearray([0, 1]))  # icur ---> interval cursor
            if isinstance(x, RectangularCursor):
                cursData.extend(bytearray([0, 2]))  # rcur ---> rectangular cursor
            data = x.toByteArray()
            cursData.extend(PointerCursor().intToByteArray(len(data)))
            cursData.extend(data)
        return bytearray(cursData)

    def loadUserData(self, userData):
        userData = bytearray(userData)
        if len(userData) == 0:
            return
        self.cursors = []
        index = 4
        size = 0
        cursor = PointerCursor()
        n = cursor.byteArrayToInt(bytearray(userData[0:4]))
        for i in range(n):
            type = bytearray(userData[index:index + 2])
            index += 2
            if type == bytearray([0, 0]):
                cursor = PointerCursor()
            if type == bytearray([0, 1]):
                cursor = IntervalCursor()
            if type == bytearray([0, 2]):
                cursor = RectangularCursor()
            size = PointerCursor().byteArrayToInt(userData[index:index + 4])
            index += 4
            cursor.fromByteArray(userData[index:index + size])
            index += size
            self.cursors.append(cursor)

    def SaveColorBar(self):
        state = self.axesSpecgram.getHistogramWidget().item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, "Save Color Bar", filter="Bar Files (*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()


    #endregion
    #endregion
