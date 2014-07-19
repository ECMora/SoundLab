# -*- coding: utf-8 -*-
#Classification Methods based on a set of previously classified elements
#stored as {'data':numpy array,''}


class ClassificationData:
    def __init__(self,trainingData = None,categories=None):
        """

        @param trainingData: list of ClassificationVector for training
        @param categories: dict of category --> list of values example {"Specie":["Homo Sapiens","Mormoops blainvillei"]}
        @raise Exception:
        """
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

    def addValue(self,category,value):
        if category in self.categories and not value in self.categories[category]:
            self.categories[category].append(value)


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


