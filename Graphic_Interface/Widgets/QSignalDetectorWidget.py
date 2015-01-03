from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from sound_lab_core.Segmentation.Elements.Element import Element
from QSignalVisualizerWidget import QSignalVisualizerWidget
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    DetectionType, OneDimensionalElementsDetector


class QSignalDetectorWidget(QSignalVisualizerWidget):
    """
    This widget performs the detections operations on a signal.
    Provide methods to interact with the detected segments: Highlight, remove, etc
    """

    # SIGNALS
    # signal raised when a detected element is clicked
    # raise the index of the clicked element
    elementClicked = QtCore.pyqtSignal(int)

    # CONSTANTS
    # the brush that is used to draw the selected region or Element
    SELECTED_ELEMENT_BRUSH = pg.mkBrush(QtGui.QColor(255, 255, 255, 60))

    def __init__(self, parent):
        # items to highlight elements or regions in the graph
        self.oscSelectionRegion = pg.LinearRegionItem([0, 0], movable=False, brush=self.SELECTED_ELEMENT_BRUSH)

        self.specSelectionRegion = pg.LinearRegionItem([0, 0], movable=False, brush=self.SELECTED_ELEMENT_BRUSH)

        # detector for one dimensional detection
        self.elements_detector = OneDimensionalElementsDetector()

        # region Envelope curve visualization
        # curve to display envelope when detection method is envelope
        self.envelopeCurve = pg.PlotCurveItem(np.array([0]), pen=pg.mkPen("CC3", width=1),
                                              shadowPen=pg.mkPen(QtGui.QColor(255, 0, 0), width=3))

        # factor to expand the envelope for best visualization
        self.envelopeFactor = 2

        # endregion

        # visibility of all detected elements.
        # is used when they are displayed
        self.visibleElements = True

        # list of detected elements. Each element contains the object
        # and the extra data for visualize it
        self.Elements = []

        QSignalVisualizerWidget.__init__(self, parent)

        # add an extra item to display envelope in oscilogram graph
        self.axesOscilogram.addItem(self.envelopeCurve)

    # region Elements
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

        if detectionsettings is None or \
                        detectionsettings.detectiontype == DetectionType.Envelope_Abs_Decay_Averaged or \
                        detectionsettings.detectiontype == DetectionType.Envelope_Rms:

            self.envelopeCurve.setData(self.getScaledEnvelope())
            self.setEnvelopeVisibility(True)
            self.axesOscilogram.threshold.setValue(self.elements_detector.getThreshold())

        else:
            self.setEnvelopeVisibility(False)

        # get the elements detected by the detector
        for index, c in enumerate(self.elements_detector.elements):
            self.Elements.append(c)
            # connect the click event of an element with the signal of the widget
            c.elementClicked.connect(lambda: self.elementClicked.emit(index))

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
        @param   : the index coordinates to shift all the elements in the specgram widget
        """
        for x in self.Elements:
            for elem in x.twoDimensionalElements:
                elem.shift(lambda x: self._from_osc_to_spec(self._from_spec_to_osc(x)))

    def drawElements(self, oscilogramItems=None):
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
                            if item not in self.axesOscilogram.items() and visible:
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
                                if item not in self.axesSpecgram.viewBox.childItems() and visible:
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
        elements = [e for e in elements if e is not None]  # validate that e is instance of Element class

        if oscilogram:
            for osc_elem in elements:
                for item, visible in osc_elem.visualwidgets():
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
        self.selectElement()
        self.Elements = []

    def selectElement(self, number=-1):
        """
        Method that select an element in the widget
        by highlighting it. If number is in the range of [0, number_of_elements] then the
        the element at index "number" would be selected.
        Otherwise the selection would be cleared.
        :param number: the element index
        """
        if 0 <= number < len(self.Elements):
            index_from, index_to = self.Elements[number].indexFrom, self.Elements[number].indexTo
            self.selectRegion(index_from, index_to)
            if index_from < self.mainCursor.min or index_to > self.mainCursor.max:
                sizeInterval = self.mainCursor.max - self.mainCursor.min

                # move the interval to make completely visible the element selected
                self.mainCursor.min = max(0, (index_from + index_to - sizeInterval) / 2)
                self.mainCursor.max = min(self.mainCursor.min + sizeInterval,
                                          len(self.signalProcessor.signal.data))
                self.graph()
        else:
            self.selectRegion(0, 0)

    def deselectElement(self):
        """
        Deselect (if any) the selected element on the widget
        :return:
        """
        # select the element at index -1
        # (the default of the selectElement method)
        # to clear the selection
        self.selectElement()

    def selectRegion(self, indexFrom, indexTo, brush=None):
        """
        Highlight a section in the graph.
        @param indexFrom: The start of the selected  section
        @param indexTo: The end of the selected  section
        @param brush: optional brush to paint inside the section
        """
        # update the oscilogram
        self.addSelectedRegionItems()

        self.oscSelectionRegion.setRegion([indexFrom, indexTo])
        self.oscSelectionRegion.setBrush(brush if brush is not None else self.SELECTED_ELEMENT_BRUSH)



        self.specSelectionRegion.setRegion([self.from_osc_to_spec(indexFrom), self.from_osc_to_spec(indexTo)])
        self.specSelectionRegion.setBrush(brush if brush is not None else self.SELECTED_ELEMENT_BRUSH)

        self.axesOscilogram.update()
        self.axesSpecgram.update()

    def addSelectedRegionItems(self):
        """
        Add to the widget the items s to mark a region.
        Those items are used when an element is selected to
        highlight the region on the widget.
        :return:
        """
        # add the oscilogram region
        if self.oscSelectionRegion not in self.axesOscilogram.items():
            # add the region to the osc widget because the graph
            # clears the items on the widget
            self.axesOscilogram.addItem(self.oscSelectionRegion)

        # add the spectrogram region
        if self.specSelectionRegion not in self.axesSpecgram.viewBox.childItems():
            self.axesSpecgram.viewBox.addItem(self.specSelectionRegion)

    def deleteSelectedElements(self):
        """
        Deletes the elements between the selection
        (zoom cursor if zoom cursor is selected and there is a selection or
        the visible interval otherwise)
        @return: the tuple (x,y) of init and end of the interval deleted.
        If no element is deleted returns None
        """
        start, end = self.getIndexFromAndTo()

        if end == start or len(self.Elements) == 0:
            return None

        # create a list with start index of each element
        sorted_arr = np.array([x.indexFrom for x in self.Elements])

        # binary search of the interval
        indexFrom, indexTo = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)
        indexFrom -= 1 if indexFrom > 0 and start <= self.Elements[indexFrom - 1].indexTo else 0

        if indexTo < indexFrom or indexTo > len(self.Elements):
            return -1, -1

        self.removeVisualElements(elements=self.Elements[indexFrom:indexTo])

        self.Elements = self.Elements[0:indexFrom] + self.Elements[indexTo:]

        for i, x in enumerate(self.Elements):
            x.setNumber(i + 1)

        self.axesOscilogram.update()
        self.axesSpecgram.update()

        return indexFrom, indexTo - 1

    # endregion

    # region Envelope Visualization

    def setEnvelopeVisibility(self, visibility):
        """
        Method that change the visibility of the envelope curve
        :param visibility: visibility of the envelope curve
        """
        envelope_in_axes = self.envelopeCurve in self.axesOscilogram.items()

        if not envelope_in_axes and visibility:
            # the curve must be set to visible
            self.axesOscilogram.addItem(self.envelopeCurve)

        elif envelope_in_axes and not visibility:
            # the curve must be set to invisible
            self.axesOscilogram.removeItem(self.envelopeCurve)

        self.axesOscilogram.update()

    def getScaledEnvelope(self):
        """
        Return the array of the envelope curve scaled by the envelope factor for display.
        :return: scaled envelope array
        """
        self.envelopeFactor = 2
        return self.envelopeFactor * self.elements_detector.envelope - \
                    (self.signal.maximumValue - self.signal.minimumValue) / 2

    # endregion

    def load_Theme(self, theme):
        """
        this method implements the  way in which the widget load the theme
        """
        QSignalVisualizerWidget.load_Theme(self, theme)

        # update values for envelope display
        self.envelopeCurve.setPen(pg.mkPen(theme.oscillogramTheme.plot_color, width=1))
        self.envelopeCurve.setShadowPen(pg.mkPen(QtGui.QColor(255, 0, 0), width=3))

    def graph(self):
        """
        Refresh the widgets visual elements and graphs
        :return:
        """
        QSignalVisualizerWidget.graph(self)

        # add the region items because the parent method clears the widget
        self.addSelectedRegionItems()

        if self.visibleElements:
            self.drawElements()

