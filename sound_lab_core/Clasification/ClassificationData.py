# -*- coding: utf-8 -*-
#Classification Methods based on a set of previously classified elements
#stored as {'data':numpy array}
from PyQt4.QtCore import pyqtSignal,QObject


class ClassificationData(QObject):
    """
    Class that handles the clasiffication
    """
    #SIGNALS

    #Signal raised when a new category was added.  str --> name of new category
    categoryAdded = pyqtSignal(str)

    #Signal raised when a new value was added into a category. str,str --> category,value
    valueAdded = pyqtSignal(str, str)

    #Signal raised when a value is removed from a category. str,str --> category,value
    valueRemoved = pyqtSignal(str, str)

    def __init__(self,trainingData = None,categories=None):
        """

        @param trainingData: list of ClassificationVector for training
        @param categories: dict of category --> list of values example {"Specie":["Homo Sapiens","Mormoops blainvillei"]}
        @raise Exception:
        """
        QObject.__init__(self)

        #set the training data
        #TODO establecer la via de almacenamiento y recuperacion de vectores de entrenamiento
        trainingData = [] if trainingData is None else trainingData

        #set the categories
        default = {"Specie": ["Cartacuba","Arriero"], "Taxa": ["Birds", "Mammals"]}
        categories = default if categories is None else categories

        if any([not isinstance(x, ClassificationVector) for x in trainingData]) or\
           categories is None or not isinstance(categories, dict):
            raise Exception("Invalid Arguments")

        self.data = trainingData
        self.categories = categories

    def addCategory(self,category):
        """

        :param category:
        :return:
        """
        if not category in self.categories:
            self.categories[category] = []
            self.categoryAdded.emit(category)
            return True
        return False

    def addValue(self,category,value):
        """
        Add a new value (if not exist) into a category.
        If category not exist is created.
        :param category: Category name
        :param value: category value
        :return:
        """
        if category not in self.categories:
            self.categories[category] = [value]

        if not value in self.categories[category]:
            self.categories[category].append(value)
            self.valueAdded.emit(category,value)
            return True
        return False

    def removeValue(self,category,value):
        """

        :param category:
        :param value:
        :return:
        """
        if category in self.categories and value in self.categories[category]:
            self.categories[category].remove(value)
            self.valueRemoved.emit(category,value)
            return True
        return False

    def getvalues(self,category):
        return self.categories[category] if category in self.categories else []

    def addTrainingVector(self,vector):
        """

        :param vector:
        :raise Exception:
        """
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