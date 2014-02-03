from PyQt4.QtCore import pyqtSignal,QRect
from PyQt4.QtGui import *
from PyQt4 import QtCore
import pyqtgraph as pg
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory
import numpy as np
import matplotlib.mlab as mlab
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.image import imsave
from numpy.lib.function_base import percentile
from PyQt4.QtCore import SIGNAL
import matplotlib.pyplot as plt
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
from Duetto_Core.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from Duetto_Core.Detectors.ElementsDetectors.SpectrogramHillDetector import SpectrogramHillDetector
from Duetto_Core.Detectors.FeatureExtractionDetectors import MeanDetector, MaxMinPeakDetector
from Duetto_Core.SignalProcessors.CommonSignalProcessor import CommonSignalProcessor
from Duetto_Core.SignalProcessors.FilterSignalProcessor import *
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor, envelope
from Duetto_Core.SignalProcessors.EditionSignalProcessor import EditionSignalProcessor
from Duetto_Core.SpecgramSettings import SpecgramSettings
from DuettoPlotWidget import DuettoPlotWidget


BACK_COLOR = "gray"


class QSignalVisualizerWidget(QWidget):
    """Class to represent the QSignalVisualizerWidget widget"""

    rangeChanged = pyqtSignal(int, int, int)

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self._Z = np.array([[0]])
        self.osc_gridx = True
        self.osc_gridy = True
        self.osc_color=QColor(255,255,255)

        self.axesOscilogram = DuettoPlotWidget(parent=self)
        self.osc_background = "000"
        self.spec_background = "000"
        self.axesOscilogram.getPlotItem().enableAutoRange()

        self.axesOscilogram.setMouseEnabled(x=False, y=False)
        self.axesOscilogram.show()

        self.axesSpecgram = pg.ImageView(parent=self)
        self.axesSpecgram.getView().setMouseEnabled(x=False, y=False)
        self.axesSpecgram.getView().setAspectLocked(False)
        self.axesSpecgram.show()

        self.axesSpecgram.getView().enableAutoRange()
        layout = QVBoxLayout()
        layout.addWidget(self.axesOscilogram)
        layout.addWidget(self.axesSpecgram)
        self.setLayout(layout)

        self.mousePressed = False
        self.movingCursorZoom = False
        self.lastX = 0
        #the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)
        #the zoom cursor
        self.zoomCursor = IntervalCursor(0, 0)
        self.axesOscilogram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
        #self.setLayout(layout)
        self.axesOscilogram.makeZoom = self.makeZoom # metodo a ejecutar si se produce un zoom


        self.zoomStep = 1
        self.visualChanges = False
        self._visibleOscillogram = False
        self._visibleSpectrogram = False

        self.clear()

        self.signalProcessor = SignalProcessor()
        self.editionSignalProcessor = EditionSignalProcessor()
        self.specgramSettings = SpecgramSettings()
        self.cursors = []
        self.cursorsmarkers = []  #the rectangles for the visualizations of cursors
        self.visibleCursors = True

        self.colorbar = None
        self.playerSpeed = 100
        self.playerLine = pg.InfiniteLine(bounds=[-1,1])
        self.oscilogram_elements_detector = OneDimensionalElementsDetector()

    #region Sound

    def play(self):
        if self.zoomCursor.min > 0 and self.zoomCursor.max > 0:
            self.signalProcessor.signal.play(self.zoomCursor.min, self.zoomCursor.max, self.playerSpeed)
            self.createPlayerLine(self.zoomCursor.min-self.mainCursor.min)
        else:
            self.signalProcessor.signal.play(self.mainCursor.min, self.mainCursor.max, self.playerSpeed)
            self.createPlayerLine(self.mainCursor.min)

    def switchPlayStatus(self):
        if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING:
            self.stop()
        else:
            self.play()

    def stop(self):
        self.signalProcessor.signal.stop()
        self.removePlayerLine()

    def record(self):
        self.signalProcessor.signal.record()
        self.createPlayerLine(self.mainCursor.min)

    def createPlayerLine(self,value):
        #creates the player cursor to display the signal playing speed
        self.playerLine.setBounds((-2**(self.signalProcessor.signal.bitDepth-1),2**(self.signalProcessor.signal.bitDepth-1)))
        self.playerLine.setValue(value)
        if(self.playerLine in self.axesOscilogram.items()):
            self.axesOscilogram.removeItem(self.playerLine)
        self.axesOscilogram.addItem(self.playerLine)

    def removePlayerLine(self):
        if(self.playerLine in self.axesOscilogram.items()):
            self.axesOscilogram.removeItem(self.playerLine)

    def pause(self):
        self.signalProcessor.signal.pause()

    def notifyPlayingCursor(self):
        if (self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING or
                self.signalProcessor.signal.playStatus == self.signalProcessor.signal.RECORDING):
            index = self.signalProcessor.signal.currentPlayingTime()
            #draw the line in the axes
            self.playerLine.setValue(index-self.mainCursor.min)
            self.axesOscilogram.update()

            if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.RECORDING:
                size = len(self.signalProcessor.signal.data)
                self.mainCursor.min, self.mainCursor.max = 5 * size / 10, 9 * size / 10
                self.visualChanges = True
                self.refresh()
                self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))


    #endregion

    #region Property oscilogram and specgram Visibility

    def _getVisibleOscilogram(self):
        return self._visibleOscillogram

    def _setVisibleOscilogram(self, value):
        self.visualChanges = True
        self.visualChanges = True
        self._visibleOscillogram = value

    visibleOscilogram = property(_getVisibleOscilogram, _setVisibleOscilogram)

    def _getVisibleSpectrogram(self):
        return self._visibleSpectrogram

    def _setVisibleSpectrogram(self, value):
        self._visibleSpectrogram = value
        self.visualChanges = True
        self.visualChanges = True

    visibleSpectrogram = property(_getVisibleSpectrogram, _setVisibleSpectrogram)
    #endregion

    #region VISUAL EVENTS AND ACTIONS
    def updatezoomcursor(self):
        #actualiza los cursores de zoom segun el area seleccionada por el usuario
        range = self.axesOscilogram.zoomRegion.getRegion()
        self.zoomCursor.min ,self.zoomCursor.max = self.mainCursor.min + int(range[0]),self.mainCursor.min + int(range[1])


    def dropEvent(self, event):
        data = event.mimeData().data()
        file= QtCore.QFile()
        file.setFileName("local.wav")
        file.write(data)
        file.close()
        event.accept()
        self.open("local.wav")



    def deselectZoomRegion(self):
        self.clearZoomCursor()
        self.visualChanges = True
        self.refresh()



    def _oscRangeChanged(self, window, viewRange):
        if not isinstance(viewRange, list):
            return
        [left, right] = viewRange[0]
        if (left, right) == (self.mainCursor.min, self.mainCursor.max):
            return
        self.changeRange(left, right, updateOscillogram=False)

    def _specRangeChanged(self, window, viewRange):
        if not isinstance(viewRange, list):
            return
        [left, right] = viewRange[0]
        (left, right) = self._from_spec_to_osc(left), self._from_spec_to_osc(right)
        if (left, right) == (self.mainCursor.min, self.mainCursor.max):
            return
        self.changeRange(left, right, updateSpectrogram=False)

    def _from_spec_to_osc(self, coord):
        return coord * len(self.signalProcessor.signal.data) / self._Z.shape[1]

    def zoomOut(self):
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

    def zoomIn(self):
        aux = (self.mainCursor.max - self.mainCursor.min) / (4 * self.zoomStep)
        if self.mainCursor.max - aux > self.mainCursor.min + aux:
            self.mainCursor.max -= aux
            self.mainCursor.min += aux
        self.visualChanges = True
        self.refresh(dataChanged=False)
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def zoomNone(self):
        if self.signalProcessor.signal.opened():
            self.mainCursor.min = 0
            self.mainCursor.max = len(self.signalProcessor.signal.data)
            self.clearZoomCursor()
            self.visualChanges = True
            self.refresh(dataChanged=False)
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def makeZoom(self,min,max):
        self.mainCursor.min, self.mainCursor.max = min, max
        self.visualChanges = True
        self.refresh()
        self.clearZoomCursor()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def changeRange(self, left, right, emit=True, updateOscillogram=True, updateSpectrogram=True):
        self.mainCursor.min, self.mainCursor.max = left, right
        self.visualChanges = True
        self.refresh(dataChanged=False, updateOscillogram=updateOscillogram, updateSpectrogram=updateSpectrogram)
        if emit:
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

    def refresh(self, dataChanged=True, updateOscillogram=True, updateSpectrogram=True):
        if not self.visualChanges:
            return
        if self.visibleOscilogram and updateOscillogram and self.signalProcessor.signal.opened()\
                and self.mainCursor.max > self.mainCursor.min:
            #if self.mainCursor.max - self.mainCursor.min > 2 * self.INTERVAL_START_DECIMATION:
            #    length = (self.mainCursor.max - self.mainCursor.min)
            #    interval = length / self.INTERVAL_START_DECIMATION
            if dataChanged:
                self.axesOscilogram.plot(self.signalProcessor.signal.data, clear=True)

                self.axesOscilogram.setRange(xRange=(0,self.mainCursor.max-self.mainCursor.min))
                self.axesOscilogram.zoomRegion.setBounds([0, self.mainCursor.max-self.mainCursor.min])
                self.axesOscilogram.setZoomRegionVisible(True)
                self.axesOscilogram.getPlotItem().showGrid(x=True, y=True)
                self.axesOscilogram.setRange(xRange=(self.mainCursor.min, self.mainCursor.max),
                                         yRange=(self.signalProcessor.signal.getMinimumValueAllowed(),
                                                 self.signalProcessor.signal.getMaximumValueAllowed()), padding=0)

        if self.visibleSpectrogram and updateSpectrogram and self.signalProcessor.signal.opened() \
                and self.mainCursor.max > self.mainCursor.min:
            if dataChanged:
                overlap = int(self.specgramSettings.NFFT * self.specgramSettings.overlap / 100)
                self.specgramSettings.Pxx , self.specgramSettings.freqs, self.specgramSettings.bins = mlab.specgram(
                    self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max],
                    self.specgramSettings.NFFT, Fs=self.signalProcessor.signal.samplingRate, detrend=mlab.detrend_none, window=self.specgramSettings.window,
                    noverlap=overlap, sides=self.SPECGRAM_COMPLEX_SIDE)
                self.specgramSettings.Pxx, self.specgramSettings.freqs, self.specgramSettings.bins\
                    = mlab.specgram(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max],
                                    self.specgramSettings.NFFT, Fs=2, detrend=mlab.detrend_none,
                                    window=self.specgramSettings.window, noverlap=overlap, sides=self.SPECGRAM_COMPLEX_SIDE)
                self._Z = 10. * np.log10(self.specgramSettings.Pxx)
                self._Z = np.flipud(self._Z)
                Zfin = np.isfinite(self._Z)
                if not np.any(Zfin):
                    return
                m = self._Z[Zfin].min()
                self._Z[np.isneginf(self._Z)] = m
                cut_off = np.amin(self._Z[np.isfinite(self._Z)])
                self._Z[self._Z < cut_off] = cut_off
                self.axesSpecgram.setImage(numpy.transpose(self._Z))
                self.axesSpecgram.getView().setAspectLocked(False)

                self.axesSpecgram.getHistogramWidget().setVisible(False)
                self.axesSpecgram.ui.roiBtn.visible=False
            osc_spec_ratio = len(self.signalProcessor.signal.data) / self._Z.shape[1]
            self.axesSpecgram.getView().setRange(xRange=(self.mainCursor.min / osc_spec_ratio,
                                                         self.mainCursor.max / osc_spec_ratio),
                                                 yRange=(0, self._Z.shape[0]), padding=0)

            self.visualChanges = False
            if(self.visibleCursors):
                self.drawCursors()


    def cursorZoomTransform(self, cursorIndex):
        return cursorIndex - self.mainCursor.min

    def drawCursors(self):
        if(self.visibleOscilogram):
            self.cursorsmarkers = [None for _ in self.cursors]
            for i in range(len(self.cursors)):
                if self.cursors[i].visualOptions.visible:
                    self.cursorsmarkers[i] = pg.LinearRegionItem([self.cursors[i].min,self.cursors[i].max], movable=False,brush=(pg.mkBrush((0, 255, 0, 70)) if i%2==0 else pg.mkBrush((0, 0, 255,70))))
                    self.axesOscilogram.addItem(self.cursorsmarkers[i])
        self.axesOscilogram.update()




    def clear(self):
        self.colorbar = None

    def clearZoomCursor(self):
        self.zoomCursor.min, self.zoomCursor.max = 0, 0
        self.axesOscilogram.zoomRegion.setBounds((self.mainCursor.min,self.mainCursor.min))
        self.axesOscilogram.setZoomRegionVisible(False)

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
        x = np.arange(len(y))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        l, = plt.plot(x, y)
        t = ax.set_title('Envelope')
        plt.show()

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

    def scale(self, factor, function="normalize",fade="IN"):
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

    def cleanVisibleCursors(self):
        for r in self.cursorsmarkers:
            self.axesOscilogram.removeItem(r)
        self.cursorsmarkers = []

    def spectrogramsElevations(self, settings):
        signal = self.signalProcessor.signal
        detector = SpectrogramHillDetector()
        detector.detect(self.signalProcessor.signal, settings['threshold'], self.specgramSettings.Pxx,
                        self.specgramSettings.freqs * signal.samplingRate / 2.0,
                        1.0 * self.specgramSettings.bins / self.signalProcessor.signal.samplingRate,
                        threshold_is_percentile=settings['percentileThreshold'],
                        minsize=(settings['minSizeFreq'] * 1000, settings['minSizeTime'] / 1000.0),
                        merge_factor=(settings['mergeFactorTime'], settings['mergeFactorFreq']))
        imsave('last.png', detector.markedPxx, format='png', origin='lower')
        for c in detector.cursors():
            c.visualOptions.visible = True
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def rms(self):
        indexFrom, indexTo = self.getIndexFromAndTo()
        cursor = PointerCursor(self.signalProcessor.rms(indexFrom, indexTo))
        cursor.visualOptions.vertical = False
        self.clearCursors()
        self.cursors.append(cursor)
        self.visualChanges = True
        self.refresh()

    def clearCursors(self):
        self.cursors = []
        self.cleanVisibleCursors()

    def detectElementsInOscilogram(self,threshold=20, decay=1, minSize=0, softfactor=5, merge_factor=0,threshold2=0):
        indexFrom, indexTo = self.getIndexFromAndTo()
        self.oscilogram_elements_detector.detect(self.signalProcessor.signal,indexFrom, indexTo, threshold, decay, minSize, softfactor, merge_factor,threshold2)
        self.clearCursors()
        for c in self.oscilogram_elements_detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def maxMinPeaks(self):
        detector = MaxMinPeakDetector()
        indexFrom, indexTo = self.getIndexFromAndTo()
        detector.detect(self.signalProcessor.signal, indexFrom, indexTo)
        self.clearCursors()
        for c in detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def mean(self):
        detector = MeanDetector()
        detector.detect(self.signalProcessor.signal, max(self.zoomCursor.min, self.mainCursor.min),
                        min(self.zoomCursor.max, self.mainCursor.max))
        self.clearCursors()

        self.visualChanges = True
        self.refresh()

    #endregion

    #region SAVE AND OPEN

    def open(self, filename):
        self.clear()
        self.signalProcessor.signal.open(filename)
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
            self.axesOscilogram.zoomRegion.setBounds([self.mainCursor.min,self.mainCursor.max])
            self.axesOscilogram.setRange(QRect(0,-2**(self.signalProcessor.signal.bitDepth-1),self.mainCursor.max-self.mainCursor.min,2**self.signalProcessor.signal.bitDepth),padding=0)
            self.axesOscilogram.zoomRegion.sigRegionChanged.connect(self.updatezoomcursor)
            self.signalProcessor.signal.play_finished = self.removePlayerLine
        self.visualChanges = True

        self.refresh()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

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