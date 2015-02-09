from PyQt4.QtCore import QObject, pyqtSignal
import numpy as np
from sound_lab_core.Clasification.ClassificationData import ClassificationData


class SegmentManager(QObject):
    """
    Manage the parameter measurement over a group of segments.
    Provide a table interface for segments parameter measurement and classification
    """

    # region SIGNALS
    measurementsChanged = pyqtSignal()
    # endregion

    def __init__(self):
        QObject.__init__(self)
        # the classifier object that would be used on segments classification
        self._classifier = None

        # the parameter measurer list
        self._measurerList = [[unicode(self.tr(u"Start(s)")), lambda x, d: x.startTime(),[]]]

        # set the connections for the classification data to
        # update when is added, changed or deleted a value or category
        self.classificationData = ClassificationData()
        self.classificationData.valueAdded.connect(self.classificationCategoryValueAdded)
        self.classificationData.valueRemoved.connect(self.classificationCategoryValueRemove)
        self.classificationData.categoryAdded.connect(self.classificationCategoryAdded)

        # stores the measured parameters of the detected elements
        # has dimensions len(Elements) * len(_measurerList)
        self.measuredParameters = np.array([[], []])

        # stores the classification data that are present in the table of meditions
        self.classificationTableData = self.classificationTableData = [[self.tr(u"No Identified")
                                                                        for _ in self.classificationColumnNames]
                                                                       for _ in range(self.rowCount)]

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

    @property
    def columnNames(self):
        return self.parameterColumnNames + self.classificationColumnNames
    
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

    @property
    def rowCount(self):
        return len(self.measuredParameters)

    @property
    def columnCount(self):
        return len(self.measurerList) + len(self.classificationColumnNames)

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
        indexes_list = [x for x in indexes_list if 0 <= x < self.rowCount]

        for i in indexes_list:
            for column, category in enumerate(self.classificationColumnNames):
                if category in dictionary:
                    self.classificationTableData[i][column] = dictionary[category]

        self.measurementsChanged.emit()

    def classificationCategoryValueAdded(self, category, value):
        # print("In Category "+category+" was added the value: "+value)
        pass

    def classificationCategoryValueRemove(self, category, value):
        for i, elem in enumerate(self.classificationTableData):
            for j, l in enumerate(elem):
                if l[0] == category and l[1] == value:
                    self.classificationTableData[i][j] = self.tr(u"No Identified")

    def classificationCategoryAdded(self, category):
        for i, elem in enumerate(self.classificationTableData):
            self.classificationTableData[i].append(self.tr(u"No Identified"))

        if self.rowCount > 0:
            for row in range(self.rowCount):
                pass

    # endregion

    # region Add-Delete Elements

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

        self.classificationTableData = self.classificationTableData[:start_index] + \
                                              self.classificationTableData[end_index + 1:]

        print(self.measuredParameters, self.classificationTableData)
        self.measurementsChanged.emit()

    def addElement(self, element, index):
        """
        Add a new element at index supplied. Execute the parameter measuremetn over it
        :param element:  the element to add
        :param index: the index to insert the element at
        :return:
        """
        if not 0 <= index <= self.rowCount:
            raise IndexError()

        # add the element
        self.measuredParameters = np.concatenate((self.measuredParameters[:index],
                                                  np.array([np.zeros(len(self.measurerList))]),
                                                  self.measuredParameters[index:]))

        self.classificationTableData.insert(index, [self.tr(u"No Identified")
                                                    for _ in self.classificationColumnNames])
        # measure parameters
        self._measure(element, index)

        self.measurementsChanged.emit()

    # endregion

    # region Measurements

    def measureParameters(self, elements):
        """
        :param tableParameterOscilogram:
        :param paramsTomeasure:
        :param elements:
        :return:
        """

        self.measuredParameters = np.zeros(len(elements) * len(self.measurerList)).reshape(
            (len(elements), len(self.measurerList)))

        self.classificationTableData = [[self.tr(u"No Identified")
                                                for _ in self.classificationColumnNames]
                                                for _ in range(self.rowCount)]

        for i in range(self.rowCount):
            self._measure(elements[i], i)

        self.measurementsChanged.emit()

    def _measure(self, element, index):
        """
        Measure the list of parameters over the element supplied
        :param element: The element to measure
        :param index: The element index on the table of measurements
        :return:
        """
        if not 0 <= index < self.rowCount:
            raise IndexError()

        for j, params in enumerate(self.measurerList):
            try:
                # get the function params.
                # params[0] is the name of the param measured
                # params[1] is the function to measure the param
                # params[2] is the dictionary of params supplied to the function
                dictionary = dict(params[2] if params[2] is not None else [])

                # compute the param with the function
                self.measuredParameters[index, j] = params[1](element, dictionary)

            except Exception as e:
                # if some error is raised set a default value
                self.measuredParameters[index, j] = 0
                print("Error measure params " + e.message)

    # endregion

    def getData(self, row, col):
        """
        """
        if row < 0 or row >= self.rowCount:
            raise IndexError()

        if col < len(self.measuredParameters[row]):
            return self.measuredParameters[row, col]

        return self.classificationTableData[row][col - len(self.measuredParameters[row])]