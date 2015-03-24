# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.OneDimensional.EnvelopeMethods.AbsDecayEnvelopeDetector import \
    AbsDecayEnvelopeDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter
import pyqtgraph as pg
from utils.Utils import fromdB


class AbsDecayEnvelopeDetectorAdapter(SoundLabAdapter):

    def __init__(self):
        SoundLabAdapter.__init__(self)

        settings = [
            {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': 1.00, u'step': 0.5,
             u'limits': (0, 10000)},
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'float', u'value': -20.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Threshold Start(dB)')), u'type': u'int', u'value': 0.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Threshold End(dB)')), u'type': u'int', u'value': 0.00, u'step': 1,
             u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1,
             u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'int', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.threshold_dB = -20
        self.min_size_ms = 2
        self.decay_ms = 1
        self.threshold2_dB = 0
        self.threshold3_dB = 0
        self.merge_factor = 5

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

        # visual items
        self.signal_max_value = 2 ** 16

        # the time region limits
        self.threshold_line_item = pg.InfiniteLine(angle=0, movable=True, pos=fromdB(self.threshold_dB, 0,
                                                                                     self.signal_max_value),
                                                   pen=pg.mkPen(color=self.COLOR, width=self.VISUAL_ITEM_LINE_WIDTH))

        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).sigValueChanged.connect(
            lambda parameter: self.threshold_line_item.setValue(fromdB(parameter.value(), 0, self.signal_max_value)))

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
            threshold2 = self.settings.param(unicode(self.tr(u'Threshold Start(dB)'))).value()
            threshold3 = self.settings.param(unicode(self.tr(u'Threshold End(dB)'))).value()
            decay = self.settings.param(unicode(self.tr(u'Decay (ms)'))).value()
            merge_factor = self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).value()

        except Exception as ex:
            threshold, threshold2, threshold3, min_size = -20, 0, 0, 2
            decay, merge_factor = 1, 5

        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.decay_ms = decay
        self.threshold2_dB = threshold2
        self.threshold3_dB = threshold3
        self.merge_factor = merge_factor

        self.signal_max_value = max(signal.data)

        return AbsDecayEnvelopeDetector(signal, self.decay_ms, self.threshold_dB, self.threshold2_dB,
                                        self.threshold3_dB, self.min_size_ms, self.merge_factor)

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
                not isinstance(adapter_copy, AbsDecayEnvelopeDetectorAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance(signal)

        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold_dB)
        self.settings.param(unicode(self.tr(u'Min Size (ms)'))).setValue(adapter_copy.min_size_ms)
        self.settings.param(unicode(self.tr(u'Threshold Start(dB)'))).setValue(adapter_copy.threshold2_dB)
        self.settings.param(unicode(self.tr(u'Threshold End(dB)'))).setValue(adapter_copy.threshold3_dB)
        self.settings.param(unicode(self.tr(u'Decay (ms)'))).setValue(adapter_copy.decay_ms)
        self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).setValue(adapter_copy.merge_factor)

    def get_visual_items(self):
        return [self.threshold_line_item]


