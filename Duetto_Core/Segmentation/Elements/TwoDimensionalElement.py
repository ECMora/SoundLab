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

    def __init__(self,signal,matrix,freqs,startfreq,endfreq,bins,starttime,endtime,number=0,one_dimensional_parent=None,location = None):
        TwoDimensionalElement.__init__(self,signal,matrix)
        self.measurementLocation = location
        if one_dimensional_parent is not None:
            starttime+=one_dimensional_parent.indexFromInPxx
            endtime+=one_dimensional_parent.indexFromInPxx
            self.parentnumber = one_dimensional_parent.number
        self.bins = bins
        self.number = number
        self.freqs = freqs
        self.timeStartIndex = starttime
        self.timeEndIndex = endtime
        self.freqStartIndex = startfreq
        self.freqEndIndex = endfreq

        self.parameters = dict(minFreq=None, maxFreq=None, peakFreq=None,peaksAbove=(None,0))
        if(location is not None):
            self.measurementLocation = location
            #width = (self.timeEndIndex-self.timeStartIndex)/5
            #height = (self.freqEndIndex-self.freqStartIndex)/5
            width = min(self.timeEndIndex-self.timeStartIndex,2)
            height = min(4,self.freqEndIndex-self.freqStartIndex)
            ypos = self.freqEndIndex-self.freqStartIndex
            xpos =  self.timeEndIndex-self.timeStartIndex
            #poner tooltips
            if(self.measurementLocation.Start):
                start = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0,self.freqStartIndex+ypos*0,    width,    height))
                start.setBrush(QtGui.QBrush(self.measurementLocation.StartMeasurementColor))
                start.setToolTip("Element: "+ str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nStart Mesurement Location")
                self.visual_locations.append([start,True])
            if(self.measurementLocation.Center):
                center = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0.5-    width/2,self.freqStartIndex+ypos*0.5,    width,    height))
                center.setBrush(QtGui.QBrush(self.measurementLocation.CenterMeasurementColor))
                center.setToolTip("Element:"+  str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nCenter Mesurement Location")
                self.visual_locations.append([center,True])
            if(self.measurementLocation.End):
                end = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*1-    width,self.freqStartIndex+ypos*1- width,    width,    height))
                end.setBrush(QtGui.QBrush(self.measurementLocation.EndMeasurementColor))
                end.setToolTip("Element:"+  str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nEnd Mesurement Location")
                self.visual_locations.append([end,True])
            if(self.measurementLocation.Quartile25):
                quartile1 = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0.25,self.freqStartIndex+ypos*0.25,width,    height))
                quartile1.setBrush(QtGui.QBrush(self.measurementLocation.Quartile1MeasurementColor))
                quartile1.setToolTip("Element:"+  str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nQuartile 25% Mesurement Location")
                self.visual_locations.append([quartile1,True])
            if(self.measurementLocation.Quartile75):
                quartile3 = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0.75,self.freqStartIndex+ypos*0.75, width,    height))
                quartile3.setBrush(QtGui.QBrush(self.measurementLocation.Quartile3MeasurementColor))
                quartile3.setToolTip("Element:"+  str(self.parentnumber) +  "\n SubElement: "+str(self.number) +"\nQuartile 75% Mesurement Location")
                self.visual_locations.append([quartile3,True])


        text = pg.TextItem(str(self.parentnumber),color=(255,255,255),anchor=(0.5,0.8))
        text.setPos(self.timeStartIndex+(self.timeEndIndex-self.timeStartIndex)/2,
                                self.freqEndIndex)
        text.setFont(QtGui.QFont("Arial",pointSize=10))
        self.visual_text.append([text,True])
        rect = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex,self.freqStartIndex,
                                                                 self.timeEndIndex-self.timeStartIndex,
                                                                 self.freqEndIndex-self.freqStartIndex))
        rect.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        self.visual_figures.append([rect,True])



    def minFreq(self):
        if(self.parameters["minFreq"] is None):
            self.parameters["minFreq"] = 0
        return self.parameters["minFreq"]

    def maxFreq(self):
        if(self.parameters["maxFreq"] is None):
            self.parameters["maxFreq"] = 0
        return self.parameters["maxFreq"]

    def peakFreq(self):
        if(self.parameters["peakFreq"] is None):
            self.parameters["peakFreq"] = 0
        return self.parameters["peakFreq"]

    def peaksAbove(self,threshold):
        if(self.parameters["peaksAbove"][0] is None or self.parameters["peaksAbove"][1] != threshold):
            self.parameters["peekToPeek"] = (0,threshold)
        return self.parameters["peekToPeek"][0]



