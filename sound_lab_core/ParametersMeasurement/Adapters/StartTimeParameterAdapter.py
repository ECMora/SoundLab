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

    @property
    def instance(self):
        return StartTimeParameter()

    def get_settings(self):
        """
        :type parameter:
        """
        return Parameter.create(name=u'Settings', type=u'group')

    def apply_settings_change(self, transform, change):
        """

        :type transform:
        """
        pass