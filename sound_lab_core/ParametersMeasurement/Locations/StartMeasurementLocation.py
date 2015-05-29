from sound_lab_core.ParametersMeasurement.Locations.FrequencyMeasurementLocation import FrequencyMeasurementLocation
from numpy import zeros


class StartFrequencyMeasurementLocation(FrequencyMeasurementLocation):
    """
    Location of measurement at the start of the segment.
    """

    def __init__(self, ms_delay=0, min_kHz=0, max_kHz=250):
        FrequencyMeasurementLocation.__init__(self, min_kHz=min_kHz, max_kHz=max_kHz)

        self.ms_delay = 0 if ms_delay <= 0 else ms_delay

        self.name = "Start" + "" if self.ms_delay == 0 else " + " + str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):
        slice_arr = zeros(segment.indexTo - segment.indexFrom)

        start_index = min(int(len(slice_arr) * 0.75), self.ms_delay * segment.signal.samplingRate / 1000)

        size = len(slice_arr) / 4

        # if start index is to far that the 1/4 of slice is outside the segment
        if start_index >= len(slice_arr) * 3.0 / 4:
            size = len(slice_arr) - start_index

        slice_arr[: size] = segment.signal.data[start_index: start_index + size]

        return slice_arr