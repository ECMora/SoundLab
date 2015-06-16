from PyQt4 import QtGui
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class SpectralParameterAdapter(ParameterAdapter):
    """
    Each spectral parameter could be computed over a spectral location.
    """
    DEFAULT_COLOR = QtGui.QColor(50, 50, 255, 255)

    def __init__(self):
        ParameterAdapter.__init__(self)
        self._settings = [{u'name': unicode(self.tr(u'Decimal Places')), u'type': u'int', u'value': 3, u'step': 1,
                           u'limits': (1, 5)},
                          {u'name': unicode(self.tr(u'Show Visual Items')), u'type': u'bool',
                           u'value': True},
                          {u'name': unicode(self.tr(u'Visual Item Color')), u'type': u'color',
                           u'value': self.DEFAULT_COLOR}]

        self.visual_item_color = self.DEFAULT_COLOR

        self.show_visual_items = True

        self.decimal_places = 3

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)

    def compute_settings(self):
        # use a try catch because the instance must be required after
        # param tree object is destroyed
        try:
            decimals = self.settings.param(unicode(self.tr(u'Decimal Places'))).value()
            visual_item_color = self.settings.param(unicode(self.tr(u'Visual Item Color'))).value()
            show_items = self.settings.param(unicode(self.tr(u'Show Visual Items'))).value()

        except Exception as e:
            decimals, visual_item_color, show_items = self.decimal_places, self.visual_item_color, self.show_visual_items

        self.decimal_places = decimals
        self.visual_item_color = visual_item_color
        self.show_visual_items = show_items

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings


class FreqParameterAdapter(SpectralParameterAdapter):
    def __init__(self):
        SpectralParameterAdapter.__init__(self)
        self._settings += [{u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'int', u'value': -20.00, u'step': 1,
                            u'limits': (-100, 0)},
                           {u'name': unicode(self.tr(u'Total')), u'type': u'bool', u'default': True, u'value': True}]

        self.threshold = -20
        self.total = True

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)

    def compute_settings(self):
        SpectralParameterAdapter.compute_settings(self)
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
        self.settings.param(unicode(self.tr(u'Decimal Places'))).setValue(adapter_copy.decimal_places)
        self.compute_settings()
