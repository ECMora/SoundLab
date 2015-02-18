# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from graphic_interface.segments.parameter_items.spectral_parameter_items.AverageFreqVisualItem import \
    AverageFreqVisualItem
from sound_lab_core.ParametersMeasurement.SpectralParameters.MaxFreqParameter import MaxFreqParameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class MaxFreqParameterAdapter(SoundLabAdapter):
    """
    Adapter class for the max freq parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)
        settings = [
            {u'name': unicode(self.tr(u'Threshold (db)')), u'type': u'int', u'value': -20.00, u'step': 1, u'limits': (-100, 0)}]

        self.threshold = -20

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return self.settings

    def get_instance(self):
        # todo improvement the way to get the calues form the param tree
        # use a try catch because the instance must be required after
        # param tree object is destroyed
        threshold = 0
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (db)'))).value()

        except Exception as e:
            threshold = self.threshold

        self.threshold = threshold

        return MaxFreqParameter(threshold=self.threshold)

    def get_visual_item(self):
        return AverageFreqVisualItem(tooltip=self.tr(u"Max Freq"))
