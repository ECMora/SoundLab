from PyQt4 import QtGui
import numpy as np
import pyqtgraph as pg
from utils.Utils import fromdB
from sound_lab_core.Segmentation.OneDimensional.ThresholdDetectors.SingleThresholdDetector import SingleThresholdDetector


class TripleThresholdDetector(SingleThresholdDetector):

    # region CONSTANTS

    THRESHOLD_2_PEN = pg.mkPen(QtGui.QColor(250, 50, 50, 255), width=2)
    THRESHOLD_3_PEN = pg.mkPen(QtGui.QColor(50, 250, 50, 255), width=2)

    # endregion

    def __init__(self, signal, threshold_db=-40, threshold2_db=0, threshold3_db=0,
                 min_size_ms=1, merge_factor=5, envelope=None):
        """
        :return:
        """
        SingleThresholdDetector.__init__(self, signal=signal, threshold_db=threshold_db, min_size_ms=min_size_ms,
                                         merge_factor=merge_factor, envelope_method=envelope)

        # variables for detection
        self._threshold2 = threshold2_db
        self._threshold3 = threshold3_db

        self.thresholds_visual_item = []

    def get_visual_items(self):
        parent_items = SingleThresholdDetector.get_visual_items(self)

        parent_items.extend(self.thresholds_visual_item)

        return parent_items

    # region Properties

    @property
    def threshold2(self):
        return self._threshold2

    @threshold2.setter
    def threshold2(self, value):
        self._threshold2 = value

    @property
    def threshold3(self):
        return self._threshold3

    @threshold3.setter
    def threshold3(self, value):
        self._threshold3 = value

    # endregion

    def detect_elements(self, acoustic_processing):
        """
        Detect the start and end of the detected elements using three thresholds.
        :param elems: List of tuples (start, end) of detected elements with one threshold
        over the acoustic processing supplied.
        :param acoustic_processing:
        :return:
        """
        elems = SingleThresholdDetector.detect_elements(self, acoustic_processing)

        if self.threshold2 >= 0 or self.threshold3 >= 0:
            return elems

        # use both thresholds start and end
        result = []
        x_scale = self.envelope_method.scale

        for element in elems:
            max_amplitude_index = np.argmax(acoustic_processing[element[0]: element[1]])

            max_amplitude_index += element[0]

            start_threshold_db = fromdB(self.threshold2, 0, acoustic_processing[max_amplitude_index])
            end_threshold_db = fromdB(self.threshold3, 0, acoustic_processing[max_amplitude_index])

            start_index, end_index = max_amplitude_index, max_amplitude_index

            # find start
            while start_index > 0 and acoustic_processing[start_index] > start_threshold_db:
                start_index -= 1

            # find end
            while end_index < len(acoustic_processing) and acoustic_processing[end_index] > end_threshold_db:
                end_index += 1

            start_threshold_db *= self._y_scale
            end_threshold_db *= self._y_scale

            element_size = end_index - start_index
            x_1 = (start_index - element_size / 4.0) * x_scale
            x_2 = (start_index + element_size / 4.0) * x_scale
            x_values1 = np.arange(x_1, x_2)

            visual_item1 = pg.PlotCurveItem(x=x_values1, y=np.ones(len(x_values1)) * start_threshold_db * self._y_scale,
                                            pen=self.THRESHOLD_2_PEN)

            x_end_1 = (end_index - element_size / 4.0) * x_scale
            x_end_2 = (end_index + element_size / 4.0) * x_scale
            x_values2 = np.arange(x_end_1, x_end_2)

            visual_item2 = pg.PlotCurveItem(x=x_values2, y=np.ones(len(x_values2)) * end_threshold_db * self._y_scale,
                                            pen=self.THRESHOLD_3_PEN)

            result.append((start_index, end_index))

            self.thresholds_visual_item.append(visual_item1)
            self.thresholds_visual_item.append(visual_item2)

        return result

