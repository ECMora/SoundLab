# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.OneDimensional.IntervalMethods.IntervalRmsDetector import IntervalRmsDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class IntervalDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'float', u'value': -40.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'int', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.threshold_dB = -40
        self.min_size_ms = 2
        self.merge_factor = 5

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
            threshold = -40
            min_size = 2
            merge_factor = 5


        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.merge_factor = merge_factor
        return IntervalRmsDetector(signal, self.threshold_dB, self.min_size_ms,self.merge_factor)
