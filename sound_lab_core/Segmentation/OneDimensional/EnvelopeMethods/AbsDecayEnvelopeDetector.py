from math import pi, sin

import matplotlib.mlab as mlab
from numpy import zeros, int32
import numpy as np

from sound_lab_core.Segmentation.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from utils.Utils import fromdB


class AbsDecayEnvelopeDetector(OneDimensionalElementsDetector):

    def __init__(self, signal, decay_ms=1, threshold_db=-40, threshold2_db=0, threshold3_db=0,
                 min_size_ms=1, merge_factor=5):
        OneDimensionalElementsDetector.__init__(self, signal, threshold_db, threshold2_db, threshold3_db,
                                                min_size_ms, merge_factor)

        self._decay_ms = decay_ms

    # region Properties

    @property
    def decay(self):
        return self._decay_ms

    @decay.setter
    def decay(self, value):
        self._decay_ms = value

    # endregion

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        threshold = fromdB(self.threshold, 0, max(self.signal.data))

        decay = int(self.decay * self.signal.samplingRate / 1000)

        data = self.signal.data[indexFrom:indexTo]

        elems, envelope = self.envelope_detector(data, threshold, decay)

        self.detectionProgressChanged.emit(65)

        self.detect_elements_start_end_thresholds(elems, envelope)

        self.detectionProgressChanged.emit(80)

        elems = self.merge_intervals(elems)

        self.detectionProgressChanged.emit(90)

        elems = self.filter_by_min_size(elems)

        self.detectionProgressChanged.emit(95)

        one_dim_class = self.get_one_dimensional_class()

        self.elements = [one_dim_class(self.signal, c[0], c[1]) for c in elems]

        self.detectionProgressChanged.emit(100)

        return self.elements

    def filter_by_min_size(self, elements):
        min_size = int(self.min_size * self.signal.samplingRate / 1000.0)
        return [c for c in elements if (c[1] - c[0]) > min_size]

    def envelope_detector(self, data, threshold, decay):
        """
        data is a numpy array
        minSize is the minThresholdLabel amplitude of an element
        merge_factor is the % of separation between 2 elements that is assumed as one (merge the 2 into one)
        """
        # create envelope
        envelope = self.abs_decay_averaged_envelope(data, decay)

        self.detectionProgressChanged.emit(50)

        return mlab.contiguous_regions(envelope > threshold), envelope

    def abs_decay_averaged_envelope(self, data, decay=1, envelope_type="sin"):
        """
        decay is the min number of samples in data that separates two elements
        """

        rectified = np.abs(data)

        self.detectionProgressChanged.emit(10)

        result = zeros(rectified.size, dtype=int32)
        current = rectified[0]
        fall_init, value, progress_step = None, 0, result.size / 10

        lineal = lambda first_value, index, start, decay: first_value - first_value * (index - start) / decay
        sin_function = lambda first_value, index, start, decay: first_value * sin(((index - start) * 1.0 * pi) / (decay * 2) + pi / 2)
        cuadratic = lambda first_value, index, start, decay: first_value * (1 - ((index - start) * 1.0) / decay) ** 2
        function = lineal if envelope_type == "lineal" else (sin_function if envelope_type == "sin" else cuadratic)

        for i in xrange(1, result.size):
            if fall_init is None:
                if rectified[i] < current:
                    fall_init = i - 1
                    value = function(rectified[i - 1], i, i - 1, decay)

            else:
                value = function(rectified[fall_init], i, fall_init, decay)

                fall_init = None if (value <= rectified[i] or i - fall_init >= decay) else fall_init

            result[i - 1] = current if fall_init is None else max(value, rectified[i])
            current = rectified[i]
            if i % progress_step == 0:
                self.detectionProgressChanged.emit(10 + (i / progress_step) * 6)

        result[-1] = current
        return result
