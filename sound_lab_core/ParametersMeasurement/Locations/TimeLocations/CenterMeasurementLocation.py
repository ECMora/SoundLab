from numpy import zeros
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class CenterMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the centre of the segment.
    """

    def __init__(self, ms_delay=0, fft_points=256):
        MeasurementLocation.__init__(self)

        self.ms_delay = ms_delay

        self.fft_spectral_samples = fft_points

        self.name = "Center"

        if self.ms_delay > 0:
            self.name += " + " + str(self.ms_delay) + "ms"

        if self.ms_delay < 0:
            self.name += str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):
        slice_arr = zeros(self.fft_spectral_samples)

        ms_delay = self.ms_delay * segment.signal.samplingRate / 1000

        index_center = segment.indexFrom + (segment.indexTo - segment.indexFrom) / 2

        index_center += ms_delay

        start_index = min(segment.indexTo - self.fft_spectral_samples, max(segment.indexFrom, index_center))

        self.time_start_index, self.time_end_index = start_index, start_index + self.fft_spectral_samples

        slice_arr[: self.fft_spectral_samples] = segment.signal.data[self.time_start_index: self.time_end_index]

        return slice_arr