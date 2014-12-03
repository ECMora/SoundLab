from PyQt4 import QtGui
import pyqtgraph as pg
import numpy as np
from sound_lab_core.Segmentation.Elements.Element import Element
from QSignalVisualizerWidget import QSignalVisualizerWidget
from sound_lab_core.Segmentation.Detectors.ElementsDetectors.OneDimensional.OneDimensionalElementsDetector import \
    DetectionType, OneDimensionalElementsDetector


class QSignalDetectorWidget(QSignalVisualizerWidget):
    """
    This widget performs the detections operations on a signal.
    Provide methods to interact with the detected segments: Highlight, remove, etc
    """

    def __init__(self, parent):
        QSignalVisualizerWidget.__init__(self, parent)

        #region Envelope curve visualization
        # curve to display envelope when detection method is envelope
        self.envelopeCurve = pg.PlotCurveItem(np.array([0]), pen=pg.mkPen(self.osc_color, width=1),
                                              shadowPen=pg.mkPen(QtGui.QColor(255, 0, 0), width=3))

        #add an extra item to display envelope in oscilogram graph
        self.axesOscilogram.addItem(self.envelopeCurve)

        #factor to expand the envelope for best visualization
        self.envelopeFactor = 2

        #endregion

        #visibility of all detected elements. is used when they are displayed
        self.visibleElements = True

        #list of elements detected each element contains the object
        #and the extra data for visualize it
        self.Elements = []

        #detector for one dimensional detection
        self.elements_detector = OneDimensionalElementsDetector()

    #region Elements
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

        a, b = self.mainCursor.min, self.mainCursor.max

        self.mainCursor.min, self.mainCursor.max = 0, len(self.signalProcessor.signal.data)

        self.computeSpecgramSettings()

        self.elements_detector.detect(self.signalProcessor.signal, 0, len(self.signalProcessor.signal.data),
                                      threshold=threshold, detectionsettings=detectionsettings, decay=decay,
                                      minSize=minSize, softfactor=softfactor, merge_factor=merge_factor,
                                      secondThreshold=threshold2, threshold_spectral=threshold_spectral,
                                      minsize_spectral=minsize_spectral, location=location, progress=progress,
                                      findSpectralSublements=findSpectralSublements,
                                      specgramSettings=self.specgramSettings)

        if detectionsettings is None or detectionsettings.detectiontype == DetectionType.Envelope_Abs_Decay_Averaged or detectionsettings.detectiontype == DetectionType.Envelope_Rms:
            self.envelopeCurve.setData(self.getTransformedEnvelope())
            self.setEnvelopeVisibility(True)
            self.axesOscilogram.threshold.setValue(self.elements_detector.getThreshold())
        else:
            self.setEnvelopeVisibility(False)

        self.axesOscilogram.setVisibleThreshold(True)

        for c in self.elements_detector.elements:
            self.Elements.append(c)  # the elment the space for the span selector and the text
            # incorporar deteccion en espectrograma

        if a != self.mainCursor.min or b != self.mainCursor.max:
            self.zoomCursor.min, self.zoomCursor.max = a, b
            self.zoomIn()

    def changeElementsVisibility(self, visible, element_type=Element.Figures, oscilogramItems=True):
        """
        Change the visibility of the visual items
        :param visible:
        :param element_type:
        :param oscilogramItems:
        """
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
        QSignalVisualizerWidget.computeSpecgramSettings(self, overlap)
        self.shiftElementsVisualObjects()

    def drawElements(self, oscilogramItems=None):
        # if oscilogramItems = None its updated the oscilogram and spectrogram widgets
        """
        Add to the visual gui widgets the visible elements of the detected segments
        :param oscilogramItems: true if draw elements in oscilogram false for spectrogram
        None for both
        """
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

        if self.visibleSpectrogram and spec:
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

    def removeVisualElements(self, oscilogram=True, specgram=True, elements=None):
        """
        Method that remove the visual representation of the elements in the widget.
        Used for remove selected elements or a group of them.
        :param oscilogram: Removes the oscilogram visual elements
        :param specgram: Removes the spectrogram visual elements
        :param elements: the elements that would be (visually) removed.
        all the self.Elements if None
        """
        elements = elements if elements is not None else self.Elements
        if oscilogram:
            for elem in elements:
                for item, visible in elem.visualwidgets():
                    self.axesOscilogram.removeItem(item)
        if specgram:
            for elem in elements:
                for elem2 in elem.twoDimensionalElements:
                    for item, visible in elem2.visualwidgets():
                        self.axesSpecgram.viewBox.removeItem(item)

    def clearDetection(self):
        """
        Clears the detected elements and their visual components from the widget
        """
        self.removeVisualElements(oscilogram=True, specgram=True)
        self.Elements = []

    def selectElement(self, number=-1):
        """
        Method that select an element in the widget
        by highlighting it
        :param number: the element index. Must be > 0.
        """
        if 0 <= number < len(self.Elements):
            index_from, index_to = self.Elements[number].indexFrom, self.Elements[number].indexTo
            self.axesOscilogram.select_region(index_from, index_to, pg.mkBrush(QtGui.QColor(255, 255, 255, 150)))
            if index_from < self.mainCursor.min or index_to > self.mainCursor.max:
                sizeInterval = self.mainCursor.max - self.mainCursor.min

                #move the interval to make completely visible the element selected
                self.mainCursor.min = max(0, (index_from + index_to - sizeInterval) / 2)
                self.mainCursor.max = min(self.mainCursor.min + sizeInterval,
                                          len(self.signalProcessor.signal.data))
                self.graph()
        else:
            self.axesOscilogram.select_region(0, 0)

    @property
    def deleteSelectedElements(self):
        """
        Deletes the elements between the selection
        (zoom cursor if zoom cursor is selected and there is a selection or
        the visible interval otherwise)
        returns the tuple (x,y) of init and end of the interval deleted.
        If no element is deleted returns None
        """
        start, end = self.getIndexFromAndTo()

        if end == start or len(self.Elements) == 0:
            return None

        #create a list with start index of each element
        sorted_arr = np.array([x.indexFrom for x in self.Elements])

        # binary search
        indexFrom, indexTo = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)
        indexFrom -= 1 if indexFrom > 0 and start <= self.Elements[indexFrom - 1].indexTo else 0

        if indexTo < indexFrom or indexTo > len(self.Elements):
            return None

        self.removeVisualElements(elements=self.Elements[indexFrom:indexTo])

        self.Elements = self.Elements[0:indexFrom] + self.Elements[indexTo:]

        for i, x in enumerate(self.Elements):
            x.setNumber(i + 1)

        self.axesOscilogram.update()
        self.axesSpecgram.update()

        return indexFrom, indexTo - 1

    #endregion

    #region Envelope Visualization

    def setEnvelopeVisibility(self, visibility):
        """
        Method that change the visibility of the envelope curve
        :param visibility: visibility of the envelope curve
        """
        envelope_in_axes = self.envelopeCurve in self.axesOscilogram.items()

        # alternative implem
        # method = self.axesOscilogram.addItem if (not envelope_in_axes and visibility) \
        # else (self.axesOscilogram.removeItem if (not visibility and envelope_in_axes) else lambda x: x)
        # method(self.envelopeCurve)

        if not envelope_in_axes and visibility:
            #the curve must be set to visible
            self.axesOscilogram.addItem(self.envelopeCurve)
        elif not visibility and envelope_in_axes:
            #the curve must be set to invisible
            self.axesOscilogram.removeItem(self.envelopeCurve)

        self.axesOscilogram.update()

    def getTransformedEnvelope(self):
        """
        Return the array of the envelope curve scaled by the envelope factor for display.
        :return: scaled envelope array
        """
        self.envelopeFactor = ((2.0 ** self.signalProcessor.signal.bitDepth) * self.maxYOsc / 100) / \
                              self.elements_detector.envelope[
                                  np.argmax(self.elements_detector.envelope)]
        return (self.envelopeFactor * self.elements_detector.envelope - 2 ** (
            self.signalProcessor.signal.bitDepth - 1) * self.maxYOsc / 100)

    #endregion

    def load_Theme(self, theme):
        """
        this method implements the  way in which the widget load the theme
        """
        QSignalVisualizerWidget.load_Theme(self, theme)

        #update values for envelope display
        self.envelopeCurve.setPen(pg.mkPen(self.osc_color, width=1))
        self.envelopeCurve.setShadowPen(pg.mkPen(QtGui.QColor(255, 0, 0), width=3))

    def refresh(self, dataChanged=True, updateOscillogram=True, updateSpectrogram=True, partial=True):
        QSignalVisualizerWidget.refresh(self, dataChanged, updateOscillogram, updateSpectrogram, partial)
        if self.visibleElements:
            self.drawElements()

