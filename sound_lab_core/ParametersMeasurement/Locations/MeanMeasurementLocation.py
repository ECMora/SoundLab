from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation

__author__ = 'y.febles'


class MeanMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at all the segment.
    """

    def __init__(self):
        MeasurementLocation.__init__(self)
        self.name = "mean"