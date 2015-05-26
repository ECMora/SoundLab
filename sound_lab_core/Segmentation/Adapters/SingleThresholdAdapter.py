# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.Segmentation.OneDimensional.ThresholdDetectors.SingleThresholdDetector import \
    SingleThresholdDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class SingleThresholdAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'float', u'value': -20.00, u'step': 1,
             u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1,
             u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'int', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.threshold_dB = -20
        self.min_size_ms = 2
        self.merge_factor = 5
        self.envelope = None

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def get_instance(self, signal):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()
            min_size = self.settings.param(unicode(self.tr(u'Min Size (ms)'))).value()
            merge_factor = self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).value()

        except Exception as ex:
            threshold, threshold2, threshold3 = -20, 0, 0
            min_size, merge_factor = 2, 5

        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.merge_factor = merge_factor
        self.envelope = None

        return SingleThresholdDetector(signal, self.threshold_dB, self.min_size_ms, self.merge_factor)