from PyQt4.QtCore import QObject
import numpy as np
from sound_lab_core.Clasification.ClassificationData import ClassificationData


class SegmentManager(QObject):
    """
    Manage the parameter measurement over a group of segments.
    Provide a table interface for segments parameter measurement and classification
    """

    def __init__(self):
        QObject.__init__(self)
        # the classifier object that would be used on segments classification
        self._classifier = None

        # the parameter measurer list
        self._measurerList = None

        # stores the measured parameters of the detected elements
        # has dimensions len(Elements)*len(_measurerList)
        self.measuredParameters = np.array([[], []])

        # set the connections for the classification data to
        # update when is added, changed or deleted a value or category
        self.classificationData = ClassificationData()
        self.classificationData.valueAdded.connect(self.classificationCategoryValueAdded)
        self.classificationData.valueRemoved.connect(self.classificationCategoryValueRemove)
        self.classificationData.categoryAdded.connect(self.classificationCategoryAdded)

        # stores the classification data that are present in the table of meditions
        self.elementsClasificationTableData = []

    # region Properties

    @property
    def classificationColumnNames(self):
        """
        The names of the columns of classification data
        :return:
        """
        return [k for k in self.classificationData.categories.keys() if
                len(self.classificationData.getvalues(k)) > 0]
    
    @property
    def parameterColumnNames(self):
        """
        The names of the columns of parameters.
        :return:
        """
        return [x[0] for x in self.measurerList]
    
    # region Classifier

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    # endregion

    # region Measurer List

    @property
    def measurerList(self):
        return self._measurerList

    @measurerList.setter
    def measurerList(self, new_measurerList):
        self._measurerList = new_measurerList

    # endregion

    # endregion

    # region Classification

    def classifyElements(self, indexes_list, dictionary):
        """
        Set the elements classification manually.
        :param indexes_list: the indexes of classified elements
        :param dictionary: the dict with the values for each category of classification
        the values ae applied to all the elements that have indexes in indexes_list
        :return:
        """
        for i in indexes_list:
            if not 0 <= i < self.rowCount():
                continue

            for column, category in enumerate(self.classificationColumnNames):
                if category in dictionary:
                    self.elementsClasificationTableData[i][column] = dictionary[category]

    def classificationCategoryValueAdded(self, category, value):
        # print("In Category "+category+" was added the value: "+value)
        pass

    def classificationCategoryValueRemove(self, category, value):
        # print("In Category "+category+" was removed the value: " + value)
        for i, elem in enumerate(self.elementsClasificationTableData):
            for j, l in enumerate(elem):
                if l[0] == category and l[1] == value:
                    self.elementsClasificationTableData[i][j] = self.tr(u"No Identified")

    def classificationCategoryAdded(self, category):
        for i, elem in enumerate(self.elementsClasificationTableData):
            self.elementsClasificationTableData[i].append(self.tr(u"No Identified"))

        if self.rowCount() > 0:
            for row in range(self.rowCount()):
                pass

    # endregion

    def rowCount(self):
        return len(self.measuredParameters)

    def columnCount(self):
        return len(self.measurerList) + len(self.classificationColumnNames)

    def getData(self, row, col):
        """
        """
        if row < 0 or row >= len(self.measuredParameters):
            raise IndexError()

        if col < len(self.measuredParameters[row]):
            return self.measuredParameters[row, col]

        return self.elementsClasificationTableData[row][col - len(self.measuredParameters[row])]

    def deleteElements(self, start_index, end_index):
        """
        Removes elements from the detected
        :param start_index: start index of removed elements
        :param end_index: end index of removed elements
        :return:
        """

        self.measuredParameters = np.concatenate(
            (self.measuredParameters[:start_index],
             self.measuredParameters[end_index + 1:]))

        self.elementsClasificationTableData = self.elementsClasificationTableData[:start_index] + \
                                              self.elementsClasificationTableData[end_index + 1:]

    def measureParameters(self, elements):
        """
        :param tableParameterOscilogram:
        :param paramsTomeasure:
        :param elements:
        :return:
        """

        self.measuredParameters = np.zeros(len(elements) * len(self.measurerList)).reshape(
            (len(elements), len(self.measurerList)))

        self.elementsClasificationTableData = [[self.tr(u"No Identified")
                                                for _ in self.classificationColumnNames]
                                                for _ in range(self.rowCount())]

        for i in range(self.rowCount()):
            for j, params in enumerate(self.measurerList):
                try:
                    # get the function params.
                    # params[0] is the name of the param measured
                    # params[1] is the function to measure the param
                    # params[2] is the dictionary of params supplied to the function
                    dictionary = dict(params[2] if params[2] is not None else [])

                    # compute the param with the function
                    self.measuredParameters[i, j] = params[1](elements[i], dictionary)

                except Exception as e:
                    # if some error is raised set a default value
                    self.measuredParameters[i, j] = 0
                    print("Error measure params " + e.message)
