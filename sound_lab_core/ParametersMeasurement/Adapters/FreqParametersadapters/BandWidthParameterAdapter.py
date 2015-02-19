# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.BandWidthParameter import BandWidthParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class BandWidthParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the band width parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)
        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'int', u'value': -20.00, u'step': 1, u'limits': (-100, 0)},
            {u'name': unicode(self.tr(u'Total')), u'type': u'bool', u'default': True, u'value': True}]
        self.threshold = -20
        self.total = True
        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings

    def get_instance(self):

        threshold = -20
        total = False
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()
            total = self.settings.param(unicode(self.tr(u'Total'))).value()

        except Exception as e:
            threshold = self.threshold
            total = self.total

        self.threshold = threshold
        self.total = total

        return BandWidthParameter(threshold=self.threshold, total=self.total)
