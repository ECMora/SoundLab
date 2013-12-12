from PyQt4.QtGui import *
from PyQt4 import QtCore
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory
import numpy as np
import matplotlib.mlab as mlab
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from numpy.lib.function_base import percentile
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
from Duetto_Core.Detectors.ElementsDetector import ElementDetector
from Duetto_Core.Detectors.SpectrogramHillDetector import SpectrogramHillDetector
from Duetto_Core.Detectors.MaxMinPeakDetector import MaxMinPeakDetector
from Duetto_Core.Detectors.MeanDetector import MeanDetector
from Duetto_Core.Detectors.SegmenterDetector import SegmenterDetector
from Duetto_Core.SignalProcessors.CommonSignalProcessor import CommonSignalProcessor
from Duetto_Core.SignalProcessors.FilterSignalProcessor import *
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
from Duetto_Core.SignalProcessors.EditionSignalProcessor import EditionSignalProcessor
from Duetto_Core.SpecgramSettings import SpecgramSettings
import matplotlib.cm as cm

BACK_COLOR="gray"
class QSignalVisualizerWidget(FigureCanvas):
    """Class to represent the QSignalVisualizerWidget widget"""

    def __init__(self, parent):
        self.figure = Figure(facecolor=BACK_COLOR)#widget container of the axes
        self.mousePressed = False
        self.movingCursorZoom = False
        self.lastX = 0
        #the cursor for the visualization of a piece of the signal
        self.mainCursor = IntervalCursor(0, 0)
        #the zoom cursor
        self.zoomCursor = IntervalCursor(0, 0)
        self.zoomStep = 1
        self.visualChanges = False
        self._visibleOscilogram = False
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
        self.playerSpeed=100
        self.detector = ElementDetector()

        FigureCanvas.__init__(self, self.figure)
        # set the parent widget
        self.setParent(parent)

        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)

    #region  Sound

    def play(self):
        if(self.zoomCursor.min > 0 and self.zoomCursor.max > 0):
            self.signalProcessor.signal.play(self.zoomCursor.min,self.zoomCursor.max,self.playerSpeed)
        else:
            self.signalProcessor.signal.play(self.mainCursor.min,self.mainCursor.max,self.playerSpeed)


    def switchPlayStatus(self):
        if(self.signalProcessor.signal.playStatus==self.signalProcessor.signal.PLAYING):
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
        if(self.signalProcessor.signal.playStatus == self.signalProcessor.signal.PLAYING or
           self.signalProcessor.signal.playStatus == self.signalProcessor.signal.RECORDING):
            index=self.signalProcessor.signal.currentPlayingTime()
            h = self.figure.bbox.height
            rect=[self.fromClientToCanvas(index),0,1,h]
            self.figure.canvas.drawRectangle(rect)
            if(self.signalProcessor.signal.playStatus == self.signalProcessor.signal.RECORDING):
                size=len(self.signalProcessor.signal.data)
                self.mainCursor.min,self.mainCursor.max=5*size/10,9*size/10
                self.visualChanges=True
                self.refresh()




    #endregion

    #region Property oscilogram and specgram Visibility

    def _getVisibleOscilogram(self):
        return self._visibleOscilogram

    def _setVisibleOscilogram(self, value):
        aux = self._visibleOscilogram
        self._visibleOscilogram = value
        if (aux != value):
            self.clear()
            self.visualChanges = True
            self.refresh()

    visibleOscilogram = property(_getVisibleOscilogram, _setVisibleOscilogram)

    def _getVisibleSpectrogram(self):
        return self._visibleSpectrogram

    def _setVisibleSpectrogram(self, value):
        aux = self._visibleSpectrogram
        self._visibleSpectrogram = value
        if (aux != value):
            self.clear()
            self.visualChanges = True
            self.refresh()

    visibleSpectrogram = property(_getVisibleSpectrogram, _setVisibleSpectrogram)
    #endregion

    #region VISUAL EVENTS AND ACTIONS
    def updateBackgroundSpanRectangle(self,event=None):
        'force an update of the background'
        if(self.visibleOscilogram):
            self.backgroundOscilogramSpanRectangle = self.figure.canvas.copy_from_bbox(self.figure.bbox)

        if(self.visibleSpectrogram):
            self.backgroundSpectrogramSpanRectangle = self.figure.canvas.copy_from_bbox(self.axesSpecgram.bbox)


    def mouseMoveEvent(self, event):
        FigureCanvas.mouseMoveEvent(self, event)

        if (self.visibleOscilogram or self.visibleSpectrogram):
            if (not self.mousePressed and self.mouseInsideZoomArea(event.x())):
                self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
            elif (not self.mouseInsideZoomArea(event.x())):
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            minx, maxx = self.zoomIntervalPixels
            if (abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES ):
                self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
            h = self.figure.canvas.figure.bbox.height
            if (self.mousePressed):

                axe = self.axesOscilogram
                if (not self.visibleOscilogram):
                    axe = self.axesSpecgram
                minx, maxx = axe.bbox.min[0], axe.bbox.max[0]
                a, b = max(minx, min(self.lastX, event.x())), min(maxx, max(self.lastX, event.x()))
                rect = [0, 0, 0, 0]
                if (not self.movingCursorZoom and abs(self.lastX - event.x()) > self.PIXELS_OF_CURSORS_CHANGES):
                    self.zoomIntervalPixels = (a, b)
                    if(self.visibleOscilogram):
                        self.spanRectangleOsgram.set_x(self.fromCanvasToClient(a)-self.mainCursor.min)
                        self.spanRectangleOsgram.set_width(self.fromCanvasToClient(b)-self.fromCanvasToClient(a))
                        self.spanRectangleOsgram.set_height(self.axesOscilogram.bbox.height)
                        self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
                        self.axesOscilogram.draw_artist(self.spanRectangleOsgram)
                        self.figure.canvas.blit(self.axesOscilogram.bbox)
                    if(self.visibleSpectrogram):
                        x1=self.specgramIndex(self.fromCanvasToClient(self.zoomIntervalPixels[0]))
                        x2=self.specgramIndex(self.fromCanvasToClient(self.zoomIntervalPixels[1]))
                        self.spanRectangleSpectrogram.set_x(x1)
                        self.spanRectangleSpectrogram.set_width(x2-x1)
                        self.spanRectangleSpectrogram.set_height(self.axesSpecgram.bbox.height)
                        self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
                        self.axesSpecgram.draw_artist(self.spanRectangleSpectrogram)
                        self.figure.canvas.blit(self.axesSpecgram.bbox)

                    #if(self.visibleSpectrogram):
                    #    self.figure.canvas.blit(self.axesSpecgram.bbox)

                elif (self.movingCursorZoom and abs(self.lastX - event.x()) > self.PIXELS_OF_CURSORS_CHANGES):
                    self.zoomIntervalPixels = (self.zoomIntervalPixels[0] + event.x() - self.lastX,
                                               self.zoomIntervalPixels[1] + event.x() - self.lastX)
                    self.lastX = event.x()

                    if(self.visibleOscilogram):
                        self.spanRectangleOsgram.set_x(self.fromCanvasToClient(self.zoomIntervalPixels[0])-self.mainCursor.min)
                        self.spanRectangleOsgram.set_width(self.fromCanvasToClient(self.zoomIntervalPixels[1])-self.fromCanvasToClient(self.zoomIntervalPixels[0]))
                        self.spanRectangleOsgram.set_height(self.figure.canvas.figure.bbox.height)
                        self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
                        self.axesOscilogram.draw_artist(self.spanRectangleOsgram)
                        self.figure.canvas.blit(self.axesOscilogram.bbox)
                    if(self.visibleSpectrogram):
                        Osgramindex=self.fromCanvasToClient(self.zoomIntervalPixels[0])
                        x1=self.specgramIndex(Osgramindex)
                        x2=self.specgramIndex(self.fromCanvasToClient(self.zoomIntervalPixels[1]))
                        self.spanRectangleSpectrogram.set_x(x1)
                        self.spanRectangleSpectrogram.set_width(x2-x1)
                        self.spanRectangleSpectrogram.set_height(self.figure.canvas.figure.bbox.height)
                        self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
                        self.axesSpecgram.draw_artist(self.spanRectangleSpectrogram)
                        self.figure.canvas.blit(self.axesSpecgram.bbox)


    def specgramIndex(self,OsgramIndex):
        minxSpecgram,maxxSpecgram=self.axesSpecgram.get_xlim()
        return minxSpecgram+(OsgramIndex-self.mainCursor.min)*(maxxSpecgram-minxSpecgram)/(self.mainCursor.max-self.mainCursor.min)


    def mousePressEvent(self, event):
        FigureCanvas.mousePressEvent(self, event)
        self.mousePressed = True

        if (self.mouseInsideZoomArea(event.x())):
            self.movingCursorZoom = True
            self.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
        self.lastX = event.x()

        minx, maxx = self.zoomIntervalPixels
        if (abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES):
            self.movingCursorZoom = False
            self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
            self.lastX = maxx
        if (abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES):
            self.movingCursorZoom = False
            self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
            self.lastX = minx

    def mouseInsideZoomArea(self, xPixel):
    #        xIndex=self.fromCanvasToClient(xPixel)
    #        return self.zoomCursor.min!=self.zoomCursor.max and xIndex>self.zoomCursor.min and xIndex<self.zoomCursor.max
        return xPixel >= self.zoomIntervalPixels[0] and xPixel <= self.zoomIntervalPixels[1]

    def mouseDoubleClickEvent(self, event):
        if (self.mouseInsideZoomArea(event.x())):
            self.mainCursor.min, self.mainCursor.max = self.zoomCursor.min, self.zoomCursor.max
            self.visualChanges = True
            self.refresh()
            self.clearZoomCursor()

    def deselectZoomRegion(self):
        self.clearZoomCursor()
        if(self.visibleOscilogram):
            self.figure.canvas.restore_region(self.backgroundOscilogramSpanRectangle)
            self.figure.canvas.blit(self.axesOscilogram.bbox)
        if(self.visibleSpectrogram):
            self.figure.canvas.restore_region(self.backgroundSpectrogramSpanRectangle)
            self.figure.canvas.blit(self.axesSpecgram.bbox)


    def mouseReleaseEvent(self, event):
        FigureCanvas.mouseReleaseEvent(self, event)
        if (self.movingCursorZoom):
            self.zoomCursor.min = self.fromCanvasToClient(self.zoomIntervalPixels[0])
            self.zoomCursor.max = self.fromCanvasToClient(self.zoomIntervalPixels[1])
        if ((self.visibleOscilogram or self.visibleSpectrogram) and not self.movingCursorZoom and abs(
                    self.lastX - event.x()) > self.PIXELS_OF_CURSORS_CHANGES):
            minx, maxx = min(event.x(), self.lastX), max(event.x(), self.lastX)
            self.zoomCursor.min = max(0, self.fromCanvasToClient(minx))
            self.zoomCursor.max = min(self.fromCanvasToClient(maxx), len(self.signalProcessor.signal.data))
            if (abs(self.zoomCursor.min - self.zoomCursor.max) < self.PIXELS_OF_CURSORS_CHANGES):
                self.zoomCursor.min, self.zoomCursor.max = 0, 0
            self.visualChanges = True
            self.lastX = event.x()
        if (self.mouseInsideZoomArea(event.x())):
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.movingCursorZoom = False
        self.mousePressed = False

    def fromClientToCanvas(self, indexX):
        """
       Translates the index in the signal array to its corresponding coordinates in the canvas
       """
        if (self.visibleOscilogram or self.visibleSpectrogram):
            axe = self.axesOscilogram
            if (not self.visibleOscilogram):
                axe = self.axesSpecgram
            minx, maxx = axe.bbox.min[0], axe.bbox.max[0]
            a, b = self.mainCursor.min, self.mainCursor.max
            return minx + (maxx - minx) * (indexX - a) * 1. / (b - a)

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        if (self.visibleOscilogram or self.visibleSpectrogram):
            axe = self.axesOscilogram
            if (not self.visibleOscilogram):
                axe = self.axesSpecgram
            minx, maxx = axe.bbox.min[0], axe.bbox.max[0]
            a, b = self.axesOscilogram.get_xlim()
            if (xPixel < minx):
                xPixel = minx
            if (xPixel > maxx):
                xPixel = maxx

            return self.mainCursor.min + int((xPixel - minx) * (b - a) * 1. / (maxx - minx))

    def zoomOut(self):
        aux = max((self.mainCursor.max - self.mainCursor.min), 4 * self.zoomStep) / (2 * self.zoomStep)
        if (self.mainCursor.max + aux < len(self.signalProcessor.signal.data)):
            self.mainCursor.max += aux
        else:
            self.mainCursor.max = len(self.signalProcessor.signal.data)

        if (self.mainCursor.min - aux >= 0):
            self.mainCursor.min -= aux
        else:
            self.mainCursor.min = 0

        self.visualChanges = True
        self.refresh()

    def zoomIn(self):
        aux = (self.mainCursor.max - self.mainCursor.min) / (4 * self.zoomStep)
        if (self.mainCursor.max - aux > self.mainCursor.min + aux):
            self.mainCursor.max -= aux
            self.mainCursor.min += aux
        self.visualChanges = True
        self.refresh()

    def zoomNone(self):
        if (self.signalProcessor.signal.opened()):
            self.mainCursor.min = 0
            self.mainCursor.max = len(self.signalProcessor.signal.data)
            self.clearZoomCursor()
            self.visualChanges = True
            self.refresh()

    SPECGRAM_YTICS_DECIMAL_PLACES = 5
    SPECGRAM_XTICS_DECIMAL_PLACES = 2
    SPECGRAM_COMPLEX_SIDE = "onesided"
    OSGRAM_XTICS_DECIMAL_PLACES = 4
    OSGRAM_FONTSIZE = 16
    PIXELS_OF_CURSORS_CHANGES=3
    TICK_INTERVAL_MS=25
    SPAN_RECT_PROPS = dict(facecolor='green',alpha=0.4)

    COLOR_INDEX=0

    def refresh(self):


        if (self.visualChanges):
            if ( self.visibleOscilogram and self.signalProcessor.signal.opened() and self.mainCursor.max > self.mainCursor.min):
                self.axesOscilogram.clear()
                self.axesOscilogram.plot(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max])
                self.axesOscilogram.set_xticklabels([
                    round((x + self.mainCursor.min) * 1.0 / self.signalProcessor.signal.samplingRate,
                          self.OSGRAM_XTICS_DECIMAL_PLACES) for x in self.axesOscilogram.get_xticks()])
                self.axesOscilogram.set_yticklabels([round(x*100./(2**self.signalProcessor.signal.bitDepth),0) for x in self.axesOscilogram.get_yticks()])
                self.axesOscilogram.set_xlim(0, self.mainCursor.max - self.mainCursor.min)
                self.axesOscilogram.grid(self.specgramSettings.grid)


            if ( self.visibleSpectrogram and self.signalProcessor.signal.opened() and self.mainCursor.max > self.mainCursor.min):
                self.axesSpecgram.clear()
                overlap = int(self.specgramSettings.NFFT * self.specgramSettings.overlap / 100)
                self.specgramSettings.Pxx, self.specgramSettings.freqs, self.specgramSettings.bins = mlab.specgram(
                    self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max],
                    self.specgramSettings.NFFT, Fs=2, detrend=mlab.detrend_none, window=self.specgramSettings.window,
                    noverlap=overlap, sides=self.SPECGRAM_COMPLEX_SIDE)
                self.axesSpecgram.grid(self.specgramSettings.grid)
                #the umbral cut
                #increases the performance with search in the indexes
                cut_off = percentile(self.powerSpectrum, self.specgramSettings.threshold)
                modify = 0

                for i in range(len(self.specgramSettings.Pxx)):
                    for j in range(len(self.specgramSettings.Pxx[i])):
                        if (self.specgramSettings.Pxx[i, j] < cut_off):
                            self.specgramSettings.Pxx[i, j] = self.min_specgram_value

                Z = 10. * np.log10(self.specgramSettings.Pxx)
                Z = np.flipud(Z)
                a = self.axesSpecgram.get_xlim()
                b = self.axesSpecgram.get_ylim()
                xextent = a[0], a[1], b[0], b[1]
                #self.self.freqs += Fc where Fc is the central frecuency
                im = self.axesSpecgram.imshow(Z,
                                              cmap=self.specgramSettings.colorPalette(),extent=xextent, interpolation="nearest")
                self.axesSpecgram.axis('auto')

                if (self.colorbar == None):
                    if (self.visibleSpectrogram and self.visibleOscilogram):
                        ax = self.figure.add_axes([0.77, 0.48, 0.22, 0.03])
                    elif (self.visibleSpectrogram):
                        ax = self.figure.add_axes([0.77, 0.982, 0.22, 0.015])

                    self.colorbar = self.figure.colorbar(im, cax=ax, orientation="horizontal")
                else:
                    self.colorbar.update_bruteforce(im)

                self.axesSpecgram.set_xticklabels(
                    [round((x + self.mainCursor.min) * 1.0 / self.signalProcessor.signal.samplingRate,
                           self.SPECGRAM_XTICS_DECIMAL_PLACES) for x in self.axesSpecgram.get_xticks()])
                self.axesSpecgram.set_yticklabels([(str(round(x * self.signalProcessor.signal.samplingRate / (2 * 1000),
                                                              self.SPECGRAM_YTICS_DECIMAL_PLACES)) + " kHz") for x in
                                                   self.axesSpecgram.get_yticks()])
            if (self.visibleCursors):
                self.drawCursors()
            self.figure.canvas.draw()
            self.visualChanges = False
    def cursorZoomTransform(self,cursorIndex):
        return cursorIndex-self.mainCursor.min



    def drawCursors(self):
        ax = None
        xlimLeft, xlimRigth = 0, 0
        for i in range(len(self.cursors)):
            if (self.cursors[i].visualOptions.visible):
                if (self.cursors[i].visualOptions.oscilogramCursor and self.visibleOscilogram):
                    ax = self.axesOscilogram
                elif (not self.cursors[i].visualOptions.oscilogramCursor and self.visibleSpectrogram):
                    ax = self.axesSpecgram
                if (ax != None):
                    if (isinstance(self.cursors[i], PointerCursor)):
                        if (self.cursors[i].visualOptions.vertical):
                            xlimLeft, xlimRigth = ax.get_xlim()
                            xlimLeft, xlimRigth=xlimLeft+self.mainCursor.min, xlimRigth+self.mainCursor.min
                            if (self.cursors[i].index > xlimLeft and self.cursors[i].index < xlimRigth):
                                ax.plot([self.cursorZoomTransform(self.cursors[i].index), self.cursorZoomTransform(self.cursors[i].index)], ax.get_ylim())
                        else:
                            xlimLeft, xlimRigth = ax.get_ylim()
                            if (self.cursors[i].index > xlimLeft and self.cursors[i].index < xlimRigth):
                                ax.plot(ax.get_xlim(), [self.cursors[i].index, self.cursors[i].index])

                    elif (isinstance(self.cursors[i], IntervalCursor)):
                        if (self.cursors[i].visualOptions.vertical):
                            a, b = ax.get_ylim()
                            xlimLeft, xlimRigth = ax.get_xlim()
                            xlimLeft, xlimRigth=xlimLeft+self.mainCursor.min, xlimRigth+self.mainCursor.min
                            if (self.cursors[i].min> xlimLeft and self.cursors[i].max < xlimRigth and
            self.cursors[i].max > xlimLeft and self.cursors[i].max < xlimRigth):#replace with lim for horizontal cursors
                                ax.plot(
                                    [self.cursorZoomTransform(self.cursors[i].min), self.cursorZoomTransform(self.cursors[i].min),
                                     self.cursorZoomTransform(self.cursors[i].max), self.cursorZoomTransform(self.cursors[i].max),
                                     self.cursorZoomTransform(self.cursors[i].min)],
                                    [a, b, b, a, a])
                        else:
                            a, b = ax.get_xlim()
                            xlimLeft, xlimRigth = ax.get_ylim()
                            if (self.cursors[i].min > xlimLeft and self.cursors[i].max < xlimRigth and
                                        self.cursors[i].max > xlimLeft and self.cursors[i].max < xlimRigth):
                                ax.plot([a, a, b, b, a],
                                        [self.cursors[i].min, self.cursors[i].max, self.cursors[i].max,
                                         self.cursors[i].min, self.cursors[i].min])
                    elif (isinstance(self.cursors[i], RectangularCursor)):
                        a, b = self.cursors[i].intervalY.min, self.cursors[i].intervalY.max
                        xlimLeft, xlimRigth = ax.get_xlim()
                        xlimLeft, xlimRigth=xlimLeft+self.mainCursor.min, xlimRigth+self.mainCursor.min
                        ylimLeft, ylimRigth = ax.get_ylim()
                        if (a > ylimLeft and a < ylimRigth and b > ylimLeft and b < ylimRigth and
                                self.cursors[i].intervalX.min > xlimLeft and
                                self.cursors[i].intervalX.min < xlimRigth and
                                self.cursors[i].intervalX.max > xlimLeft and
                                self.cursors[i].intervalX.max< xlimRigth):
                            ax.plot([self.cursorZoomTransform(self.cursors[i].intervalX.min),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.min),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.max),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.max),
                                     self.cursorZoomTransform(self.cursors[i].intervalX.min)],
                                    [a, b, b, a, a])
            ax = None
    def clear(self):
            self.figure.clf()
            self.colorbar = None
            self.figure.hold(False)
            if (self.visibleOscilogram and self.visibleSpectrogram):
                self.axesOscilogram = self.figure.add_subplot(211)
                self.axesSpecgram = self.figure.add_subplot(212)
                self.axesOscilogram.set_position([0.08, 0.55, 0.9, 0.40])
                trans = blended_transform_factory(self.axesOscilogram.transData, self.axesOscilogram.transAxes)
                self.spanRectangleOsgram=Rectangle( (0,0), 0,self.axesOscilogram.bbox.height,transform=trans,visible=True,**self.SPAN_RECT_PROPS)
                self.figure.canvas.mpl_connect('draw_event', self.updateBackgroundSpanRectangle)
                trans2 = blended_transform_factory(self.axesSpecgram.transData, self.axesSpecgram.transAxes)
                self.spanRectangleSpectrogram=Rectangle( (0,0), 0,self.axesSpecgram.bbox.height,transform=trans2,visible=True,**self.SPAN_RECT_PROPS)
                self.figure.canvas.mpl_connect('draw_event', self.updateBackgroundSpanRectangle)

                #the relative to parent proportions dimension of axes [left,bottom,width, heitgh]
                #self.axesOscilogram.set_title('Oscilogram',fontsize=self.OSGRAM_FONTSIZE,color='blue')
                self.axesSpecgram.set_position([0.08, 0.05, 0.9, 0.40])
                #self.axesSpecgram.set_title('Spectrogram',fontsize=16,color='blue')
            elif (self.visibleOscilogram):
                self.axesOscilogram = self.figure.add_subplot(111)
                self.axesOscilogram.set_position([0.075, 0.05, 0.91, 0.9])
                trans = blended_transform_factory(self.axesOscilogram.transData, self.axesOscilogram.transAxes)
                self.spanRectangleOsgram=Rectangle( (0,0), 0,self.axesOscilogram.bbox.height,transform=trans,visible=True,**self.SPAN_RECT_PROPS)
                self.figure.canvas.mpl_connect('draw_event', self.updateBackgroundSpanRectangle)


            elif (self.visibleSpectrogram):
                self.axesSpecgram = self.figure.add_subplot(111)
                self.axesSpecgram.set_position([0.075, 0.05, 0.91, 0.9])
                trans2 = blended_transform_factory(self.axesSpecgram.transData, self.axesSpecgram.transAxes)
                self.spanRectangleSpectrogram=Rectangle( (0,0), 0,self.axesSpecgram.bbox.height,transform=trans2,visible=True,**self.SPAN_RECT_PROPS)
                self.figure.canvas.mpl_connect('draw_event', self.updateBackgroundSpanRectangle)

                #self.axesSpecgram.set_title('Spectrogram',fontsize=16,color='blue')



    def clearZoomCursor(self):
        self.zoomCursor.min, self.zoomCursor.max = 0, 0
        self.zoomIntervalPixels=(0,0)
        self.movingCursorZoom = False

#endregion

    #region SIGNAL PROCESSING

    #region Edition CUT,COPY PASTE
    def cut(self):
        self.editionSignalProcessor.cut(self.zoomCursor.min, self.zoomCursor.max)
        self.mainCursor.max -= self.zoomCursor.max - self.zoomCursor.min
        self.visualChanges = True
        if (self.mainCursor.max < 1):
            self.zoomOut()
        self.refresh()

    def copy(self):
        return self.editionSignalProcessor.copy(self.zoomCursor.min, self.zoomCursor.max)

    def paste(self):
        self.editionSignalProcessor.paste(self.editionSignalProcessor.clipboard, self.zoomCursor.min)
        self.mainCursor.max = self.mainCursor.max + len(self.editionSignalProcessor.clipboard)
        self.visualChanges = True
        self.refresh()

    #endregion

    def reverse(self):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).reverse)
    def getIndexFromAndTo(self):
        indexFrom, indexTo = self.mainCursor.min, self.mainCursor.max
        if (self.zoomCursor.min > 0 and self.zoomCursor.max > 0):
            indexFrom, indexTo = self.zoomCursor.min, self.zoomCursor.max
            #the delegate has the responsability of modify just the portion of the signal
            #given by indexFrom:indexTo for an eficient action.
        return indexFrom,indexTo

    def signalProcessingAction(self, delegate, *args):
        indexFrom, indexTo=self.getIndexFromAndTo()
        self.signalProcessor.signal = delegate(indexFrom, indexTo, *args)
        self.clearZoomCursor()
        self.visualChanges = True
        self.refresh()

    def insertSilence(self, ms=0):
        self.signalProcessingAction(CommonSignalProcessor(self.signalProcessor.signal).insertSilence, ms)

    def scale(self, factor,function="normalize",fade="IN"):
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

    def uniformSegmenter(self):
        segmenter = SegmenterDetector()
        segmenter.detect(self.signalProcessor.signal)
        for c in segmenter.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def spectrogramsElevations(self):
        detector = SpectrogramHillDetector()
        overlap = int(self.specgramSettings.NFFT * self.specgramSettings.overlap / 100)
        detector.detect(self.signalProcessor.signal, 80, self.specgramSettings.Pxx, self.specgramSettings.freqs,
                        self.specgramSettings.bins)
        for c in detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def pseudoUniformSegmenter(self):
        segmenter = SegmenterDetector()
        segmenter.detect(self.signalProcessor.signal, segment_mode=segmenter.PSEUDOUNIFORM_SEGMENTER)
        for c in segmenter.cursors():
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

    def elements(self,type="simple"):
        indexFrom, indexTo = self.getIndexFromAndTo()
        rms=self.signalProcessor.rms(indexFrom,indexTo)
        self.detector.detect(self.signalProcessor.signal,indexFrom, indexTo,rms,type)
        for c in self.detector.cursors():
            self.cursors.append(c)
        self.visualChanges = True
        self.refresh()

    def envelope(self):
        self.axesOscilogram.plot(range(len(self.signalProcessor.signal.data)),
                                 map(self.signalProcessor.envelope, self.signalProcessor.signal.data))

    def maxMinPeaks(self):
        detector = MaxMinPeakDetector()
        indexFrom,indexTo=self.getIndexFromAndTo()
        detector.detect(self.signalProcessor.signal,indexFrom,indexTo)
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

        if (isinstance(self.signalProcessor.signal, WavFileSignal)):
            self.loadUserData(self.signalProcessor.signal.userData)
        self.mainCursor.min = 0
        self.mainCursor.max = len(self.signalProcessor.signal.data)
        if(self.mainCursor.max/self.signalProcessor.signal.samplingRate > 10000 ):#10 seg
            self.mainCursor.max = 10000*self.signalProcessor.signal.samplingRate
        self.powerSpectrum = real(fft(self.signalProcessor.signal.data[self.mainCursor.min:self.mainCursor.max]))
        self.meanSignalValue = real(np.mean(self.powerSpectrum))
        self.max_specgram_value = max(self.powerSpectrum)
        self.min_specgram_value = min(self.powerSpectrum)
        self.specgramSettings.threshold = 50
        self.visualChanges = True
        self.refresh()

    def save(self, fname):
        chunk = self.cursorsData()
        self.signalProcessor.signal = self.signalProcessor.signal.toWav()
        self.signalProcessor.signal.save(fname, chunk)

    def cursorsData(self):

        cursData = PointerCursor().intToByteArray(len(self.cursors))
        for x in self.cursors:
            if (isinstance(x, PointerCursor)):
                cursData.extend(bytearray([0, 0]))#pcur---> pointer cursor

            if (isinstance(x, IntervalCursor)):
                cursData.extend(bytearray([0, 1]))#icur---> interval cursor

            if (isinstance(x, RectangularCursor)):
                cursData.extend(bytearray([0, 2]))#rcur---> rectangular cursor

            data = x.toByteArray()
            cursData.extend(PointerCursor().intToByteArray(len(data)))
            cursData.extend(data)
        return bytearray(cursData)

    def loadUserData(self, userData):
        userData = bytearray(userData)
        if (len(userData) == 0):
            return
        self.cursors = []
        index = 4
        size = 0
        cursor = PointerCursor()
        n = cursor.byteArrayToInt(bytearray(userData[0:4]))
        for i in range(n):
            type = bytearray(userData[index:index + 2])
            index += 2
            if (type == bytearray([0, 0])):
                cursor = PointerCursor()
            if (type == bytearray([0, 1])):
                cursor = IntervalCursor()
            if (type == bytearray([0, 2])):
                cursor = RectangularCursor()
            size = PointerCursor().byteArrayToInt(userData[index:index + 4])
            index += 4
            cursor.fromByteArray(userData[index:index + size])
            index += size
            self.cursors.append(cursor)


#endregion