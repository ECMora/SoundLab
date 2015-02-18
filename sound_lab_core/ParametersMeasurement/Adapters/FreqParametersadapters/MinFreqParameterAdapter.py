# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.MinFreqParameter import MinFreqParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class MinFreqParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the max freq parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)
        settings = [
            {u'name': unicode(self.tr(u'Threshold (db)')), u'type': u'int', u'value': -20.00, u'step': 1, u'limits': (-100, 0)}]

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings

    def get_instance(self):
        threshold = self.settings.param(unicode(self.tr(u'Threshold (db)'))).value()

        return MinFreqParameter(threshold=threshold)
