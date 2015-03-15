# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import Parameter, ParameterTree

from graphic_interface.windows.ui_python_files.detectElementsDialog import Ui_Dialog
from utils.Utils import small_signal
from sound_lab_core.AdapterFactories import *
from sound_lab_core.Clasification.Adapters.ManualClassifierAdapter import ManualClassifierAdapter


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

        self._detector = None
        self._classifier = None

        # get the factory adapters for parameters, segmentation and classification
        self._parameterAdapterFactory = ParametersAdapterFactory()
        self._segmentationAdapterFactory = SegmentationAdapterFactory()
        self._classificationAdapterFactory = ClassificationAdapterFactory()

        self.parameter_tree_widget = ParameterTree()
        self.param_measurement_tree = None

        self.segmentation_classification_tree_widget = ParameterTree()
        self.segmentation_classification_tree = None

        self.create_parameter_trees()

        self.detect()

    def restore_previous_state(self, parameter_adapters, segmentation_adapter=None, classification_adapter=None):
        """
        Restore the dialog previous selected data to avoid lose of previous selected parameters
        :param parameter_adapters: The list of parameters adapters previously selected
        :param segmentation_adapter: The segmentation adapter previously selected
        :param classification_adapter: The classification adapter previously selected
        :return:
        """
        parameters_groups = self.param_measurement_tree.children()

        # parameters adapters
        for group in parameters_groups:
            for parameter in group.children():
                adapter = self.parameter_adapter_factory.get_adapter(parameter.name())
                for p in parameter_adapters:
                    if type(adapter) == type(p):
                        parameter.param(unicode(self.tr(u'Measure'))).setValue(True)
                        adapter.restore_settings(p, self.widget.signal)
                        break

        # segmentation method
        self._restore_method(segmentation_adapter, self.segmentation_adapter_factory, u'Segmentation')

        # classification method
        self._restore_method(classification_adapter, self.classification_adapter_factory, u'Classification')

    def _restore_method(self, adapter, adapter_factory, method_name):
        """
        Restore the segmentation or classification adpater previously used
        (user friendly restore of previous values of the dialog)
        :param adapter: the adapter (segmentation or classification adapter)
        :param method_name: the method name (one of 'Segmentation', 'Classification')
        :return:
        """
        if not adapter:
            return

        for parameter in self.segmentation_classification_tree.param(unicode(self.tr(method_name))).children():
            if parameter.type() == u"bool":
                adapter_name = parameter.name()
                method_adapter = adapter_factory.get_adapter(adapter_name)
                if type(adapter) == type(method_adapter):
                    method_adapter.restore_settings(adapter, self.widget.signal)
                    parameter.setValue(True)

    def create_parameter_trees(self):
        """
        Create the ParameterTree with the options of the dialog.
        The ParameterTree contains the combo box of
        the active parameters parameters and to select.
        :return:
        """
        self.create_segmentation_classification_param_tree()
        self.create_measurement_parameter_tree()
        self.configure_parameter_trees_layout()

    def create_segmentation_classification_param_tree(self):

        # get the adapters for segmentation methods
        segmentation_adapters = self.segmentation_adapter_factory.adapters_names()
        segmentation_adapters = [(self.tr(unicode(t)), t) for t in segmentation_adapters]

        # get the adapters for classification methods
        classification_adapters = self.classification_adapter_factory.adapters_names()
        classification_adapters = [(self.tr(t), t) for t in classification_adapters]

        # the list of segmentation adapters check boxes to select method (radio buttons unavailable)
        list_param = [{u'name': unicode(x[1]), u'type': u'bool', u'value': False, u'default': False}
                      for x in segmentation_adapters]

        # the method settings
        list_param.append({u'name': unicode(self.tr(u'Method Settings')), u'type': u'group', u'children': []})

        # the list of classification adapters check boxes to select method (radio buttons unavailable)
        list_classification = [{u'name': unicode(x[1]), u'type': u'bool', u'value': False, u'default': False}
                      for x in classification_adapters]

        # the method settings
        list_classification.append({u'name': unicode(self.tr(u'Method Settings')), u'type': u'group', u'children': []})

        params = [{u'name': unicode(self.tr(u'Segmentation')),
                   u'type': u'group', u'children': list_param},
                  {u'name': unicode(self.tr(u'Classification')),
                   u'type': u'group', u'children': list_classification}]

        self.segmentation_classification_tree = Parameter.create(
            name=unicode(self.tr(u'Segmentation-Classification')), type=u'group', children=params)

        self.segmentation_classification_tree.param(unicode(self.tr(u'Segmentation'))). \
            sigTreeStateChanged.connect(lambda param, changes:
                                        self.segmentation_classification_changed(param, changes, u'Segmentation',
                                                                                 self.segmentation_adapter_factory))

        self.segmentation_classification_tree.param(unicode(self.tr(u'Classification'))). \
            sigTreeStateChanged.connect(lambda param, changes:
                                        self.segmentation_classification_changed(param, changes, u'Classification',
                                                                                 self.classification_adapter_factory))

        # create and set initial properties
        self.segmentation_classification_tree_widget.setAutoScroll(True)
        self.segmentation_classification_tree_widget.setHeaderHidden(True)
        self.segmentation_classification_tree_widget.setParameters(self.segmentation_classification_tree)

    def create_measurement_parameter_tree(self):
        # set the segmentation and classification parameters
        self.param_measurement_tree = Parameter.create(name=unicode(self.tr(u'Parameter Measurements')), type=u'group')

        # create a group for each parameter group category
        for parameter_group in self.parameter_adapter_factory.parameter_groups:
            parameter_group_tree = Parameter.create(name=unicode(self.tr(unicode(parameter_group.name))),
                                                    type=u'group', expanded=False)

            # for each group category add all the parameters on that category
            for adapter_name in parameter_group.adapters_names():
                group = Parameter.create(name=unicode(self.tr(unicode(adapter_name))),
                                         type=u'group', expanded=True)

                # the measure/ not measure check box to select parameter for measurement
                measure = Parameter.create(name=unicode(self.tr(u'Measure')), type=u'bool', default=False, value=False)

                # get the parameter settings if any (Parameter tree interface of the parameter adapter)
                param_settings = parameter_group.get_adapter(adapter_name).get_settings()

                group.addChild(measure)

                if param_settings is not None:
                    group.addChild(param_settings)

                parameter_group_tree.addChild(group)

            self.param_measurement_tree.addChild(parameter_group_tree)

        self.parameter_tree_widget.setAutoScroll(True)
        self.parameter_tree_widget.setHeaderHidden(True)
        self.parameter_tree_widget.setParameters(self.param_measurement_tree)

    def configure_parameter_trees_layout(self):
        """
        Configure the layout of the parameter trees of segmentation,
        classification methods and parameter measurement.
        :return:
        """
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.segmentation_classification_tree_widget)
        self.segmentation_classification_settings.setLayout(layout)

        layout2 = QtGui.QVBoxLayout()
        layout2.setMargin(0)
        layout2.addWidget(self.parameter_tree_widget)
        self.parameter_measurement_settings.setLayout(layout2)

    def segmentation_classification_changed(self, param, changes, param_tree_name, adapter_factory):
        """
        Process a change into the parameter tree of segmentation
        :param param:
        :param changes:
        :return:
        """
        # block signals because there is changes that involve tree updates
        # (select a segmentation method with settings that must be added into the tree by example)
        self.segmentation_classification_tree.blockSignals(True)

        for parameter, _, value in changes:

            # if the value is bool then is the selection of the segmentation or classification method
            # if the change came from the segmentation or classification method settings
            # then continue (each method would take care about it's settings)
            if isinstance(value, bool) and value and\
                parameter not in self.segmentation_classification_tree.param(unicode(self.tr(param_tree_name))). \
                    param(unicode(self.tr(u'Method Settings'))).children():
                try:
                    # the parameter changed is has the method name
                    adapter = adapter_factory.get_adapter(parameter.name())

                    # change the method settings if any (Parameter tree interface of adapter)
                    param_settings = self.segmentation_classification_tree.param(
                        unicode(self.tr(param_tree_name))).param(unicode(self.tr(u'Method Settings')))

                    param_settings.clearChildren()

                    method_settings = adapter.get_settings()
                    if method_settings:
                        param_settings.addChild(method_settings)

                except Exception as ex:
                    print(ex.message)

                params_to_update = self.segmentation_classification_tree.param(
                    unicode(self.tr(param_tree_name))).children()

                params_to_update = [p for p in params_to_update if p.type() == u"bool" and
                                    p.name() != parameter.name()]

                # set to false the others segmentation methods (radio button behavior, only select one method)
                for p in params_to_update:
                    p.setValue(False)

        self.segmentation_classification_tree.blockSignals(False)
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
    def parameter_adapter_factory(self):
        return self._parameterAdapterFactory

    @property
    def segmentation_adapter_factory(self):
        return self._segmentationAdapterFactory

    @property
    def classification_adapter_factory(self):
        return self._classificationAdapterFactory

    # endregion

    # region Detector, Parameter Measurers and Classifier
    def _get_adapter(self, param_tree_name, adapter_factory, default_adapter_class):
        try:
            name = ""
            parameters = self.segmentation_classification_tree.param(unicode(self.tr(param_tree_name))).children()

            for parameter in parameters:
                if parameter.type() == u"bool" and parameter.value():
                    name = parameter.name()
                    break

            adapter = adapter_factory.get_adapter(name)

        except Exception as e:
            print("Fail to get the adapter instance. In " + param_tree_name + " " + e.message)
            adapter = default_adapter_class()
        return adapter

    @property
    def detector(self):
        """
        :return: The selected detector adapter to perform segmentation
        """
        self._detector = self._get_adapter(u'Segmentation', self.segmentation_adapter_factory,
                                           ManualDetectorAdapter)
        return self._detector

    @property
    def classifier(self):
        self._classifier = self._get_adapter(u'Classification', self.classification_adapter_factory,
                                             ManualClassifierAdapter)
        return self._classifier

    def get_measurer_list(self):
        """
        :return: The list of selected parameters adapters to measure
        """
        parameters_groups = self.param_measurement_tree.children()

        parameters_list = []
        for group in parameters_groups:
            parameters_list.extend(group.children())

        # get just the parameter selected by user to be measured
        parameters_adapters_list = [self.parameter_adapter_factory.get_adapter(x.name()) for x in parameters_list
                                    if x.param(unicode(self.tr(u'Measure'))).value()]

        return parameters_adapters_list

    # endregion

    def detect(self):
        """
        Perform the detection on the small signal to visualize an
        approximation of the detection algorithm
        :return:
        """

        detector = self.detector.get_instance(self.widget.signal)
        visual_items = self.detector.get_visual_items()

        self.widget.elements = detector.detect()
        self.widget.add_segmentation_items(visual_items)

        self.widget.graph()