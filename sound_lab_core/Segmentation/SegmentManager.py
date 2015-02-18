from PyQt4.QtCore import QObject, pyqtSignal
import numpy as np
from duetto.audio_signals import AudioSignal
from sound_lab_core.Clasification.ClassificationData import ClassificationData


class SegmentManager(QObject):
    """
    Manage the parameter measurement over a group of segments.
    Provide a table interface for segments parameter measurement and classification
    """

    # region SIGNALS
    measurementsChanged = pyqtSignal()

    # signal raised when a parameter is measured on a segment
    # raise the segment index and the parameter visual item associated
    segmentParameterMeasured = pyqtSignal(int, object)

    # endregion

    def __init__(self):
        QObject.__init__(self)
        # the classifier object that would be used on segments classification
        self._classifier = None

        # the detector object that would be used on segments detection
        self._detector = None

        # the parameter measurer adapter list
        self._measurerList = []

        # the detected elements
        self._elements = []

        # the signal in which would be detected the elements
        self._signal = None

        # set the connections for the classification data to
        # update when is added, changed or deleted a value or category
        self.classificationData = ClassificationData()
        self.classificationData.valueAdded.connect(self.classificationCategoryValueAdded)
        self.classificationData.valueRemoved.connect(self.classificationCategoryValueRemove)
        self.classificationData.categoryAdded.connect(self.classificationCategoryAdded)

        # stores the measured parameters of the detected elements
        # has dimensions len(Elements) * len(_measurerList)
        self.measuredParameters = np.array([])

        # stores the classification data that are present in the table of meditions
        self.classificationTableData = self.classificationTableData = [[]]

    # region Properties

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements_list):
        self._elements = elements_list
        self.recompute_element_table()

    @property
    def measurerList(self):
        return self._measurerList

    @measurerList.setter
    def measurerList(self, new_measurerList):
        self._measurerList = new_measurerList
        self.recompute_element_table()

    def recompute_element_table(self):
        """
        Recompute the shape of the elements parameter table
        when a change is made on the amount of elements or the amount of
        measured parameters
        :return:
        """
        # clear the measurements
        rows = len(self.elements)
        cols = len(self.measurerList)

        self.measuredParameters = np.zeros(rows * cols).reshape((rows, cols))

        self.classificationTableData = [[self.tr(u"No Identified")
                                         for _ in self.classificationColumnNames]
                                        for _ in range(len(self._elements))]
        self.measurementsChanged.emit()

    @property
    def classificationColumnNames(self):
        """
        The names of the columns of classification data
        :return:
        """
        return [k for k in self.classificationData.categories if
                len(self.classificationData.getvalues(k)) > 0]
    
    @property
    def parameterColumnNames(self):
        """
        The names of the columns of parameters.
        :return:
        """
        return [x.get_instance().name for x in self.measurerList]

    @property
    def columnNames(self):
        return self.parameterColumnNames + self.classificationColumnNames

    @property
    def detector(self):
        return self._detector

    @detector.setter
    def detector(self, value):
        self._detector = value
        self._detector.signal = self.signal

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        """
        Modify and update the internal variables that uses the signal.

        :param new_signal: the new AudioSignal
        :raise Exception: If signal is not of type AudioSignal
        """
        if new_signal is None or not isinstance(new_signal, AudioSignal):
            raise Exception("Invalid assignation value. Must be of type AudioSignal")

        self._signal = new_signal

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    @property
    def rowCount(self):
        return len(self.elements)

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

        self.measurementsChanged.emit()

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

        self.classificationTableData = self.classificationTableData[:start_index] +\
                                       self.classificationTableData[end_index + 1:]

        self._elements = self.elements[:start_index] + self.elements[end_index+1:]

        self.measurementsChanged.emit()

    def addElement(self, element, index):
        """
        Add a new element at index supplied. Execute the parameter measurement over it
        :param element:  the element to add
        :param index: the index to insert the element at
        :return:
        """
        if not 0 <= index <= self.rowCount:
            raise IndexError()

        if self.rowCount == 0:
            # the property would update the other variables
            self.elements = [element]

        else:
            # add the element
            self.measuredParameters = np.concatenate((self.measuredParameters[:index],
                                                      np.array([np.zeros(len(self.measurerList))]),
                                                      self.measuredParameters[index:]))

            self.classificationTableData.insert(index, [self.tr(u"No Identified")
                                                        for _ in self.classificationColumnNames])

            self.elements.insert(index, element)

        # measure parameters
        self._measure(element, index)

        self.measurementsChanged.emit()

    def detectElements(self):
        """
        Detect elements in the signal using the parameters.
        """
        if self.detector is None:
            return
        self.detector.detect()

        self.elements = self.detector.elements

    # endregion

    # region Measurements

    def measureParameters(self):
        """
        :param tableParameterOscilogram:
        :param paramsTomeasure:
        :param elements:
        :return:
        """

        if len(self.measurerList) == 0:
            return

        for i in range(self.rowCount):
            self._measure(self.elements[i], i)

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

        for j, parameter_adapter in enumerate(self.measurerList):
            try:
                # compute the param with the function
                measure_method = parameter_adapter.get_instance()
                self.measuredParameters[index, j] = measure_method.measure(element)

                visual_item = parameter_adapter.get_visual_item()
                if visual_item:
                    visual_item.set_data(self.signal, self.elements[index], self.measuredParameters[index, j])

                self.segmentParameterMeasured.emit(index, visual_item)

            except Exception as e:
                # if some error is raised set a default value
                self.measuredParameters[index, j] = 0
                print("Error measure params " + e.message)


    # endregion

    def getData(self, row, col):
        # todo (yasel) implement as indexer
        if row < 0 or row >= self.rowCount:
            raise IndexError()

        if col < len(self.measurerList):
            return self.measuredParameters[row, col]

        return self.classificationTableData[row][col - len(self.measurerList)]