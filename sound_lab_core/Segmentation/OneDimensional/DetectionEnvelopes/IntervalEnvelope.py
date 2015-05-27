from PyQt4.QtCore import pyqtSignal, QObject
import numpy as np
from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.DetectionEnvelope import DetectionEnvelope
from utils.Utils import fromdB


class IntervalEnvelope(DetectionEnvelope):
    """
    An envelope that is a function constant by intervals.
    """

    # region SIGNALS

    # signal raised while the acoustic processing is been computed.
    # Raise the percent of progress.
    progressChanged = pyqtSignal(int)

    # endregion

    # region CONSTANTS

    # the number of calls to the interval_function method before send a
    # progress message
    PROGRESS_STEP = 15

    # endregion

    def __init__(self, threshold_db=-40, min_size=40):
        QObject.__init__(self)

        self._threshold = threshold_db

        # the scale of each value of the acoustic processing
        # on the real signal data
        self._scale = 1
        self._min_size = min_size

    # region Properties

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    @property
    def min_size(self):
        return self._min_size

    @min_size.setter
    def min_size(self, value):
        self._min_size = value

    # endregion

    def get_threshold_level(self, data):
        """
        Computes the threshold level from an array of data supplied.
        :param data:
        :return:
        """
        return fromdB(self.threshold, 0, max(data))

    def get_acoustic_processing(self, data):
        min_size = max(2, int(self.min_size))

        arr_size = data.size * 2 / min_size

        k = min_size / 2

        # update the scale of the acoustic processing
        self.scale = k

        interval_acoustic_processing = np.array(
            [0 if i == 0 else self.interval_function(data[(i - 1) * k: i * k], i, arr_size)
             for i in xrange(arr_size)])

        self.progressChanged.emit(90)

        return interval_acoustic_processing

    def function_progress(self, step, total):
        """
        :param progress: int of progress go from 0 to total
        :param total: the total steps of the interval_function calls
        :return:
        """
        self.progressChanged.emit(step * 90.0 / total)

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