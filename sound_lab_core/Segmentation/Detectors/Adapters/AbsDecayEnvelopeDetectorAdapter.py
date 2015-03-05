# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.OneDimensional.EnvelopeMethods.AbsDecayEnvelopeDetector import \
    AbsDecayEnvelopeDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter
import pyqtgraph as pg


class AbsDecayEnvelopeDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

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
            threshold, threshold2, min_size = -40, 0, 2
            decay, soft_factor, merge_factor = 1, 6, 5

        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.decay_ms = decay
        self.threshold2_dB = threshold2
        self.soft_factor = soft_factor
        self.merge_factor = merge_factor

        return AbsDecayEnvelopeDetector(signal, self.decay_ms, self.threshold_dB, self.min_size_ms,
                                        self.merge_factor, self.soft_factor)

    def restore_settings(self, adapter_copy):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
                not isinstance(adapter_copy, AbsDecayEnvelopeDetectorAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance(None)

        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold_dB)
        self.settings.param(unicode(self.tr(u'Min Size (ms)'))).setValue(adapter_copy.min_size_ms)
        self.settings.param(unicode(self.tr(u'Threshold 2(dB)'))).setValue(adapter_copy.threshold2_dB)
        self.settings.param(unicode(self.tr(u'Decay (ms)'))).setValue(adapter_copy.decay_ms)
        self.settings.param(unicode(self.tr(u'Soft Factor'))).setValue(adapter_copy.soft_factor)
        self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).setValue(adapter_copy.merge_factor)

    def get_visual_items(self):
        return []


