from numpy import zeros
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class StartMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the start of the segment.
    """

    def __init__(self, ms_delay=0, NFFT=512, overlap=50):
        MeasurementLocation.__init__(self, NFFT, overlap)

        self.ms_delay = 0 if ms_delay <= 0 else ms_delay

        self.name = u"Start " + u"" if self.ms_delay == 0 else " + " + unicode(self.ms_delay) + u"ms"

    def get_data_array_slice(self, segment):

        ms_delay = self.ms_delay * segment.signal.samplingRate / 1000

        start_index = min(segment.indexTo - self.NFFT, segment.indexFrom + ms_delay)

        if start_index >= segment.indexTo:
            raise Exception("The location requested is outside the segment")

        end_index = min(start_index + self.NFFT, segment.indexTo)

        self.time_start_index, self.time_end_index = start_index, end_index

        return segment.signal.data[self.time_start_index: self.time_end_index]

