# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import Parameter,ParameterTree
from pyqtgraph.parametertree.parameterTypes import ListParameter
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.windows.ui_python_files.detectElementsDialog import Ui_Dialog
from Utils.Utils import smallSignal
from sound_lab_core.AdapterFactory import ParametersAdapterFactory, SegmentationAdapterFactory, ClassificationAdapterFactory
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
            self.widget.signal = smallSignal(signal)
            # else load a didactic signal

        self._detector = None
        self._classifier = None

        self._parameterAdapterFactory = ParametersAdapterFactory(self)
        self._segmentationAdapterFactory = SegmentationAdapterFactory(self)
        self._classificationAdapterFactory = ClassificationAdapterFactory(self)

        self.widget.visibleSpectrogram = False
        self.widget.visibleOscilogram = True

        # Parameter Tree Settings
        self.__createParameterTrees()

        self.detect()

    # region Parameter Tree Options

    # region  Factory Adapters
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

    def __createParameterTrees(self):
        """
        Create the ParameterTree with the options of the dialog.
        The ParameterTree contains the combo box of
        the active parameters measurements and to select.
        :return:
        """
        self.createSegmentation_ClassificationParameterTree()
        self.createParameterMeasurementParameterTree()
        self.configureParameterTreesLayout()

    def createSegmentation_ClassificationParameterTree(self):
        # set the segmentation and classification parameters
        segmentation_adapters = self.segmentationAdapterFactory.adapters_names()
        segmentation_adapters = [(self.tr(unicode(t)), t) for t in segmentation_adapters]

        classification_adapters = self.classificationAdapterFactory.adapters_names()
        classification_adapters = [(self.tr(unicode(t)), t) for t in classification_adapters]

        params = [
            {u'name': unicode(self.tr(u'Segmentation Method')),
             u'type': u'list',
             u'value': segmentation_adapters[0][1],
             u'default': segmentation_adapters[0][1],
             u'values': segmentation_adapters},

            {u'name': unicode(self.tr(u'Classification Method')),
             u'type': u'list',
             u'value': classification_adapters[0][1],
             u'default': classification_adapters[0][1],
             u'values': classification_adapters}
        ]

        ListParameter.itemClass = DuettoListParameterItem
        self.segmentation_classificationParamTree = Parameter.create(name=u'', type=u'group', children=params)

        # create and set initial properties
        self.segmentation_classification_paramTree = ParameterTree()
        self.segmentation_classification_paramTree.setAutoScroll(True)
        self.segmentation_classification_paramTree.setHeaderHidden(True)
        self.segmentation_classification_paramTree.setParameters(self.segmentation_classificationParamTree)

    def createParameterMeasurementParameterTree(self):
        # set the segmentation and classification parameters
        parameters_measurements_adapters = self.parameterAdapterFactory.adapters_names()
        parameters_measurements_adapters = [(self.tr(unicode(t)), t) for t in parameters_measurements_adapters]

        params = [
            {u'name': unicode(self.tr(u'Parameter Measurements')),
             u'type': u'group', u'children':
            [{u'name': p[1], u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'Measure')),
                  u'type': u'bool', u'default': False,
                  u'value': False}] + self.parameterAdapterFactory.get_adapter(p[1]).get_settings()
             } for p in parameters_measurements_adapters]
            }]

        ListParameter.itemClass = DuettoListParameterItem
        self.parameter_measurementParamTree = Parameter.create(name=u'', type=u'group', children=params)

        # create and set initial properties
        self.parameter_measurement_paramTree = ParameterTree()
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

    # endregion

    # endregion

    # region WorkSpace

    def load_workspace(self, workspace):
        """
        Method that loads the workspace to update visual options from main window.
        :param workspace:
        """
        self.widget.load_workspace(workspace)

    # endregion

    # region Detector, Parameter Measurers and Classifier

    @property
    def detector(self):
        """
        :return: The selected detector to perform segmentation
        """
        # create manually the detector
        self._detector = AbsDecayEnvelopeDetector(self.widget.signal, 1, -40, 2, 5, 6)
        return self._detector

    @detector.setter
    def detector(self, value):
        self._detector = value

    @property
    def measurerList(self):
        """
        :return: The list of selected parameters to measure
        """
        return []

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, value):
        self._classifier = value

    # endregion

    @pyqtSlot()
    def detect(self):
        """
        :return:
        """
        self.widget.detector = self.detector

        self.widget.detectElements()

        self.widget.graph()