from math import floor, ceil, log10
from matplotlib import mlab
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.TwoDimensionalElementsDetector import TwoDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements.TwoDimensionalElement import SpecgramElement
import numpy as np
import pyqtgraph as pg
from Duetto_Core.Segmentation.Elements.Element import Element
from PyQt4 import QtGui, QtCore


class SpectralMeasurementLocation:
    START,CENTER,END,QUARTILE25,QUARTILE75 = range(5)
    MEDITIONS = [
        [True,  QtGui.QColor(255, 0, 0, 255)],
        [True, QtGui.QColor(0, 255, 0, 255)],
        [True,  QtGui.QColor(0, 0, 255, 255)],
        [False, QtGui.QColor(255,255,255, 255)],
        [False,  QtGui.QColor(255, 255, 255, 255)]]
    #(Active computation, color)


class OneDimensionalElement(Element):
    """
    Represents the minimal piece of information to clasify
    An element is a time and spectral region of the signal that contains a superior energy that the fragment of signal
    near to it
    """
    def __init__(self, signal, indexFrom, indexTo):
        Element.__init__(self, signal)
        self.indexFrom =  indexFrom#index of start of the element
        self.indexTo = indexTo # end of element in ms
        self.parameterDecimalPlaces = 4

    def startTime(self):
        #the start time in s
        return round(self.indexFrom*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)

    def endTime(self):
        return round(self.indexTo*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)

    def duration(self):
        """
        returns the len in s of an element (float)
        """
        return round((self.indexTo-self.indexFrom)*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)


class OscilogramElement(OneDimensionalElement):

    def __init__(self, signal, indexFrom, indexTo,number=0,threshold_spectral=0, pxx=[], freqs=[], bins=[], minsize_spectral=(0,0), location = None,findSpectralSublements = True,overlap = 0):
        OneDimensionalElement.__init__(self,signal,indexFrom,indexTo)
        text = pg.TextItem(str(number),color=(255,255,255),anchor=(0.5,0.5))
        text.setPos(self.indexFrom/2.0+self.indexTo/2.0, 0.75*2**(signal.bitDepth-1))
        lr = pg.LinearRegionItem([self.indexFrom,self.indexTo], movable=False,brush=(pg.mkBrush(QtGui.QColor(0, 255, 0, 100)) if number%2==0 else pg.mkBrush(QtGui.QColor(0, 0, 255,100))))
        self.number = number
        self.twoDimensionalElements = []
        #the memoize pattern implemented to compute parameters functions
        self.parameters = dict(StartToMax=None, peekToPeek=None, rms=None, minFreq=dict(), maxFreq=dict(),
                               peakFreq=dict(),peaksAbove=dict(),peakAmplitude=dict(),bandwidth=dict())

        tooltip = "Element: "+str(self.number)+"\nStart Time: "+ str(self.startTime()) + "s\n" \
                  + "End Time:"+ str(self.endTime()) + "s\n"\
                  + "RMS: "+ str(self.rms()) + "\n"\
                  + "PeekToPeek: "+ str(self.peekToPeek())
        lr.setToolTip(tooltip)
        self.visual_figures.append([lr,True])#item visibility
        self.visual_text.append([text,True])

        if(location is not None):
            self.measurementLocation = location
            #width = (indexTo-indexFrom)/5
            #height = (2**signal.bitDepth)/5
            #ypos = 2**signal.bitDepth
            #xpos = indexTo-indexFrom
            #ystart = -2**(signal.bitDepth-1)
            #poner tooltips
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.START][0]):
            #    start = QtGui.QGraphicsRectItem(QtCore.QRectF(indexFrom+ xpos*0,ystart + ypos*0,   width,    height))
            #    start.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.START][1]))
            #    start.setToolTip("Element: "+ str(self.number) +"\nStart Mesurement Location")
            #    self.visual_locations.append([start,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.CENTER][0]):
            #    center = QtGui.QGraphicsRectItem(QtCore.QRectF(indexFrom+ xpos*0.5- width/2,ystart +ypos*0.5 -height/2,    width,    height))
            #    center.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.CENTER][1]))
            #    center.setToolTip("Element:"+str(self.number) +"\nCenter Mesurement Location")
            #    self.visual_locations.append([center,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.END][0]):
            #    end = QtGui.QGraphicsRectItem(QtCore.QRectF(indexFrom+ xpos*1- width,ystart+ypos*1- height,    width,    height))
            #    end.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.END][1]))
            #    end.setToolTip("Element:"+str(self.number) +"\nEnd Mesurement Location")
            #    self.visual_locations.append([end,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE25][0]):
            #    quartile1 = QtGui.QGraphicsRectItem(QtCore.QRectF(indexFrom+ xpos*0.25 -width/2,ystart+ypos*0.25 -height/2,width,    height))
            #    quartile1.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE25][1]))
            #    quartile1.setToolTip("Element:"+str(self.number) +"\nQuartile 25% Mesurement Location")
            #    self.visual_locations.append([quartile1,True])
            #if(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE75][0]):
            #    quartile3 = QtGui.QGraphicsRectItem(QtCore.QRectF(indexFrom+ xpos*0.75- width/2,ystart+ypos*0.75-height/2, width,    height))
            #    quartile3.setBrush(QtGui.QBrush(self.measurementLocation.MEDITIONS[self.measurementLocation.QUARTILE75][1]))
            #    quartile3.setToolTip("Element:"+str(self.number) +"\nQuartile 75% Mesurement Location")
            #    self.visual_locations.append([quartile3,True])
        else:
            self.measurementLocation = SpectralMeasurementLocation()

        if pxx != [] and bins != [] and freqs != []:
            #spec_resolution, temp_resolution = signal.samplingRate/2.0*len(freqs),bins[1]-bins[0]
            spec_resolution, temp_resolution = 1000.0/freqs[1],(bins[1]-bins[0])*1000.0
            #minsize came with the hz, sec of min size elements and its translated to index values in pxx for comparations
            minsize_spectral = (max(1,int(minsize_spectral[0]*spec_resolution)),max(1,int(minsize_spectral[1]*temp_resolution)))
            sr = signal.samplingRate*1.0
            columnsize = (bins[1] - bins[0])*sr
            overlap = int(round(overlap,0))
            overlap_delay = 0 if overlap <= 0 else overlap/(100-overlap)
            aux = max(0,int(indexFrom/columnsize)-overlap_delay)
            aux2 = min(int(round(indexTo/columnsize,0))+overlap_delay,len(pxx[0]))
            self.matrix = pxx[:,aux:aux2]
            self.freqs = freqs
            self.bins = bins
            self.indexFromInPxx,self.indexToInPxx = aux,aux2

            self.twoDimensionalElements = [SpecgramElement(signal,self.matrix,freqs,0,len(freqs),bins,0,aux2-aux,number,self,location,multipleSubelements=False)]

            if findSpectralSublements:
                self.computeTwoDimensionalElements(threshold_spectral,self.matrix,freqs,bins,minsize_spectral)

    def computeTwoDimensionalElements(self,threshold_spectral, pxx, freqs, bins, minsize_spectral):
        detector = TwoDimensionalElementsDetector()
        detector.detect(self.signal,threshold_spectral, pxx,freqs,bins, minsize_spectral,one_dimensional_parent=self,location= self.measurementLocation)
        for elem in detector.elements():
            self.twoDimensionalElements.append(elem)

    def distanceFromStartToMax(self):
        if(self.parameters["StartToMax"] is None):
            self.parameters["StartToMax"] = round(np.argmax(self.signal.data[self.indexFrom:self.indexTo])*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)
        return self.parameters["StartToMax"]

    def peekToPeek(self):
        if(self.parameters["peekToPeek"] is None):
            self.parameters["peekToPeek"] = round(np.ptp(self.signal.data[self.indexFrom:self.indexTo])*1.0/(2**self.signal.bitDepth),self.parameterDecimalPlaces)
        return self.parameters["peekToPeek"]

    def rms(self):
        """
        computes the root mean square of the signal.
        indexFrom,indexTo the optionally limits of the interval
        """
        if(self.parameters["rms"] is None):
            n = self.indexTo-self.indexFrom
            globalSum = 0.0
            intervalSum = 0.0
            for i in range(n):
                intervalSum += (self.signal.data[self.indexFrom+i]**2)
                if i % 10 == 0:
                    globalSum += intervalSum * 1.0 / n
                    intervalSum = 0.0

            globalSum += intervalSum * 1.0 / n
            self.parameters["rms"] = round(np.sqrt(globalSum)*1.0/(2**self.signal.bitDepth),self.parameterDecimalPlaces)
        return self.parameters["rms"]

    def spectralElements(self):
        s = len(self.twoDimensionalElements)
        return s-1 if s > 0 else s

    def peakFreqAverage(self):
        return 0

    def maxFreqAverage(self):
        return 0

    def minFreqAverage(self):
        return 0

    #espectral parameters
    def getMatrixIndexFromLocation(self,location):
        size = len(self.matrix[0])
        if location == self.measurementLocation.START:
            return 0
        if location == self.measurementLocation.CENTER:
            return size/2
        if location == self.measurementLocation.END:
            return size-1
        if location == self.measurementLocation.QUARTILE25:
            return size/4
        if location == self.measurementLocation.QUARTILE75:
            return 3*size/4

    #The following methods measure properties that needs aditional parameters for its calculation
    #dict are a dictionary with the aditional data
    #
    def peak_f_a(self,index):
        """
        returns the peak frecuency and amplitude in db in the index location
        """
        freq_index = np.argmax(self.matrix[:, index])
        minIndex = np.argmin(self.matrix[:, index])
        value = int(round(self.freqs[freq_index],0))
        value -= value % 10
        return value,freq_index,round(-20*log10(1 if self.freqs[freq_index]< 0.1 else self.freqs[freq_index]),self.parameterDecimalPlaces)

    def peakFreq(self,dict):
        if "location" in dict:
            location = dict["location"]
            index = self.getMatrixIndexFromLocation(location)
            if index not in self.parameters["peakFreq"]:
                peak,freq_index,peakamplitude = self.peak_f_a(index)
                if(len(self.twoDimensionalElements)>0):
                    rect = QtGui.QGraphicsRectItem(QtCore.QRectF(self.indexFromInPxx + index-1,freq_index-1,2,2))
                    rect.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0)))
                    rect.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 100) if self.number%2==0 else QtGui.QColor(0, 0, 255,100)))
                    self.twoDimensionalElements[0].visual_figures.append([rect, True])

                self.parameters["peakFreq"][index],self.parameters["peakAmplitude"][index] = peak,peakamplitude
            return self.parameters["peakFreq"][index]
        return "Invalid Params"

    def peakAmplitude(self,dict):
        if "location" in dict:
            location = dict["location"]
            index = self.getMatrixIndexFromLocation(location)
            if index not in self.parameters["peakAmplitude"]:
                peak,freq_index,peakamplitude = self.peak_f_a(index)
                self.parameters["peakFreq"][index],self.parameters["peakAmplitude"][index] = peak,peakamplitude
            return self.parameters["peakAmplitude"][index]
        return "Invalid Params"

    def freq_min_max_band_peaksAbove(self,index,threshold, peaksThreshold):
        """
        returns the min freq with its index , the max freq with its index, the band width and the peaks above the threshold
        """
        arr = self.matrix[:, index]
        minx,maxx = min(arr),max(arr)
        thresholdValue = (10.0**((60+threshold)/20.0))*(maxx - minx)/1000.0
        peaksThresholdValue = (10.0**((60+peaksThreshold)/20.0))*(maxx - minx)/1000.0
        regions = mlab.contiguous_regions(arr > thresholdValue)
        regionsPeaks = regions if threshold == peaksThreshold else mlab.contiguous_regions(arr > peaksThreshold)
        minf = self.freqs[0]-self.freqs[0] % 10
        maxf = self.freqs[len(self.freqs)-1]-self.freqs[len(self.freqs)-1] % 10

        if len(regions) >0:
            minf = int(round(self.freqs[regions[0][0]],0))
            minf -= minf % 10
            maxf = int(round(self.freqs[regions[len(regions)-1][1]],0))
            maxf -= maxf % 10
        return minf,regions[0][0],maxf,regions[len(regions)-1][1],maxf-minf,len(regionsPeaks)

    def minFreq(self,dict):
        if "location" in dict and "threshold" in dict and "peaksThreshold" in dict:
            location = dict["location"]
            threshold = dict["threshold"]
            peakthreshold = dict["peaksThreshold"]
            index = self.getMatrixIndexFromLocation(location)
            if (index,threshold) not in self.parameters["minFreq"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
                self.parameters["minFreq"][(index,threshold)],self.parameters["maxFreq"][(index,threshold)],\
                self.parameters["bandwidth"][(index,threshold)],self.parameters["peaksAbove"][(index,peakthreshold)] = minf, maxf, band, peaks
                if(len(self.twoDimensionalElements)>0):
                    g = pg.GraphItem()
                    ## Define positions of nodes
                    pos = np.array([
                        [self.indexFromInPxx + index, minfIndex],
                        [self.indexFromInPxx + index, maxfIndex]
                        ])
                    adj = np.array([
                        [0,1]
                        ])
                    g.setData(pos=pos, size=min(maxfIndex-minfIndex,3), symbol=['+','+'], pxMode=False,adj=adj,pen=(pg.mkPen(QtGui.QColor(0, 255, 0, 100),width=3) if self.number%2==0 else pg.mkPen(QtGui.QColor(0, 0, 255,100),width=3)))
                    self.twoDimensionalElements[0].visual_figures.append([g,True])
            return self.parameters["minFreq"][(index,threshold)]
        return "Invalid Params"

    def maxFreq(self,dict):
        if "location" in dict and "threshold" in dict and "peaksThreshold" in dict:
            location = dict["location"]
            threshold = dict["threshold"]
            peakthreshold = dict["peaksThreshold"]
            index = self.getMatrixIndexFromLocation(location)
            if (index,threshold) not in self.parameters["maxFreq"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
                self.parameters["minFreq"][(index,threshold)],self.parameters["maxFreq"][(index,threshold)],\
                self.parameters["bandwidth"][(index,threshold)],self.parameters["peaksAbove"][(index,peakthreshold)] = minf, maxf, band, peaks
                if(len(self.twoDimensionalElements)>0):
                    g = pg.GraphItem()
                    ## Define positions of nodes
                    pos = np.array([
                        [self.indexFromInPxx + index, minfIndex],
                        [self.indexFromInPxx + index, maxfIndex]
                        ])
                    adj = np.array([
                        [0,1]
                        ])
                    g.setData(pos=pos, size=min(maxfIndex-minfIndex,3), symbol=['+','+'], pxMode=False,adj=adj,pen=(pg.mkPen(QtGui.QColor(0, 255, 0, 100),width=3) if self.number%2==0 else pg.mkPen(QtGui.QColor(0, 0, 255,100),width=3)))
                    self.twoDimensionalElements[0].visual_figures.append([g,True])
            return self.parameters["maxFreq"][(index,threshold)]
        return "Invalid Params"

    def bandwidth(self,dict):
        if "location" in dict and "threshold" in dict and "peaksThreshold" in dict:
            location = dict["location"]
            threshold = dict["threshold"]
            peakthreshold = dict["peaksThreshold"]
            index = self.getMatrixIndexFromLocation(location)
            if (index,threshold) not in self.parameters["bandwidth"]:
                self.parameters["minFreq"][(index,threshold)], minfIndex, self.parameters["maxFreq"][(index,threshold)],maxfIndex,\
                self.parameters["bandwidth"][(index,threshold)],self.parameters["peaksAbove"][(index,peakthreshold)] = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
            return self.parameters["bandwidth"][(index,threshold)]
        return "Invalid Params"

    def peaksAbove(self,dict):
        if "location" in dict and "threshold" in dict and "peaksThreshold" in dict:
            location = dict["location"]
            threshold = dict["threshold"]
            peakthreshold = dict["peaksThreshold"]
            index = self.getMatrixIndexFromLocation(location)
            if (index,peakthreshold) not in self.parameters["peaksAbove"]:
                self.parameters["minFreq"][(index,threshold)], minfIndex,self.parameters["maxFreq"][(index,threshold)], maxfIndex,\
                self.parameters["bandwidth"][(index,threshold)],self.parameters["peaksAbove"][(index,peakthreshold)] = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
            return self.parameters["peaksAbove"][(index,peakthreshold)]
        return "Invalid Params"

