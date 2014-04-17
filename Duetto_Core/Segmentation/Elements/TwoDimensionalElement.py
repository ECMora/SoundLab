from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
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

    def __init__(self,signal,matrix,freqs,startfreq,endfreq,bins,starttime,endtime,number=0,one_dimensional_parent=None,location = None, multipleSubelements = False):
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
            #width = min(self.timeEndIndex-self.timeStartIndex,max(4,(self.timeEndIndex-self.timeStartIndex)/5))
            #height = min(max(4,(self.freqEndIndex-self.freqStartIndex)/5),self.freqEndIndex-self.freqStartIndex)
            #ypos = self.freqEndIndex-self.freqStartIndex
            #xpos =  self.timeEndIndex-self.timeStartIndex
            ##poner tooltips
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.START][0]):
            #    start = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0,self.freqStartIndex+ypos*0,   width,    height))
            #    start.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.START][1]))
            #    start.setToolTip("Element: "+ str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nStart Mesurement Location")
            #    self.visual_locations.append([start,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.CENTER][0]):
            #    center = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0.5-    width/2,self.freqStartIndex+ypos*0.5 -height/2,    width,    height))
            #    center.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.CENTER][1]))
            #    center.setToolTip("Element:"+  str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nCenter Mesurement Location")
            #    self.visual_locations.append([center,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.END][0]):
            #    end = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*1- width,self.freqStartIndex+ypos*1- height,    width,    height))
            #    end.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.END][1]))
            #    end.setToolTip("Element:"+  str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nEnd Mesurement Location")
            #    self.visual_locations.append([end,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE25][0]):
            #    quartile1 = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0.25 -width/2,self.freqStartIndex+ypos*0.25 -height/2,width,    height))
            #    quartile1.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE25][1]))
            #    quartile1.setToolTip("Element:"+  str(self.parentnumber) + "\n SubElement: "+str(self.number) +"\nQuartile 25% Mesurement Location")
            #    self.visual_locations.append([quartile1,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE75][0]):
            #    quartile3 = QtGui.QGraphicsRectItem(QtCore.QRectF(self.timeStartIndex+ xpos*0.75-width/2,self.freqStartIndex+ypos*0.75-height/2, width,    height))
            #    quartile3.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE75][1]))
            #    quartile3.setToolTip("Element:"+  str(self.parentnumber) +  "\n SubElement: "+str(self.number) +"\nQuartile 75% Mesurement Location")
            #    self.visual_locations.append([quartile3,True])
        self.addPeaksVisualObjects()
        if multipleSubelements:
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
        else:

            g = pg.GraphItem()
            f = self.freqEndIndex-self.freqStartIndex
            t = self.timeEndIndex-self.timeStartIndex
            ## Define positions of nodes
            pos = np.array([
                [self.timeStartIndex,self.freqEndIndex-f*3/8],
                [self.timeStartIndex,self.freqEndIndex-f*1/4],
                [self.timeEndIndex,self.freqEndIndex-f*1/4],
                [self.timeEndIndex,self.freqEndIndex-f*3/8]
                ])
            adj = np.array([
                [0,1],
                [1,2],
                [2,3]
                ])
            g.setData(pos=pos, size=1, symbol='d', pxMode=False,adj=adj,pen=(pg.mkPen(QtGui.QColor(0, 255, 0, 100),width=3) if number%2==0 else pg.mkPen(QtGui.QColor(0, 0, 255,100),width=3)))
            self.visual_figures.append([g,True])
            text = pg.TextItem(str(one_dimensional_parent.number),color=(255,255,255),anchor=(0.5,0))
            text.setPos(self.timeStartIndex/2.0+self.timeEndIndex/2.0, self.freqStartIndex+f*3/4)
            self.visual_text.append([text,True])

    def addPeaksVisualObjects(self):
        g = pg.GraphItem()
        f = self.freqEndIndex-self.freqStartIndex
        t = self.timeEndIndex-self.timeStartIndex
        ## Define positions of nodes
        pos = []
        adj = []
        index = np.argmax(self.matrix[:,0])
        pos.append([self.timeStartIndex,self.freqStartIndex+index])
        for i in range(1,len(self.matrix[0])):
            index = np.argmax(self.matrix[:,i])
            pos.append([self.timeStartIndex+i,self.freqStartIndex+index])
            adj.append([i-1,i])
        pos = np.array(pos)
        adj = np.array(adj)
        g.setData(pos=pos, size=1, symbol='d', pxMode=False,adj=adj,pen=(pg.mkPen(QtGui.QColor(0, 255, 0, 100),width=3) if self.parentnumber%2==0 else pg.mkPen(QtGui.QColor(0, 0, 255,100),width=3)))
        self.visual_peaksfreqs.append([g,False])

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



