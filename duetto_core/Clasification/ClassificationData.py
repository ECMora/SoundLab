# -*- coding: utf-8 -*-
#Classification Methods based on a set of previously classified elements
#stored as {'data':numpy array,''}
from PyQt4.QtCore import pyqtSignal,QObject


class ClassificationData(QObject):
    categoryAdded = pyqtSignal(str)    #category that was added
    valueAdded = pyqtSignal(str, str)   #New category,value
    valueRemoved = pyqtSignal(str, str) #category,value that was removed


    def __init__(self,trainingData = None,categories=None):
        """

        @param trainingData: list of ClassificationVector for training
        @param categories: dict of category --> list of values example {"Specie":["Homo Sapiens","Mormoops blainvillei"]}
        @raise Exception:
        """
        QObject.__init__(self)
        trainingData = [] if trainingData is None else trainingData
        default = {"Specie":["Cartacuba","Sinsonte"]
                   }
        categories =  default if categories is None else categories
        if any([not isinstance(x,ClassificationVector) for x in trainingData]) or\
           categories is None or not isinstance(categories, dict):

            raise Exception("Invalid Arguments")

        self.data = trainingData
        self.categories = categories

    def addCategory(self,category):
        if not category in self.categories:
            self.categories[category] = []
            self.categoryAdded.emit(category)
            return True
        return False

    def addValue(self,category,value):
        if category not in self.categories:
            self.categories[category] = []

        if not value in self.categories[category]:
            self.categories[category].append(value)
            self.valueAdded.emit(category,value)
            return True
        return False

    def removeValue(self,category,value):
        if category in self.categories and value in self.categories[category]:
            self.categories[category].remove(value)
            self.valueRemoved.emit(category,value)
            return True
        return False

    def getvalues(self,category):
        return self.categories[category] if category in self.categories else []

    def addTrainingVector(self,vector):
        if not isinstance(vector,ClassificationVector):
            raise Exception("Invalid Arguments")
        self.data.append(vector)
        if not vector.category in self.categories:
            self.categories[vector.category] = [vector.value]
        elif not vector.value in self.categories[vector.category]:
            self.categories[vector.category].append(vector.value)


class ClassificationVector:

    def __init__(self, data, category, value):
        """
        @param data: "Parameter measured" --> Medition Value
        """
        if not isinstance(data,dict):
            raise Exception("Invalid Arguments")
        self.data = data
        self.category = category
        self.value = value