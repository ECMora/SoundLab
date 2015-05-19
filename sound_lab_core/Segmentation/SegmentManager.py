from PyQt4.QtCore import QObject, pyqtSignal
import numpy as np
from duetto.audio_signals import AudioSignal

from sound_lab_core.Segmentation.Adapters import ManualDetectorAdapter
from sound_lab_core.Clasification.Adapters import ManualClassifierAdapter
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement
from utils.Utils import SegmentationThread, MeasurementThread


class SegmentManager(QObject):
    """
    Manage the parameter measurement ad classification over a group of segments.
    Provide a table interface for segments parameter measurement and classification.
    Allow to save on db the measurements made on segments.
    """

    # region SIGNALS

    # signal raised when the parameters of the segments change
    measurementsChanged = pyqtSignal()

    # signal raised when a parameter is measured on a segment
    # raise the segment index and the list of visual items associated
    segmentVisualItemAdded = pyqtSignal(int, list)

    # signal raised when the segmentation has finished
    segmentationFinished = pyqtSignal()

    # signal raised when the measurement of parameteers and classification has finished
    measurementsFinished = pyqtSignal()

    # signal raised while detection is been made. Raise the percent of detection progress.
    detectionProgressChanged = pyqtSignal(int)

    # endregion

    def __init__(self):
        QObject.__init__(self)
        # the classifier object that would be used on segments classification
        self._classifier = None

        # the detector adapter object that would be used on segments detection
        self._detector = None

        # the parameter measurer list
        self._measurerList = []

        # the detected elements
        self._elements = []

        # the segmentation_thread to perform the segmentation with
        self.segmentation_thread = SegmentationThread(parent=None)
        self.segmentation_thread.finished.connect(self._get_elements)

        # the thread to perform the measurements with
        self.measurement_thread = MeasurementThread(segment_manager=self)
        self.measurement_thread.finished.connect(self._get_measurements)

        # the signal in which would be detected the elements
        self._signal = None

        # stores the measured parameters of the detected elements
        # has dimensions len(elements) * len(measurerList)
        self.measuredParameters = np.array([])

        # stores the classification data that are present in the table of parameters
        # list of ClassificationData
        self.classificationTableData = []

    # region Properties

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements_list):
        """
        :param elements_list: Accepts a list of One dimensional elements or a list of tuples
        :return:
        """
        self._elements = elements_list

        self.recompute_element_table()

    @property
    def parameters(self):
        return self._measurerList

    @parameters.setter
    def parameters(self, new_parameter_measurers):
        self._measurerList = new_parameter_measurers
        self.recompute_element_table()

    def recompute_element_table(self):
        """
        Recompute the shape of the elements parameter table
        when a change is made on the amount of elements or the amount of
        measured parameters
        :return:
        """
        # clear the parameters
        rows, cols = len(self.elements), len(self.parameters)

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
        return [x.getName() for x in self.parameters]

    @property
    def columnNames(self):
        return self.parameterColumnNames + self.classificationColumnNames

    @property
    def detector_adapter(self):
        return self._detector if self._detector is not None else ManualDetectorAdapter()

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
        return self._classifier if self._classifier is not None else ManualClassifierAdapter()

    @classifier_adapter.setter
    def classifier_adapter(self, classifier):
        self._classifier = classifier

    @property
    def rowCount(self):
        return len(self.elements)

    @property
    def columnCount(self):
        return len(self.parameters) + len(self.classificationColumnNames)

    # endregion

    # region Classification

    def get_segment_classification(self, segment_index):
        """
        Returns the classification value of the segment at index segment_index
        :param segment_index: the index of the segment to ask for classification value
        :return:
        """
        if not 0 <= segment_index < len(self.elements):
            raise Exception("Index out of range")

        return self.classificationTableData[segment_index]

    def set_manual_elements_classification(self, indexes_list, classification):
        """
        Set the elements classification manually.
        :param indexes_list: the indexes of classified elements
        :param classification: the value for classification Data.
        the values are applied to all the elements that have indexes in indexes_list.
        :return:
        """
        indexes_list = [index for index in indexes_list if 0 <= index < self.rowCount]

        for i in indexes_list:
            self.update_elements_visual_items(self.classifier_adapter, i, classification)
            self.classificationTableData[i] = classification

        self.measurementsChanged.emit()

    def classify_elements(self):
        """
        Execute the automatic classification for all the detected
        elements with the current selected classifier.
        :return:
        """
        # get the classification parameters and classifier
        classifier = self.classifier_adapter.get_instance()

        classifier.parameters = self.parameters

        # classify each element
        for i in xrange(len(self.elements)):
            #                                     parameter adapter, value
            parameter_vector = [self.measuredParameters[i, j] for j, x in enumerate(self.parameters)]
            self._classify_element(element_index=i, classifier=classifier, parameter_vector=parameter_vector)

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
        classifier = classifier if classifier is not None else self.classifier_adapter.get_instance()

        parameter_vector = parameter_vector if parameter_vector is not None else \
            [self.measuredParameters[element_index, j] for j in xrange(len(self.parameters))]

        classification_value = classifier.classify(self.elements[element_index], parameter_vector)

        self.classificationTableData[element_index] = classification_value

        # update visualization
        self.update_elements_visual_items(self.classifier_adapter, element_index, classification_value)

    def update_elements_visual_items(self, parameter, element_index, value):
        """
        Method that raises the signal segmentVisualItemAdded
        with the according visual items founded for an specific
        detected element.
        :return:
        """
        visual_items = parameter.get_visual_items()
        if not visual_items:
            return

        for item in visual_items:
            item.set_data(self.  signal, self.elements[element_index], value)

        self.segmentVisualItemAdded.emit(element_index, visual_items)

    # endregion

    # region Detection

    def delete_elements(self, start_index, end_index):
        """
        Removes elements from the detected
        :param start_index: start index of removed elements
        :param end_index: end index of removed elements
        :return:
        """

        self.measuredParameters = np.concatenate((self.measuredParameters[:start_index],
                                                  self.measuredParameters[end_index + 1:]))

        self.classificationTableData = self.classificationTableData[:start_index] +\
                                       self.classificationTableData[end_index + 1:]

        self._elements = self.elements[:start_index] + self.elements[end_index+1:]

        self.measurementsChanged.emit()

    def add_element(self, index, index_from, index_to):
        """
        Add a new element at index supplied. Execute the parameter measurement over it
        :type index_from: the start index of the new element in signal data values
        :type index_to: the end index of the new element in signal data values
        :param element:  the element to add
        :param index: the index to insert the element at
        :return:
        """
        # index could be equal to rowCount if insert after all previous elements
        if not 0 <= index <= self.rowCount:
            raise IndexError()

        element = OneDimensionalElement(self.signal, index_from, index_to)

        if self.rowCount == 0:
            # the property would update the other variables
            self.elements = [element]

        else:
            # add the element
            self.classificationTableData.insert(index, None)
            self._elements.insert(index, element)
            self.measuredParameters = np.concatenate((self.measuredParameters[:index],
                                                      np.array([np.zeros(len(self.parameters))]),
                                                      self.measuredParameters[index:]))
        # measure parameters
        self._measure(element, index, raise_visual_items=True)
        self._classify_element(index)

        self.measurementsChanged.emit()

    def detect_elements(self):
        """
        Detect elements in the signal using the detector
        """
        if self.segmentation_thread.isRunning():
            return

        detector = self.detector_adapter.get_instance(self.signal)
        detector.detectionProgressChanged.connect(lambda x: self.detectionProgressChanged.emit(x))

        self.segmentation_thread.detector = detector
        self.segmentation_thread.start()

    def _get_elements(self):
        """
        update the elements when the segmentation thread finish
        :return:
        """
        self.elements = self.segmentation_thread.detector.elements
        self.segmentationFinished.emit()

    # endregion

    # region Measurements

    def measure_parameters_and_classify(self):
        """
        Measure the parameters over the detected elements and
        performs the classification of them
        :return:
        """
        if not self.measurement_thread.isRunning():
            self.measurement_thread.start()

    def _get_measurements(self):
        """
        Callback that is called when measurement thread finish.
        Raises the visual items for segments and emit the finish measurements signal
        """
        # update visual items of segments measurements
        for i in xrange(self.rowCount):
            for j, parameter_adapter in enumerate(self.parameters):
                self.update_elements_visual_items(parameter_adapter, i, self.measuredParameters[i, j])

        self.measurementsFinished.emit()
        self.measurementsChanged.emit()

    def measure_parameters(self):
        """
        :param tableParameterOscilogram:
        :param paramsTomeasure:
        :param elements:
        :return:
        """
        if len(self.parameters) == 0:
            return

        for i in xrange(self.rowCount):
            self._measure(self.elements[i], i)

    def _measure(self, element, index, measure_methods=None, raise_visual_items=False):
        """
        Measure the list of parameters over the element supplied
        :param update_visual_items_and_db: True if the visual items of measurements and the db session
        would be updated False otherwise. Efficiency improvement
        :param element: The element to measure
        :param index: The element index on the table of parameters
        :return:
        """

        if not 0 <= index < self.rowCount:
            raise IndexError()

        if measure_methods is None:
            measure_methods = self.parameters

        for j, parameter_adapter in enumerate(self.parameters):
            try:
                # measure param
                self.measuredParameters[index, j] = measure_methods[j].measure(element)

                # raise the parameter visual item if any
                if raise_visual_items:
                    self.update_elements_visual_items(parameter_adapter, index, self.measuredParameters[index, j])

            except Exception as e:
                # if some error is raised set a default value
                self.measuredParameters[index, j] = measure_methods[j].default_value
                print("Error measure params " + e.message)

    # endregion

    def save_data_on_db(self):
        """
        Save on db the data of detected segments, measurements and classification made.
        :return:
        """
        pass

    def __getitem__(self, item):
        if not isinstance(item, tuple) or not len(item) == 2:
            raise Exception("Invalid Argument exception")

        row, col = item

        if row < 0 or row >= self.rowCount:
            raise IndexError()

        if col < len(self.parameters):
            return self.measuredParameters[row, col]

        # the order of the classification taxonomy may change
        classification = self.classificationTableData[row]
        if classification is None:
            return self.tr(u"No Identified")

        index = col - len(self.parameters)

        if index == 0 and classification.family is not None:
            return classification.family

        elif index == 1 and classification.genus is not None:
            return classification.genus

        # specie
        return self.tr(u"No Identified") if classification.specie is None else classification.specie