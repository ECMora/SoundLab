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
            {u'name': unicode(self.tr(u'Threshold 2(dB)')), u'type': u'float', u'value': 0.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'float', u'value': 6, u'step': 1, u'limits': (0, 50)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'float', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

        self.settings.sigTreeStateChanged.connect(self.apply_settings_change)

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def get_instance(self):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()
        min_size = self.settings.param(unicode(self.tr(u'Min Size (ms)'))).value()
        decay = self.settings.param(unicode(self.tr(u'Decay (ms)'))).value()
        soft_factor = self.settings.param(unicode(self.tr(u'Soft Factor'))).value()
        merge_factor = self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).value()


        return AbsDecayEnvelopeDetector(None, decay, threshold, min_size, merge_factor, soft_factor)

    def apply_settings_change(self,parameter, changes):
        print(changes)