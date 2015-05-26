from matplotlib import mlab as mlab
import numpy as np
from utils.Utils import fromdB


class IntervalEnvelope:
    # region CONSTANTS

    # the number of calls to the interval_function method before send a
    # progress message
    PROGRESS_STEP = 15

    # endregion

    def __init__(self, threshold_db=-40):
        self._threshold = threshold_db

    # region Properties

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    # endregion

    def get_threshold_level(self, data):
        """
        Computes the threshold level from an array of data supplied.
        :param data:
        :return:
        """
        return fromdB(self.threshold, 0, max(data))

    def get_acoustic_processing(self, data, min_size):
        min_size = max(2, int(min_size))

        arr_size = data.size * 2 / min_size

        k = min_size / 2

        interval_acoustic_processing = np.array(
            [0 if i == 0 else self.interval_function(data[(i - 1) * k: i * k], i, arr_size)
             for i in xrange(arr_size)])

        threshold = self.get_threshold_level(interval_acoustic_processing)

        self.detectionProgressChanged.emit(60)

        return mlab.contiguous_regions(interval_acoustic_processing > threshold), interval_acoustic_processing

    def function_progress(self, step, total):
        """
        :param progress: int of progress go from 0 to total
        :param total: the total steps of the interval_function calls
        :return:
        """
        self.detectionProgressChanged.emit(5 + step * 70.0 / total)

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


