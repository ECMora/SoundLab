import numpy as np
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.FreqParameterAdapter import \
    SpectralParameterAdapter


class FourierParameterAdapter(SpectralParameterAdapter):
    """
    """
    selected_function = u"Mean"

    def __init__(self):
        SpectralParameterAdapter.__init__(self)

        self._settings += [{u'name': unicode(self.tr(u'Function')), u'type': u'list',
                            u'values': [(x, x) for x in [u"Mean", u"Variance"]],
                            u'default': self.selected_function,
                            u'value': self.selected_function}]

        self.function_name = str(self.selected_function)
        self.func = np.var if self.name is u"Variance" else np.mean

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)

    def compute_settings(self):
        SpectralParameterAdapter.compute_settings(self)
        try:
            function = self.settings.param(unicode(self.tr(u'Function'))).value()

        except Exception as e:
            function = self.selected_function

        self.func = np.var if function is u"Variance" else np.mean
        self.function_name = str(function)