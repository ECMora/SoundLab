#  -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Elements.Element import Element
from PyQt4 import QtGui, QtCore


class SpectralMeasurementLocation:
    START, CENTER, END, QUARTILE25, QUARTILE75 = range(5)
    MEDITIONS = [
        [False,  QtGui.QColor(255, 0, 0, 255)],
        [False, QtGui.QColor(0, 255, 0, 255)],
        [False,  QtGui.QColor(0, 0, 255, 255)],
        [False, QtGui.QColor(255,255,255, 255)],
        [False,  QtGui.QColor(255, 255, 255, 255)]]


class OneDimensionalElement(Element):
    """
    Element defined in one-dimensional transform of a signal.
    """
    # SIGNALS
    #  called when the element is clicked
    #  raise the index of the element (number)
    elementClicked = QtCore.Signal(int)

    # CONSTANTS
    #  decimal places to round the measurements
    DECIMAL_PLACES = 4

    # different colors for the even and odds rows in the parameter table and segment colors.
    COLOR_ODD = QtGui.QColor(0, 0, 255, 100)
    COLOR_EVEN = QtGui.QColor(0, 255, 0, 100)

    def __init__(self, signal, indexFrom, indexTo):
        Element.__init__(self, signal)
        self.indexFrom = indexFrom
        self.indexTo = indexTo
