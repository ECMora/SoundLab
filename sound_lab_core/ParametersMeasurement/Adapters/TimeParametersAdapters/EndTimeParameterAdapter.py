# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.TimeParameters.EndTimeParameter import EndTimeParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class EndTimeParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_instance(self):
        return EndTimeParameter()
