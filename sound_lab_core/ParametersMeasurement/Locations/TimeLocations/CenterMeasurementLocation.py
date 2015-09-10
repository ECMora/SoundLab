from numpy import zeros
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class CenterMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the centre of the segment.
    """

    def __init__(self, ms_delay=0, NFFT=512, overlap=50):
        MeasurementLocation.__init__(self, NFFT, overlap)

        self.ms_delay = ms_delay

        self.name = "Center "

        if self.ms_delay > 0:
            self.name += " + " + unicode(self.ms_delay) + "ms"

        if self.ms_delay < 0:
            self.name += unicode(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):

        ms_delay = self.ms_delay * segment.signal.samplingRate / 1000

        index_center = segment.indexFrom + (segment.indexTo - segment.indexFrom) / 2

        index_center += ms_delay

        start_index = max(segment.indexFrom, index_center)

        end_index = min(start_index + self.NFFT, segment.indexTo)

        self.time_start_index, self.time_end_index = start_index, end_index

        return segment.signal.data[self.time_start_index: self.time_end_index]
