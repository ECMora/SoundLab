# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.OneDimensional.EnvelopeMethods.AbsDecayEnvelopeDetector import \
    AbsDecayEnvelopeDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class AbsDecayEnvelopeDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'float', u'value': -40.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': 1.00, u'step': 0.5, u'limits': (0, 10000)},
            {u'name': unicode(self.tr(u'Threshold 2(dB)')), u'type': u'int', u'value': 0.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'int', u'value': 6, u'step': 1, u'limits': (0, 50)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'int', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.threshold_dB = -40
        self.min_size_ms = 2
        self.decay_ms = 1
        self.threshold2_dB = 0
        self.soft_factor = 6
        self.merge_factor = 5

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

        self.settings.sigTreeStateChanged.connect(self.apply_settings_change)

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
            threshold2 = self.settings.param(unicode(self.tr(u'Threshold 2(dB)'))).value()
            decay = self.settings.param(unicode(self.tr(u'Decay (ms)'))).value()
            soft_factor = self.settings.param(unicode(self.tr(u'Soft Factor'))).value()
            merge_factor = self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).value()

        except Exception as ex:
            threshold = -40
            min_size = 2
            threshold2 = 0
            decay = 1
            soft_factor = 6
            merge_factor = 5


        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.decay_ms = decay
        self.threshold2_dB = threshold2
        self.soft_factor = soft_factor
        self.merge_factor = merge_factor
        return AbsDecayEnvelopeDetector(signal, self.decay_ms, self.threshold_dB, self.min_size_ms,
                                        self.merge_factor, self.soft_factor)

    def apply_settings_change(self,parameter, changes):
        print(changes)