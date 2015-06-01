from sound_lab_core.ParametersMeasurement.Adapters.Locations.FrequencyMeasurementLocationAdapter import \
    FrequencyMeasurementLocationAdapter
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class SpectralParameterAdapter(ParameterAdapter):
    """
    Each spectral parameter could be computed over a spectral location.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        self._spectral_location_adapter = FrequencyMeasurementLocationAdapter()

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=[])

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings

    def get_spectral_location_adapter(self):
        """
        :return: the adapter for the spectral location definition
        """
        return self._spectral_location_adapter

    def update_data(self, signal):
        self._spectral_location_adapter.update_data(signal)


class FreqParameterAdapter(SpectralParameterAdapter):
    def __init__(self):
        SpectralParameterAdapter.__init__(self)
        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'int', u'value': -20.00, u'step': 1,
             u'limits': (-100, 0)},
            {u'name': unicode(self.tr(u'Total')), u'type': u'bool', u'default': True, u'value': True}]

        self.threshold = -20
        self.total = True

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def compute_settings(self):
        # use a try catch because the instance must be required after
        # param tree object is destroyed
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()
            total = self.settings.param(unicode(self.tr(u'Total'))).value()

        except Exception as e:
            threshold = self.threshold
            total = self.total

        self.threshold = threshold
        self.total = total

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
           not isinstance(adapter_copy, FreqParameterAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.compute_settings()

        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold)
        self.settings.param(unicode(self.tr(u'Total'))).setValue(adapter_copy.total)

        self.compute_settings()




