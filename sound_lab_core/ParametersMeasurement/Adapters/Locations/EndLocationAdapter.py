# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import FixedTimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.EndMeasurementLocation import EndMeasurementLocation


class EndLocationAdapter(FixedTimeLocationAdapter):
    """
    The FixedTimeLocationAdapter for the end of the segment
    """

    def __init__(self):
        FixedTimeLocationAdapter.__init__(self)

        self.settings.param(unicode(self.tr(u'ms delay'))).setLimits((-1000000, 0))

        self.name = self.tr(u'End')

    def get_instance(self):
        self.update_instance_variables()

        return [EndMeasurementLocation(ms_delay=self.ms_delay,  NFFT=self.fft_points, overlap=self.overlap)]



