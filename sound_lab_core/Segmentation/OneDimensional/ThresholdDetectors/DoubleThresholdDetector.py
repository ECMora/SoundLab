from PyQt4 import QtGui
from sound_lab_core.Segmentation.OneDimensional.ThresholdDetectors.SingleThresholdDetector import SingleThresholdDetector
from utils.Utils import fromdB
import numpy as np
import pyqtgraph as pg


class DoubleThresholdDetector(SingleThresholdDetector):

    # region CONSTANTS

    THRESHOLD_2_PEN = pg.mkPen(QtGui.QColor(250, 50, 50, 255), width=2)

    # endregion

    def __init__(self, signal, threshold_db=-40, threshold2_db=0, min_size_ms=1, merge_factor=5, envelope=None):
        """
        :return:
        """
        SingleThresholdDetector.__init__(self, threshold_db=threshold_db, signal=signal,
                                         min_size_ms=min_size_ms, merge_factor=merge_factor, envelope_method=envelope)

        # variables for detection
        self._threshold2 = threshold2_db

        self.threshold2_visual_item = []

    # region Properties

    @property
    def threshold2(self):
        return self._threshold2

    @threshold2.setter
    def threshold2(self, value):
        self._threshold2 = value

    # endregion

    def get_visual_items(self):
        parent_items = SingleThresholdDetector.get_visual_items(self)
        parent_items.extend(self.threshold2_visual_item)

        return parent_items

    def detect_elements(self, acoustic_processing):
        """
        Detect the start and end of the detected elements using three thresholds.
        :param elems: List of tuples (start, end) of detected elements with one threshold
        over the acoustic processing supplied.
        :param acoustic_processing:
        :return:
        """
        elems = SingleThresholdDetector.detect_elements(self, acoustic_processing)

        self.threshold2_visual_item = []

        if self.threshold2 >= 0:
            return elems

        result = []
        x_scale = self.envelope_method.scale

        for element in elems:
            max_amplitude_index = np.argmax(acoustic_processing[element[0]: element[1]])

            max_amplitude_index += element[0]

            threshold_db = fromdB(self.threshold2, 0, acoustic_processing[max_amplitude_index])

            start_index, end_index = max_amplitude_index, max_amplitude_index
            # find start
            while start_index > 0 and acoustic_processing[start_index] > threshold_db:
                start_index -= 1

            # find end
            while end_index < len(acoustic_processing) and acoustic_processing[end_index] > threshold_db:
                end_index += 1

            result.append((start_index, end_index))

            if start_index > 0:
                start_index -= 1

            if end_index < len(acoustic_processing):
                end_index += 1

            x_values = np.arange(start_index * x_scale, end_index * x_scale)
            visual_item = pg.PlotCurveItem(x=x_values, y=np.ones(len(x_values)) * threshold_db * self._y_scale,
                                           pen=self.THRESHOLD_2_PEN)

            self.threshold2_visual_item.append(visual_item)

        return result

