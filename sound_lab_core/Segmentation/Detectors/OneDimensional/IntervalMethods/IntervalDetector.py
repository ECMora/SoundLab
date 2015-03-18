from math import sqrt
import matplotlib.mlab as mlab
import numpy as np
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from utils.Utils import fromdB


class IntervalDetector(OneDimensionalElementsDetector):

    # region CONSTANTS

    # the number of calls to the interval_function method before send a
    # progress message
    PROGRESS_STEP = 15

    # endregion

    def __init__(self, signal, threshold_db=-40, threshold2_db=0, threshold3_db=0, min_size_ms=1, merge_factor=5):
        OneDimensionalElementsDetector.__init__(self, signal, threshold_db, threshold2_db, threshold3_db,
                                                min_size_ms, merge_factor)

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        self.detectionProgressChanged.emit(5)

        detected, acoustic_processing = self.get_acoustic_processing(self.signal.data[indexFrom:indexTo])

        self.detectionProgressChanged.emit(70)

        detected = self.detect_elements_start_end_thresholds(detected, acoustic_processing)

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

    def get_acoustic_processing(self, data):
        min_size = max(1, int(self.min_size * self.signal.samplingRate / 1000.0))

        arr_size = data.size * 2 / min_size

        k = min_size / 2

        interval_acoustic_processing = np.array([0 if i == 0 else self.interval_function(data[(i - 1) * k: i * k], i, arr_size)
                                       for i in xrange(arr_size)])

        threshold = self.get_threshold_level(interval_acoustic_processing)

        self.detectionProgressChanged.emit(60)

        return mlab.contiguous_regions(interval_acoustic_processing > threshold), interval_acoustic_processing

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
        self.detectionProgressChanged.emit(5 + step * 70.0/total)

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