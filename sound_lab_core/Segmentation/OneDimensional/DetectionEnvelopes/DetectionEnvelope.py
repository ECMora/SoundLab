from PyQt4.QtCore import pyqtSignal, QObject
from utils.Utils import fromdB
import numpy as np


class DetectionEnvelope(QObject):
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

    def __init__(self, threshold_db=-40):
        QObject.__init__(self)

        self._threshold = threshold_db

        # the scale of each value of the acoustic processing
        # on the real signal data
        self._scale = 1

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

    # endregion

    def get_threshold_level(self, data):
        """
        Computes the threshold level from an array of data supplied.
        :param data:
        :return:
        """
        return fromdB(self.threshold, 0, max(data))

    def get_acoustic_processing(self, data):
        return data

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

    def local_max(self, data):
        """
        Identify the local  (positives or not) max that are above threshold
        :param data:  Array of int with the signal data information
        :return:
        """
        data = abs(np.array(data))

        indexes = [i for i in xrange(1, data.size - 1) if (data[i - 1] <= data[i] >= data[i + 1])]

        return np.array(indexes), data[indexes]