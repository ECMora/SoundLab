# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.FreqParameterAdapter import \
    SpectralParameterAdapter
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeaksAboveParameter import PeaksAboveParameter


class PeaksAboveParameterAdapter(SpectralParameterAdapter):
    """
    Adapter class for the peaks above parameter.
    """

    def __init__(self):
        SpectralParameterAdapter.__init__(self)
        self.name = self.tr(u'PeaksAbove')

        self._settings += [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'int', u'value': -20.00, u'step': 1, u'limits': (-100, 0)}]

        self.threshold = -20
        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)

    def get_instance(self):
        self.compute_settings()

        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()

        except Exception as e:
            threshold = self.threshold

        self.threshold = threshold

        return PeaksAboveParameter(threshold=self.threshold, decimal_places=self.decimal_places)

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SpectralParameterAdapter) or \
           not isinstance(adapter_copy, PeaksAboveParameterAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance()
        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold)
