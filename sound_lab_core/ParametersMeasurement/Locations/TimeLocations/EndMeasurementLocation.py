from numpy import zeros
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class EndMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the end of the segment.
    """

    def __init__(self, ms_delay=0, NFFT=512, overlap=50):
        MeasurementLocation.__init__(self, NFFT, overlap)

        self.ms_delay = 0 if ms_delay >= 0 else ms_delay

        self.name = "End " + "" if self.ms_delay == 0 else str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):

        slice_arr = zeros(self.NFFT)

        ms_delay = self.ms_delay * segment.signal.samplingRate / 1000

        # ms_delay is < 0
        start_index = max(segment.indexFrom, segment.indexTo - self.NFFT + ms_delay)

        self.time_start_index, self.time_end_index = start_index, start_index + self.NFFT

        slice_arr[: self.NFFT] = segment.signal.data[self.time_start_index: self.time_end_index]

        return slice_arr