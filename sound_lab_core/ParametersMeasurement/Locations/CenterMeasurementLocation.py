from numpy import zeros
from matplotlib import mlab
from sound_lab_core.ParametersMeasurement.Locations.FrequencyMeasurementLocation import FrequencyMeasurementLocation


class CenterFrequencyMeasurementLocation(FrequencyMeasurementLocation):
    """
    Location of measurement at the centre of the segment.
    """

    def __init__(self, ms_delay=0, min_kHz=0, max_kHz=250):
        FrequencyMeasurementLocation.__init__(self, min_kHz=min_kHz, max_kHz=max_kHz)

        self.ms_delay = ms_delay

        self.name = "Center"

        if self.ms_delay > 0:
            self.name += " + " + str(self.ms_delay) + "ms"

        if self.ms_delay < 0:
            self.name += " - " + str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):
        slice_arr = zeros(segment.indexTo - segment.indexFrom)

        start_index = max(0, len(slice_arr)/2 + self.ms_delay * segment.signal.samplingRate / 1000)

        start_index = min(start_index, int(len(slice_arr) * 0.75))

        size = len(slice_arr) / 4

        # if start index is to far that the 1/4 of slice is outside the segment
        if start_index >= len(slice_arr) * 3.0 / 4:
            size = len(slice_arr) - start_index

        slice_arr[: size] = segment.signal.data[start_index: start_index + size]
        return slice_arr