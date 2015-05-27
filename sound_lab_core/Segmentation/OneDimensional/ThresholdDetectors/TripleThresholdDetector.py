from sound_lab_core.Segmentation.OneDimensional.ThresholdDetectors.SingleThresholdDetector import SingleThresholdDetector
from utils.Utils import fromdB


class TripleThresholdDetector(SingleThresholdDetector):

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

        if self.threshold2 < 0 and self.threshold3 < 0:
            # use both thresholds start and end
            result = []
            for element in elems:
                max_amplitude = max(acoustic_processing[element[0]: element[1]])

                start_threshold_db = fromdB(self.threshold2, 0, max_amplitude)
                end_threshold_db = fromdB(self.threshold3, 0, max_amplitude)

                start_index, end_index = element
                # find start
                while acoustic_processing[start_index] > start_threshold_db and start_index > 0:
                    start_index -= 1

                # find end
                while acoustic_processing[end_index] > end_threshold_db and end_index < len(acoustic_processing):
                    end_index += 1

                result.append((start_index, end_index))

            return result

        return elems