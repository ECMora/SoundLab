#  -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4 import QtGui


class VisualElement(QObject):
    """

    """

    # region SIGNALS
    # called when the element is clicked
    #  raise the index of the element (number)
    elementClicked = pyqtSignal(int)
    # endregion

    # region CONSTANTS
    #  decimal places to round the measurements
    DECIMAL_PLACES = 4

    # different colors for the even and odds rows in the parameter table and segment colors.
    COLOR_ODD = QtGui.QColor(0, 0, 255, 100)
    COLOR_EVEN = QtGui.QColor(0, 255, 0, 100)
    # endregion

    Figures, Text, Parameters = range(3)

    def __init__(self, number=0):
        QObject.__init__(self)

        # the optional data interesting for the transform ej name, parameters, etc
        # visual options for plotting the element
        self.visible = True

        # the visual elements that show text
        self.visual_text = []

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

    def visual_widgets(self):
        """
        all the visual items that represents this element.
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

    def addParameterItem(self, parameter_item):
        """

        :param parameter_item: the new parameter item to visualize
        :return:
        """
        # visible by default
        self.visual_parameters_items.append([parameter_item, True])
