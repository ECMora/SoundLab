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
            {u'name': unicode(self.tr(u'Threshold (db)')), u'type': u'float', u'value': -40.00, u'step': 1},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1},
            {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': 1.00, u'step': 0.5},
            {u'name': unicode(self.tr(u'Threshold 2(db)')), u'type': u'float', u'value': 0.00, u'step': 1},
            {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'float', u'value': 6, u'step': 1},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'float', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """

        return self.settings

    @property
    def instance(self):
        """
        Gets a new instance of the corresponding parameter measurement.
        :return: A new instance of the corresponding parameter measurement class
        """
        return AbsDecayEnvelopeDetector(None,1,-40,1,5,5)

    def apply_settings_change(self, transform, change):
        """

        :type transform:
        """
        pass