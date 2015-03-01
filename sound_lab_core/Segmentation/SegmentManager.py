from PyQt4.QtCore import QObject, pyqtSignal
import numpy as np
from duetto.audio_signals import AudioSignal


class SegmentManager(QObject):
    """
    Manage the parameter measurement over a group of segments.
    Provide a table interface for segments parameter measurement and classification
    """

    # region SIGNALS

    # signal raised when the measurements of the segments change
    measurementsChanged = pyqtSignal()

    # signal raised when a parameter is measured on a segment
    # raise the segment index and the visual item associated
    segmentVisualItemAdded = pyqtSignal(int, object)

    # signal raised while detection is been made. Raise the percent of detection progress.
    detectionProgressChanged = pyqtSignal(int)

    # signal raised while the parameters are being computed.
    # raise the percent of the parameter measuring process.
    measureParametersProgressChanged = pyqtSignal(int)

    # endregion

    def __init__(self):
        QObject.__init__(self)
        # the classifier object that would be used on segments classification
        self._classifier = None

        # the detector adapter object that would be used on segments detection
        self._detector = None

        # the parameter measurer adapter list
        self._measurerList = []

        # the detected elements
        self._elements = []

        # the signal in which would be detected the elements
        self._signal = None

        # stores the measured parameters of the detected elements
        # has dimensions len(Elements) * len(_measurerList)
        self.measuredParameters = np.array([])

        # stores the classification data that are present in the table of measurements
        # list of ClassificationData
        self.classificationTableData = []

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

        self.classificationTableData = [None for _ in self._elements]

        self.measurementsChanged.emit()

    @property
    def classificationColumnNames(self):
        """
        The names of the columns of classification data
        :return:
        """
        return [self.tr(u"Family"), self.tr(u"Genera"), self.tr(u"Specie")]
    
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
    def detector_adapter(self):
        return self._detector

    @detector_adapter.setter
    def detector_adapter(self, value):
        self._detector = value

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
    def classifier_adapter(self):
        return self._classifier

    @classifier_adapter.setter
    def classifier_adapter(self, classifier):
        self._classifier = classifier

    @property
    def rowCount(self):
        return len(self.elements)

    @property
    def columnCount(self):
        return len(self.measurerList) + len(self.classificationColumnNames)

    # endregion

    # region Classification

    def set_manual_elements_classification(self, indexes_list, classification):
        """
        Set the elements classification manually.
        :param indexes_list: the indexes of classified elements
        :param classification: the value for classification.
        the values are applied to all the elements that have indexes in indexes_list.
        :return:
        """
        indexes_list = [x for x in indexes_list if 0 <= x < self.rowCount]

        for i in indexes_list:
            self.update_classification_visual_item(i, classification)
            self.classificationTableData[i] = classification

        self.measurementsChanged.emit()

    def classify_elements(self):
        """
        Execute the classification for all the detected elements with the current classifier.
        :return:
        """
        # get the classification parameters and classifier
        classifier = self.classifier_adapter.get_instance()
        parameter_vector = self.get_parameter_measured_vector()

        # classify each element
        for i in xrange(len(self.elements)):
            self._classify_element(element_index=i, classifier=classifier,
                                   parameter_vector=parameter_vector)

        self.measurementsChanged.emit()

    def _classify_element(self, element_index, classifier=None, parameter_vector=None):
        """
        Helper method that classify a single element.
        :param element_index: The index of the element to classify
        :param classifier: the classifier instance if any (If None the classifier would be computed)
        :param parameter_vector: the vector of parameters to supply to the classifier
        (If None the vector would be computed)
        :return:
        """
        # get the classification parameters and method
        classifier = classifier if classifier is not None else self.classifier_adapter.get_instance()
        parameter_vector = parameter_vector if parameter_vector is not None else self.get_parameter_measured_vector()

        # classify
        classification_value = classifier.classify(self.elements[element_index], parameter_vector)
        self.classificationTableData[element_index] = classification_value

        self.update_classification_visual_item(element_index, classification_value)

    def update_classification_visual_item(self, element_index, classification_value):
        # update the visualization
        visual_item = self.classifier_adapter.get_visual_item()
        if visual_item:
            visual_item.set_data(self.signal, self.elements[element_index], classification_value)
            self.segmentVisualItemAdded.emit(element_index, visual_item)

    def get_parameter_measured_vector(self):
        """
        Method that compute the parameter of vectors that must be supplied to the
        classifiers to performs the classification process
        :return: the vector
        """
        return []

    # endregion

    # region Detection

    def delete_elements(self, start_index, end_index):
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

    def add_element(self, element, index):
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

            self.classificationTableData.insert(index, None)
            self._classify_element(index)

            self.elements.insert(index, element)

        # measure parameters
        self._measure(element, index)

        self.measurementsChanged.emit()

    def detect_elements(self):
        """
        Detect elements in the signal using the detector
        """

        detector = self.detector_adapter.get_instance(self.signal)

        detector.detectionProgressChanged.connect(lambda x: self.detectionProgressChanged.emit(x))

        detector.detect()

        self.elements = detector.elements

    # endregion

    # region Measurements

    def measure_parameters(self):
        """
        :param tableParameterOscilogram:
        :param paramsTomeasure:
        :param elements:
        :return:
        """

        self.measureParametersProgressChanged.emit(0)

        if len(self.measurerList) == 0:
            return

        for i in range(self.rowCount):
            self._measure(self.elements[i], i)
            self.measureParametersProgressChanged.emit(100.0/self.rowCount)

        self.measurementsChanged.emit()
        self.measureParametersProgressChanged.emit(100)

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

                # raise the parameter visual item if any
                visual_item = parameter_adapter.get_visual_item()
                if visual_item:
                    visual_item.set_data(self.signal, self.elements[index], self.measuredParameters[index, j])
                    self.segmentVisualItemAdded.emit(index, visual_item)

            except Exception as e:
                # if some error is raised set a default value
                self.measuredParameters[index, j] = 0
                print("Error measure params " + e.message)

    # endregion

    def __getitem__(self, item):
        if not isinstance(item, tuple) or not len(item) == 2:
            raise Exception("Invalid Argument exception")

        row, col = item

        if row < 0 or row >= self.rowCount:
            raise IndexError()

        if col < len(self.measurerList):
            return self.measuredParameters[row, col]

        # the order of the classification taxonomy may change
        classification = self.classificationTableData[row]
        if classification is None:
            return self.tr(u"No Identified")

        index = col - len(self.measurerList)

        if index == 0:
            # family
            return self.tr(u"No Identified") if classification.family is None else classification.family

        elif index == 1:
            # genera
            return self.tr(u"No Identified") if classification.genus is None else classification.genus

        # specie
        return self.tr(u"No Identified") if classification.specie is None else classification.specie