from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from sound_lab_core.Elements.Element import Element
from QSignalVisualizerWidget import QSignalVisualizerWidget
from sound_lab_core.Elements.OneDimensionalElements.OscilogramElement import OscilogramElement


class QSignalDetectorWidget(QSignalVisualizerWidget):
    """
    This widget performs the detections operations on a signal.
    Provide methods to interact with the detected segments: Highlight, remove, etc
    """

    # region SIGNALS

    # signal raised when a detected element is clicked
    # raise the index of the clicked element
    elementClicked = QtCore.pyqtSignal(int)

    # endregion

    # region CONSTANTS

    # the brush that is used to draw the selected region or Element
    SELECTED_ELEMENT_BRUSH = pg.mkBrush(QtGui.QColor(255, 0, 0, 200))

    # endregion

    def __init__(self, parent):
        # items to highlight elements or regions in the graph
        self.oscSelectionRegion = pg.LinearRegionItem([0, 0], movable=False, brush=self.SELECTED_ELEMENT_BRUSH)

        self.specSelectionRegion = pg.LinearRegionItem([0, 0], movable=False, brush=self.SELECTED_ELEMENT_BRUSH)

        # visibility of all detected elements.
        # is used when they are displayed
        self.visibleElements = True

        # list of detected elements. Each element contains the object
        # and the extra data for visualize it
        self._elements = []

        QSignalVisualizerWidget.__init__(self, parent)

    # region Elements Property
    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements_list):
        self.clearDetection()

        self._elements = []

        # get the elements detected by the detector
        for index, c in enumerate(elements_list):
            self._elements.append(c)
            # connect the click event of an element with the signal of the widget
            c.elementClicked.connect(lambda i: self.elementClicked.emit(i))

    # endregion

    # region Elements

    # region Visual Representation

    def drawElements(self, oscilogramItems=None):
        """
        Add to the visual gui widgets the visible elements of the detected segments
        :param oscilogramItems: true if draw elements in oscilogram false for spectrogram
        None for both
        """
        osc = oscilogramItems is None or oscilogramItems
        # spec = oscilogramItems is None or not oscilogramItems

        if self.visibleOscilogram and osc:
            for i in range(len(self.elements)):
                if self.elements[i].visible:
                    for item, visible in self.elements[i].visualwidgets():
                        if not visible:
                            self.axesOscilogram.removeItem(item)
                        else:
                            if item not in self.axesOscilogram.items() and visible:
                                self.axesOscilogram.addItem(item)
                else:
                    for item, visible in self.elements[i].visualwidgets():
                        self.axesOscilogram.removeItem(item)
            self.axesOscilogram.update()

            # do not update the specgram elements until better design
            # if self.visibleSpectrogram and spec:
            # for i in range(len(self.Elements)):
            #         for j in range(len(self.Elements[i].twoDimensionalElements)):
            #             if self.Elements[i].twoDimensionalElements[j].visible:
            #                 for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
            #                     if not visible:
            #                         self.axesSpecgram.viewBox.removeItem(item)
            #                     else:
            #                         if item not in self.axesSpecgram.viewBox.childItems() and visible:
            #                             self.axesSpecgram.viewBox.addItem(item)
            #             else:
            #                 for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
            #                     self.axesSpecgram.viewBox.removeItem(item)
            #
            #     self.axesSpecgram.update()

    def removeVisualElements(self, oscilogram=True, specgram=True, elements=None):
        """
        Method that remove the visual representation of the elements in the widget.
        Used for remove selected elements or a group of them.
        :param oscilogram: Removes the oscilogram visual elements
        :param specgram: Removes the spectrogram visual elements
        :param elements: the elements that would be (visually) removed.
        all the self.elements if None
        """
        elements = elements if elements is not None else self.elements
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

    def changeElementsVisibility(self, visible, element_type=Element.Figures, oscilogramItems=True):
        """
        Change the visibility of the visual items
        :param visible:
        :param element_type:
        :param oscilogramItems:
        """
        iterable = self.elements
        if not oscilogramItems:
            aux = [x.twoDimensionalElements for x in self.elements]
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

    # endregion

    # region Selection-Deselection

    def clearDetection(self):
        """
        Clears the detected elements and their visual components from the widget
        """
        self.removeVisualElements(oscilogram=True, specgram=True)
        self.deselectElement()

    def selectElement(self, number=-1):
        """
        Method that select an element in the widget
        by highlighting it. If number is in the range of [0, number_of_elements] then the
        the element at index "number" would be selected.
        Otherwise the selection would be cleared.
        :param number: the element index
        """
        if 0 <= number < len(self.elements):
            index_from, index_to = self.elements[number].indexFrom, self.elements[number].indexTo
            self.selectRegion(index_from, index_to)

            if index_from < self.mainCursor.min or index_to > self.mainCursor.max:
                sizeInterval = self.mainCursor.max - self.mainCursor.min

                # update the interval of visualization if the element is outside the current visible region
                if index_from < self.mainCursor.min or index_to > self.mainCursor.max:
                    self.mainCursor.min = index_from
                    self.mainCursor.max = index_to

                    # move the interval to make completely visible the element selected
                    self.mainCursor.min = max(0, index_from - sizeInterval/2)
                    self.mainCursor.max = min(self.signal.length, index_to + sizeInterval/2)
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

        # self.specSelectionRegion.setRegion([self.from_osc_to_spec(indexFrom), self.from_osc_to_spec(indexTo)])
        # self.specSelectionRegion.setBrush(brush if brush is not None else self.SELECTED_ELEMENT_BRUSH)

        self.axesOscilogram.update()
        # self.axesSpecgram.update()

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
        # if self.specSelectionRegion not in self.axesSpecgram.viewBox.childItems():
        #     self.axesSpecgram.viewBox.addItem(self.specSelectionRegion)

    # endregion

    def deleteSelectedElements(self):
        """
        Deletes the elements between the selection
        (zoom cursor if zoom cursor is selected and there is a selection or
        the visible interval otherwise)
        @return: the tuple (x,y) of init and end of the interval deleted.
        If no element is deleted returns None
        """
        start, end = self.selectedRegion

        if end == start or len(self.elements) == 0:
            return None

        # create a list with start index of each element
        sorted_arr = np.array([x.indexFrom for x in self.elements])

        # binary search of the interval
        indexFrom, indexTo = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)

        # if the region selected starts before the previous element finish then include it
        indexFrom -= 1 if indexFrom > 0 and start <= self.elements[indexFrom - 1].indexTo else 0

        if indexTo < indexFrom or indexTo > len(self.elements):
            return -1, -1

        # remove the selected region Element if is contained on the removed elements region
        selected_rgn_start, selected_rgn_end = self.oscSelectionRegion.getRegion()

        if start <= selected_rgn_start <= end or start <= selected_rgn_end <= end:
            self.selectElement()

        self.removeVisualElements(elements=self.elements[indexFrom:indexTo])

        self.elements = self.elements[0:indexFrom] + self.elements[indexTo:]

        for i, x in enumerate(self.elements):
            x.setNumber(i + 1)

        self.graph()

        return indexFrom, indexTo - 1

    def markRegionAsElement(self, interval=None, update=True):
        """
        Try to add a new element with manual segmentation using the interval supplied
        if None is supplied use the current selected region as delimiters from start and end in time
        domain.
        :return: index of the new element inserted if success None otherwise.
        Could fail because there is no selected region or the region
        overlaps with others elements
        """
        if interval is None:
            start, end = self.selectedRegion
        else:
            start, end = interval

        # no selected region
        if end <= start or (self.mainCursor.min == start and self.mainCursor.max == end):
            return None

        sorted_arr = np.array([x.indexFrom for x in self.elements])

        indexFrom, indexTo = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)
        indexFrom -= 1 if indexFrom > 0 and start <= self.elements[indexFrom - 1].indexTo else 0

        # overlaps with other elements
        if indexFrom != indexTo:
            return None

        # todo hard code instance must be used an injection of dependencies
        element = OscilogramElement(self.signal, start, end)
        self.elements.insert(indexFrom, element)
        element.elementClicked.connect(lambda i: self.elementClicked.emit(i))

        for index, e in enumerate(self.elements):
            e.setNumber(index+1)

        # for efficiency when add multiple elements
        if update:
            self.graph()

        return indexFrom

    def saveElementsOnSignal(self):
        """
        Store the list of (start, end) indexes of detetcted elements
        :return:
        """
        self.signal.extraData = [(x.indexFrom, x.indexTo) for x in self.elements]

    # endregion

    # region Widgets synchronization

    def updateOscillogram(self, x1, x2):
        """
        Method invoked when the oscilogram range change
        :param x1: start index of the interval changed
        :param x2: end index of the interval changed
        :return:
        """
        QSignalVisualizerWidget.updateOscillogram(self, x1, x2)
        self.graphElements()

    def updateSpecgram(self, x1, x2):
        """
        Method invoked when the spectrogram range change
        :param x1: start index of the interval changed
        :param x2: end index of the interval changed
        :return:
        """
        QSignalVisualizerWidget.updateSpecgram(self, x1, x2)
        self.graphElements()

    # endregion

    def graph(self):
        """
        Refresh the widgets visual elements and graphs
        :return:
        """
        QSignalVisualizerWidget.graph(self)
        self.graphElements()

    def graphElements(self):
        """
        Execute the logic of update the visual representation of the detected elements
        :return:
        """
        # add the region items because the parent method clears the widget
        self.addSelectedRegionItems()

        if self.visibleElements:
            self.drawElements()