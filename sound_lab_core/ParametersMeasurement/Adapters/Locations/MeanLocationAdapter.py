# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.MeanMeasurementLocation import MeanMeasurementLocation


class MeanLocationAdapter(LocationAdapter):
    """
    Location adapter for mean location (all the segment)
    """

    def __init__(self):
        LocationAdapter.__init__(self)
        self.name = self.tr(u'Mean')

    def get_instance(self):
        return [MeanMeasurementLocation()]



