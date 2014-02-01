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


BACK_COLOR = "gray"


class QSignalVisualizerWidget(QWidget):
    """Class to represent the QSignalVisualizerWidget widget"""

    rangeChanged = pyqtSignal(int, int, int)

    def __init__(self, parent):

        #self.figure = Figure(facecolor=BACK_COLOR)  # widget container of the axes
        #FigureCanvas.__init__(self, self.figure)
        # set the parent widget
        #self.setParent(parent)
        QWidget.__init__(self,parent)
        layout = QVBoxLayout()
        self.osc_gridx = True
        self.osc_grridy = True
        self.osc_color=QColor(255,255,255)
        self.axesOscilogram = pg.PlotWidget(parent=self)
        self.axesOscilogram.getPlotItem().enableAutoRange()

        self.axesSpecgram = pg.ImageView(parent=self)
        self.axesSpecgram.getView().enableAutoRange()

        self.setLayout(layout)
        self.mousePressed = False
        self.movingCursorZoom = False
        self.lastX = 0
        #the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)
        #the zoom cursor
        self.zoomCursor = IntervalCursor(0, 0)
        self.zoomStep = 1
        self.visualChanges = False
        self._visibleOscillogram = False
        self._visibleSpectrogram = False
        self.clear()
        self.signalProcessor = SignalProcessor()
        self.editionSignalProcessor = EditionSignalProcessor()
        self.specgramSettings = SpecgramSettings()
        self.cursors = []
        self.visibleCursors = True
        self.zoomIntervalPixels = (0, 0)
        self.colorbar = None
        self.meanSignalValue = None
        self.powerSpectrum = np.array([])
        self.playerSpeed = 100
        self.oscilogram_elements_detector = OneDimensionalElementsDetector()

    #region Sound

    def play(self):
        if self.zoomCursor.min > 0 and self.zoomCursor.max > 0:
            self.signalProcessor.signal.play(self.zoomCursor.min, self.zoomCursor.max, self.playerSpeed)
        else:
            self.signalProcessor.signal.play(self.mainCursor.min, self.mainCursor.max, self.playerSpeed)

    def switchPlayStatus(self):
        if self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING:
            self.stop()
        else:
            self.play()

    def stop(self):
        self.signalProcessor.signal.stop()

    def record(self):
        self.signalProcessor.signal.record()

    def pause(self):
        self.signalProcessor.signal.pause()

    def recordCursor(self):
        pass

    def notifyPlayingCursor(self):
        if (self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING or
                self.signalProcessor.signal.playStatus == self.signalProcessor.signal.RECORDING):
            index = self.signalProcessor.signal.currentPlayingTime()
            h = self.axesOscilogram.height
            rect = [self.fromClientToCanvas(index), 0, 1, h]
            self.figure.canvas.drawRectangle(rect)
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
        self._visibleOscillogram = value

    visibleOscilogram = property(_getVisibleOscilogram, _setVisibleOscilogram)

    def _getVisibleSpectrogram(self):
        return self._visibleSpectrogram

    def _setVisibleSpectrogram(self, value):
        self._visibleSpectrogram = value
        self.visualChanges = True

    visibleSpectrogram = property(_getVisibleSpectrogram, _setVisibleSpectrogram)
    #endregion

    #region VISUAL EVENTS AND ACTIONS

    #def dropEvent(self, event):
    #    data = event.mimeData().data()
    #    file= QtCore.QFile()
    #    file.setFileName("local.wav")
    #    file.write(data)
    #    file.close()
    #    event.accept()
    #    self.open("local.wav")
    #
    #def updateBackgroundSpanRectangle(self, event=None):
    #    """force an update of the background"""
    #    if self.visibleOscilogram:
    #        self.backgroundOscilogramSpanRectangle = self.figure.canvas.copy_from_bbox(self.figure.bbox)
    #    if self.visibleSpectrogram:
    #        self.backgroundSpectrogramSpanRectangle = self.figure.canvas.copy_from_bbox(self.axesSpecgram.bbox)
    #
    #def updateSpanSelector(self):
    #    if self.visibleOscilogram:
    #        self.spanRectangleOsgram.set_x(self.mainCursor.min)
    #        self.spanRectangleOsgram.set_width(self.mainCursor.max - self.mainCursor.min)
    #        self.spanRectangleOsgram.set_height(self.axesOscilogram.bbox.height)
    #        self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
    #        self.axesOscilogram.draw_artist(self.spanRectangleOsgram)
    #        self.figure.canvas.blit(self.axesOscilogram.bbox)
    #    if self.visibleSpectrogram:
    #        x1 = self.mainCursor.min
    #        x2 = self.mainCursor.max
    #        self.spanRectangleSpectrogram.set_x(x1)
    #        self.spanRectangleSpectrogram.set_width(x2 - x1)
    #        self.spanRectangleSpectrogram.set_height(self.axesSpecgram.bbox.height)
    #        self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
    #        self.axesSpecgram.draw_artist(self.spanRectangleSpectrogram)
    #        self.figure.canvas.blit(self.axesSpecgram.bbox)

    #def mouseMoveEvent(self, event):
        #FigureCanvas.mouseMoveEvent(self, event)
        #if self.visibleOscilogram or self.visibleSpectrogram:
        #    if not self.mousePressed and self.mouseInsideZoomArea(event.x()):
        #        self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        #    elif not self.mouseInsideZoomArea(event.x()):
        #        self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        #    minx, maxx = self.zoomIntervalPixels
        #    if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or abs(
        #                    maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
        #        self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
        #    h = self.figure.canvas.figure.bbox.height
        #    if self.mousePressed:
        #        axe = self.axesOscilogram
        #        if not self.visibleOscilogram:
        #            axe = self.axesSpecgram
        #        minx, maxx = axe.bbox.min[0], axe.bbox.max[0]
        #        a, b = max(minx, min(self.lastX, event.x())), min(maxx, max(self.lastX, event.x()))
        #        rect = [0, 0, 0, 0]
        #        if not self.movingCursorZoom and abs(self.lastX - event.x()) > self.PIXELS_OF_CURSORS_CHANGES:
        #            self.zoomIntervalPixels = (a, b)
        #            if self.visibleOscilogram:
        #                self.spanRectangleOsgram.set_x(self.fromCanvasToClient(a) - self.mainCursor.min)
        #                self.spanRectangleOsgram.set_width(self.fromCanvasToClient(b) - self.fromCanvasToClient(a))
        #                self.spanRectangleOsgram.set_height(self.axesOscilogram.bbox.height)
        #                self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
        #                self.axesOscilogram.draw_artist(self.spanRectangleOsgram)
        #                self.figure.canvas.blit(self.axesOscilogram.bbox)
        #            if self.visibleSpectrogram:
        #                x1 = self.specgramIndex(self.fromCanvasToClient(self.zoomIntervalPixels[0]))
        #                x2 = self.specgramIndex(self.fromCanvasToClient(self.zoomIntervalPixels[1]))
        #                self.spanRectangleSpectrogram.set_x(x1)
        #                self.spanRectangleSpectrogram.set_width(x2 - x1)
        #                self.spanRectangleSpectrogram.set_height(self.axesSpecgram.bbox.height)
        #                self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
        #                self.axesSpecgram.draw_artist(self.spanRectangleSpectrogram)
        #                self.figure.canvas.blit(self.axesSpecgram.bbox)
        #
        #                #if(self.visibleSpectrogram):
        #                #    self.figure.canvas.blit(self.axesSpecgram.bbox)
        #
        #        elif self.movingCursorZoom and abs(self.lastX - event.x()) > self.PIXELS_OF_CURSORS_CHANGES:
        #            self.zoomIntervalPixels = (self.zoomIntervalPixels[0] + event.x() - self.lastX,
        #                                       self.zoomIntervalPixels[1] + event.x() - self.lastX)
        #            self.lastX = event.x()
        #
        #            if self.visibleOscilogram:
        #                self.spanRectangleOsgram.set_x(
        #                    self.fromCanvasToClient(self.zoomIntervalPixels[0]) - self.mainCursor.min)
        #                self.spanRectangleOsgram.set_width(
        #                    self.fromCanvasToClient(self.zoomIntervalPixels[1]) - self.fromCanvasToClient(
        #                        self.zoomIntervalPixels[0]))
        #                self.spanRectangleOsgram.set_height(self.figure.canvas.figure.bbox.height)
        #                self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
        #                self.axesOscilogram.draw_artist(self.spanRectangleOsgram)
        #                self.figure.canvas.blit(self.axesOscilogram.bbox)
        #            if self.visibleSpectrogram:
        #                Osgramindex = self.fromCanvasToClient(self.zoomIntervalPixels[0])
        #                x1 = self.specgramIndex(Osgramindex)
        #                x2 = self.specgramIndex(self.fromCanvasToClient(self.zoomIntervalPixels[1]))
        #                self.spanRectangleSpectrogram.set_x(x1)
        #                self.spanRectangleSpectrogram.set_width(x2 - x1)
        #                self.spanRectangleSpectrogram.set_height(self.figure.canvas.figure.bbox.height)
        #                self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
        #                self.axesSpecgram.draw_artist(self.spanRectangleSpectrogram)
        #                self.figure.canvas.blit(self.axesSpecgram.bbox)

    #def specgramIndex(self,OsgramIndex):
    #    minxSpecgram,maxxSpecgram=self.axesSpecgram.get_xlim()
    #    return minxSpecgram+(OsgramIndex-self.mainCursor.min)*(maxxSpecgram-minxSpecgram)/(self.mainCursor.max-self.mainCursor.min)
    #
    #def mousePressEvent(self, event):
    #    #FigureCanvas.mousePressEvent(self, event)
    #    self.mousePressed = True
    #
    #    if self.mouseInsideZoomArea(event.x()):
    #        self.movingCursorZoom = True
    #        self.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
    #    self.lastX = event.x()
    #
    #    minx, maxx = self.zoomIntervalPixels
    #    if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
    #        self.movingCursorZoom = False
    #        self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
    #        self.lastX = maxx
    #    if abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
    #        self.movingCursorZoom = False
    #        self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
    #        self.lastX = minx
    #
    #def mouseInsideZoomArea(self, xPixel):
    #    #xIndex = self.fromCanvasToClient(xPixel)
    #    #return self.zoomCursor.min!=self.zoomCursor.max and xIndex>self.zoomCursor.min and xIndex<self.zoomCursor.max
    #    return xPixel >= self.zoomIntervalPixels[0] and xPixel <= self.zoomIntervalPixels[1]
    #
    #def mouseDoubleClickEvent(self, event):
    #    if self.mouseInsideZoomArea(event.x()):
    #        self.mainCursor.min, self.mainCursor.max = self.zoomCursor.min, self.zoomCursor.max
    #        self.visualChanges = True
    #        self.refresh()
    #        self.clearZoomCursor()
    #        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))
    #
    #def deselectZoomRegion(self):
    #    self.clearZoomCursor()
    #    if self.visibleOscilogram:
    #        self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
    #        self.figure.canvas.blit(self.axesOscilogram.bbox)
    #    if self.visibleSpectrogram:
    #        self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
    #        self.figure.canvas.blit(self.axesSpecgram.bbox)
    #
    #def mouseReleaseEvent(self, event):
    #    #FigureCanvas.mouseReleaseEvent(self, event)
    #    if self.movingCursorZoom:
    #        self.zoomCursor.min = self.fromCanvasToClient(self.zoomIntervalPixels[0])
    #        self.zoomCursor.max = self.fromCanvasToClient(self.zoomIntervalPixels[1])
    #    if (self.visibleOscilogram or self.visibleSpectrogram) and not self.movingCursorZoom \
    #        and abs(self.lastX - event.x()) > self.PIXELS_OF_CURSORS_CHANGES:
    #        minx, maxx = min(event.x(), self.lastX), max(event.x(), self.lastX)
    #        self.zoomCursor.min = max(0, self.fromCanvasToClient(minx))
    #        self.zoomCursor.max = min(self.fromCanvasToClient(maxx), len(self.signalProcessor.signal.data))
    #        if abs(self.zoomCursor.min - self.zoomCursor.max) < self.PIXELS_OF_CURSORS_CHANGES:
    #            self.zoomCursor.min, self.zoomCursor.max = 0, 0
    #        self.visualChanges = True
    #        self.lastX = event.x()
    #    if self.mouseInsideZoomArea(event.x()):
    #        self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
    #    else:
    #        self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
    #    self.movingCursorZoom = False
    #    self.mousePressed = False
    #    self.emit(SIGNAL("IntervalChanged"))
    #
    #def fromClientToCanvas(self, indexX):
    #    """
    #   Translates the index in the signal array to its corresponding coordinates in the canvas
    #   """
    #    if self.visibleOscilogram or self.visibleSpectrogram:
    #        axe = self.axesOscilogram
    #        if not self.visibleOscilogram:
    #            axe = self.axesSpecgram
    #        minx, maxx = axe.bbox.min[0], axe.bbox.max[0]
    #        a, b = self.mainCursor.min, self.mainCursor.max
    #        return minx + (maxx - minx) * (indexX - a) * 1. / (b - a)
    #
    #def fromCanvasToClient(self, xPixel):
    #    """
    #    Translates the coordinates from the canvas to its corresponding  index in the signal array
    #    """
    #    if self.visibleOscilogram or self.visibleSpectrogram:
    #        axe = self.axesOscilogram
    #        if not self.visibleOscilogram:
    #            axe = self.axesSpecgram
    #        minx, maxx = axe.bbox.min[0], axe.bbox.max[0]
    #        a, b = self.axesOscilogram.get_xlim()
    #        if xPixel < minx:
    #            xPixel = minx
    #        if xPixel > maxx:
    #            xPixel = maxx
    #
    #        return self.mainCursor.min + int((xPixel - minx) * (b - a) * 1. / (maxx - minx))

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
        self.refresh()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def zoomIn(self):
        aux = (self.mainCursor.max - self.mainCursor.min) / (4 * self.zoomStep)
        if self.mainCursor.max - aux > self.mainCursor.min + aux:
            self.mainCursor.max -= aux
            self.mainCursor.min += aux
        self.visualChanges = True
        self.refresh()
        self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def zoomNone(self):
        if self.signalProcessor.signal.opened():
            self.mainCursor.min = 0
            self.mainCursor.max = len(self.signalProcessor.signal.data)
            self.clearZoomCursor()
            self.visualChanges = True
            self.refresh()
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    def changeRange(self, left, right, emit=True):
        self.mainCursor.min, self.mainCursor.max = left, right
        self.visualChanges = True
        self.refresh()
        if emit:
            self.rangeChanged.emit(self.mainCursor.min, self.mainCursor.max, len(self.signalProcessor.signal.data))

    SPECGRAM_YTICS_DECIMAL_PLACES = 5
    SPECGRAM_XTICS_DECIMAL_PLACES = 2
    SPECGRAM_COMPLEX_SIDE = "onesided"
    OSGRAM_XTICS_DECIMAL_PLACES = 4
    OSGRAM_FONTSIZE = 16
    PIXELS_OF_CURSORS_CHANGES = 3
    TICK_INTERVAL_MS = 25
    INTERVAL_START_DECIMATION = 1000000
    SPAN_RECT_PROPS = dict(facecolor='green', alpha=0.4)

    COLOR_INDEX = 0

    def refresh(self):
        if self.visualChanges:
            if self.visibleOscilogram and self.signalProcessor.signal.opened() and self.mainCursor.max > self.mainCursor.min:
                self.axesOscilogram.clear()
                if((self.mainCursor.max-self.mainCursor.min)>2*self.INTERVAL_START_DECIMATION):
                    length = (self.mainCursor.max-self.mainCursor.min)
                    interval = length/self.INTERVAL_START_DECIMATION
                    self.axesOscilogram.plot(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max:interval],pen=self.osc_color)
                else:
                    self.axesOscilogram.plot(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max],pen=self.osc_color)
                self.axesOscilogram.setLabels(bottom="10ms")

                self.axesOscilogram.getPlotItem().showGrid(x=self.osc_gridx, y=self.osc_gridy)
            if self.visibleSpectrogram and self.signalProcessor.signal.opened() and self.mainCursor.max > self.mainCursor.min:
                overlap = int(self.specgramSettings.NFFT * self.specgramSettings.overlap / 100)

                self.specgramSettings.Pxx , self.specgramSettings.freqs, self.specgramSettings.bins = mlab.specgram(
                    self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max],
                    self.specgramSettings.NFFT, Fs=self.signalProcessor.signal.samplingRate, detrend=mlab.detrend_none, window=self.specgramSettings.window,
                    noverlap=overlap, sides=self.SPECGRAM_COMPLEX_SIDE)

                Z = 10. * np.log10(self.specgramSettings.Pxx)
                Z = np.flipud(Z)

                cut_off = np.percentile(Z,self.specgramSettings.threshold)
                Z[Z < cut_off] = cut_off

                self.axesSpecgram.getView().setAspectLocked(False)
                self.axesSpecgram.setImage(numpy.transpose(Z))
            self.visualChanges = False

    def cursorZoomTransform(self, cursorIndex):
        return cursorIndex - self.mainCursor.min

    def drawCursors(self):
        ax = None
        xlimLeft, xlimRigth = 0, 0
        for i in range(len(self.cursors)):
            if self.cursors[i].visualOptions.visible:
                if self.cursors[i].visualOptions.oscilogramCursor and self.visibleOscilogram:
                    ax = self.axesOscilogram
                elif not self.cursors[i].visualOptions.oscilogramCursor and self.visibleSpectrogram:
                    ax = self.axesSpecgram
                if ax != None:
                    if isinstance(self.cursors[i], PointerCursor):
                        if self.cursors[i].visualOptions.vertical:
                            xlimLeft, xlimRigth = ax.get_xlim()
                            xlimLeft, xlimRigth = xlimLeft + self.mainCursor.min, xlimRigth + self.mainCursor.min
                            if self.cursors[i].index > xlimLeft and self.cursors[i].index < xlimRigth:
                                ax.plot([self.cursorZoomTransform(self.cursors[i].index),
                                         self.cursorZoomTransform(self.cursors[i].index)], ax.get_ylim())
                        else:
                            xlimLeft, xlimRigth = ax.get_ylim()
                            if self.cursors[i].index > xlimLeft and self.cursors[i].index < xlimRigth:
                                ax.plot(ax.get_xlim(), [self.cursors[i].index, self.cursors[i].index])

                    elif isinstance(self.cursors[i], IntervalCursor):
                        if self.cursors[i].visualOptions.vertical:
                            a, b = ax.get_ylim()
                            xlimLeft, xlimRigth = ax.get_xlim()
                            xlimLeft, xlimRigth = xlimLeft + self.mainCursor.min, xlimRigth + self.mainCursor.min
                            if self.cursors[i].min > xlimLeft and xlimRigth > self.cursors[i].max > xlimLeft and \
                                            self.cursors[i].max < xlimRigth:  # replace with lim for horizontal cursors
                                ax.plot(
                                    [self.cursorZoomTransform(self.cursors[i].min),
                                     self.cursorZoomTransform(self.cursors[i].min),
                                     self.cursorZoomTransform(self.cursors[i].max),
                                     self.cursorZoomTransform(self.cursors[i].max),
                                     self.cursorZoomTransform(self.cursors[i].min)],
                                    [a, b, b, a, a])
                        else:
                            a, b = ax.get_xlim()
                            xlimLeft, xlimRigth = ax.get_ylim()
                            if self.cursors[i].min > xlimLeft and xlimLeft < self.cursors[
                                i].max < xlimRigth < xlimRigth:
                                ax.plot([a, a, b, b, a],
                                        [self.cursors[i].min, self.cursors[i].max, self.cursors[i].max,
                                         self.cursors[i].min, self.cursors[i].min])
                    elif isinstance(self.cursors[i], RectangularCursor):
                        a, b = self.cursors[i].intervalY.min, self.cursors[i].intervalY.max
                        xlimLeft, xlimRigth = ax.get_xlim()
                        xlimLeft, xlimRigth = xlimLeft + self.mainCursor.min, xlimRigth + self.mainCursor.min
                        ylimLeft, ylimRigth = ax.get_ylim()
                        if ylimLeft < a < ylimRigth and ylimLeft < b < ylimRigth \
                            and xlimLeft < self.cursors[i].intervalX.min < xlimRigth \
                            and xlimLeft < self.cursors[i].intervalX.max < xlimRigth:
                            ax.plot([self.cursorZoomTransform(self.cursors[i].intervalX.min),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.min),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.max),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.max),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.min)],
                                    [a, b, b, a, a])
            ax = None

    def clear(self):
        self.colorbar = None
        layout = QVBoxLayout()
        self.layout().removeWidget(self.axesOscilogram)
        self.layout().removeWidget(self.axesSpecgram)
        self.axesSpecgram.setGeometry(QRect(0,0,0,0))
        self.axesOscilogram.setGeometry(QRect(0,0,0,0))
        if self.visibleOscilogram:
            self.layout().addWidget(self.axesOscilogram)
        if self.visibleSpectrogram:
            self.layout().addWidget(self.axesSpecgram)


    def clearZoomCursor(self):
        self.zoomCursor.min, self.zoomCursor.max = 0, 0
        self.zoomIntervalPixels = (0, 0)
        self.movingCursorZoom = False

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
        ax.set_xticklabels([round(x * 1.0 / self.signalProcessor.signal.samplingRate,self.OSGRAM_XTICS_DECIMAL_PLACES) for x in self.axesOscilogram.get_xticks()])
        ax.set_yticklabels([str(int(y * 500 /(2**self.signalProcessor.signal.bitDepth)))+"dB" for y in self.axesOscilogram.get_yticks()])
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
        self.cursors.append(cursor)
        self.visualChanges = True
        self.refresh()

    def clearCursors(self):
        self.cursors = []

    def detectElementsInOscilogram(self,threshold=20, decay=1, minSize=0, softfactor=5, merge_factor=0,threshold2=0):
        indexFrom, indexTo = self.getIndexFromAndTo()
        self.oscilogram_elements_detector.detect(self.signalProcessor.signal,indexFrom, indexTo, threshold, decay, minSize, softfactor, merge_factor,threshold2)
        for c in self.oscilogram_elements_detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def maxMinPeaks(self):
        detector = MaxMinPeakDetector()
        indexFrom, indexTo = self.getIndexFromAndTo()
        detector.detect(self.signalProcessor.signal, indexFrom, indexTo)
        for c in detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def mean(self):
        detector = MeanDetector()
        detector.detect(self.signalProcessor.signal, max(self.zoomCursor.min, self.mainCursor.min),
                        min(self.zoomCursor.max, self.mainCursor.max))
        for c in detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    #endregion

    #region SAVE AND OPEN

    def open(self, filename):
        self.clear()
        self.signalProcessor.signal.open(filename)
        self.cursors = []
        self.editionSignalProcessor = EditionSignalProcessor(self.signalProcessor.signal)
        self.signalProcessor.signal.setTickInterval(self.TICK_INTERVAL_MS)
        self.signalProcessor.signal.timer.timeout.connect(self.notifyPlayingCursor)

        if isinstance(self.signalProcessor.signal, WavFileSignal):
            self.loadUserData(self.signalProcessor.signal.userData)
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        if self.mainCursor.max / self.signalProcessor.signal.samplingRate > 10000:  # 10 seg
            self.mainCursor.max = 10000 * self.signalProcessor.signal.samplingRate
        #self.powerSpectrum = real(fft(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max]))
        #self.meanSignalValue = real(np.mean(self.powerSpectrum))
        #self.max_specgram_value = max(self.powerSpectrum)
        #self.min_specgram_value = min(self.powerSpectrum)
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