# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, pyqtSignal


class ElementsDetector(QObject):
    """
    Base class for the detection hierarchy. Parent of the one
    and two dimension's elements detectors
    """

    #  region SIGNALS

    #  signal raised while detection is been made.
    # Raise the percent of detection progress.
    detectionProgressChanged = pyqtSignal(int)

    # endregion

    def __init__(self, signal):
        QObject.__init__(self)
        self.elements = []
        self.signal = signal

    def detect(self):
        """
        The method that detect the elements in the signal and storage into the corresponding list
        """
        return self.elements

    def get_visual_items(self):
        return []





