# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeaksAboveParameter import PeaksAboveParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class PeaksAboveParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the peaks above parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)
        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'int', u'value': -20.00, u'step': 1, u'limits': (-100, 0)}]
        self.threshold = -20
        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings

    def get_instance(self):
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()

        except Exception as e:
            threshold = self.threshold

        self.threshold = threshold

        return PeaksAboveParameter(threshold=self.threshold)

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
           not isinstance(adapter_copy, PeaksAboveParameterAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance()
        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold)
