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

    Figures, Text = range(2)

    def __init__(self, number=0):
        QObject.__init__(self)

        # the optional data interesting for the transform ej name, parameters, etc
        # visual options for plotting the element
        self.visible = True

        # the visual elements that show text
        self.visual_text = []

        # the visual components that show the elements representation
        self.visual_figures = []

        # the number of this element for visualization and ordering options
        self.number = number

    def visual_widgets(self):
        """
        all the visual elements that represents this element.
        @return: iterator of objects of the form (object visual element, bool visibility)
        """
        for f in self.visual_figures:
            yield f

        for t in self.visual_text:
            yield t

    def mouseClickEvent(self, event):
        """
        Interception of GUI events by switching this method for its similar
        in the visual figures of the element
        @param event: The event raised
        """
        self.elementClicked.emit(self.number - 1)

    def setNumber(self, n):
        pass
