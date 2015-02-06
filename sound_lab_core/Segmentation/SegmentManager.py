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
        self.measuredParameters = np.array([[], []])

        # set the connections for the classification data to
        # update when is added, changed or deleted a value or category
        self.classificationData = ClassificationData()
        self.classificationData.valueAdded.connect(self.classificationCategoryValueAdded)
        self.classificationData.valueRemoved.connect(self.classificationCategoryValueRemove)
        self.classificationData.categoryAdded.connect(self.classificationCategoryAdded)

        # stores the classification data that are present in the table of meditions
        # has the form of a list with [["category name","category value"]] for each element
        # example with 2 elements and 2 categories
        # [[["Specie","Cartacuba"],["Location","Cuba"]],
        # [["Specie","Sinsonte"],["Location","Camaguey"]]]
        self.elementsClasificationTableData = []

        # the names of the columns in the table of parameters measured
        self.columnNames = []

    def updateClassifTableData(self):
        """
        temporal method to factorice
        """
        self.elementsClasificationTableData = [[[k, self.tr(u"No Identified")] for k in self.validcategories()]
                                                              for _ in range(self.rowCount())]

    def validcategories(self):
        return [k for k in self.classificationData.categories.keys() if
                len(self.classificationData.getvalues(k)) > 0]

    def rowCount(self):
        return len(self.measuredParameters)

    def columnCount(self):
        return len(self.columnNames) + len(self.validcategories())

    def getData(self, row, col):
        """
        """
        if row >= len(self.measuredParameters):
            raise IndexError()

        return self.measuredParameters[row, col]

    # region Properties

    # region Classifier

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    # endregion

    # region Measurer

    @property
    def measurerList(self):
        return self._measurer

    @measurerList.setter
    def measurerList(self, new_measurer):
        self._measurer = new_measurer

    # endregion

    # endregion

    # region Classification
    def classificationCategoryValueAdded(self, category, value):
        # print("In Category "+category+" was added the value: "+value)
        pass

    def classificationCategoryValueRemove(self, category, value):
        # print("In Category "+category+" was removed the value: " + value)
        for i, elem in enumerate(self.elementsClasificationTableData):
            for j, l in enumerate(elem):
                if l[0] == category and l[1] == value:
                    self.elementsClasificationTableData[i][j][1] = self.tr(u"No Identified")
                    # item = QtGui.QTableWidgetItem(unicode(self.elementsClasificationTableData[i][j][1]))
                    # item.setBackgroundColor(
                    #     self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                    # tableParameterOscilogram.setItem(i, len(self.measuredParameters[i]) + j, item)

    def classificationCategoryAdded(self, category):
        for i, elem in enumerate(self.elementsClasificationTableData):
            self.elementsClasificationTableData[i].append([str(category), self.tr(u"No Identified")])

        if self.rowCount() > 0:
            # tableParameterOscilogram.insertColumn(tableParameterOscilogram.columnCount())
            # column = tableParameterOscilogram.columnCount() - 1
            # put rows in table
            for row in range(self.rowCount()):
                pass
                # item = QtGui.QTableWidgetItem(unicode(self.tr(u"No Identified")))
                # item.setBackgroundColor(
                #     self.TABLE_ROW_COLOR_ODD if row % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                # tableParameterOscilogram.setItem(row, column, item)
                # tableParameterOscilogram.setHorizontalHeaderItem(column, QtGui.QTableWidgetItem(category))
            # insert data in clasification Data

    # endregion

    def addSegment(self, segment):
        """
        Add a new segment to the list of detected elements on the
        manager. if a parameter measurer is selected
        """
        pass

    def measureParameters(self, elements):
        """
        :param tableParameterOscilogram:
        :param paramsTomeasure:
        :param elements:
        :return:
        """
        self.measuredParameters = np.zeros(len(elements) * len(self.measurerList)).reshape(
            (len(elements), self.measurerList))

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
