# -*- coding: utf-8 -*-
from sound_lab_core.Clasification.Adapters.ClassifierAdapter import ClassifierAdapter
from sound_lab_core.Clasification.Classifiers.ManualClassifier import ManualClassifier


class ManualClassifierAdapter(ClassifierAdapter):
    """
    Adapter class for the manual classifier
    """

    def __init__(self):
        ClassifierAdapter.__init__(self)

        self.name = u'Manual'

    def get_instance(self):
        return ManualClassifier()