from PyQt4.QtCore import QObject, pyqtSignal
import numpy as np
from utils.db.DB_ORM import Segment, DB, Measurement
from duetto.audio_signals import AudioSignal


class SegmentManager(QObject):
    """
    Manage the parameter measurement over a group of segments.
    Provide a table interface for segments parameter measurement and classification
    """

    # region SIGNALS

    # signal raised when the parameters of the segments change
    measurementsChanged = pyqtSignal()

    # signal raised when a parameter is measured on a segment
    # raise the segment index and the list of visual items associated
    segmentVisualItemAdded = pyqtSignal(int, list)

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

        # the db representation of the elements
        self.segments_db_objects = []
        self.db_session = DB().get_db_session()

        # the signal in which would be detected the elements
        self._signal = None

        # stores the measured parameters of the detected elements
        # has dimensions len(Elements) * len(_measurerList)
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
        self._elements = elements_list

        try:
            self.segments_db_objects = [Segment() for _ in self._elements]

            # add the new segments
            for s in self.segments_db_objects:
                self.db_session.add(s)

            self.db_session.commit()

        except Exception as ex:
            print("segment creation error" + ex.message)

        self.recompute_element_table()

    @property
    def measurer_adapters(self):
        return self._measurerList

    @measurer_adapters.setter
    def measurer_adapters(self, new_measurer_adapters):
        self._measurerList = new_measurer_adapters
        self.recompute_element_table()

    def recompute_element_table(self):
        """
        Recompute the shape of the elements parameter table
        when a change is made on the amount of elements or the amount of
        measured parameters
        :return:
        """
        # clear the parameters
        rows = len(self.elements)
        cols = len(self.measurer_adapters)

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
        return [x.get_instance().name for x in self.measurer_adapters]

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
        return len(self.measurer_adapters) + len(self.classificationColumnNames)

    # endregion

    # region Classification

    def segment_classification(self, segment_index):
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

        for i in indexes_list:
            if 0 <= i < self.rowCount:
                self.update_classification_visual_item(i, classification)
                self.classificationTableData[i] = classification
                self.add_identification_on_db(i, classification)

        self.db_session.commit()
        self.measurementsChanged.emit()

    def classify_elements(self):
        """
        Execute the classification for all the detected elements with the current classifier.
        :return:
        """
        # get the classification parameters and classifier
        classifier = self.classifier_adapter.get_instance()

        # get the classification parameters and method
        classifier = classifier if classifier is not None else self.classifier_adapter.get_instance()
        classifier.parameters = self.measurer_adapters

        # classify each element
        for i in xrange(len(self.elements)):
            # parameter adapter, value
            parameter_vector = [self.measuredParameters[i, j] for j, x in enumerate(self.measurer_adapters)]
            self._classify_element(element_index=i, classifier=classifier,
                                   parameter_vector=parameter_vector)

        self.db_session.commit()

        self.measurementsChanged.emit()

    def _classify_element(self, element_index, classifier=None, parameter_vector=None, commit_changes=False):
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
            [self.measuredParameters[element_index, j] for j in xrange(len(self.measurer_adapters))]

        classification_value = classifier.classify(self.elements[element_index], parameter_vector)
        self.classificationTableData[element_index] = classification_value

        # save on db
        self.add_identification_on_db(element_index, classification_value)

        # update visualization
        self.update_classification_visual_item(element_index, classification_value)

        if commit_changes:
            self.db_session.commit()

    def update_classification_visual_item(self, element_index, classification_value):
        """

        :param element_index:
        :param classification_value:
        :return:
        """
        # update the visualization
        self.update_elements_visual_items(self.classifier_adapter, element_index, classification_value)
        visual_item = self.classifier_adapter.get_visual_items()
        if visual_item:
            visual_item.set_data(self.signal, self.elements[element_index], classification_value)
            self.segmentVisualItemAdded.emit(element_index, visual_item)

    def update_elements_visual_items(self, adapter, element_index, value):
        """
        Method that raises the signal segmentVisualItemAdded
        with the according visual items founded for an specific
        detected element.
        :return:
        """
        visual_items = adapter.get_visual_items()
        if visual_items:
            for item in visual_items:
                item.set_data(self.signal, self.elements[element_index], value)

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

        self.measuredParameters = np.concatenate(
            (self.measuredParameters[:start_index],
             self.measuredParameters[end_index + 1:]))

        self.classificationTableData = self.classificationTableData[:start_index] +\
                                       self.classificationTableData[end_index + 1:]

        self._elements = self.elements[:start_index] + self.elements[end_index+1:]

        self.segments_db_objects = self.segments_db_objects[:start_index] + self.segments_db_objects[end_index + 1:]

        self.measurementsChanged.emit()

    def add_element(self, element, index):
        """
        Add a new element at index supplied. Execute the parameter measurement over it
        :param element:  the element to add
        :param index: the index to insert the element at
        :return:
        """
        if not 0 <= index < self.rowCount:
            raise IndexError()

        if self.rowCount == 0:
            # the property would update the other variables
            self.elements = [element]

        else:
            # add the element
            self.measuredParameters = np.concatenate((self.measuredParameters[:index],
                                                      np.array([np.zeros(len(self.measurer_adapters))]),
                                                      self.measuredParameters[index:]))

            self.classificationTableData.insert(index, None)
            self._classify_element(index, commit_changes=True)

            self.elements.insert(index, element)

            new_segment = Segment()
            self.db_session.add(new_segment)
            self.db_session.commit()

            self.segments_db_objects.insert(index, new_segment)

        # measure parameters
        self._measure(element, index, commit_changes=True)

        self.measurementsChanged.emit()

    def detect_elements(self):
        """
        Detect elements in the signal using the detector
        """

        detector = self.detector_adapter.get_instance(self.signal)

        detector.detectionProgressChanged.connect(lambda x: self.detectionProgressChanged.emit(x))

        import time
        t = time.time()

        detector.detect()
        print("Time consuming detecting " + str(len(detector.elements)) + " elements: " + str(time.time() - t))

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
        import time

        t = time.time()

        if len(self.measurer_adapters) == 0:
            return

        measure_methods = [parameter_adapter.get_instance() for parameter_adapter in self.measurer_adapters]
        orm_parameters_mappers = [parameter_adapter.get_db_orm_mapper() for parameter_adapter in self.measurer_adapters]

        for i in xrange(self.rowCount):
            self._measure(self.elements[i], i, measure_methods, orm_parameters_mappers)
            self.measureParametersProgressChanged.emit((i+1) * 100.0/self.rowCount)

        print("Time consuming measurement parameters: " + str(time.time() - t))

        self.db_session.commit()
        self.measurementsChanged.emit()
        self.measureParametersProgressChanged.emit(100)

    def _measure(self, element, index, measure_methods=None, orm_parameters_mappers=None, commit_changes=False):
        """
        Measure the list of parameters over the element supplied
        :param element: The element to measure
        :param index: The element index on the table of parameters
        :return:
        """
        if not 0 <= index < self.rowCount:
            raise IndexError()

        if measure_methods is None:
            measure_methods = [parameter_adapter.get_instance() for parameter_adapter in self.measurer_adapters]

        if orm_parameters_mappers is None:
            orm_parameters_mappers = [parameter_adapter.get_db_orm_mapper() for parameter_adapter in
                                      self.measurer_adapters]

        for j, parameter_adapter in enumerate(self.measurer_adapters):
            try:
                # compute the param with the interval_function
                self.measuredParameters[index, j] = measure_methods[j].measure(element)
                # raise the parameter visual item if any
                self.update_elements_visual_items(parameter_adapter, index, self.measuredParameters[index, j])

                # try to store the parameter measurement on db
                self.add_measurement_on_db(self.segments_db_objects[index],
                                           orm_parameters_mappers[j],
                                           self.measuredParameters[index, j])
            except Exception as e:
                # if some error is raised set a default value
                self.measuredParameters[index, j] = 0
                print("Error measure params " + e.message)

        if commit_changes:
            self.db_session.commit()

    # endregion

    # region DB interaction

    def add_measurement_on_db(self, segment, parameter, value):
        """
        adds to the db the measurement of a parameter over a segment.
        Must be called commit after to make persistent the changes
        :param segment:
        :param parameter:
        :param value:
        :return:
        """
        if segment is None or parameter is None:
            return

        try:
            self.db_session.add(Measurement(segment_id=segment.segment_id,
                                            parameter_id=parameter.parameter_id,
                                            value=value))

        except Exception as ex:
            print("db connexion error. Measurements. " + ex.message)
            self.db_session = DB().get_db_session(new_session=True)

    def add_identification_on_db(self, element_index, classification):
        """
        Adds the identification of a segment in the database.
        Must call commit after to make persistent the changes
        :param element_index:
        :param classification:
        :return:
        """
        if not 0 <= element_index < len(self.elements):
            raise Exception()
        try:
            if classification.specie:
                self.segments_db_objects[element_index].specie = classification.specie
            elif classification.genus:
                self.segments_db_objects[element_index].genus = classification.genus
            elif classification.family:
                self.segments_db_objects[element_index].family = classification.family

            self.db_session.add(self.segments_db_objects[element_index])

        except Exception as ex:
            print("db connexion error. Segments. " + ex.message)
            self.db_session = DB.get_session(new_session=True)

    # endregion

    def __getitem__(self, item):
        if not isinstance(item, tuple) or not len(item) == 2:
            raise Exception("Invalid Argument exception")

        row, col = item

        if row < 0 or row >= self.rowCount:
            raise IndexError()

        if col < len(self.measurer_adapters):
            return self.measuredParameters[row, col]

        # the order of the classification taxonomy may change
        classification = self.classificationTableData[row]
        if classification is None:
            return self.tr(u"No Identified")

        index = col - len(self.measurer_adapters)

        if index == 0 and classification.family is not None:
            return classification.family

        elif index == 1 and classification.genus is not None:
            return classification.genus

        # specie
        return self.tr(u"No Identified") if classification.specie is None else classification.specie