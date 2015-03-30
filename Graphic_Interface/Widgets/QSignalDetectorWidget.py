from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QColor
import pyqtgraph as pg
import numpy as np
from graphic_interface.segment_visualization.DetectedSoundLabElement import DetectedSoundLabElement
from graphic_interface.segment_visualization.VisualElement import VisualElement
from QSignalVisualizerWidget import QSignalVisualizerWidget
from graphic_interface.segment_visualization.VisualItemsCache import VisualItemsCache


class QSignalDetectorWidget(QSignalVisualizerWidget):
    """
    This widget performs the detections operations on a signal.
    Provide methods to interact with the detected segments: Highlight it, remove it, etc
    """

    # region SIGNALS

    # signal raised when a detected element is clicked
    # raise the index of the clicked element
    elementClicked = QtCore.pyqtSignal(int)

    # endregion

    # region CONSTANTS

    # the pen for no visible items groups draw
    NO_VISIBLE_ELEMENTS_PEN = pg.mkPen(QColor(255, 0, 0, 255), width=3)

    visual_items_cache = None

    # the brush that is used to draw the selected region or Element
    SELECTED_ELEMENT_BRUSH = pg.mkBrush(QtGui.QColor(255, 0, 0, 220))

    # the min size in pixels that must have an element to be visualized
    MIN_ELEMENT_WIDTH_PIXELS = 3

    # endregion

    def __init__(self, parent):
        # items to highlight elements or regions in the graph
        self.oscSelectionRegion = pg.LinearRegionItem([0, 0], movable=False, brush=self.SELECTED_ELEMENT_BRUSH)

        if self.visual_items_cache is None:
            self.visual_items_cache = VisualItemsCache()

        # the visual items for segmentation
        self.segmentation_visual_items = []

        # the list of visual parameter items of every element.
        # Are stored separated because the elements are loaded lazy and
        # maybe the parameter for an element is supplied when its instance are not yet computed
        self.parameters_items = []

        # the items for no visible elements list of tuples (item, visibility)
        self.no_visible_items = []

        # list of detected sound lab elements.
        self._elements = []

        QSignalVisualizerWidget.__init__(self, parent)

    # region Elements Property
    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements_list):
        # release the resources of visual items to be available for future use
        self.release_items()
        self.deselect_element()

        # just keep a list opf tuples start, end for lightweight
        self._elements = [(e.indexFrom, e.indexTo) for e in elements_list]
        self.parameters_items = [[] for _ in self._elements]

    def _get_element(self, index):
        """
        Return a detected element as DetectedSoundLab instance.
        The objects on list of detected elements could be tuples or detected elements
        this method is a wrapper to get the detected sound lab instance by lazy load.
        :param index: the index of the element to get
        :return:
        """
        if not 0 <= index < len(self.elements):
            raise IndexError()

        # if the element is not a DetectedSoundLab instance then create it
        if not isinstance(self.elements[index], DetectedSoundLabElement):
            self.elements[index] = self.visual_items_cache.get_visual_item(self.signal, self.elements[index][0],
                                                                           self.elements[index][1],
                                                                           index + 1, self.elementClicked)

            # add parameter items if any

            for param in self.parameters_items[index]:
                self.elements[index].add_visual_item(param)

        return self.elements[index]

    # endregion

    # region Elements Visibility

    def _is_element_visible(self, element):
        """
        Computes the visibility of the element supplied. An element is visible if
        is inside the visible interval on the widget graph and its size in pixels
        is greater than the min size in pixels approved.
        :param element: the element to compute visibility rule
        :return: True if the supplied detected object (tuple or DetectedSoundLab)
        satisfy the visibility requirements False otherwise.
        """
        # current visible area interval
        start, end = self.mainCursor.min, self.mainCursor.max

        # get the element interval
        index_from, index_to = (element.indexFrom, element.indexTo) if isinstance(element, DetectedSoundLabElement) \
            else (element[0], element[1])

        # if the elem is in the visible range of the widget graph
        interval_visible = (start <= index_from <= end) or (start <= index_to <= end)

        # if the elem size in pixels is greater than minimum required
        widget_scene_width, widget_pixel_width = self.axesOscilogram.viewRect().width(), self.axesOscilogram.width() * 1.0
        pixel_visible = (index_to - index_from) * widget_pixel_width / widget_scene_width > self.MIN_ELEMENT_WIDTH_PIXELS

        return interval_visible and pixel_visible

    def get_visible_elements(self):
        """
        :return: The visible elements that match the visibility rules (pixel size and interval)
        """
        # get the visible elements
        return [self._get_element(i) for i in xrange(len(self.elements))
                if self._is_element_visible(self.elements[i])]

    def change_elements_visibility(self, visibility, element_type=VisualElement.Text, oscgram_items=None, update=True):
        """
        Change the visibility of the visual items
        :type update: Bool for efficiency optimization when change multiples elements visibility.
        True if must be update the widget False otherwise
        :param visibility: (bool) the new visibility of the items
        :param element_type: The type of items to change visibility
        :param oscgram_items: the domain widget to change visibility. True if Oscilogram items would be changed,
         False if spectrogram items, None if both
        """
        iterable = [e for e in self.elements if isinstance(e, DetectedSoundLabElement)]

        osc_update = oscgram_items is None or oscgram_items
        spec_update = oscgram_items is None or not oscgram_items

        selector = lambda e: e.visual_figures if element_type is VisualElement.Figures else \
                   (e.visual_text if element_type is VisualElement.Text else e.visual_parameters_items)

        items = [item for e in iterable for item in selector(e.time_element) if osc_update]
        items.extend([item for e in iterable for item in selector(e.spectral_element) if spec_update])

        for item in items:
            item[1] = visibility

        # update visibility for no visible elements items
        if element_type == VisualElement.Figures:
            for item in self.no_visible_items:
                if item in self.axesOscilogram.items() and not visibility:
                    self.axesOscilogram.removeItem(item)

                elif item not in self.axesOscilogram.items() and visibility:
                    self.axesOscilogram.addItem(item)

        if update:
            self.graph()

    # endregion  v

    # region Elements Draw

    def _update_elements_numbers(self):
        """
        Updates the numbers for all the elements on the detected elements list
        :return:
        """
        for i in xrange(len(self.elements)):
            if isinstance(self.elements[i], DetectedSoundLabElement):
                self.elements[i].setNumber(i + 1)

    def draw_elements(self, draw_oscilogram=True, draw_specgram=True, elements=None):
        """
        Add to the visual gui widgets the visible elements of the detected segments
        :type elements: the elements to be draw. If no specified all the visible elements would be updated
        :param oscilogramItems: true if draw elements in oscilogram false for spectrogram
        None for both
        """
        import time
        t = time.time()

        elements = elements if elements is not None else self.get_visible_elements()

        self.remove_visual_elements(oscilogram=draw_oscilogram, specgram=draw_specgram, elements=elements)

        self.add_visual_elements(elements, draw_oscilogram, draw_specgram)

        # translate the coord of the visible added items
        for e in self.elements:
            if isinstance(e, DetectedSoundLabElement):
                e.spectral_element.translate_time_freq_coords(self.from_osc_to_spec, self.get_freq_index)

        print("DRAWING elements: " + str(time.time() - t))

    # endregion

    # region Elements Visual Items

    def release_items(self, index_from=None, index_to=None):
        """
        Release the visual items of the elements list
        between the indexes supplied
        :param indexFrom: inclusive lower bound
        :param indexTo: inclusive upper bound
        :return:
        """

        # the elements of the list could be a tuple or a DetectedSoundLab
        index_from = index_from if index_from is not None else 0
        index_to = index_to if index_to is not None else len(self._elements) - 1

        self.remove_visual_elements(elements=[e for e in self.elements[index_from: index_to + 1] if
                                              isinstance(e, DetectedSoundLabElement)])

        # release items
        for i in xrange(index_from, index_to + 1):
            if isinstance(self.elements[i], DetectedSoundLabElement):
                self.visual_items_cache.release_visual_item(self.elements[i])
                self.elements[i] = (self.elements[i].indexFrom, self.elements[i].indexTo)

    def _get_no_visible_visual_items_tuples(self, elements):
        """
        Computes the start, end of the no visible elements group representation
        to visualize
        :param elements: The current visible elements
        :return: List of tuples (start, end) in indexes of detected elements with the positions of the
        elements indexes that are not visible Ej [(0,5),(9,11)]
        means that elements from 0 to 5  and from 9 to 11 are invisible
        """
        if len(self.elements) == 0:
            return []

        if len(elements) == 0:
            return [(0, len(self.elements) - 1)]

        visible_elements_indexes = [e.number - 1 for e in elements]

        no_visible_elements_items_tuples = [(visible_elements_indexes[i - 1] + 1, visible_elements_indexes[i] - 1)
                                            for i in xrange(1, len(elements))
                                            if visible_elements_indexes[i] - visible_elements_indexes[i - 1] > 1]

        # include the interval of start if the first element is no visible
        if visible_elements_indexes[0] > 0:
            no_visible_elements_items_tuples.append((0, visible_elements_indexes[0]))

        # include the interval of end if the last element is no visible
        if visible_elements_indexes[len(visible_elements_indexes) - 1] < len(self.elements) - 1:
            no_visible_elements_items_tuples.append((visible_elements_indexes[-1] + 1, len(self.elements) - 1))

        return no_visible_elements_items_tuples

    def get_no_visible_visual_item(self, start, end):
        """
        Computes and returns the visual items to represents the groups of no visible elements
        :param start: index of the start elements on invisible region
        :param end: index of the end elements on invisible region
        :return: tuple of (list, list) with the visual elements for the group
        of no visible elements in the range [start, end] for oscilogram
        and spectrogram widgets respectively
        """
        osc_items, spec_items = [], []

        # viewRange of plotWidget [[xmin, xmax], [ymin, ymax]]
        x_max = self.axesOscilogram.viewRange()[0][1]

        start_position = self._get_element(start).indexTo if start > 0 else 0
        end_position = self._get_element(end).indexFrom if end < len(self.elements) - 1 else x_max

        max_value = self.signal.maximumValue

        widget_scene_width, widget_pixel_width = self.axesOscilogram.viewRect().width(), self.axesOscilogram.width() * 1.0

        # pixel_visible_text
        if (end_position - start_position) * widget_pixel_width / widget_scene_width > 30:
            text = "(" + str(start + 1) + "..." + str(end + 1) + ")" if end > start else "(" + str(start + 1) + ")"
            text_item = pg.TextItem(text, color=(255, 255, 255), anchor=(0.5, 0.5))
            text_item.setPos(start_position / 2.0 + end_position / 2.0, 0.75 * max_value)
            osc_items.append(text_item)

        graph_item = pg.GraphItem()

        # Define positions of nodes
        graph_pos = np.array([
            [start_position, max_value * 0.8],
            [start_position, max_value * 0.85],
            [end_position, max_value * 0.85],
            [end_position, max_value * 0.8]
        ])

        graph_adj = np.array([[0, 1], [1, 2], [2, 3]])
        options = dict(size=1, symbol='d', pxMode=False, pen=self.NO_VISIBLE_ELEMENTS_PEN)
        graph_item.setData(pos=graph_pos, adj=graph_adj, **options)
        osc_items.append(graph_item)

        return osc_items, spec_items

    def add_visual_elements(self, elements, osc, spec):
        """
        Adds the elements visual representation into the widgets.
        :param elements: the list of elements to draw
        :param osc: True if oscilogram elements must be updated False otherwise
        :param spec: True if spectrogram elements must be updated False otherwise
        :return:
        """

        segmentation_items = [x[0] for x in self.segmentation_visual_items if x[1]]

        # add no_visible_items_osc item, visibility
        self.no_visible_items = [item for start, end in self._get_no_visible_visual_items_tuples(elements)
                                 for item in self.get_no_visible_visual_item(start, end)[0]]

        segmentation_items.extend(self.no_visible_items)

        osc_items = [x[0] for e in elements for x in e.time_element.visual_widgets()
                     if x[1]] if self.visibleOscilogram and osc else []

        osc_items.extend(segmentation_items)

        osc_items = set(osc_items)

        spec_items = set([x[0] for e in elements for x in e.spectral_element.visual_widgets() if x[1]]\
                          if self.visibleSpectrogram and spec else [])

        osc_items_to_add = osc_items.difference(set(self.axesOscilogram.items()))

        spec_items_to_add = spec_items.difference(set(self.axesSpecgram.viewBox.allChildren()))

        for item in osc_items_to_add:
            self.axesOscilogram.addItem(item)

        for item in spec_items_to_add:
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
        elements = elements if elements is not None else [e for e in self.elements
                                                          if isinstance(e, DetectedSoundLabElement)]

        osc_items = [] if not oscilogram else [item
                                               for elem in elements
                                               for item, visible in elem.time_element.visual_widgets()
                                               if visible and item in self.axesOscilogram.items()]

        osc_items.extend(self.no_visible_items)

        spec_items = [] if not specgram else [item
                                              for elem in elements
                                              for item, visible in elem.spectral_element.visual_widgets()
                                              if visible and item in self.axesSpecgram.viewBox.allChildren()]

        for item in osc_items:
            self.axesOscilogram.removeItem(item)

        for item in spec_items:
            self.axesSpecgram.viewBox.removeItem(item)

    def add_parameter_visual_items(self, element_index, parameter_items):
        """
        Add a new visual item of a parameter measurement.
        :param element_index: the index of the segment measured
        :param parameter_items: the list of parameter items to visualize
        :return:
        """
        if not 0 <= element_index < len(self.elements):
            return

        if isinstance(self.elements[element_index], DetectedSoundLabElement):
            for item in parameter_items:
                self.elements[element_index].add_visual_item(item)

            self.draw_elements(elements=[self.elements[element_index]])

        self.parameters_items[element_index].extend(parameter_items)

    def add_segmentation_items(self, items):
        """
        Add a group of visual items that illustrates
        the segmentation process and settings
        :param items: the visual items of segmentation
        :return:
        """
        # visualize the segmentation items !!JUST ON OSCILOGRAM BY NOW!!
        for item, visible in self.segmentation_visual_items:
            if visible:
                self.axesOscilogram.removeItem(item)

        self.segmentation_visual_items = [(item, True) for item in items]

        for item, visible in self.segmentation_visual_items:
            if visible:
                self.axesOscilogram.addItem(item)

        self.axesOscilogram.update()

    # endregion

    # region Elements Selection-Deselection

    def select_element(self, index=-1):
        """
        Method that select an element in the widget
        by highlighting it. If index is in the xrange of [0, number_of_elements] then the
        the element at index "index" would be selected.
        Otherwise the selection would be cleared.
        :type update_graph: True if the widget graph would be updated False otherwise
        :param index: the element index
        """
        if index < 0 or index >= len(self.elements):
            self.oscSelectionRegion.setRegion((0, 0))
            self.axesOscilogram.update()
            return

        index_from, index_to = self._get_element(index).indexFrom, self._get_element(index).indexTo
        self.oscSelectionRegion.setRegion((index_from, index_to))
        self.axesOscilogram.update()

        # update the interval of visualization if the element is outside the current visible region
        if index_from < self.mainCursor.min or index_to > self.mainCursor.max:
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
        self.select_element()

    def selected_element_signal(self):
        """
        :return: The (Audio) signal slice of the selected element region
        """
        start, end = self.oscSelectionRegion.getRegion()
        if end <= start:
            return None

        return self.signal.copy(start, end)

    def selected_elements_interval(self):
        """
        :return: tuple of int (start, end) with the indexes of start and end
        selected elements or None if no selection is made.
        """
        start, end = self.selectedRegion

        # if no area is selected
        if end == start or len(self.elements) == 0 or (start == self.mainCursor.min and end == self.mainCursor.max):
            return None

        # create a list with start index of each element
        sorted_arr = np.array([x.indexFrom if isinstance(x, DetectedSoundLabElement) else x[0] for x in self.elements])

        # binary search of the interval
        indexFrom, indexTo = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)

        # if the region selected starts before the previous element finish then include it
        indexFrom -= 1 if indexFrom > 0 and start <= self._get_element(indexFrom - 1).indexTo else 0

        if indexTo < indexFrom or indexTo > len(self.elements):
            return None

        return indexFrom, indexTo - 1

    # endregion

    # region Elements Add-Delete-Save

    def delete_selected_elements(self):
        """
        Deletes the elements between the selection
        (zoom cursor if zoom cursor is selected and there is a selection or
        the visible interval otherwise)
        @return: the tuple (x,y) of init and end of the interval deleted.
        If no element is deleted returns None
        """
        selection = self.selected_elements_interval()
        if selection is None:
            return

        # remove the selected region Element if is contained on the removed elements region
        selected_rgn_start, selected_rgn_end = self.oscSelectionRegion.getRegion()
        start, end = self.selectedRegion
        if start <= selected_rgn_start <= end or start <= selected_rgn_end <= end:
            self.select_element()

        indexFrom, indexTo = selection
        self.release_items(indexFrom, indexTo)

        # do not call the property to avoid recompute the unnecessary visualization release items
        self._elements = self.elements[0:indexFrom] + self.elements[indexTo + 1:]
        self._update_elements_numbers()
        self.graph()

    def mark_region_as_element(self, interval=None, update=True):
        """
        Try to add a new element manually using the interval supplied
        if None is supplied use the current selected region as delimiters from start and end in time
        domain.
        :type update: variable used for efficiency when add multiple elements
        :return: index of the new element inserted if success None otherwise.
        Could fail because there is no selected region or the region
        overlaps with others elements
        """
        start, end = self.selectedRegion if interval is None else interval
        # if no selected region return
        if end <= start or (self.mainCursor.min == start and self.mainCursor.max == end):
            return None

        # get the index of insertion on the sorted array of elements
        sorted_arr = np.array([x.indexFrom if isinstance(x, DetectedSoundLabElement) else x[0] for x in self.elements])
        index_from, index_to = np.searchsorted(sorted_arr, start), np.searchsorted(sorted_arr, end)
        index_from -= 1 if index_from > 0 and start <= self._get_element(index_from - 1).indexTo else 0

        # insert the new element
        element = self.visual_items_cache.get_visual_item(self.signal, start, end, 0, self.elementClicked)
        self.elements.insert(index_from, element)

        # update the widget
        if update:
            self._update_elements_numbers()
            self.draw_elements()
            self.axesOscilogram.repaint()
            self.axesSpecgram.repaint()

        return index_from

    def save_segments_into_signal(self):
        """
        Store the list of (start, end) indexes of detected elements into the
        signal extra data.
        :return:
        """
        self.signal.extraData = [(x.indexFrom, x.indexTo) if isinstance(x, DetectedSoundLabElement) else x
                                 for x in self.elements]

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
        if self.oscSelectionRegion not in self.axesOscilogram.items():
            self.axesOscilogram.addItem(self.oscSelectionRegion)

        self.draw_elements()