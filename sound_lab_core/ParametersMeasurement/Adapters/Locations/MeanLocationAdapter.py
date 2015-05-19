# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Locations.MeanMeasurementLocation import MeanMeasurementLocation
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class MeanLocationAdapter(SoundLabAdapter):

    def __init__(self):
        SoundLabAdapter.__init__(self)
        self.name = self.tr(u'Mean')

    def get_instance(self):
        return MeanMeasurementLocation()



