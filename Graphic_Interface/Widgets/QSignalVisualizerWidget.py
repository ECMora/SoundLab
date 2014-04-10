from datetime import datetime

from PyQt4.QtCore import pyqtSignal,QRect, Qt, QRectF
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
import pyqtgraph as pg
import numpy as np
import matplotlib.mlab as mlab
from pyqtgraph.Point import Point

from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements.Element import Element
from Duetto_Core.SignalProcessors.CommonSignalProcessor import CommonSignalProcessor
from Duetto_Core.SignalProcessors.FilterSignalProcessor import *
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor, envelope
from Duetto_Core.SignalProcessors.EditionSignalProcessor import EditionSignalProcessor

from Duetto_Core.SpecgramSettings import SpecgramSettings
from DuettoPlotWidget import DuettoPlotWidget
from Graphic_Interface.Widgets.DuettoImageWidget import DuettoImageWidget


class UndoRedoManager:
    def __init__(self):
        self.actionsList = [None for _ in range(20)] #initial space for actions
        self.actionIndex = 0

    def undo(self):
        if(self.actionIndex > 0):
            tuple = self.actionsList[self.actionIndex]
            if(tuple[0] is not None):
                tuple[0]()
            self.actionIndex -= 1

    def redo(self):
        if(self.actionIndex < len(self.actionsList)):
            tuple = self.actionsList[self.actionIndex]
            if(tuple[1] is not None):
                tuple[1]()
            self.actionIndex += 1

    def addAction(self,undoAction=None, redoAction=None):
        self.actionIndex += 1
        if(len(self.actionsList)<= self.actionIndex):
            list = [None for _ in range(2*len(self.actionsList))]
            for x,i in enumerate(self.actionsList):
                list[i] = x
            self.actionsList = list
        else:
            for i in range(self.actionIndex,len(self.actionsList)):
                self.actionsList[i] = (None,None)

        self.actionsList[self.actionIndex] = (undoAction,redoAction)




BACK_COLOR = "gray"

class OscXAxis(pg.AxisItem):
    def __init__(self,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.Fs = 1
        self.setLabel(text="Time (s)")

    def tickStrings(self, values, scale, spacing):
        strns = []
        s = "{:.2f}"
        for x in values:
            strns.append(s.format(x*1.0/self.Fs))
        return strns

    def tickSpacing(self, minVal, maxVal, size):
        return [(max((maxVal-minVal)/(10.0*self.Fs),0.01)*self.Fs,0)]

    def setFrequency(self,rate):
        self.Fs = rate


class OscYAxis(pg.AxisItem):
    def __init__(self,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.Max = 1
        self.setLabel(text="Amplitude (%)")

    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            strns.append("{:.0f}".format(x*100.0/self.Max))
        return strns

    def setMaxVal(self,maxVal):
        self.Max = maxVal

class Tools:
    """
    the tools for interaction with the signal in the QSignalVisualizerWidget.
    """
    Zoom,RectangularCursor,CircularEraser,RectangularEraser, OscilogramThreshold = range(5)


class QSignalVisualizerWidget(QWidget):
    """Class to represent the QSignalVisualizerWidget widget"""
    playing = pyqtSignal(int)
    rangeChanged = pyqtSignal(int, int, int)
    _doRefresh = pyqtSignal(bool, bool, bool, bool)

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.histogram = None
        self._Z = np.array([[0]])
        self.osc_gridx = True
        self.osc_gridy = True
        self.spec_gridx = True
        self.spec_gridy = True
        self.osc_color = QColor(255, 255, 255)
        self.axisXOsc = OscXAxis(orientation = 'bottom')
        self.axisYOsc = OscYAxis(orientation = 'left')
        self.axesOscilogram = DuettoPlotWidget(parent=self,axisItems={'bottom': self.axisXOsc,'left':self.axisYOsc})
        self.tool = Tools().Zoom
        self.osc_background = "000"
        self.spec_background = "000"
        self.undoRedoManager = UndoRedoManager()
        self.minYOsc = -100
        self.maxYOsc =  100
        self.minYSpc = 0
        self.maxYSpc = 22

        self.axesOscilogram.setMouseEnabled(x=False, y=False)
        self.axesOscilogram.getPlotItem().hideButtons()
        self.axesOscilogram.show()
        self.axesOscilogram.setRange(QRect(0,0,1,1))
        self.axesSpecgram = DuettoImageWidget(parent=self)
        self.axesSpecgram.show()

        self.axesOscilogram.IntervalOscChanged.connect(self.updateSpecZoomRegion)
        self.axesSpecgram.IntervalSpecChanged.connect(self.updateOscZoomRegion)

        layout = QVBoxLayout()
        layout.addWidget(self.axesOscilogram)
        layout.addWidget(self.axesSpecgram)
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        self.mousePressed = False
        self.movingCursorZoom = False
        self.lastX = 0
        #the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)
        #the zoom cursor
        self.zoomCursor = IntervalCursor(0, 0)
        self.axesOscilogram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
        self.axesSpecgram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
        #self.setLayout(layout)
        self.axesOscilogram.makeZoom = self.makeZoom  # metodo a ejecutar si se produce un zoom
        self.axesSpecgram.makeZoom = self.makeZoom
        self.zoomStep = 1
        self.visualChanges = False
        self._visibleOscillogram = False
        self._visibleSpectrogram = False
        self.axesOscilogram.setMenuEnabled(False)


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

        self._lastRecordRefresh = datetime.now()
        self._recordRefreshRate = 5

        self._doRefresh.connect(self._refresh)
        self.playing.connect(self.notifyPlayingCursor)

    def load_Theme(self,theme):
        """
        this method implements the  way in wich the controls load the theme
        all changes made by the theme are made in this place
        """
        self.osc_background = theme.osc_background
        self.osc_color = theme.osc_plot
        self.osc_gridx = theme.osc_GridX
        self.osc_gridy = theme.osc_GridY


    def createContextCursor(self,actions):
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        for act in actions:
            self.addAction(act)

    def updateSpecZoomRegion(self,a,b):
        min = self._from_osc_to_spec(a)
        max = self._from_osc_to_spec(b)
        self.axesSpecgram.emitIntervalSpecChanged = False
        self.axesSpecgram.zoomRegion.setRegion([min, max])
        self.axesSpecgram.emitIntervalSpecChanged = True
        self.stop()
        #self.axesSpecgram.update()

    def updateOscZoomRegion(self,a,b):
        min = self._from_spec_to_osc(a)
        max = self._from_spec_to_osc(b)
        self.axesOscilogram.emitIntervalOscChanged = False
        self.axesOscilogram.zoomRegion.setRegion([min, max])

        self.axesOscilogram.emitIntervalOscChanged = True

        self.stop()
        #self.axesOscilogram.update()
    #region Sound

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Left:
            self.zoomCursor.shift(-1)
            self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
            #self.axesSpecgram.zoomRegion.setRegion([self._from_osc_to_spec(self.zoomCursor.min),
            #                                        self._from_osc_to_spec(self.zoomCursor.max)])
        elif QKeyEvent.key() == Qt.Key_Right:
            self.zoomCursor.shift(1)
            self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
            #self.axesSpecgram.zoomRegion.setRegion([self._from_osc_to_spec(self.zoomCursor.min),
            #                                        self._from_osc_to_spec(self.zoomCursor.max)])
        elif QKeyEvent.key() == Qt.Key_Space:
            self.switchPlayStatus()

    def play(self):
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
            self.axesOscilogram.setVisible(self.visibleOscilogram)
            self.axesSpecgram.setVisible(self.visibleSpectrogram)
            self.visualChanges = True
            self.refresh()

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

    def removePlayerLine(self):
        if self.playerLineOsc in self.axesOscilogram.getPlotItem().getViewBox().addedItems:
            self.axesOscilogram.getPlotItem().getViewBox().removeItem(self.playerLineOsc)
        if self.playerLineSpec in self.axesSpecgram.viewBox.addedItems:
            self.axesSpecgram.viewBox.removeItem(self.playerLineSpec)

    def pause(self):
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
        return 1.0 * coord * (self.mainCursor.max - self.mainCursor.min) / self._Z.shape[1]

    def _from_osc_to_spec(self, coord):
        return 1.0 * coord * self._Z.shape[1] / (self.mainCursor.max - self.mainCursor.min)

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
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))
        #self.axesSpecgram.zoomRegion.setRegion([0, 0])

    def zoomIn(self):
        if not self.signalProcessor.signal.opened():
            return
        aux = (self.mainCursor.max - self.mainCursor.min) / (4 * self.zoomStep)
        if self.mainCursor.max - aux > self.mainCursor.min + aux:
            self.mainCursor.max -= aux
            self.mainCursor.min += aux
        self.visualChanges = True
        self.refresh(dataChanged=False)
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def zoomNone(self):
        if not self.signalProcessor.signal.opened():
            return
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        #self.clearZoomCursor()
        self.visualChanges = True
        self.refresh(dataChanged=False)
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def makeZoom(self, _min, _max, specCoords=False):
        if not self.signalProcessor.signal.opened():
            return
        if specCoords:
            _min = self._from_spec_to_osc(_min)
            _max = self._from_spec_to_osc(_max)
        self.changeRange(_min, _max)
        self.zoomCursor.max = self.zoomCursor.min
        self.axesOscilogram.zoomRegion.setRegion([self.zoomCursor.min, self.zoomCursor.max])
        self.axesSpecgram.zoomRegion.setRegion([self._from_osc_to_spec(self.zoomCursor.min),
                                                self._from_osc_to_spec(self.zoomCursor.max)])


    def changeRange(self, left, right, emit=True, updateOscillogram=True, updateSpectrogram=True):
        self.mainCursor.min, self.mainCursor.max = left, right
        self.visualChanges = True
        self.refresh(dataChanged=False, updateOscillogram=updateOscillogram, updateSpectrogram=updateSpectrogram)
        if emit:
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def on_newDataRecorded(self, frame_count):
        self.mainCursor.min = max(0, len(self.signalProcessor.signal.data) - 50000)
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        self.visualChanges = True
        self.refresh(updateSpectrogram=False)
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    SPECGRAM_YTICS_DECIMAL_PLACES = 5
    SPECGRAM_XTICS_DECIMAL_PLACES = 2
    SPECGRAM_COMPLEX_SIDE = "onesided"
    OSGRAM_XTICS_DECIMAL_PLACES = 4
    OSGRAM_FONTSIZE = 16

    TICK_INTERVAL_MS = 10
    INTERVAL_START_DECIMATION = 500000
    SPAN_RECT_PROPS = dict(facecolor='green', alpha=0.4)

    COLOR_INDEX = 0

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

    def refresh(self, dataChanged=True, updateOscillogram=True, updateSpectrogram=True, partial=False):
        # perform some heavy calculations
        width = self.axesSpecgram.viewBox.width()
        if self.visibleSpectrogram and updateSpectrogram and self.signalProcessor.signal \
           and self.signalProcessor.signal.opened() and self.signalProcessor.signal.playStatus != AudioSignal.RECORDING\
           and self.mainCursor.max > self.mainCursor.min and width:
            normOverlap = self.specgramSettings.overlap / 100.0
            if normOverlap < 0:
                normOverlap = 1 - 1.0 * (self.mainCursor.max-self.mainCursor.min) / (self.specgramSettings.NFFT * width)
            overlap = int(self.specgramSettings.NFFT * normOverlap)
            self.specgramSettings.Pxx, self.specgramSettings.freqs, self.specgramSettings.bins\
                = mlab.specgram(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max],
                                self.specgramSettings.NFFT, Fs=self.signalProcessor.signal.samplingRate,
                                detrend=mlab.detrend_none, window=self.specgramSettings.window, noverlap=overlap,
                                sides=self.SPECGRAM_COMPLEX_SIDE)
            self._Z = 10. * np.log10(self.specgramSettings.Pxx)
            #self._Z = np.flipud(self._Z)
            Zfin = np.isfinite(self._Z)
            if np.any(Zfin):
                m = self._Z[Zfin].min()
                self._Z[np.isneginf(self._Z)] = m
                cut_off = np.amin(self._Z[np.isfinite(self._Z)])
                self._Z[self._Z < cut_off] = cut_off
            else:
                self._Z[self._Z < -100] = -100
            self.axesSpecgram.yAxis.refresh(self.specgramSettings.freqs)
        # do actual refresh
        print(self._Z.shape)

        self._doRefresh.emit(dataChanged, updateOscillogram, updateSpectrogram, partial)

    def _refresh(self, dataChanged, updateOscillogram, updateSpectrogram, partial):

        if not self.visualChanges:
            return
        self.axesOscilogram.setRange(xRange=(self.mainCursor.min, self.mainCursor.max),
                                         yRange=(self.minYOsc*0.01*self.signalProcessor.signal.getMaximumValueAllowed(),
                                                 self.maxYOsc*0.01*self.signalProcessor.signal.getMaximumValueAllowed()), padding=0,update = True)

        if (self.visibleOscilogram or self.signalProcessor.signal.playStatus == AudioSignal.RECORDING) \
           and updateOscillogram and self.signalProcessor.signal and self.signalProcessor.signal.opened()\
           and self.mainCursor.max > self.mainCursor.min:
            #if self.mainCursor.max - self.mainCursor.min > 2 * self.INTERVAL_START_DECIMATION:
            #    length = (self.mainCursor.max - self.mainCursor.min)
            #    interval = length / self.INTERVAL_START_DECIMATION
            if dataChanged:
                self.axesOscilogram.plot(self.signalProcessor.signal.data, clear=True, pen=self.osc_color,
                                         autoDownsample=True, clipToView=partial)

            #self.axesOscilogram.setRange(xRange=(0, self.mainCursor.max - self.mainCursor.min))
            self.axesSpecgram.zoomRegion.setBounds([0, self._from_osc_to_spec(self.mainCursor.max)])
            self.axesOscilogram.zoomRegion.setBounds([0, self.mainCursor.max])
            self.axesOscilogram.setZoomRegionVisible(True)

        self.axesOscilogram.getPlotItem().showGrid(x=self.osc_gridx, y=self.osc_gridy)
        self.axesOscilogram.setBackground(self.osc_background)

        if self.visibleSpectrogram and updateSpectrogram and self.signalProcessor.signal \
           and self.signalProcessor.signal.opened() and self.signalProcessor.signal.playStatus != AudioSignal.RECORDING\
           and self.mainCursor.max > self.mainCursor.min:
            self.axesSpecgram.imageItem.setImage(numpy.transpose(self._Z))
            self.axesSpecgram.imageItem.setRect(QRectF(self._from_osc_to_spec(self.mainCursor.min), 0,
                                                       self._Z.shape[1], self._Z.shape[0]))
            self.axesSpecgram.viewBox.setRange(xRange=(self._from_osc_to_spec(self.mainCursor.min),
                                                       self._from_osc_to_spec(self.mainCursor.max)),
            YSpec = np.searchsorted(self.specgramSettings.freqs,[self.minYSpc*1000, self.maxYSpc*1000])
                                               yRange=(0, self._Z.shape[0]), padding=0)
            self.updateSpectrogramColors()
        self.axesSpecgram.setBackground(self.spec_background)
        self.axesSpecgram.showGrid(x=self.spec_gridx, y=self.spec_gridy)
        self.refreshAxes()
        self.visualChanges = False
        if self.visibleElements:
            self.drawElements()

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


    def drawElements(self):
        if(self.visibleOscilogram):
            for i in range(len(self.Elements)):
                if self.Elements[i].visible:
                    for item, visible in self.Elements[i].visualwidgets():
                        if(not item in self.axesOscilogram.items() and visible):
                            self.axesOscilogram.addItem(item)
                        elif item in self.axesOscilogram.items() and not visible:
                            self.axesOscilogram.removeItem(item)
                else:
                    for item, visible  in self.Elements[i].visualwidgets():
                        if(item in self.axesOscilogram.items()):
                            self.axesOscilogram.removeItem(item)
        if(self.visibleSpectrogram):
            for i in range(len(self.Elements)):
                for j in range(len(self.Elements[i].twoDimensionalElements)):
                    if self.Elements[i].twoDimensionalElements[j].visible:
                        for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            if(not item in self.axesSpecgram.items() and visible):
                                self.axesSpecgram.viewBox.addItem(item)
                            elif item in self.axesSpecgram.items() and not visible:
                                self.axesSpecgram.viewBox.removeItem(item)
                    else:
                        for item, visible  in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            if(item in self.axesSpecgram.items()):
                                self.axesSpecgram.viewBox.removeItem(item)

        self.axesOscilogram.update()
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
            self.signalProcessor.signal = f.filter(self.zoomCursor.min,self.zoomCursor.min+ms*self.signalProcessor.signal.samplingRate/1000.0,type,Fc,Fl,Fu)
            self.visualChanges=True
            self.refresh()

    def resampling(self,samplingRate):
        self.signalProcessor.signal.resampling(samplingRate)
        self.visualChanges=True
        self.refresh()

    def envelope(self):
        #add cofig dialog and plot the envelope
        indexFrom, indexTo = self.getIndexFromAndTo()
        y = envelope(self.signalProcessor.signal.data[indexFrom:indexTo],decay=self.signalProcessor.signal.samplingRate/1000)
        env_window = pg.PlotWidget()
        env_window.show()
        env_window.plot(y)




    def getIndexFromAndTo(self):
        indexFrom, indexTo = self.mainCursor.min, self.mainCursor.max
        if self.zoomCursor.min > 0 and self.zoomCursor.max > 0:
            indexFrom, indexTo = self.zoomCursor.min, self.zoomCursor.max
            #the delegate has the responsability of modify just the portion of the signal
            #given by indexFrom:indexTo for an eficient action.
        return indexFrom, indexTo

    def signalProcessingAction(self, delegate, *args):
        indexFrom, indexTo = self.getIndexFromAndTo()
        self.signalProcessor.signal = delegate(indexFrom, indexTo, *args)
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


    def detectElements(self,threshold=20, decay=1, minSize=0, softfactor=5, merge_factor=0,threshold2=0, threshold_spectral=95, pxx=[], freqs=[], bins=[], minsize_spectral=(0, 0),
               merge_factor_spectral=(1,1),location= None):
        self.clearCursors()
        self.elements_detector.detect(self.signalProcessor.signal,0,len(self.signalProcessor.signal.data), threshold, decay, minSize, softfactor, merge_factor,threshold2,
                                      threshold_spectral=threshold_spectral, pxx =  self.specgramSettings.Pxx, freqs=self.specgramSettings.freqs,
                                      bins=self.specgramSettings.bins, minsize_spectral=minsize_spectral,
               merge_factor_spectral=merge_factor_spectral,location=location)

        for c in self.elements_detector.elements():
            self.Elements.append(c)# the elment the space for the span selector and the text
        #incorporar deteccion en espectrograma
        self.visualChanges = True
        self.refresh()

    #endregion

    #region SAVE AND OPEN

    def openNew(self, samplingRate=1, bitDepth=8, duration=1, whiteNoise=False):
        self.open(None, samplingRate, bitDepth, duration, whiteNoise)

    def open(self, filename, samplingRate=1, bitDepth=8, duration=1, whiteNoise=False):
        #self.axesOscilogram.sigRangeChanged.disconnect()
        #self.axesSpecgram.viewBox.sigRangeChanged.disconnect()
        self.clear()
        if filename:
            self.signalProcessor.signal = WavFileSignal(filename)
        else:
            self.signalProcessor.signal = WavFileSignal(samplingRate=samplingRate, duration=duration, bitDepth=bitDepth,
                                                        whiteNoise=whiteNoise)
        self.cursors = []
        self.editionSignalProcessor = EditionSignalProcessor(self.signalProcessor.signal)
        #self.signalProcessor.signal.setTickInterval(self.TICK_INTERVAL_MS)
        #self.signalProcessor.signal.timer.timeout.connect(self.notifyPlayingCursor)

        if isinstance(self.signalProcessor.signal, WavFileSignal):
            self.loadUserData(self.signalProcessor.signal.userData)
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        if self.mainCursor.max / self.signalProcessor.signal.samplingRate > 10000:  # 10 seg
            self.mainCursor.max = 10000 * self.signalProcessor.signal.samplingRate
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
        self.axisXOsc.setFrequency(self.signalProcessor.signal.samplingRate)
        self.axisYOsc.setMaxVal(2**(self.signalProcessor.signal.bitDepth-1))
        self.maxYSpc = self.signalProcessor.signal.samplingRate / 2000
        self.refresh()
        self.zoomIn()
        self.zoomNone()
        self.axesOscilogram.getPlotItem().getViewBox().sigRangeChangedManually.connect(self._oscRangeChanged)
        self.axesSpecgram.viewBox.sigRangeChangedManually.connect(self._specRangeChanged)
        self.signalProcessor.signal.recordNotifier = self.on_newDataRecorded#self.newDataRecorded.emit
        self.signalProcessor.signal.playNotifier = self.playing.emit
        self.rangeChanged.emit(0, len(self.signalProcessor.signal.data), len(self.signalProcessor.signal.data))


    def save(self, fname):
        chunk = self.cursorsData()
        self.signalProcessor.signal = self.signalProcessor.signal.toWav()
        self.signalProcessor.signal.save(fname, chunk)

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
