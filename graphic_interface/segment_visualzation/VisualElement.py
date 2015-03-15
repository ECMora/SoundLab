#  -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt4.QtGui import QColor
from graphic_interface.segment_visualzation.VisualItemsCache import VisualItemsCache


class VisualElement:
    """
    The base class for all the visual elements from segmentation
    and parameter measurement. A visual element may contain multiple visual items
    """

    # region CONSTANTS
    #  decimal places to round the parameters
    DECIMAL_PLACES = 4

    # the width of the lines on the element region delimiter
    ELEMENT_REGION_WIDTH = 3

    # different colors for the even and odds rows in the parameter table and segment colors.
    COLOR_ODD = QColor(0, 0, 255, 100)
    COLOR_EVEN = QColor(0, 255, 0, 100)

    # classes of visual elements,
    # FIGURES for the elements representation visual item
    # TEXT for the numbers and labels used
    # PARAMETERS for the measured parameters
    Figures, Text, Parameters = range(3)

    brush_odd = pg.mkBrush(COLOR_ODD)
    brush_even = pg.mkBrush(COLOR_EVEN)

    pen_odd = pg.mkPen(COLOR_ODD, width=ELEMENT_REGION_WIDTH)
    pen_even = pg.mkPen(COLOR_EVEN, width=ELEMENT_REGION_WIDTH)

    # endregion

    def __init__(self, number=0):
        # callback to execute when the element is clicked. Signals are not used for efficiency
        self.elementClicked = None

        # the optional data interesting for the transform ej name, parameters, etc
        # visual options for plotting the element
        self.visible = True

        # the visual elements that show text
        self.text_number = VisualItemsCache().get_text_item(number)
        self.visual_text = [[self.text_number, True]]

        # the visual components that show the elements representation
        self.visual_figures = []

        # the visual components that show the measured parameters representation
        # list of (VisualItemWrapper, bool)
        self.visual_parameters_items = []

        # the number of this element for visualization and ordering options
        self._number = number

    def set_element_clicked_callback(self, callback):
        """

        :param callback:
        :return:
        """
        self.elementClicked = callback if callback is not None else self.elementClicked

    @property
    def color(self):
        """
        :return: the current element visual color
        """
        return self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN

    @property
    def brush(self):
        return self.brush_odd if self.number % 2 == 0 else self.brush_even

    @property
    def pen(self):
        return self.pen_odd if self.number % 2 == 0 else self.pen_even

    @property
    def number(self):
        return self._number

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

        for t, visibility in self.visual_parameters_items:
            # if the parameter has an item to show
            item = t.get_item()
            if item:
                yield item, visibility

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
        # visible by default
        self.visual_parameters_items.append([parameter_item, True])
