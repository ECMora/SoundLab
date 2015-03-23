from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QColor
import pyqtgraph as pg
import numpy as np
from graphic_interface.segment_visualzation.DetectedSoundLabElement import DetectedSoundLabElement
from graphic_interface.segment_visualzation.VisualElement import VisualElement
from QSignalVisualizerWidget import QSignalVisualizerWidget
from graphic_interface.segment_visualzation.VisualItemsCache import VisualItemsCache


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

    # the pen for no visible items groups draw
    NO_VISIBLE_ELEMENTS_PEN = pg.mkPen(QColor(255, 0, 0, 100), width=3)

    visual_items_cache = None

    # the brush that is used to draw the selected region or Element
    SELECTED_ELEMENT_BRUSH = pg.mkBrush(QtGui.QColor(255, 0, 0, 200))

    # the number of elements visible by default when a detection is made (efficiency)
    VISIBLE_ELEMENTS_COUNT = 1000

    # the min size in pixels that must have an element to be visualized
    MIN_ELEMENT_WIDTH_PIXELS = 5

    # endregion

    def __init__(self, parent):
        # items to highlight elements or regions in the graph
        self.oscSelectionRegion = pg.LinearRegionItem([0, 0], movable=False, brush=self.SELECTED_ELEMENT_BRUSH)

        if self.visual_items_cache is None:
            self.visual_items_cache = VisualItemsCache()

        # visibility of all detected elements used when they are displayed
        self.visibleElements = True

        # the visual items for segmentation
        self.segmentation_visual_items = []

        # list of detected sound lab elements.
        self._elements = []

        QSignalVisualizerWidget.__init__(self, parent)

    # region Elements Property
    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements_list):
        self.deselect_element()
        import time

        t = time.time()
        # release the resources of visual items
        for e in self._elements:
            e.release_resources()
            for item, visible in e.spectral_element.visual_widgets():
                if item in self.axesSpecgram.viewBox.allChildren():
                    self.axesSpecgram.viewBox.removeItem(item)

        function_get_elements = lambda i: DetectedSoundLabElement(elements_list[i].signal,
                                                                  elements_list[i].indexFrom,
                                                                  elements_list[i].indexTo,
                                                                  i + 1, self.elementClicked)

        self._elements = map(function_get_elements, xrange(len(elements_list)))

        # just show an interval of a fixed amount of elements visible for starting
        if len(self.elements) > self.VISIBLE_ELEMENTS_COUNT:
            self.mainCursor.min, self.mainCursor.max = 0, self.elements[self.VISIBLE_ELEMENTS_COUNT - 1].indexTo

        print("Time consuming on creation of elements: " + str(time.time() - t))

    # endregion

    # region Elements Visual Representation

    def draw_elements(self, oscilogramItems=None):
        """
        Add to the visual gui widgets the visible elements of the detected segments
        :param oscilogramItems: true if draw elements in oscilogram false for spectrogram
        None for both
        """
        import time

        t = time.time()

        osc = oscilogramItems is None or oscilogramItems
        spec = oscilogramItems is None or not oscilogramItems

        # just update the visualization of visible elements
        start, end = self.mainCursor.min, self.mainCursor.max

        # get the visible elements
        elements = [e for e in self.elements if start <= e.indexFrom <= end or start <= e.indexTo <= end]

        # removes all the elements on spectrogram (not oscilogram because it's cleared on graph)
        for i in xrange(len(self.elements)):
            for item, visible in self.elements[i].spectral_element.visual_widgets():
                if item in self.axesSpecgram.viewBox.allChildren():
                    self.axesSpecgram.viewBox.removeItem(item)

            # recompute the locations of the spectrogram elements
            self.elements[i].spectral_element.translate_time_freq_coords(self.from_osc_to_spec, self.get_freq_index)

        # filter to get just the truly visible elements based on pixels width
        widget_scene_width = self.axesOscilogram.viewRect().width()
        widget_pixel_width = self.axesOscilogram.width() * 1.0
        elements = [e for e in elements if (e.indexTo - e.indexFrom) * widget_pixel_width / widget_scene_width >
                    self.MIN_ELEMENT_WIDTH_PIXELS]

        self.add_elements_items(elements, osc, spec)

        self.repaint()

        print("Time consuming on drawing elements: " + str(time.time() - t))

    def _get_no_visible_elements_tuples(self, elements):
        """
        Computes the start, end of the no visible elements group representation
        to visualize
        :param elements: The current visible elements
        :return: List of tuples (start, end) in indexes of detected elements
        """
        visible_elements_indexes = [e.number - 1 for e in elements]

        min_elems = 3
        no_visible_elements_items_tuples = []
        if len(elements) == 0 and len(self.elements) > 1:
            no_visible_elements_items_tuples = [(0, len(self.elements) - 1)]
        #
        # elif visible_elements_indexes[0] < min_elems:
        #     no_visible_elements_items_tuples = [(1, visible_elements_indexes[0] - 1)]

        no_visible_elements_items_tuples.extend([(visible_elements_indexes[i - 1], visible_elements_indexes[i])
                                                 for i in xrange(1, len(elements)) if
                                                 visible_elements_indexes[i] - visible_elements_indexes[i - 1] >= min_elems])

        # if len(visible_elements_indexes) > 0 and visible_elements_indexes[-1] + min_elems <= len(self.elements):
        #     # if the last element is not visible
        #     no_visible_elements_items_tuples.append((elements[-1] + 1, len(self.elements)))

        return no_visible_elements_items_tuples

    def get_no_visible_visual_items(self, start, end):
        """
        Computes and returns the visual items to represents
        :param start: index of the start elements on invisible region
        :param end: index of the end elements on invisible region
        :return: tuple of (list, list) with the visual elements for the group
        of no visible elements in the range [start, end] for oscilogram
        and spectrogram widgets respectively
        """

        start_position, end_position = self.elements[start].indexFrom, self.elements[end].indexTo

        max_value = self.signal.maximumValue

        text_item = self.visual_items_cache.get_text_item()
        text_item.setText("(" + str(start + 2) + "..." + str(end) + ")")
        text_item.setPos(start_position / 2.0 + end_position / 2.0,
                         0.75 * max_value)

        # graph_item = self.visual_items_cache.get_graph_item()
        #
        # # Define positions of nodes
        # graph_pos = np.array([
        #     [start_position, max_value * 0.8],
        #     [start_position, max_value * 0.85],
        #     [end_position, max_value * 0.85],
        #     [end_position, max_value * 0.8]
        # ])
        #
        # graph_adj = np.array([[0, 1], [1, 2], [2, 3]])
        # options = dict(size=1, symbol='d', pxMode=False, pen=self.NO_VISIBLE_ELEMENTS_PEN)
        # graph_item.setData(pos=graph_pos, adj=graph_adj, **options)

        return [text_item], []

    def add_elements_items(self, elements, osc, spec):
        """

        :param elements:
        :param osc:
        :param spec:
        :return:
        """

        for i in xrange(len(elements)):
            if self.visibleOscilogram and osc:
                for item, visible in elements[i].time_element.visual_widgets():
                    if visible:
                        self.axesOscilogram.addItem(item)

            if self.visibleSpectrogram and spec:
                for item, visible in elements[i].spectral_element.visual_widgets():
                    if visible:
                        self.axesSpecgram.viewBox.addItem(item)

        # visualize the segmentation items
        if self.visibleOscilogram and osc:
            for item, visible in self.segmentation_visual_items:
                if visible:
                    self.axesOscilogram.addItem(item)

        # add items for continuous groups (more than 2) of no visible detected elements
        for start, end in self._get_no_visible_elements_tuples(elements):
            osc_items, spec_items = self.get_no_visible_visual_items(start, end)
            for item in osc_items:
                self.axesOscilogram.addItem(item)
            for item in spec_items:
                self.axesSpecgram.viewBox.addItem(item)

    def remove_visual_elements(self, oscilogram=True, specgram=True, elements=None):
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

        try:
            for elem in elements:
                if oscilogram:
                    for item, visible in elem.time_element.visual_widgets():
                        self.axesOscilogram.removeItem(item)
                if specgram:
                    for item, visible in elem.spectral_element.visual_widgets():
                        self.axesSpecgram.viewBox.removeItem(item)

        except Exception as ex:
            print(ex.message)

    def change_elements_visibility(self, visibility, element_type=VisualElement.Text, oscilogram_items=None,
                                   update=True):
        """
        Change the visibility of the visual items
        :type update: Bool for efficiency optimization when change multiples elements visibility.
        True if must be update the widget False otherwise
        :param visibility: (bool) the new visibility of the items
        :param element_type: The type of items to change visibility
        :param oscilogram_items: the domain widget to change visibility. True if Oscilogram items would be changed,
         False if spectrogram items, None if both
        """
        iterable = self.elements
        osc_update = oscilogram_items is None or oscilogram_items
        spec_update = oscilogram_items is None or not oscilogram_items
        changes = False

        for e in iterable:
            if element_type is VisualElement.Figures:
                if osc_update:
                    for x in e.time_element.visual_figures:
                        changes = changes or x[1] != visibility
                        x[1] = visibility

                if spec_update:
                    for x in e.spectral_element.visual_figures:
                        changes = changes or x[1] != visibility
                        x[1] = visibility

            elif element_type is VisualElement.Text:
                if osc_update:
                    for x in e.time_element.visual_text:
                        changes = changes or x[1] != visibility
                        x[1] = visibility

                if spec_update:
                    for x in e.spectral_element.visual_text:
                        changes = changes or x[1] != visibility
                        x[1] = visibility

            elif element_type is VisualElement.Parameters:
                if osc_update:
                    for x in e.time_element.visual_parameters_items:
                        changes = changes or x[1] != visibility
                        x[1] = visibility

                if spec_update:
                    for x in e.spectral_element.visual_parameters_items:
                        changes = changes or x[1] != visibility
                        x[1] = visibility

        if changes and update:
            self.draw_elements()

    def add_visual_items(self, element_index, parameter_items):
        """
        Add a new visual item of a parameter measurement.
        :param element_index: the index of the segment measured
        :param parameter_items: the list of parameter items to visualize
        :return:
        """
        if not 0 <= element_index < len(self.elements):
            return
        for item in parameter_items:
            self.elements[element_index].add_visual_item(item)

        # todo add into the widgets
        self.update()

    def add_segmentation_items(self, items):
        """
        Add a group of visual items that illustrates
        the segmentation process and settings
        :param items: the visual items of segmentation
        :return:
        """
        # visualize the segmentation items !!JUST ON OSCILOGRAM BY NOW!!
        for item, visible in self.segmentation_visual_items:
            self.axesOscilogram.removeItem(item)

        self.segmentation_visual_items = [(item, True) for item in items]

        if self.visibleOscilogram:
            for item, visible in self.segmentation_visual_items:
                if visible:
                    self.axesOscilogram.addItem(item)

        self.update()

    # endregion

    # region Elements Selection-Deselection

    def clear_detection(self):
        """
        Clears the detected elements and their visual components from the widget
        """
        self.remove_visual_elements(oscilogram=True, specgram=True)
        self.deselect_element()

    def select_element(self, index=-1):
        """
        Method that select an element in the widget
        by highlighting it. If index is in the xrange of [0, number_of_elements] then the
        the element at index "index" would be selected.
        Otherwise the selection would be cleared.
        :param index: the element index
        """
        if index < 0 or index >= len(self.elements):
            self.select_region(0, 0)
            return

        index_from, index_to = self.elements[index].indexFrom, self.elements[index].indexTo
        self.select_region(index_from, index_to)

        if index_from < self.mainCursor.min or index_to > self.mainCursor.max:
            # update the interval of visualization if the element is outside the current visible region
            interval_size = self.mainCursor.max - self.mainCursor.min

            # move the interval to make completely visible the element selected
            self.mainCursor.min = max(0, index_from - interval_size / 2)
            self.mainCursor.max = min(self.signal.length, index_to + interval_size / 2)
            self.graph()

    def deselect_element(self):
        """
        Deselect (if any) the selected element on the widget
        :return:
        """
        # select the element at index -1
        # (the default of the select_element method)
        # to clear the selection
        self.select_element()

    def select_region(self, indexFrom, indexTo, brush=None):
        """
        Highlight a section in the graph.
        @param indexFrom: The start of the selected  section
        @param indexTo: The end of the selected  section
        @param brush: optional brush to paint inside the section
        """
        # update the oscilogram
        self.add_selected_region_items()

        self.oscSelectionRegion.setRegion([indexFrom, indexTo])
        self.oscSelectionRegion.setBrush(brush if brush is not None else self.SELECTED_ELEMENT_BRUSH)

        self.axesOscilogram.update()

    def add_selected_region_items(self):
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

    def selected_element_signal(self):
        """
        :return: The (Audio) signal slice of the selected element region
        """
        start, end = self.oscSelectionRegion.getRegion()
        if end <= start:
            return None

        return self.signal.copy(start, end)

    # endregion

    # region Elements Add-Delete-Save

    def selected_elements_interval(self):
        """
        :return: tuple of int (start, end) with the indexes of start and end
        selected elements or None if no selection is made.
        """
        start, end = self.selectedRegion

        # if no area is selected
        if end == start or len(self.elements) == 0 or \
                (start == self.mainCursor.min and end == self.mainCursor.max):
            return None

        # create a list with start index of each element
        sorted_arr = np.array([x.indexFrom for x in self.elements])

        # binary search of the interval
        indexFrom, indexTo = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)

        # if the region selected starts before the previous element finish then include it
        indexFrom -= 1 if indexFrom > 0 and start <= self.elements[indexFrom - 1].indexTo else 0

        if indexTo < indexFrom or indexTo > len(self.elements):
            return None

        return indexFrom, indexTo - 1

    def delete_selected_elements(self):
        """
        Deletes the elements between the selection
        (zoom cursor if zoom cursor is selected and there is a selection or
        the visible interval otherwise)
        @return: the tuple (x,y) of init and end of the interval deleted.
        If no element is deleted returns None
        """
        start, end = self.selectedRegion
        selection = self.selected_elements_interval()

        if selection is None:
            return

        indexFrom, indexTo = selection

        # remove the selected region Element if is contained on the removed elements region
        selected_rgn_start, selected_rgn_end = self.oscSelectionRegion.getRegion()

        if start <= selected_rgn_start <= end or start <= selected_rgn_end <= end:
            self.select_element()

        self.remove_visual_elements(elements=self.elements[indexFrom:indexTo + 1])

        # do not call the property to avoid recompute the unnecessary visualization
        self._elements = self.elements[0:indexFrom] + self.elements[indexTo + 1:]

        for i, x in enumerate(self.elements):
            x.setNumber(i + 1)

        self.draw_elements()

    def mark_region_as_element(self, interval=None, update=True):
        """
        Try to add a new element manually using the interval supplied
        if None is supplied use the current selected region as delimiters from start and end in time
        domain.
        :return: index of the new element inserted if success None otherwise.
        Could fail because there is no selected region or the region
        overlaps with others elements
        """
        start, end = self.selectedRegion if interval is None else interval

        # no selected region
        if end <= start or (self.mainCursor.min == start and self.mainCursor.max == end):
            return None

        sorted_arr = np.array([x.indexFrom for x in self.elements])

        index_from, index_to = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)
        index_from -= 1 if index_from > 0 and start <= self.elements[index_from - 1].indexTo else 0

        element = DetectedSoundLabElement(self.signal, start, end, signal_callback=self.elementClicked)
        self.elements.insert(index_from, element)
        element.set_element_clicked_callback(lambda i: self.elementClicked.emit(i))

        for index, e in enumerate(self.elements):
            e.setNumber(index + 1)

        # variable used for efficiency when add multiple elements
        if update:
            self.graph()

        return index_from

    def save_segments_into_signal(self):
        """
        Store the list of (start, end) indexes of detected elements into the
        signal extra data.
        :return:
        """
        self.signal.extraData = [(x.indexFrom, x.indexTo) for x in self.elements]

    # endregion

    # region Widgets synchronization

    def updateOscillogram(self, x1, x2):
        """
        Method invoked when the oscilogram xrange change
        :param x1: start index of the interval changed
        :param x2: end index of the interval changed
        :return:
        """
        QSignalVisualizerWidget.updateOscillogram(self, x1, x2)
        self.graph_elements()

    def updateSpecgram(self, x1, x2):
        """
        Method invoked when the spectrogram xrange change
        :param x1: start index of the interval changed
        :param x2: end index of the interval changed
        :return:
        """
        QSignalVisualizerWidget.updateSpecgram(self, x1, x2)
        self.graph_elements()

    # endregion

    def get_visible_region(self):
        """
        :return: The region that is visible in signal oscilogram coordinates
        """
        return self.mainCursor.max - self.mainCursor.min

    def graph(self):
        """
        Refresh the widgets visual elements and graphs
        :return:
        """
        QSignalVisualizerWidget.graph(self)
        self.graph_elements()

    def graph_elements(self):
        """
        Execute the logic of update the visual representation of the detected elements
        :return:
        """
        # add the region items because the parent method clears the widget
        self.add_selected_region_items()

        if self.visibleElements:
            self.draw_elements()