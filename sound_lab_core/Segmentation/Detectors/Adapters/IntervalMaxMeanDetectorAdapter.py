# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.Adapters.IntervalDetectorAdapter import IntervalDetectorAdapter


class IntervalMaxMeanDetectorAdapter(IntervalDetectorAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        IntervalDetectorAdapter.__init__(self, parent)
