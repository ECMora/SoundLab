from math import log10
from PyQt4.QtGui import QFont
import numpy as np
import pyqtgraph as pg
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement
from sound_lab_core.Segmentation.Detectors.TwoDimensional.TwoDimensionalElementsDetector import \
    TwoDimensionalElementsDetector
from sound_lab_core.Elements.TwoDimensionalElements.TwoDimensionalElement import SpecgramElement


class OscilogramElement(OneDimensionalElement):
    def __init__(self, signal, indexFrom, indexTo, number=0):
        """
        @param signal: The signal in wich is defined this element
        @param findSpectralSublements: If this element should perform the search of sub elements
        @param specgramSettings: Settings of specgram computation
        @param trim_threshold: Threshold to select the section of specgram corresponding
        to this element for parameter measurement. The section depends of overlap and NFFT in  specgramSettings
        but if there is no energy enough that section would be trimed for left and right
        until the energy increases this trim_threshold.
        @return:
        """
        OneDimensionalElement.__init__(self, signal, indexFrom, indexTo)
        # the visible text for number
        text = pg.TextItem(str(number), color=(255, 255, 255), anchor=(0.5, 0.5))
        text.setPos(self.indexFrom / 2.0 + self.indexTo / 2.0, 0.75 * 2 ** (signal.bitDepth - 1))

        font = QFont()
        font.setPointSize(13)
        text.setFont(font)
        self.number = number

        self.color = self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN
        self.element_region = pg.LinearRegionItem([self.indexFrom, self.indexTo], movable=False, brush=(pg.mkBrush(self.color)))
        self.twoDimensionalElements = []

        # the memoize pattern implemented to compute parameters functions
        self.parameters = dict(StartToMax=None, peekToPeek=None, rms=None, minFreq=dict(), maxFreq=dict(),
                               average=dict(), peakFreq=dict(), peaksAbove=dict(), peakAmplitude=dict(),
                               bandwidth=dict())

        # a tooltip for the element's easy information access
        # tooltip = "Element: " + str(self.number) + "\nStart Time: " + str(self.startTime()) + "s\n" \
        #           + "End Time:" + str(self.endTime()) + "s\n" \
        #           + "RMS: " + str(self.rms()) + "\n" \
        #           + "PeekToPeek: " + str(self.peekToPeek())
        # self.element_region.setToolTip(tooltip)

        self.element_region.mouseClickEvent = self.mouseClickEvent

        # update the visual representation
        self.visual_figures.append([self.element_region, True])  # item visibility
        self.visual_text.append([text, True])

        # self.detectTwoDimElements()

    def detectTwoDimElements(self):

        if self.specgramSettings.Pxx != [] and self.specgramSettings.bins != [] and self.specgramSettings.freqs != []:
            # spec_resolution, temp_resolution = signal.samplingRate/2.0*len(freqs),bins[1]-bins[0]
            spec_resolution, temp_resolution = 1000.0 / self.specgramSettings.freqs[1], (
                self.specgramSettings.bins[1] - self.specgramSettings.bins[0]) * 1000.0

            # minsize came with the hz, sec of minThresholdLabel size elements and its translated to index values in pxx for comparations
            minsize_spectral = (
                max(1, int(minsize_spectral[0] * spec_resolution)), max(1, int(minsize_spectral[1] * temp_resolution)))

            sr = signal.samplingRate * 1.0
            columnsize = (self.specgramSettings.bins[1] - self.specgramSettings.bins[0]) * sr
            overlap = int(round(self.specgramSettings.overlap, 0))
            overlap_delay = 0 if overlap <= 0 else 99 if overlap >= 100 else overlap / (100 - overlap)

            aux = max(0, int(indexFrom * 1.0 / columnsize))
            aux2 = min(int(indexTo * 1.0 / columnsize) + overlap_delay, len(self.specgramSettings.Pxx[0]))

            left, rigth = self.trimMatrix(self.specgramSettings.Pxx, aux, aux2, trim_threshold)

            self.matrix = self.specgramSettings.Pxx[:, left:rigth]
            self.indexFromInPxx, self.indexToInPxx = left, rigth

            self.twoDimensionalElements = [
                SpecgramElement(signal, self.matrix, self.specgramSettings.freqs, 0, len(self.specgramSettings.freqs),
                                self.specgramSettings.bins, 0, rigth - left, number, self, location,
                                multipleSubelements=False)]

            if findSpectralSublements:
                self.computeTwoDimensionalElements(threshold_spectral, self.matrix, self.specgramSettings.freqs,
                                                   self.specgramSettings.bins, minsize_spectral)

    def trimMatrix(self, pxx, aux, aux2, threshold_spectral):
        left = aux
        rigth = aux2 - 1
        while left < rigth and max(pxx[:, left]) < threshold_spectral:
            left += 1
        while rigth > left and max(pxx[:, rigth]) < threshold_spectral:
            rigth -= 1

        return aux, aux2

    def computeTwoDimensionalElements(self, threshold_spectral, pxx, freqs, bins, minsize_spectral):
        detector = TwoDimensionalElementsDetector()
        detector.detect(self.signal, threshold_spectral, pxx, freqs, bins, minsize_spectral,
                        one_dimensional_parent=self)
        for elem in detector.elements:
            self.twoDimensionalElements.append(elem)

    # region Spectral Parameter Measurement
    def peakFreqAverage(self):
        index = 1
        if "peak" not in self.parameters["average"]:
            Pxx, freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo], Fs=self.signal.samplingRate,
                                  NFFT=self.specgramSettings.NFFT, noverlap=self.specgramSettings.overlap,
                                  window=self.specgramSettings.window, scale_by_freq=False)
            index = np.argmax(Pxx)
            self.parameters["average"]["peak"] = int(freqs[index] - freqs[index] % 10)

        if len(self.twoDimensionalElements) > 0 and not ("peak", "visual") in self.parameters["average"]:
            # #  Define positions of nodes
            pos = np.array([
                [self.indexFromInPxx, index],
                [self.indexToInPxx, index]
            ])
            adj = np.array([[0, 1]])
            self.parameters["average"][("peak", "visual")] = True
            self.twoDimensionalElements[0].addVisualGraph(pos, adj, dict(size=2, symbol='o', pxMode=False))

        return self.parameters["average"]["peak"]

    def maxFreqAverage(self, dictionary):
        if "Threshold (db)" in dictionary:
            threshold = dictionary["Threshold (db)"]
            minIndex = 1
            maxIndex = 1
            maxf, minf = 0, 0
            if "maxThresholdLabel" not in self.parameters["average"]:
                Pxx, freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo], Fs=self.signal.samplingRate,
                                      NFFT=self.specgramSettings.NFFT, window=self.specgramSettings.window,
                                      noverlap=self.specgramSettings.overlap, scale_by_freq=False)
                Pxx, freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo], Fs=self.signal.samplingRate,
                                      NFFT=self.specgramSettings.NFFT, window=self.specgramSettings.window,
                                      noverlap=self.specgramSettings.overlap, scale_by_freq=False)
                minf, minIndex, maxf, maxIndex, _, __ = self.freq_min_max_band_peaksAbove(0, threshold, threshold, Pxx)
                self.parameters["average"]["minThresholdLabel"] = (minf, minIndex)
                self.parameters["average"]["maxThresholdLabel"] = (maxf, maxIndex)

            if len(self.twoDimensionalElements) > 0 and not ("maxThresholdLabel", "visual") in self.parameters[
                "average"]:
                # #  Define visual positions of node
                pos = np.array([
                    [self.indexFromInPxx, self.parameters["average"]["maxThresholdLabel"][1]],
                    [self.indexToInPxx, self.parameters["average"]["maxThresholdLabel"][1]]
                ])
                adj = np.array([[0, 1]])
                self.parameters["average"][("maxThresholdLabel", "visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos, adj, dict(size=2, symbol='o', pxMode=False))

            return self.parameters["average"]["maxThresholdLabel"][0]

    def minFreqAverage(self, dictionary):
        if "Threshold (db)" in dictionary:
            threshold = dictionary["Threshold (db)"]
            minIndex = 1
            maxIndex = 1
            maxf, minf = 0, 0
            if "minThresholdLabel" not in self.parameters["average"]:
                Pxx, freqs = mlab.psd(self.signal.data[self.indexFrom:self.indexTo], Fs=self.signal.samplingRate,
                                      NFFT=self.specgramSettings.NFFT, window=self.specgramSettings.window,
                                      noverlap=self.specgramSettings.overlap, scale_by_freq=False)
                minf, minIndex, maxf, maxIndex, _, __ = self.freq_min_max_band_peaksAbove(0, threshold, threshold, Pxx)
                self.parameters["average"]["minThresholdLabel"] = (minf, minIndex)
                self.parameters["average"]["maxThresholdLabel"] = (maxf, maxIndex)
            if len(self.twoDimensionalElements) > 0 and not ("minThresholdLabel", "visual") in self.parameters[
                "average"]:
                # #  Define positions of nodes
                pos = np.array([
                    [self.indexFromInPxx, self.parameters["average"]["minThresholdLabel"][1]],
                    [self.indexToInPxx, self.parameters["average"]["minThresholdLabel"][1]]
                ])
                adj = np.array([[0, 1]])
                self.parameters["average"][("minThresholdLabel", "visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos, adj, dict(size=2, symbol='o', pxMode=False))
            return self.parameters["average"]["minThresholdLabel"][0]

    def getMatrixIndexFromLocation(self, location):
        """
        @param location: the measurement location
        @return: the index of the column in the matrix that corresponds to the location
        """
        return 0


    # The following methods measure properties that needs aditional parameters for its calculation
    # dict are a dictionary with the aditional data
    #
    def peak_f_a(self, index):
        """
        returns the peak frecuency and amplitude in db in the index location
        """
        freq_index = np.argmax(self.matrix[:, index])
        minIndex = np.argmin(self.matrix[:, index])
        value = int(round(self.specgramSettings.freqs[freq_index], 0))
        value -= value % 10
        return value, freq_index, round(-20 * log10(
            1 if self.specgramSettings.freqs[freq_index] < 0.1 else self.specgramSettings.freqs[freq_index]),
                                        self.DECIMAL_PLACES)

    def peakFreq(self, dictionary):
        if "location" in dictionary:
            location = dictionary["location"]
            index = self.getMatrixIndexFromLocation(location)
            if index not in self.parameters["peakFreq"]:
                peak, freq_index, peakamplitude = self.peak_f_a(index)
                if len(self.twoDimensionalElements) > 0:
                    rect = QtGui.QGraphicsRectItem(QtCore.QRectF(self.indexFromInPxx + index, freq_index, 1, 1))
                    rect.setPen(QtGui.QPen(self.color, 2))
                    t = (self.indexFromInPxx + index, freq_index, 1, 1)
                    self.twoDimensionalElements[0].figurePosition.append(t)
                    self.twoDimensionalElements[0].visual_figures.append([rect, True])

                self.parameters["peakFreq"][index], self.parameters["peakAmplitude"][index] = peak, peakamplitude
            return self.parameters["peakFreq"][index]
        return 0
        # return "Invalid Params"

    def peakAmplitude(self, dictionary):
        if "location" in dictionary:
            location = dictionary["location"]
            index = self.getMatrixIndexFromLocation(location)
            if index not in self.parameters["peakAmplitude"]:
                peak, freq_index, peakamplitude = self.peak_f_a(index)
                self.parameters["peakFreq"][index], self.parameters["peakAmplitude"][index] = peak, peakamplitude
            return self.parameters["peakAmplitude"][index]
        # return "Invalid Params"
        return 0

    def freq_min_max_band_peaksAbove(self, index, threshold, peaksThreshold, array=None):
        """
        returns the minThresholdLabel freq with its index , the maxThresholdLabel freq with its index, the band width and the peaks above the threshold
        index is the location in the spectrogram matrix of the medition
        if arr is not None the meditions are made in arr an not in matrix[:,index]
        """
        arr = array if array is not None else self.matrix[:, index]
        minx, maxx = min(arr), max(arr)
        thresholdValue = (10.0 ** ((60 + threshold) / 20.0)) * (maxx - minx) / 1000.0
        peaksThresholdValue = (10.0 ** ((60 + peaksThreshold) / 20.0)) * (maxx - minx) / 1000.0
        regions = mlab.contiguous_regions(arr > thresholdValue)
        regionsPeaks = regions if threshold == peaksThreshold else mlab.contiguous_regions(arr > peaksThreshold)
        minf = self.specgramSettings.freqs[0] - self.specgramSettings.freqs[0] % 10
        maxf = self.specgramSettings.freqs[len(self.specgramSettings.freqs) - 1] - self.specgramSettings.freqs[len(
            self.specgramSettings.freqs) - 1] % 10
        maxfIndex, minfIndex = 0, 0
        if len(regions) > 0:
            minf = int(round(self.specgramSettings.freqs[regions[0][0]], 0))
            minfIndex = regions[0][0]
            minf -= minf % 10
            maxf = int(round(self.specgramSettings.freqs[regions[len(regions) - 1][1]], 0))
            maxfIndex = regions[len(regions) - 1][1]
            maxf -= maxf % 10
        return minf, minfIndex, maxf, maxfIndex, maxf - minf, len(regionsPeaks)

    def minFreq(self, dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index, threshold) not in self.parameters["minFreq"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index, threshold,
                                                                                                  peakthreshold)
                self.parameters["minFreq"][(index, threshold)] = [minf, minfIndex]
                self.parameters["maxFreq"][(index, threshold)] = [maxf, maxfIndex]
                self.parameters["bandwidth"][(index, threshold)] = [band, minfIndex, maxfIndex]
                self.parameters["peaksAbove"][(index, peakthreshold)] = peaks

            if len(self.twoDimensionalElements) > 0 and not (index, "visual") in self.parameters["minFreq"]:
                # #  Define positions of nodes
                pos = np.array([[self.indexFromInPxx + index, self.parameters["minFreq"][(index, threshold)][1]]])
                self.parameters["minFreq"][(index, "visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos, np.array([]), dict(size=min(
                    self.parameters["maxFreq"][(index, threshold)][1] - self.parameters["minFreq"][(index, threshold)][
                        1], 2), symbol='d', pxMode=False))

            return self.parameters["minFreq"][(index, threshold)][0]
        # return "Invalid Params"
        return 0

    def maxFreq(self, dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index, threshold) not in self.parameters["maxFreq"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index, threshold,
                                                                                                  peakthreshold)
                self.parameters["minFreq"][(index, threshold)] = [minf, minfIndex]
                self.parameters["maxFreq"][(index, threshold)] = [maxf, maxfIndex]
                self.parameters["bandwidth"][(index, threshold)] = [band, minfIndex, maxfIndex]
                self.parameters["peaksAbove"][(index, peakthreshold)] = peaks

            if len(self.twoDimensionalElements) > 0 and not (index, "visual") in self.parameters["maxFreq"]:
                # #  Define positions of nodes
                pos = np.array([
                    [self.indexFromInPxx + index, self.parameters["maxFreq"][(index, threshold)][1]]
                ])
                self.parameters["maxFreq"][(index, "visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos, np.array([]), dict(size=min(
                    self.parameters["maxFreq"][(index, threshold)][1] - self.parameters["minFreq"][(index, threshold)][
                        1], 2), symbol='+', pxMode=False))

            return self.parameters["maxFreq"][(index, threshold)][0]

        # return "Invalid Params"
        return 0

    def bandwidth(self, dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index, threshold) not in self.parameters["bandwidth"]:
                minf, minfIndex, maxf, maxfIndex, band, peaks = self.freq_min_max_band_peaksAbove(index, threshold,
                                                                                                  peakthreshold)
                self.parameters["minFreq"][(index, threshold)] = [minf, minfIndex]
                self.parameters["maxFreq"][(index, threshold)] = [maxf, maxfIndex]
                self.parameters["bandwidth"][(index, threshold)] = [band, minfIndex, maxfIndex]
                self.parameters["peaksAbove"][(index, peakthreshold)] = peaks

            if len(self.twoDimensionalElements) > 0 and not (index, "visual") in self.parameters["bandwidth"]:
                # #  Define positions of nodes
                pos = np.array([
                    [self.indexFromInPxx + index, self.parameters["bandwidth"][(index, threshold)][1]],
                    [self.indexFromInPxx + index, self.parameters["bandwidth"][(index, threshold)][2]]
                ])
                adj = np.array([[0, 1]])
                self.parameters["bandwidth"][(index, "visual")] = True
                self.twoDimensionalElements[0].addVisualGraph(pos, adj, dict(size=min(
                    self.parameters["bandwidth"][(index, threshold)][2] -
                    self.parameters["bandwidth"][(index, threshold)][1], 2),
                                                                             symbol='+', pxMode=False))

            return self.parameters["bandwidth"][(index, threshold)][0]

        return 0
        # return "Invalid Params"

    def peaksAbove(self, dictionary):
        if "location" in dictionary and "Threshold (db)" in dictionary:
            location = dictionary["location"]
            threshold = dictionary["Threshold (db)"]
            peakthreshold = dictionary["Peaks Threshold (db)"] if "Peaks Threshold (db)" in dictionary else threshold
            index = self.getMatrixIndexFromLocation(location)
            if (index, peakthreshold) not in self.parameters["peaksAbove"]:
                self.parameters["minFreq"][(index, threshold)], minfIndex, self.parameters["maxFreq"][
                    (index, threshold)], maxfIndex, \
                self.parameters["bandwidth"][(index, threshold)], self.parameters["peaksAbove"][
                    (index, peakthreshold)] = self.freq_min_max_band_peaksAbove(index, threshold, peakthreshold)
            return self.parameters["peaksAbove"][(index, peakthreshold)]
        return 0
        # return "Invalid Params"

    # endregion

    def mouseClickEvent(self, event):
        """
        Interception of GUI events by switching this method for its similar
        in the visual figures of the element
        @param event: The event raised
        """
        self.elementClicked.emit(self.number - 1)

    def setNumber(self, n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        self.number = n
        self.visual_text[0][0].setText(str(n))

        for e in self.twoDimensionalElements:
            e.setNumber(n)

        self.color = self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN
        self.element_region.setBrush(pg.mkBrush(self.color))