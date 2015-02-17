# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree.parameterTypes import ListParameter
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.windows.ui_python_files.detectElementsDialog import Ui_Dialog
from Utils.Utils import small_signal
from sound_lab_core.AdapterFactory import ParametersAdapterFactory, SegmentationAdapterFactory, \
    ClassificationAdapterFactory
from sound_lab_core.Segmentation.Detectors.OneDimensional.EnvelopeMethods.AbsDecayEnvelopeDetector import \
    AbsDecayEnvelopeDetector


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    """
    Dialog that allow to the user to select
    the segmentation, parameter measurement and classification
    type that would be used on the process of a segment.
    Factory of detectors, parameter measurers and classifiers
    """

    # region Initialize

    def __init__(self, parent, signal=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        if signal is not None:
            self.widget.signal = small_signal(signal)
            # else load a didactic signal

        self._detector = None
        self._classifier = None

        self._parameterAdapterFactory = ParametersAdapterFactory(self)
        self._segmentationAdapterFactory = SegmentationAdapterFactory(self)
        self._classificationAdapterFactory = ClassificationAdapterFactory(self)

        self.parameter_measurement_paramTree = ParameterTree()
        self.parameter_measurementParamTree = None

        self.segmentation_classification_paramTree = ParameterTree()
        self.segmentation_classificationParamTree = None

        self.widget.visibleSpectrogram = False
        self.widget.visibleOscilogram = True

        # Parameter Tree Settings
        self.__createParameterTrees()

        self.detect()

    def __createParameterTrees(self):
        """
        Create the ParameterTree with the options of the dialog.
        The ParameterTree contains the combo box of
        the active parameters measurements and to select.
        :return:
        """
        self.createSegmentation_ClassificationParameterTree()
        self.createMeasurementParameterTree()
        self.configureParameterTreesLayout()

    def createSegmentation_ClassificationParameterTree(self):
        # set the segmentation and classification parameters
        segmentation_adapters = self.segmentationAdapterFactory.adapters_names()
        segmentation_adapters = [(self.tr(unicode(t)), t) for t in segmentation_adapters]

        classification_adapters = self.classificationAdapterFactory.adapters_names()
        classification_adapters = [(self.tr(unicode(t)), t) for t in classification_adapters]

        params = [
            {u'name': unicode(self.tr(u'Segmentation')),
             u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'Method')),
                  u'type': u'list',
                  u'value': segmentation_adapters[0][1],
                  u'default': segmentation_adapters[0][1],
                  u'values': segmentation_adapters}],
             u'expanded': False
            },
            {u'name': unicode(self.tr(u'Classification')),
             u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'Method')),
                  u'type': u'list',
                  u'values': classification_adapters}],
             u'expanded': False
            }]

        ListParameter.itemClass = DuettoListParameterItem
        self.segmentation_classificationParamTree = Parameter.create(
            name=unicode(self.tr(u'Segmentation-Classification')), type=u'group', children=params)

        self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))). \
            param(unicode(self.tr(u'Method'))).sigValueChanged.connect(self.segmentationChanged)

        self.segmentation_classificationParamTree.param(unicode(self.tr(u'Classification'))). \
            param(unicode(self.tr(u'Method'))).sigValueChanged.connect(self.segmentationChanged)

        # create and set initial properties
        self.segmentation_classification_paramTree.setAutoScroll(True)
        self.segmentation_classification_paramTree.setHeaderHidden(True)
        self.segmentation_classification_paramTree.setParameters(self.segmentation_classificationParamTree)

    def createMeasurementParameterTree(self):
        # set the segmentation and classification parameters
        ListParameter.itemClass = DuettoListParameterItem
        self.parameter_measurementParamTree = Parameter.create(name=unicode(self.tr(u'Parameter Measurements')),
                                                               type=u'group')
        for p in self.parameterAdapterFactory.adapters_names():
            group = Parameter.create(name=unicode(self.tr(unicode(p))),
                                     type=u'group', expanded=False)

            measure = Parameter.create(name=unicode(self.tr(u'Measure')), type=u'bool', default=False,
                                       value=False)
            group.addChild(measure)

            param_settings = self.parameterAdapterFactory.get_adapter(p).get_settings()

            if param_settings is not None:
                group.addChild(param_settings)

            self.parameter_measurementParamTree.addChild(group)

        self.parameter_measurement_paramTree.setAutoScroll(True)
        self.parameter_measurement_paramTree.setHeaderHidden(True)
        self.parameter_measurement_paramTree.setParameters(self.parameter_measurementParamTree)

    def configureParameterTreesLayout(self):
        """
        Configure the layout of the parameter trees of segmentation,
        classification methods and parameter measurement.
        :return:
        """
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.segmentation_classification_paramTree)
        self.segmentation_classification_settings.setLayout(layout)

        layout2 = QtGui.QVBoxLayout()
        layout2.setMargin(0)
        layout2.addWidget(self.parameter_measurement_paramTree)
        self.parameter_measurement_settings.setLayout(layout2)

    def segmentationChanged(self, parameter):
        """
        :param parameter:
        :return:
        """
        try:
            parameter.clearChildren()

            adapter = self.segmentationAdapterFactory.get_adapter(parameter.value())

            method_settings = adapter.get_settings()
            if method_settings:
                parameter.addChild(method_settings)

        except Exception as ex:
            print("Error getting the segmentation settings. " + ex.message)

    # endregion

    # region WorkSpace

    def load_workspace(self, workspace):
        """
        Method that loads the workspace to update visual options from main window.
        :param workspace:
        """
        self.widget.load_workspace(workspace)

    # endregion

    # region  Factory Adapters Properties
    @property
    def parameterAdapterFactory(self):
        return self._parameterAdapterFactory

    @property
    def segmentationAdapterFactory(self):
        return self._segmentationAdapterFactory

    @property
    def classificationAdapterFactory(self):
        return self._classificationAdapterFactory

    # endregion

    # region Detector, Parameter Measurers and Classifier

    @property
    def detector(self):
        """
        :return: The selected detector to perform segmentation
        """
        # create manually the detector
        detector_instance = None
        try:
            detector_name = self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))). \
                param(unicode(self.tr(u'Method'))).value()

            adapter = self.segmentationAdapterFactory.get_adapter(detector_name)

            detector_instance = adapter.get_instance()

        except Exception as e:
            print("Fail to get the detector instance. " + e.message)
            detector_instance = None

        self._detector = detector_instance if detector_instance is not None else AbsDecayEnvelopeDetector(
            self.widget.signal, 1, -40, 2, 5, 6)

        self._detector.signal = self.widget.signal

        return self._detector

    @detector.setter
    def detector(self, value):
        self._detector = value

    def get_measurer_list(self):
        """
        :return: The list of selected parameters to measure
        """
        parameters_list = self.parameter_measurementParamTree.children()

        # get just the parameter selected by user to be measured
        parameters_adapters_list = [self.parameterAdapterFactory.get_adapter(x.name()) for x in parameters_list
                                    if x.param(unicode(self.tr(u'Measure'))).value()]

        return [p.get_instance() for p in parameters_adapters_list]

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, value):
        self._classifier = value

    # endregion

    def detect(self):
        """
        :return:
        """
        self.widget.elements = self.detector.detect()

        self.widget.graph()