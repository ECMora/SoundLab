import numpy as np
from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.DetectionEnvelope import DetectionEnvelope


class AbsDecayEnvelope(DetectionEnvelope):
    """
    """

    def __init__(self, signal=None, threshold_db=-40, min_size=1, envelope_type="sin"):
        DetectionEnvelope.__init__(self, threshold_db=threshold_db)

        self.min_size = min_size if min_size > 0 else 1
        self.type = envelope_type

    def get_acoustic_processing(self, data):
        """
        decay is the min number of samples in data that separates two elements
        """

        rectified = np.abs(data)

        self.progressChanged.emit(10)

        result = np.zeros(rectified.size, dtype=np.int32)
        current = rectified[0]
        fall_init, value, progress_step = None, 0, result.size / 10

        lineal = lambda first_value, index, start, decay: first_value - first_value * (index - start) / decay
        sin_function = lambda first_value, index, start, decay: first_value * np.sin(
            ((index - start) * 1.0 * np.pi) / (decay * 2) + np.pi / 2)
        cuadratic = lambda first_value, index, start, decay: first_value * (1 - ((index - start) * 1.0) / decay) ** 2
        function = lineal if self.type == "lineal" else (sin_function if self.type == "sin" else cuadratic)

        for i in xrange(1, result.size):
            if fall_init is None:
                if rectified[i] < current:
                    fall_init = i - 1
                    value = function(rectified[i - 1], i, i - 1, self.min_size)

            else:
                value = function(rectified[fall_init], i, fall_init, self.min_size)

                fall_init = None if (value <= rectified[i] or i - fall_init >= self.min_size) else fall_init

            result[i - 1] = current if fall_init is None else max(value, rectified[i])
            current = rectified[i]
            if i % progress_step == 0:
                self.progressChanged.emit(10 + (i / progress_step) * 6)

        result[-1] = current
        return result