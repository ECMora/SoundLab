# -*- coding: utf-8 -*-
#Classification Methods based on a set of previously classified elements
#stored as {'data':numpy array,''}


class ClassificationMethod:
    def __init__(self,trainingData,classification):
        if trainingData is None or len(trainingData) == 0:
            raise Exception("Invalid Arguments")

        self.data = trainingData
        self.classification = classification

    def dimension(self):
        return len(self.data[0])

    def classify(self,newData):
        pass

