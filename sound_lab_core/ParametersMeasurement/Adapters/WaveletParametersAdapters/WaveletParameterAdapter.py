# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.FreqParameterAdapter import \
    SpectralParameterAdapter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class WaveletParameterAdapter(SpectralParameterAdapter):
    """
    Adapter class for the peaks above parameter.
    """

    def __init__(self):
        SpectralParameterAdapter.__init__(self)
        selected_wavelet = "db10"
        wavelets = [(unicode(x), x) for x in ["haar","db2","db4","db6","db8","db10"]]
        self._settings += [{u'name': unicode(self.tr(u'Wavelet')), u'type': u'list',
                            u'values': wavelets,
                            u'default': unicode(selected_wavelet),
                            u'value': unicode(selected_wavelet)},
                           {u'name': unicode(self.tr(u'Level')), u'type': u'int',
                            u'value': 0, u'default': 0, u'limits': (0, 7)}]

        self.level = 0
        self.wavelet = selected_wavelet
        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)
        self.settings.param(unicode(self.tr(u'Wavelet'))).setValue(selected_wavelet)

    def compute_settings(self):
        SpectralParameterAdapter.compute_settings(self)

        try:
            level = self.settings.param(unicode(self.tr(u'Level'))).value()

        except Exception as e:
            level = self.level

        self.level = level

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
           not isinstance(adapter_copy, WaveletParameterAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance()
        self.settings.param(unicode(self.tr(u'Wavelet'))).setValue(adapter_copy.wavelet)
