#  -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFont


class VisualElement:
    """
    The base class for all the visual elements from segmentation
    and parameter measurement. A visual element may contain multiple visual items
    """

    # region CONSTANTS
    # the font size for text labels
    FONT_SIZE = 13
    FONT = QFont("Arial", pointSize=FONT_SIZE)  # the queue with free items

    #  decimal places to round the parameters
    DECIMAL_PLACES = 4

    # the width of the lines on the element region delimiter
    ELEMENT_REGION_WIDTH = 3

    # different colors for the even and odds rows in the parameter table and segment colors.
    COLOR_ODD = QColor(0, 0, 255, 100)
    COLOR_EVEN = QColor(0, 255, 0, 100)

    # classes of visual elements,
    # FIGURES ----- for elements representation visual item
    # TEXT -------- for numbers and labels used
    # PARAMETERS -- for measured parameters
    Figures, Text, Parameters = range(3)

    brush_odd = pg.mkBrush(COLOR_ODD)
    brush_even = pg.mkBrush(COLOR_EVEN)

    pen_odd = pg.mkPen(COLOR_ODD, width=ELEMENT_REGION_WIDTH)
    pen_even = pg.mkPen(COLOR_EVEN, width=ELEMENT_REGION_WIDTH)

    # endregion

    def __init__(self, number=0, signal=None, indexFrom=0, indexTo=0):
        # callback to execute when the element is clicked. Signals are not used for efficiency
        self.elementClicked = None
        self.signal = signal

        self._indexFrom = indexFrom
        self._indexTo = indexTo

        # the optional data interesting for the transform ej name, parameters, etc
        # visual options for plotting the element
        self.visible = True

        # the visual elements that show text
        self.text_number = pg.TextItem(str(number), color=(255, 255, 255), anchor=(0.5, 0.5))
        self.text_number.setFont(self.FONT)
        self.visual_text = [self.text_number]

        # the visual components that show the elements representation
        self.visual_figures = []

        # the visual components that show the measured parameters representation
        self.visual_parameters_items = []

        # the number of this element for visualization and ordering options
        self._number = number

    def set_element_clicked_callback(self, callback):
        """
        :param callback:
        :return:
        """
        self.elementClicked = callback

    def _update_items_pos(self):
        """
        Update visual items variables from a change on signal or bounds
        :return:
        """
        pass

    def set_bounds(self, index_from, index_to):
        self._indexFrom = index_from
        self._indexTo = index_to
        self._update_items_pos()

    # region Properties

    @property
    def indexFrom(self):
        return self._indexFrom

    @property
    def indexTo(self):
        return self._indexTo

    @property
    def color(self):
        """
        :return: the current element visual color
        """
        return VisualElement.COLOR_ODD if self.number % 2 == 0 else VisualElement.COLOR_EVEN

    @property
    def brush(self):
        return VisualElement.brush_odd if self.number % 2 == 0 else VisualElement.brush_even

    @property
    def pen(self):
        return VisualElement.pen_odd if self.number % 2 == 0 else VisualElement.pen_even

    @property
    def number(self):
        return self._number

    # endregion

    def clone(self):
        return VisualElement(self.number, self.signal, self.indexFrom, self.indexTo)

    def setNumber(self, n):
        self._number = n
        self.text_number.setText(str(n))

    def visual_widgets(self):
        """
        Iterator for the visual items that contains this element.
        @return: iterator of objects of the form (object visual element, bool visibility)
        """
        for f in self.visual_figures:
            yield f

        for t in self.visual_text:
            yield t

        for t in self.visual_parameters_items:
            # if the parameter has an item to show
            item = t.get_item()
            if item:
                yield item

    def mouseClickEvent(self, event):
        """
        Interception of GUI events by switching this method for its similar
        in the visual figures of the element
        @param event: The event raised
        """
        if self.elementClicked:
            self.elementClicked.emit(self.number - 1)

    def add_parameter_item(self, parameter_item):
        """
        :param parameter_item: the new parameter item to visualize
        :return:
        """
        self.visual_parameters_items.append(parameter_item)