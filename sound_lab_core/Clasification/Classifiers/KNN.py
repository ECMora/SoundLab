# -*- coding: utf-8 -*-
from sound_lab_core.Clasification import ClassificationMethod


class KNN(ClassificationMethod):

    def __init__(self,classificationData=None):
        ClassificationMethod.__init__(self,classificationData)

    def classify(self,newData):
        pass