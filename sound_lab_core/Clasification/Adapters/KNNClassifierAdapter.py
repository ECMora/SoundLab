# -*- coding: utf-8 -*-
from sound_lab_core.Clasification.Adapters.ClassifierAdapter import ClassifierAdapter
from sound_lab_core.Clasification.Classifiers.KNNClassifier import KNNClassifier


class KNNClassifierAdapter(ClassifierAdapter):
    """
    Adapter class for the manual classifier
    """

    def __init__(self):
        ClassifierAdapter.__init__(self)

    def get_instance(self):
        return KNNClassifier()