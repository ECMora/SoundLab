from sound_lab_core.Segmentation.OneDimensional.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from utils.Utils import fromdB


class EnvelopeDetector(OneDimensionalElementsDetector):
    # region CONSTANTS

    # the number of calls to the interval_function method before send a
    # progress message
    PROGRESS_STEP = 15

    # endregion

    def __init__(self, signal, threshold_db=-40, min_size_ms=1, merge_factor=5, envelope_method=None):
        """
        :return:
        """
        OneDimensionalElementsDetector.__init__(self, signal=signal, min_size_ms=min_size_ms, merge_factor=merge_factor)

        # variables for detection
        self._threshold = threshold_db
        self._envelope_method = envelope_method

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        self.detectionProgressChanged.emit(5)

        detected, acoustic_processing = self.get_acoustic_processing(self.signal.data[indexFrom:indexTo])

        self.detectionProgressChanged.emit(70)

        detected = self.detect_elements(detected, acoustic_processing)

        self.detectionProgressChanged.emit(80)

        detected = self.filter_by_min_size(detected)

        self.detectionProgressChanged.emit(90)

        detected = self.merge_intervals(detected)

        self.detectionProgressChanged.emit(95)

        one_dim_class = self.get_one_dimensional_class()

        self.elements = [one_dim_class(self.signal, c[0], c[1]) for c in detected]

        self.detectionProgressChanged.emit(100)

        return self.elements

    def get_threshold_level(self, data):
        """
        Computes the threshold level from an array of data supplied.
        :param data:
        :return:
        """
        return fromdB(self.threshold, 0, max(data))

    def interval_function(self, data, step, total):
        """
        function that is applied to all intervals to get the acoustic processing
        :param data:  array with interval data
        :param step: the number of the current interval function call request
        :param total: the total number of calls to the interval function (used for progress update)
        :return:
        """
        if step % self.PROGRESS_STEP == 0:
            self.function_progress(step, total)
        return 0

    def get_acoustic_processing(self, data):
        if self.envelope_method is None:
            return []

        return self.envelope_method.\
            get_acoustic_processing(data, self.min_size * self.signal.samplingRate / 1000.0)

    def filter_by_min_size(self, detected):
        """
        Define a filter by min size for the intervals acoustic processing
        :param detected: the data array to filter. Is a list of tuples (start, end)
        :return:
        """
        min_size = max(1, int(self.min_size * self.signal.samplingRate / 1000.0))

        return [((x[0] - 1) * min_size / 2, (x[1]) * min_size / 2) for x in detected if x[1] > 1 + x[0]]

    def function_progress(self, step, total):
        """
        :param progress: int of progress go from 0 to total
        :param total: the total steps of the interval_function calls
        :return:
        """
        self.detectionProgressChanged.emit(5 + step * 70.0 / total)

    # region Properties

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    @property
    def envelope_method(self):
        return self._envelope_method

    @envelope_method.setter
    def envelope_method(self, value):
        self._envelope_method = value

    # endregion

    def detect_elements(self, elems, acoustic_processing):
        """
        Detect the start and end of the detected elements using three thresholds.
        :param elems: List of tuples (start, end) of detected elements with one threshold
        over the acoustic processing supplied.
        :param acoustic_processing:
        :return:
        """
        if self.threshold2 < 0 or self.threshold3 < 0:
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