# -*- coding: utf-8 -*-
from math import  log10

from PyQt4.QtGui import QFont
from matplotlib import mlab
import numpy as np
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore

from sound_lab_core.Segmentation.Detectors.TwoDimensional.TwoDimensionalElementsDetector import TwoDimensionalElementsDetector
from sound_lab_core.Segmentation.Elements.TwoDimensionalElement import SpecgramElement
from sound_lab_core.Segmentation.Elements.Element import Element


class SpectralMeasurementLocation:
    START, CENTER, END, QUARTILE25, QUARTILE75 = range(5)
    MEDITIONS = [
        [False,  QtGui.QColor(255, 0, 0, 255)],
        [False, QtGui.QColor(0, 255, 0, 255)],
        [False,  QtGui.QColor(0, 0, 255, 255)],
        [False, QtGui.QColor(255,255,255, 255)],
        [False,  QtGui.QColor(255, 255, 255, 255)]]
    #(Active computation, color)


class OneDimensionalElement(Element):
    """
    Element defined in one-dimensional transform of a signal.
    """
    #SIGNALS
    # called when the element is clicked
    # raise the index of the element (number)
    elementClicked = QtCore.Signal(int)

    #CONSTANTS
    # decimal places to round the measurements
    DECIMAL_PLACES = 4

    def __init__(self, signal, indexFrom, indexTo):
        Element.__init__(self, signal)
        self.indexFrom =  indexFrom #index of start of the element
        self.indexTo = indexTo



class OscilogramElement(OneDimensionalElement):

    def __init__(self, signal, indexFrom, indexTo,number=0,threshold_spectral=0, minsize_spectral=(0,0), location = None,findSpectralSublements = True,specgramSettings = None,trim_threshold=0):
        """
        @param signal: The signal in wich is defined this element
        @param indexFrom: Start time of the element in the signal
        @param indexTo: End time of the element in the signal
        @param number: The number of this element in the list of detected elements in signal
        @param threshold_spectral: The threshold spectral for detection of two dimensional elements
        @param minsize_spectral: The spectral min size of two dimensional elements detection
        @param location:
        @param findSpectralSublements: If this element should perform the search of sub elements
        @param specgramSettings: Settings of specgram computation
        @param trim_threshold: Threshold to select the section of specgram corresponding
        to this element for parameter measurement. The section depends of overlap and NFFT in  specgramSettings
        but if there is no energy enough that section would be trimed for left and right
        until the energy increases this trim_threshold.
        @return:
        """
        OneDimensionalElement.__init__(self,signal,indexFrom,indexTo)
        #the visible text for
        text = pg.TextItem(str(number),color=(255,255,255),anchor=(0.5,0.5))
        text.setPos(self.indexFrom/2.0+self.indexTo/2.0, 0.75*2**(signal.bitDepth-1))

        font = QFont()
        font.setPointSize(13)
        text.setFont(font)
        self.number = number

        self.color = QtGui.QColor(0, 255, 0, 100) if self.number%2==0 else QtGui.QColor(0, 0, 255,100)
        self.lr = pg.LinearRegionItem([self.indexFrom,self.indexTo], movable=False,brush=(pg.mkBrush(self.color)))
        self.twoDimensionalElements = []

        #the memoize pattern implemented to compute parameters functions
        self.parameters = dict(StartToMax=None, peekToPeek=None, rms=None, minFreq=dict(), maxFreq=dict(),
                               average=dict(),peakFreq=dict(),peaksAbove=dict(),peakAmplitude=dict(),bandwidth=dict())

        #a tooltip for the element's easy information access
        tooltip = "Element: "+str(self.number)+"\nStart Time: "+ str(self.startTime()) + "s\n" \
                  + "End Time:"+ str(self.endTime()) + "s\n"\
                  + "RMS: "+ str(self.rms()) + "\n"\
                  + "PeekToPeek: "+ str(self.peekToPeek())
        self.lr.setToolTip(tooltip)

        self.lr.mouseClickEvent = self.mouseClickEvent

        #update the visual representation
        self.visual_figures.append([self.lr,True]) #item visibility
        self.visual_text.append([text,True])

        #region location
        if location is not None:
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

        #endregion

        if specgramSettings is None:
            raise Exception("None parameter")

        self.specgramSettings = specgramSettings

        if self.specgramSettings.Pxx != [] and self.specgramSettings.bins != [] and self.specgramSettings.freqs != []:
            #spec_resolution, temp_resolution = signal.samplingRate/2.0*len(freqs),bins[1]-bins[0]
            spec_resolution, temp_resolution = 1000.0/self.specgramSettings.freqs[1],(self.specgramSettings.bins[1]-self.specgramSettings.bins[0])*1000.0

            #minsize came with the hz, sec of min size elements and its translated to index values in pxx for comparations
            minsize_spectral = (max(1,int(minsize_spectral[0]*spec_resolution)),max(1,int(minsize_spectral[1]*temp_resolution)))

            sr = signal.samplingRate*1.0
            columnsize = (self.specgramSettings.bins[1] - self.specgramSettings.bins[0])*sr
            overlap = int(round(self.specgramSettings.overlap,0))
            overlap_delay = 0 if overlap <= 0 else 99 if overlap >=100 else overlap/(100-overlap)

            aux = max(0,int(indexFrom*1.0/columnsize))
            aux2 = min(int(indexTo*1.0/columnsize)+overlap_delay,len(self.specgramSettings.Pxx[0]))

            left, rigth = self.trimMatrix(self.specgramSettings.Pxx,aux,aux2,trim_threshold)

            self.matrix = self.specgramSettings.Pxx[:,left:rigth]
            self.indexFromInPxx,self.indexToInPxx = left,rigth

            self.twoDimensionalElements = [SpecgramElement(signal,self.matrix,self.specgramSettings.freqs,0,len(self.specgramSettings.freqs),self.specgramSettings.bins,0,rigth-left,number,self,location,multipleSubelements=False)]

            if findSpectralSublements:
                self.computeTwoDimensionalElements(threshold_spectral,self.matrix,self.specgramSettings.freqs,self.specgramSettings.bins,minsize_spectral)

    def trimMatrix(self, pxx, aux, aux2, threshold_spectral):
        left =aux
        rigth = aux2-1
        while left<rigth and max(pxx[:,left]) < threshold_spectral:
            left+=1
        while rigth>left and max(pxx[:,rigth]) < threshold_spectral:
            rigth-=1

        return aux, aux2

    def computeTwoDimensionalElements(self,threshold_spectral, pxx, freqs, bins, minsize_spectral):
        detector = TwoDimensionalElementsDetector()
        detector.detect(self.signal,threshold_spectral, pxx,freqs,bins, minsize_spectral,one_dimensional_parent=self,location= self.measurementLocation)
        for elem in detector.elements:
            self.twoDimensionalElements.append(elem)

    #region Oscilogram parameter measurement
    def startTime(self):
        #the start time in s
        return round(self.indexFrom*1.0/self.signal.samplingRate,self.DECIMAL_PLACES)

    def endTime(self):
        return round(self.indexTo*1.0/self.signal.samplingRate,self.DECIMAL_PLACES)

    def duration(self):
        """
        returns the len in s of an element (float)
        """
        return round((self.indexTo-self.indexFrom)*1.0/self.signal.samplingRate,self.DECIMAL_PLACES)

    def distanceFromStartToMax(self):
        if(self.parameters["StartToMax"] is None):
            self.parameters["StartToMax"] = round(np.argmax(self.signal.data[self.indexFrom:self.indexTo])*1.0/self.signal.samplingRate,self.DECIMAL_PLACES)
        return self.parameters["StartToMax"]

    def peekToPeek(self):
        if(self.parameters["peekToPeek"] is None):
            self.parameters["peekToPeek"] = round(np.ptp(self.signal.data[self.indexFrom:self.indexTo])*1.0/(2**self.signal.bitDepth),self.DECIMAL_PLACES)
        return self.parameters["peekToPeek"]

    def rms(self):
        """
        computes the root mean square of the signal.
        indexFrom,indexTo the optionally limits of the interval
        """
        if(self.parameters["rms"] is None):
            globalSum = 0.0
            intervalSum = 0.0
            for i in range(self.indexFrom, self.indexTo):
                intervalSum += (self.signal.data[i]**2)
                if i % 10 == 0:
                    globalSum += intervalSum * 1.0 / max(self.indexTo-self.indexFrom,1)
                    intervalSum = 0.0

            globalSum += intervalSum * 1.0 / max(self.indexTo-self.indexFrom,1)
            self.parameters["rms"] = round(np.sqrt(globalSum)*1.0/(2**self.signal.bitDepth),self.DECIMAL_PLACES)
        return self.parameters["rms"]

    def spectralElements(self):
        s = len(self.twoDimensionalElements)
        return s-1 if s > 0 else s

    #endregion

    #region Spectral Parameter Measurement
    def peakFreqAverage(self):
        index = 1
        if "peak" not in self.parameters["average"]:
            Pxx , freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo],Fs=self.signal.samplingRate,NFFT=self.specgramSettings.NFFT,noverlap=self.specgramSettings.overlap,window=self.specgramSettings.window,scale_by_freq=False)
            index = np.argmax(Pxx)
            self.parameters["average"]["peak"] = int(freqs[index] - freqs[index]%10)

        if len(self.twoDimensionalElements) > 0 and not ("peak","visual") in self.parameters["average"]:
            ## Define positions of nodes
            pos = np.array([
                [self.indexFromInPxx,index],
                [self.indexToInPxx, index]
            ])
            adj = np.array([[0,1]])
            self.parameters["average"][("peak","visual")] = True
            self.twoDimensionalElements[0].addVisualGraph(pos,adj,dict(size=2, symbol='o', pxMode=False))


        return self.parameters["average"]["peak"]

    def maxFreqAverage(self,dictionary):
        if "Threshold (db)" in dictionary:
            threshold = dictionary["Threshold (db)"]
            minIndex = 1
            maxIndex = 1
            maxf,minf=0,0
            if "max" not in self.parameters["average"]:
                Pxx , freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo],Fs= self.signal.samplingRate,NFFT=self.specgramSettings.NFFT,window=self.specgramSettings.window,noverlap=self.specgramSettings.overlap,scale_by_freq=False)
                Pxx , freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo],Fs= self.signal.samplingRate,NFFT=self.specgramSettings.NFFT,window=self.specgramSettings.window,noverlap=self.specgramSettings.overlap,scale_by_freq=False)
                minf,minIndex,maxf, maxIndex, _, __ = self.freq_min_max_band_peaksAbove(0,threshold,threshold,Pxx)
                self.parameters["average"]["min"] = (minf,minIndex)
                self.parameters["average"]["max"] = (maxf,maxIndex)

            if len(self.twoDimensionalElements) > 0 and not ("max","visual") in self.parameters["average"]:
                ## Define visual positions of node
                pos = np.array([
                    [self.indexFromInPxx,self.parameters["average"]["max"][1]],
                    [self.indexToInPxx, self.parameters["average"]["max"][1]]
                ])
                adj = np.array([[0,1]])
                self.parameters["average"][("max","visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos,adj,dict(size=2, symbol='o', pxMode=False))

            return self.parameters["average"]["max"][0]

    def minFreqAverage(self,dictionary):
        if "Threshold (db)" in dictionary:
            threshold = dictionary["Threshold (db)"]
            minIndex = 1
            maxIndex = 1
            maxf,minf=0,0
            if "min" not in self.parameters["average"]:
                Pxx , freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo],Fs= self.signal.samplingRate,NFFT=self.specgramSettings.NFFT,window=self.specgramSettings.window,noverlap=self.specgramSettings.overlap,scale_by_freq=False)
                minf,minIndex,maxf, maxIndex, _, __ = self.freq_min_max_band_peaksAbove(0,threshold,threshold,Pxx)
                self.parameters["average"]["min"] = (minf,minIndex)
                self.parameters["average"]["max"] = (maxf,maxIndex)
            if len(self.twoDimensionalElements) > 0 and not ("min","visual") in self.parameters["average"]:
                ## Define positions of nodes
                pos = np.array([
                    [self.indexFromInPxx,self.parameters["average"]["min"][1]],
                    [self.indexToInPxx, self.parameters["average"]["min"][1]]
                ])
                adj = np.array([[0,1]])
                self.parameters["average"][("min","visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos,adj,dict(size=2, symbol='o', pxMode=False))
            return self.parameters["average"]["min"][0]


    def getMatrixIndexFromLocation(self,location):
        """
        @param location: the measurement location
        @return: the index of the column in the matrix that corresponds to the location
        """
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
        value = int(round(self.specgramSettings.freqs[freq_index],0))
        value -= value % 10
        return value,freq_index,round(-20*log10(1 if self.specgramSettings.freqs[freq_index]< 0.1 else self.specgramSettings.freqs[freq_index]),self.DECIMAL_PLACES)

    def peakFreq(self,dictionary):
        if "location" in dictionary:
            location = dictionary["location"]
            index = self.getMatrixIndexFromLocation(location)
            if index not in self.parameters["peakFreq"]:
                peak, freq_index, peakamplitude = self.peak_f_a(index)
                if len(self.twoDimensionalElements) > 0:
                    rect = QtGui.QGraphicsRectItem(QtCore.QRectF(self.indexFromInPxx + index, freq_index, 1, 1))
                    rect.setPen(QtGui.QPen(self.color,2))
                    t = (self.indexFromInPxx + index,freq_index,1,1)
                    self.twoDimensionalElements[0].figurePosition.append(t)
                    self.twoDimensionalElements[0].visual_figures.append([rect, True])

                self.parameters["peakFreq"][index],self.parameters["peakAmplitude"][index] = peak,peakamplitude
            return self.parameters["peakFreq"][index]
        return 0
        # return "Invalid Params"

    def peakAmplitude(self,dictionary):
        if "location" in dictionary:
            location = dictionary["location"]
            index = self.getMatrixIndexFromLocation(location)
            if index not in self.parameters["peakAmplitude"]:
                peak,freq_index,peakamplitude = self.peak_f_a(index)
                self.parameters["peakFreq"][index],self.parameters["peakAmplitude"][index] = peak,peakamplitude
            return self.parameters["peakAmplitude"][index]
        # return "Invalid Params"
        return 0

    def freq_min_max_band_peaksAbove(self,index,threshold, peaksThreshold,array=None):
        """
        returns the min freq with its index , the max freq with its index, the band width and the peaks above the threshold
        index is the location in the spectrogram matrix of the medition
        if arr is not None the meditions are made in arr an not in matrix[:,index]
        """
        arr = array if array is not None else self.matrix[:, index]
        minx,maxx = min(arr),max(arr)
        thresholdValue = (10.0**((60+threshold)/20.0))*(maxx - minx)/1000.0
        peaksThresholdValue = (10.0**((60+peaksThreshold)/20.0))*(maxx - minx)/1000.0
        regions = mlab.contiguous_regions(arr > thresholdValue)
        regionsPeaks = regions if threshold == peaksThreshold else mlab.contiguous_regions(arr > peaksThreshold)
        minf = self.specgramSettings.freqs[0]-self.specgramSettings.freqs[0] % 10
        maxf = self.specgramSettings.freqs[len(self.specgramSettings.freqs)-1]-self.specgramSettings.freqs[len(self.specgramSettings.freqs)-1] % 10
        maxfIndex,minfIndex = 0,0
        if len(regions) >0:
            minf = int(round(self.specgramSettings.freqs[regions[0][0]],0))
            minfIndex = regions[0][0]
            minf -= minf % 10
            maxf = int(round(self.specgramSettings.freqs[regions[len(regions)-1][1]],0))
            maxfIndex = regions[len(regions)-1][1]
            maxf -= maxf % 10
        return minf,minfIndex,maxf,maxfIndex,maxf-minf,len(regionsPeaks)

    def minFreq(self,dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index,threshold) not in self.parameters["minFreq"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
                self.parameters["minFreq"][(index,threshold)] = [minf,minfIndex]
                self.parameters["maxFreq"][(index,threshold)] = [maxf,maxfIndex]
                self.parameters["bandwidth"][(index,threshold)] = [band,minfIndex,maxfIndex]
                self.parameters["peaksAbove"][(index,peakthreshold)] = peaks

            if len(self.twoDimensionalElements) > 0 and not (index,"visual") in self.parameters["minFreq"]:
                ## Define positions of nodes
                pos = np.array([[self.indexFromInPxx + index,self.parameters["minFreq"][(index,threshold)][1]]])
                self.parameters["minFreq"][(index,"visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos,np.array([]),dict(size=min(self.parameters["maxFreq"][(index,threshold)][1]-self.parameters["minFreq"][(index,threshold)][1],2), symbol='d', pxMode=False))


            return self.parameters["minFreq"][(index,threshold)][0]
        # return "Invalid Params"
        return 0

    def maxFreq(self,dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index,threshold) not in self.parameters["maxFreq"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
                self.parameters["minFreq"][(index,threshold)] = [minf,minfIndex]
                self.parameters["maxFreq"][(index,threshold)] = [maxf,maxfIndex]
                self.parameters["bandwidth"][(index,threshold)] = [band,minfIndex,maxfIndex]
                self.parameters["peaksAbove"][(index,peakthreshold)] = peaks

            if len(self.twoDimensionalElements) > 0 and not  (index,"visual") in self.parameters["maxFreq"]:

                ## Define positions of nodes
                pos = np.array([
                    [self.indexFromInPxx + index, self.parameters["maxFreq"][(index,threshold)][1]]
                ])
                self.parameters["maxFreq"][ (index,"visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos,np.array([]),dict(size=min(self.parameters["maxFreq"][(index,threshold)][1]-self.parameters["minFreq"][(index,threshold)][1],2), symbol='+', pxMode=False))

            return self.parameters["maxFreq"][(index,threshold)][0]

        # return "Invalid Params"
        return 0

    def bandwidth(self,dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index,threshold) not in self.parameters["bandwidth"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
                self.parameters["minFreq"][(index,threshold)] = [minf,minfIndex]
                self.parameters["maxFreq"][(index,threshold)] = [maxf,maxfIndex]
                self.parameters["bandwidth"][(index,threshold)] = [band,minfIndex,maxfIndex]
                self.parameters["peaksAbove"][(index,peakthreshold)] = peaks

            if len(self.twoDimensionalElements) > 0 and not (index,"visual") in self.parameters["bandwidth"]:
                ## Define positions of nodes
                pos = np.array([
                    [self.indexFromInPxx + index, self.parameters["bandwidth"][(index,threshold)][1]],
                    [self.indexFromInPxx + index, self.parameters["bandwidth"][(index,threshold)][2]]
                ])
                adj = np.array([[0,1]])
                self.parameters["bandwidth"][(index,"visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos,adj,dict(size=min(self.parameters["bandwidth"][(index,threshold)][2]-self.parameters["bandwidth"][(index,threshold)][1],2),
                          symbol='+', pxMode=False))

            return self.parameters["bandwidth"][(index,threshold)][0]

        return 0
        # return "Invalid Params"

    def peaksAbove(self,dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index,peakthreshold) not in self.parameters["peaksAbove"]:
                self.parameters["minFreq"][(index,threshold)], minfIndex,self.parameters["maxFreq"][(index,threshold)], maxfIndex,\
                self.parameters["bandwidth"][(index,threshold)],self.parameters["peaksAbove"][(index,peakthreshold)] = self.freq_min_max_band_peaksAbove(index,threshold,peakthreshold)
            return self.parameters["peaksAbove"][(index,peakthreshold)]
        return 0
        # return "Invalid Params"

    #endregion

    def mouseClickEvent(self, event):
        """
        Interception of GUI events by switching this method for its similar
        in the visual figures of the element
        @param event: The event raised
        """
        self.elementClicked.emit(self.number-1)

    def setNumber(self,n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        self.number = n
        self.visual_text[0][0].setText(str(n))
        for e in self.twoDimensionalElements:
            e.setNumber(n)
        self.color = QtGui.QColor(0, 255, 0, 100) if self.number%2 == 0 else QtGui.QColor(0, 0, 255,100)
        self.lr.setBrush(pg.mkBrush(self.color))