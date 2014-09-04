from PyQt4 import QtGui
from Duetto_Core.Segmentation.Elements.Element import Element
from .QSignalVisualizerWidget import QSignalVisualizerWidget
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensional.OneDimensionalElementsDetector import DetectionType,OneDimensionalElementsDetector
import pyqtgraph as pg
import numpy as np


class QSignalDetectorWidget(QSignalVisualizerWidget):
    """This widget performs the detections operations on a signal.
    """

    def __init__(self,parent):
        QSignalVisualizerWidget.__init__(self, parent)
        self.envelopeCurve = pg.PlotCurveItem(np.array([0]), pen=pg.mkPen(self.osc_color, width=1),
                                              shadowPen=pg.mkPen(QtGui.QColor(255, 0, 0), width=3))
        self.axesOscilogram.addItem(self.envelopeCurve)
        self.envelopeFactor = 2 #factor to expand the envelope for best visualization
        self.visibleElements = True
        self.Elements = []  # list of elements detected in oscilogram each element contains the object it self and the extra data for visualize it
        self.elements_detector = OneDimensionalElementsDetector()

    def load_Theme(self, theme):
        """
        this method implements the  way in wich the controls load the theme
        all changes made by the theme are made in this place
        """
        #assert isinstance(theme,SerializedData)
        QSignalVisualizerWidget.load_Theme(self,theme)

        self.histogram.item.region.setRegion(theme.histRange)
        self.histogram.item.gradient.restoreState(theme.colorBarState)


        self.envelopeCurve.setPen(pg.mkPen(self.osc_color, width=1))
        self.envelopeCurve.setShadowPen(pg.mkPen(QtGui.QColor(255, 0, 0), width=3))

    def setEnvelopeVisibility(self, bool):
        inaxes = self.envelopeCurve in self.axesOscilogram.items()
        if bool and not inaxes:
            self.axesOscilogram.addItem(self.envelopeCurve)
        elif not bool and inaxes:
            self.axesOscilogram.removeItem(self.envelopeCurve)
        self.axesOscilogram.update()

    def getTransformedEnvelope(self, array):
        self.envelopeFactor = (2.0 ** (self.signalProcessor.signal.bitDepth) * self.maxYOsc / 100) / array[
            np.argmax(array)]
        return (self.envelopeFactor * array - 2 ** (self.signalProcessor.signal.bitDepth - 1) * self.maxYOsc / 100)

    def detectElements(self, threshold=20, decay=1, minSize=0, detectionsettings=None, softfactor=5, merge_factor=50,
                       threshold2=0, threshold_spectral=95, pxx=[], freqs=[], bins=[], minsize_spectral=(0, 0),
                       location=None, progress=None, findSpectralSublements=True):
        """
        Detect elements in the signal using the parameters.
        Just performs the detection.
        To visualize all the elements has to call drawElements after detection
        @param threshold:
        @param decay:
        @param minSize:
        @param detectionsettings:
        @param softfactor:
        @param merge_factor:
        @param threshold2:
        @param threshold_spectral:
        @param pxx:
        @param freqs:
        @param bins:
        @param minsize_spectral:
        @param location:
        @param progress:
        @param findSpectralSublements:
        """
        self.clearDetection()

        a,b = self.mainCursor.min,self.mainCursor.max

        self.mainCursor.min,self.mainCursor.max = 0,len(self.signalProcessor.signal.data)

        self.computeSpecgramSettings()

        self.elements_detector.detect(self.signalProcessor.signal, 0, len(self.signalProcessor.signal.data),
                                      threshold=threshold, detectionsettings=detectionsettings, decay=decay,
                                      minSize=minSize, softfactor=softfactor, merge_factor=merge_factor,
                                      secondThreshold=threshold2, threshold_spectral=threshold_spectral,
                                      minsize_spectral=minsize_spectral, location=location, progress=progress,
                                      findSpectralSublements=findSpectralSublements,
                                      specgramSettings=self.specgramSettings)

        if detectionsettings is None or detectionsettings.detectiontype == DetectionType.Envelope_Abs_Decay_Averaged or detectionsettings.detectiontype == DetectionType.Envelope_Rms:
            self.envelopeCurve.setData(self.getTransformedEnvelope(self.elements_detector.envelope))
            self.setEnvelopeVisibility(True)
            self.axesOscilogram.threshold.setValue(self.elements_detector.getThreshold())
        else:
            self.setEnvelopeVisibility(False)

        self.axesOscilogram.setVisibleThreshold(True)

        for c in self.elements_detector.elements:
            self.Elements.append(c)# the elment the space for the span selector and the text
            #incorporar deteccion en espectrograma

        if a != self.mainCursor.min or b != self.mainCursor.max:
            self.zoomCursor.min,self.zoomCursor.max = a,b
            self.zoomIn()

    def changeElementsVisibility(self, visible, element_type=Element.Figures, oscilogramItems=True):
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

    def shiftElementsVisualObjects(self):
        """
        Shifts left or right (if n is negative or positive respectively) all the detected elements's
        visual objects. That means all the visual representation in specgram widget visualization.
        This is necessary because the specgram is recomputed in every new piece(window) of analysis\
        for efficiency.
        @param n: the index coordinates to shift all the elements in the specgram widget
        """
        for x in self.Elements:
            for elem in x.twoDimensionalElements:
                elem.shift(lambda x: self._from_osc_to_spec(self._from_spec_to_osc(x)))

    def computeSpecgramSettings(self, overlap=None):
        QSignalVisualizerWidget.computeSpecgramSettings(self,overlap)
        self.shiftElementsVisualObjects()

    def drawElements(self, oscilogramItems=None):
        # if oscilogramItems = None its updated the oscilogram and spectrogram widgets
        osc = oscilogramItems is None or oscilogramItems
        spec = oscilogramItems is None or not oscilogramItems

        if self.visibleOscilogram and osc:
            for i in range(len(self.Elements)):
                if self.Elements[i].visible:
                    for item, visible in self.Elements[i].visualwidgets():
                        if not visible:
                            self.axesOscilogram.removeItem(item)
                        else:
                            if not item in self.axesOscilogram.items() and visible:
                                self.axesOscilogram.addItem(item)
                else:
                    for item, visible in self.Elements[i].visualwidgets():
                        self.axesOscilogram.removeItem(item)
            self.axesOscilogram.update()

        if (self.visibleSpectrogram and spec):
            for i in range(len(self.Elements)):
                for j in range(len(self.Elements[i].twoDimensionalElements)):
                    if self.Elements[i].twoDimensionalElements[j].visible:
                        for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            if not visible:
                                self.axesSpecgram.viewBox.removeItem(item)
                            else:
                                if not item in self.axesSpecgram.items() and visible:
                                    self.axesSpecgram.viewBox.addItem(item)
                    else:
                        for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            self.axesSpecgram.viewBox.removeItem(item)

            self.axesSpecgram.update()

    def removeVisualElements(self, oscilogram=True, specgram=True,elements=None):
        elements = elements if elements is not None else self.Elements
        if (oscilogram):
            for elem in elements:
                for item, visible in elem.visualwidgets():
                    self.axesOscilogram.removeItem(item)
        if (specgram):
            for elem in elements:
                for elem2 in elem.twoDimensionalElements:
                    for item, visible in elem2.visualwidgets():
                        self.axesSpecgram.viewBox.removeItem(item)

    def clearDetection(self, oscilogram=True, specgram=True):
        self.removeVisualElements(oscilogram=True, specgram=True)
        self.Elements = [] if oscilogram and specgram else self.Elements

    def selectElement(self, number=-1):
        if len(self.Elements) > number and number >= 0:
            f, t = self.Elements[number].indexFrom, self.Elements[number].indexTo
            self.axesOscilogram.select_region(f, t, pg.mkBrush(QtGui.QColor(255, 255, 255, 150)))
            if f < self.mainCursor.min or t > self.mainCursor.max:
                sizeInterval = self.mainCursor.max - self.mainCursor.min
                self.mainCursor.min = max(0, (f + t - sizeInterval) / 2)
                self.mainCursor.max = min(self.mainCursor.min + sizeInterval, len(self.signalProcessor.signal.data))
                self.refresh()
        else:
            self.axesOscilogram.select_region(0, 0)

    @property
    def deleteSelectedElements(self):
        """
        Deletes the elements between the zoom cursor if any
        returns the tuple (x,y) of init and end of the interval deleted.
        If no element is deleted returns None
        """
        start,end = self.zoomCursor.min,self.zoomCursor.max
        if end == start or len(self.Elements) == 0:
            return None

        sorted_arr = np.array([x.indexFrom for x in self.Elements])

        indexFrom,indexTo = np.searchsorted(sorted_arr,start),np.searchsorted(sorted_arr,end)
        indexFrom -= 1 if indexFrom > 0 and start <= self.Elements[indexFrom-1].indexTo else 0

        if indexTo < indexFrom or indexTo > len(self.Elements):
            return None

        self.removeVisualElements(elements=self.Elements[indexFrom:indexTo])

        self.Elements = self.Elements[0:indexFrom]+self.Elements[indexTo:]

        for i,x in enumerate(self.Elements):
            x.setNumber(i+1)

        self.axesOscilogram.update()
        self.axesSpecgram.update()

        return indexFrom,indexTo-1

    def refresh(self, dataChanged=True, updateOscillogram=True, updateSpectrogram=True, partial=True):
        QSignalVisualizerWidget.refresh(self,dataChanged, updateOscillogram, updateSpectrogram, partial)
        if self.visibleElements:
            self.drawElements()