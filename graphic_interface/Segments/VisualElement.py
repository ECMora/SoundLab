#  -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4 import QtGui
import pyqtgraph as pg
from PyQt4.QtGui import QFont


class VisualElement(QObject):
    """
    The base class for all the visual elements from segmentation
    and parameter measurement. A visual element may contain multiple visual items
    """

    # region SIGNALS
    # called when the element is clicked
    #  raise the index of the element (number)
    elementClicked = pyqtSignal(int)
    # endregion

    # region CONSTANTS
    #  decimal places to round the measurements
    DECIMAL_PLACES = 4

    # the font size for text labels
    FONT_SIZE = 13

    # different colors for the even and odds rows in the parameter table and segment colors.
    COLOR_ODD = QtGui.QColor(0, 0, 255, 100)
    COLOR_EVEN = QtGui.QColor(0, 255, 0, 100)

    # classes of visual elements,
    # FIGURES for the elements representation visual item
    # TEXT for the numbers and labels used
    # PARAMETERS for the measured parameters
    Figures, Text, Parameters = range(3)

    # endregion

    def __init__(self, number=0):
        QObject.__init__(self)

        # the optional data interesting for the transform ej name, parameters, etc
        # visual options for plotting the element
        self.visible = True

        # the visual elements that show text
        self.visual_text = []
        font = QFont()
        font.setPointSize(self.FONT_SIZE)

        self.text_number = pg.TextItem(str(number), color=(255, 255, 255), anchor=(0.5, 0.5))
        self.text_number.setFont(font)
        self.visual_text.append([self.text_number, True])

        # the visual components that show the elements representation
        self.visual_figures = []

        # the visual components that show the measured parameters representation
        # list of (ParameterVisualItem, bool)
        self.visual_parameters_items = []

        # the number of this element for visualization and ordering options
        self._number = number

    @property
    def color(self):
        """
        :return: the current element visual color
        """
        return self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN

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
        self.elementClicked.emit(self.number - 1)

    def add_parameter_item(self, parameter_item):
        """
        :param parameter_item: the new parameter item to visualize
        :return:
        """
        # visible by default
        self.visual_parameters_items.append([parameter_item, True])
