# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import FixedTimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.EndMeasurementLocation import EndMeasurementLocation


class EndLocationAdapter(FixedTimeLocationAdapter):

    def __init__(self):
        FixedTimeLocationAdapter.__init__(self)
        self.name = self.tr(u'End')

    def get_instance(self):
        self.update_instance_variables()

        return [EndMeasurementLocation(ms_delay=self.ms_delay)]



