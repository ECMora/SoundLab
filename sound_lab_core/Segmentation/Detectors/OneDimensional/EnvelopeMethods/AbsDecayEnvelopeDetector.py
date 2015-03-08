from math import pi, sin
import matplotlib.mlab as mlab
from numpy import zeros, array, int32, mean
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from utils.Utils import fromdB


class AbsDecayEnvelopeDetector(OneDimensionalElementsDetector):

    def __init__(self, signal, decay_ms=1, threshold_db=-40, min_size_ms=1, merge_factor=5, soft_factor=5):
        OneDimensionalElementsDetector.__init__(self, signal)

        self._decay = decay_ms
        self._threshold = threshold_db
        self._merge_factor = merge_factor
        self._soft_factor = soft_factor
        self._min_size = min_size_ms

    # region Properties

    @property
    def decay(self):
        return self._decay

    @decay.setter
    def decay(self, value):
        self._decay = value

    @property
    def merge_factor(self):
        return self._merge_factor

    @merge_factor.setter
    def merge_factor(self, value):
        self._merge_factor = value

    @property
    def softfactor(self):
        return self._soft_factor

    @softfactor.setter
    def softfactor(self, value):
        self._soft_factor = value

    @property
    def min_size(self):
        return self._min_size

    @min_size.setter
    def min_size(self, value):
        self._min_size = value

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    # endregion

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        threshold = fromdB(self.threshold, 0, self.signal.maximumValue)

        min_size = int(self.min_size * self.signal.samplingRate / 1000.0)

        decay = int(self.decay * self.signal.samplingRate / 1000)  # salto para evitar caidas locales

        elems = self.envelope_detector(self.signal.data[indexFrom:indexTo], threshold, decay, min_size)

        self.detectionProgressChanged.emit(90)

        self.elements = [None for _ in elems]
        one_dim_class = self.get_one_dimensional_class()

        for i, c in enumerate(elems):
            self.elements[i] = one_dim_class(self.signal, c[0], c[1])

        self.detectionProgressChanged.emit(100)

        return self.elements

    def envelope_detector(self,data, threshold, decay, min_size):
        """
        data is a numpy array
        minSize is the minThresholdLabel amplitude of an element
        merge_factor is the % of separation between 2 elements that is assumed as one (merge the 2 into one)
        """
        # create envelope
        envelope = self.abs_decay_averaged_envelope(data, decay, self.softfactor)

        self.detectionProgressChanged.emit(70)

        regions = mlab.contiguous_regions(envelope > threshold)

        self.detectionProgressChanged.emit(80)

        if self.merge_factor > 0:
            regions = self.merge_intervals(regions, self.merge_factor)

        self.detectionProgressChanged.emit(90)

        # d = {}
        result = []
        for i, c in enumerate(regions):
            if (c[1] - c[0]) > min_size:
                # d[i] = c
                result.append(c)

        # values = d.values()
        # values.sort(lambda x, y: x[0] <= y[0])
        # return values
        return result

    def abs_decay_averaged_envelope(self, data, decay=1, softfactor=6, envelope_type="sin"):
        """
        decay is the min number of samples in data that separates two elements
        """

        rectified = array(abs(data))

        self.detectionProgressChanged.emit(10)

        i = 1
        arr = zeros(len(rectified), dtype=int32)
        current = rectified[0]
        fall_init = None
        progress_step = len(arr) / 10

        while i < len(arr):
            if fall_init is not None:
                value = rectified[fall_init]
                if envelope_type == "lineal":
                    value -= rectified[fall_init] * (i - fall_init) / decay  # lineal
                elif envelope_type == "sin":
                    value = rectified[fall_init] * sin(((i - fall_init) * 1.0 * pi) / (decay * 2) + pi / 2)
                elif envelope_type == "cuadratic":
                    value = rectified[fall_init] * (1 - ((i - fall_init) * 1.0) / decay) ** 2

                arr[i - 1] = max(value, rectified[i])
                fall_init = None if (value <= rectified[i] or i - fall_init >= decay) else fall_init
            else:
                fall_init = i - 1 if rectified[i] < current else None
                arr[i - 1] = current
            current = rectified[i]
            i += 1
            if i % progress_step == 0:
                self.detectionProgressChanged.emit(10 + (i / progress_step) * 6)

        arr[-1] = current

        if softfactor > 1:
            return array([mean(arr[i - softfactor:i]) for i, _ in enumerate(arr, start=softfactor)])
        return arr
