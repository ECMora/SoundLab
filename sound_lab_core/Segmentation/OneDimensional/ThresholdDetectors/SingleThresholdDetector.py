from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.IntervalMaxEnvelope import IntervalMaxEnvelope
from sound_lab_core.Segmentation.OneDimensional.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from matplotlib import mlab as mlab
import pyqtgraph as pg
import numpy as np


class SingleThresholdDetector(OneDimensionalElementsDetector):

    def __init__(self, signal, threshold_db=-40, min_size_ms=1, merge_factor=5,
                 envelope_method=None):
        OneDimensionalElementsDetector.__init__(self, signal=signal, min_size_ms=min_size_ms,
                                                merge_factor=merge_factor)

        # variables for detection
        self._threshold = threshold_db
        self._envelope_method = None
        self.envelope_method = envelope_method if envelope_method is not None else IntervalMaxEnvelope()

        # visual elements
        self.envelope = None
        self.threshold_visual_item = None

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
        if value is not None:
            self._envelope_method = value
            self._envelope_method.threshold = self.threshold
            self._envelope_method.progressChanged.connect(lambda x: self.detectionProgressChanged.emit(5 + x * 0.7))

    # endregion

    def get_visual_items(self):
        items = []

        if self.envelope is not None:
            items.append(self.envelope)

        if self.threshold_visual_item is not None:
            items.append(self.threshold_visual_item)

        return items

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        self.detectionProgressChanged.emit(5)

        acoustic_processing = self.get_acoustic_processing(self.signal.data[indexFrom:indexTo])

        detected = self.detect_elements(acoustic_processing)

        self.envelope = pg.PlotCurveItem(x=np.arange(len(acoustic_processing)) * self.envelope_method.scale,
                                         y=acoustic_processing)



        # convert the logic units of the envelope to the real ones on the signal data array
        # accord to the scale of each index on the envelope method array
        detected = [c * self.envelope_method.scale for c in detected]

        self.detectionProgressChanged.emit(80)

        detected = self.filter_by_min_size(detected)

        self.detectionProgressChanged.emit(90)

        detected = self.merge_intervals(detected)

        self.detectionProgressChanged.emit(95)

        one_dim_class = self.get_one_dimensional_class()

        self.elements = [one_dim_class(self.signal, c[0], c[1]) for c in detected]

        self.detectionProgressChanged.emit(100)

        return self.elements

    def detect_elements(self, acoustic_processing):
        if self.envelope_method is None:
            return []

        threshold = self.envelope_method.get_threshold_level(acoustic_processing)

        return mlab.contiguous_regions(acoustic_processing > threshold)

    def get_acoustic_processing(self, data):
        if self.envelope_method is None:
            return []

        return self.envelope_method.\
            get_acoustic_processing(data)

    def filter_by_min_size(self, detected):
        """
        Define a filter by min size for the intervals acoustic processing
        :param detected: the data array to filter. Is a list of tuples (start, end)
        :return:
        """
        min_size = max(1, int(self.min_size * self.signal.samplingRate / 1000.0))

        return [((x[0] - 1) * min_size / 2, (x[1]) * min_size / 2) for x in detected if x[1] > 1 + x[0]]