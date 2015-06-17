# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject
from sound_lab_core.Clasification.Adapters import *
from sound_lab_core.Segmentation.Adapters import *


class AdapterFactory(QObject):
    """
    Class that provides the adapters for segmentation, classification
    and parameter measurement.
    """

    def __init__(self):
        QObject.__init__(self)

        # list of all the adapters provided.
        self.adapters = []

    def adapters_names(self):
        """
        Gets the list of names of all registered adapters.
        :return: a list of str each one is the name of one adapter
        """
        return [x.name for x in self.adapters]

    def get_adapter(self, name):
        """
        :return: an instance of the corresponding adapter
        :raise: Exception if no adapter is found with name supplied
        """
        # self.adapters contains tuples with shape (name, adapter)
        adapters = [x for x in self.adapters if name == x.name]

        if len(adapters) == 0:
            raise Exception("Not found adapter")

        # the adapter name must be unique
        if len(adapters) > 1:
            raise Exception("Multiple Adapters match name supplied")

        return adapters[0]


class SegmentationAdapterFactory(AdapterFactory):
    """
    The adapters factory for segmentation methods.
    Provides a list of the segmentation methods adapters to create them
    """

    def __init__(self):
        AdapterFactory.__init__(self)

        self.adapters = [ManualDetectorAdapter(),

                         # thresholds methods
                         SingleThresholdAdapter(),
                         DoubleThresholdAdapter(),
                         TripleThresholdAdapter(),

                         # image methods
                         WatershedDetectorAdapter(),
                         AdaptThreshDetectorAdapter(),
                         GrabCutDetectorAdapter()]


class ClassificationAdapterFactory(AdapterFactory):
    """
    The adapters factory for classification methods.
    Provides a list of the classification methods adapters to create them
    """
    def __init__(self):
        AdapterFactory.__init__(self)

        self.adapters = [ManualClassifierAdapter(), KNNClassifierAdapter(), NeuralNetsAdapter()]
