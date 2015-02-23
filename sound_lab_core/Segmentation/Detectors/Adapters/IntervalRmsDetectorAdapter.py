# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.Adapters.IntervalDetectorAdapter import IntervalDetectorAdapter


class IntervalRmsDetectorAdapter(IntervalDetectorAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        IntervalDetectorAdapter.__init__(self)
