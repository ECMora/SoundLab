from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class FrequencyMeasurementLocation(MeasurementLocation):
    """
    A frequency location of measurement is an interval of the segment
    in which would be measured parameters. It provides an interval of frequency on which
    perform the measurement
    """

    def __init__(self, min_kHz=0, max_kHz=250):
        # name of the measurement location
        MeasurementLocation.__init__(self)

        # the freq interval in which would be measured
        # the parameters
        self.min_kHz = min_kHz
        self.max_kHz = max_kHz