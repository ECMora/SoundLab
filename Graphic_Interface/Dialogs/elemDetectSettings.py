# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import Parameter, ParameterTree
from graphic_interface.windows.ui_python_files.detectElementsDialog import Ui_Dialog
from Utils.Utils import small_signal
from sound_lab_core.AdapterFactory import *
from sound_lab_core.Segmentation.Detectors.ManualDetector import ManualDetector


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

        # Parameter Tree Settings
        self.blockSignals = False
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
        classification_adapters = [(self.tr(t), t) for t in classification_adapters]
        list_param = [{u'name': unicode(x[1]),
                       u'type': u'bool',
                       u'value': False, u'default': False} for x in segmentation_adapters]

        list_param.append({u'name': unicode(self.tr(u'Method Settings')),
                          u'type': u'group', u'children':[]})
        params = [
            {u'name': unicode(self.tr(u'Segmentation')),
             u'type': u'group', u'children': list_param},
            {u'name': unicode(self.tr(u'Classification')),
             u'type': u'group', u'expanded': False, u'children':
                [{u'name': unicode(self.tr(u'Method')),
                  u'type': u'list',
                  u'values': classification_adapters}]
            }]

        self.segmentation_classificationParamTree = Parameter.create(
            name=unicode(self.tr(u'Segmentation-Classification')), type=u'group', children=params)

        self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))). \
            sigTreeStateChanged.connect(self.segmentationChanged)

        # create and set initial properties
        self.segmentation_classification_paramTree.setAutoScroll(True)
        self.segmentation_classification_paramTree.setHeaderHidden(True)
        self.segmentation_classification_paramTree.setParameters(self.segmentation_classificationParamTree)

    def createMeasurementParameterTree(self):
        # set the segmentation and classification parameters
        self.parameter_measurementParamTree = Parameter.create(name=unicode(self.tr(u'Parameter Measurements')),
                                                               type=u'group')
        for parameter_group in self.parameterAdapterFactory.parameter_groups:
            parameter_group_tree = Parameter.create(name=unicode(self.tr(unicode(parameter_group.name))),
                                               type=u'group', expanded=False)

            for adapter_name in parameter_group.adapters_names():
                group = Parameter.create(name=unicode(self.tr(unicode(adapter_name))),
                                         type=u'group', expanded=False)

                measure = Parameter.create(name=unicode(self.tr(u'Measure')), type=u'bool', default=False,
                                           value=False)
                group.addChild(measure)

                param_settings = parameter_group.get_adapter(adapter_name).get_settings()

                if param_settings is not None:
                    group.addChild(param_settings)

                parameter_group_tree.addChild(group)

            self.parameter_measurementParamTree.addChild(parameter_group_tree)

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

    def segmentationChanged(self, param, changes):
        if self.blockSignals:
            return

        for parameter, _, value in changes:
            if parameter in self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))). \
                            param(unicode(self.tr(u'Method Settings'))).children():
                pass
            else:
                self.blockSignals = True
                if isinstance(value, bool) and value:
                    # add the parameter settings
                    try:
                        adapter = self.segmentationAdapterFactory.get_adapter(parameter.name())

                        param_settings = self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))).\
                                         param(unicode(self.tr(u'Method Settings')))
                        param_settings.clearChildren()

                        method_settings = adapter.get_settings()
                        if method_settings:
                            param_settings.addChild(method_settings)

                    except Exception as ex:
                        print(ex.message)

                    # set to false the others segmentation methods
                    for p in self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))).children():
                        if p.type() == u"bool" and p.name() != parameter.name():
                            p.setValue(False)

        self.blockSignals = False
        self.detect()

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
            detector_name = ""
            for p in self.segmentation_classificationParamTree.param(unicode(self.tr(u'Segmentation'))).children():
                if p.type() == u"bool" and p.value():
                    detector_name = p.name()
                    break

            adapter = self.segmentationAdapterFactory.get_adapter(detector_name)

            detector_instance = adapter.get_instance(self.widget.signal)

        except Exception as e:
            print("Fail to get the detector instance. " + e.message)
            detector_instance = None

        self._detector = detector_instance if detector_instance is not None else ManualDetector(self.widget.signal)

        return self._detector

    @detector.setter
    def detector(self, value):
        self._detector = value

    def get_measurer_list(self):
        """
        :return: The list of selected parameters to measure
        """
        parameters_groups = self.parameter_measurementParamTree.children()

        parameters_list = []
        for group in parameters_groups:
            parameters_list.extend(group.children())

        # get just the parameter selected by user to be measured
        parameters_adapters_list = [self.parameterAdapterFactory.get_adapter(x.name()) for x in parameters_list
                                    if x.param(unicode(self.tr(u'Measure'))).value()]

        return parameters_adapters_list

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