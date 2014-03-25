from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
from Duetto_Core.Segmentation.Elements.Element import Element


class TwoDimensionalElement(Element):
    """
    In an acoustic procesing transform of 2 dimensional as spectrogram an element is a 2 dimensional region
    of local maximum in the rectangular matrix of specgram
    """
    def __init__(self, signal,matrix):
        Element.__init__(self,signal)
        self.matrix = matrix


class SpecgramElement(TwoDimensionalElement):

    def __init__(self,signal,matrix,freqs,startfreq,endfreq,bins,starttime,endtime,number=0):
        TwoDimensionalElement.__init__(self,signal,matrix)
        self.bins = bins
        self.freqs = freqs
        self.timeStartIndex = starttime
        self.timeEndIndex = endtime
        self.freqStartIndex = startfreq
        self.freqEndIndex = endfreq
        text = pg.TextItem(str(number),color=(255,0,0),anchor=(0.5,0.5))
        text.setPos(self.timeStartIndex+(self.timeEndIndex-self.timeStartIndex)/2,
                                self.freqStartIndex+(self.freqEndIndex-self.freqStartIndex)/2)
        rect = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex,self.freqStartIndex,
                                                                 self.timeEndIndex-self.timeStartIndex,
                                                                 self.freqEndIndex-self.freqStartIndex))
        rect.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        self.visualwidgets = [text,rect]

    def startTime(self):
        return self.bins[self.timeStartIndex]

    def endTime(self):
        return self.bins[self.timeEndIndex]

    def minFreq(self):
        return self.freqs[self.freqStartIndex]

    def maxFreq(self):
        return self.freqs[self.freqEndIndex]

    def PeakFreq(self,meditionTime = 0.0):
        return 0





