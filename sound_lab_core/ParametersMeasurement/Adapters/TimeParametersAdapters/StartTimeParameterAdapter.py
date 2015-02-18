# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.StartTimeParameter import StartTimeParameter
from pyqtgraph.parametertree import Parameter


class StartTimeParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

    def get_instance(self):
        return StartTimeParameter()
