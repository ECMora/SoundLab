# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import Parameter, ParameterTree
from graphic_interface.windows.ui_python_files.detectElementsDialog import Ui_Dialog
from graphic_interface.windows.ParametersWindow import ParametersWindow
from utils.Utils import small_signal
from sound_lab_core.AdapterFactories import *
from sound_lab_core.Clasification.Adapters import *


# tuples of classifiers (get a tuple of all an not of super class because a bug (?) on isinstance method)
classifiers_tuple = (KNNClassifierAdapter, ManualClassifierAdapter, NeuralNetsAdapter)


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    """
    Dialog that allow the selection of segmentation, parameter measurement
    and  classification  methods that would be used to  process a  segment.
    It's a factory interface of detectors, parameter measurers and classifiers
    """

    # region Initialize

    def __init__(self, parent, signal, parameter_manager, segment_manager=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.widget.signal = small_signal(signal)

        self._detector = None
        self._classifier = None

        # the factory adapters for segmentation and classification
        self._segmentationAdapterFactory = SegmentationAdapterFactory()
        self._classificationAdapterFactory = ClassificationAdapterFactory()

        # to manage the parameter selection and configuration
        self.parameter_manager = parameter_manager

        # the widget to visualize the segmentation and classification methods
        self.segmentation_classification_tree = None
        self.segmentation_classification_tree_widget = ParameterTree()
        self.segmentation_classification_tree_widget.setAutoScroll(True)
        self.segmentation_classification_tree_widget.setHeaderHidden(True)

        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.segmentation_classification_tree_widget)
        self.segmentation_classification_settings.setLayout(layout)

        self.create_segmentation_classification_param_tree()

        if segment_manager is not None:
            self.restore_previous_state(segment_manager)

        self.detect()

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

        params = [{u'name': unicode(self.tr(u'Parameter Measurements')), u'type': u'action'},
                  {u'name': unicode(self.tr(u'Segmentation')), u'type': u'group', u'children': list_param},
                  {u'name': unicode(self.tr(u'Classification')), u'type': u'group', u'children': list_classification}]

        self.segmentation_classification_tree = Parameter.create(name=unicode(self.tr(u'Settings')),
                                                                 type=u'group', children=params)

        self.connect_segmentation_classification_changed_events()

    def connect_segmentation_classification_changed_events(self):

        self.segmentation_classification_tree.param(unicode(self.tr(u'Segmentation'))). \
            sigTreeStateChanged.connect(lambda param, changes:
                                        self.segmentation_classification_changed(param, changes, u'Segmentation',
                                                                                 self.segmentation_adapter_factory))

        self.segmentation_classification_tree.param(unicode(self.tr(u'Classification'))). \
            sigTreeStateChanged.connect(lambda param, changes:
                                        self.segmentation_classification_changed(param, changes, u'Classification',
                                                                                 self.classification_adapter_factory))

        self.segmentation_classification_tree.param(unicode(self.tr(u'Parameter Measurements'))). \
            sigActivated.connect(self.configure_parameters)

        # create and set initial properties
        self.segmentation_classification_tree_widget.setParameters(self.segmentation_classification_tree)

    def configure_parameters(self):
        """
        Opens a parameter window to allow parameter measurement configuration.
        through the window the user can select and configure the parameters to measure.
        :return:
        """
        param_window = ParametersWindow(self, self.parameter_manager)
        param_window.exec_()

    def segmentation_classification_changed(self, param, changes, param_tree_name, adapter_factory):
        """
        Process a change into the parameter tree of segmentation and classification
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
            # then continue (each method adapter would take care about it's settings)
            if isinstance(value, bool) and value and \
               parameter not in self.segmentation_classification_tree.param(unicode(self.tr(param_tree_name))). \
               param(unicode(self.tr(u'Method Settings'))).children():

                try:
                    # the parameter changed has the method name
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

    # region Restore Previous Status

    def restore_previous_state(self, segment_manager):
        """
        Restore the dialog previous selected data to avoid lose of previous selected information
        :return:
        """

        # segmentation method restoration
        self._restore_method(segment_manager.detector_adapter, self.segmentation_adapter_factory, u'Segmentation')

        # classification method restoration
        self._restore_method(segment_manager.classifier_adapter, self.classification_adapter_factory, u'Classification')

    def _restore_method(self, adapter, adapter_factory, method_name):
        """
        Restore the segmentation or classification adapter previously used
        (user friendly restore of previous values of the dialog)
        :param adapter: the adapter (segmentation or classification adapter)
        :param method_name: the method name (one of 'Segmentation', 'Classification')
        :return:
        """

        for parameter in self.segmentation_classification_tree.param(unicode(self.tr(method_name))).children():
            if parameter.type() == u"bool":
                adapter_name = parameter.name()

                method_adapter = adapter_factory.get_adapter(adapter_name)

                if type(adapter) == type(method_adapter):
                    method_adapter.restore_settings(adapter, self.widget.signal)
                    parameter.setValue(True)

    # endregion

    # region  Factory Adapters Properties

    @property
    def segmentation_adapter_factory(self):
        return self._segmentationAdapterFactory

    @property
    def classification_adapter_factory(self):
        return self._classificationAdapterFactory

    @property
    def detector(self):
        """
        :return: The selected detector adapter to perform segmentation
        """
        self._detector = self._get_adapter(self.segmentation_adapter_factory)
        return self._detector

    @property
    def classifier(self):
        self._classifier = self._get_adapter(self.classification_adapter_factory)
        return self._classifier

    # endregion

    # region Detector, Parameter Measurers and Classifier

    def _get_adapter(self, adapter_factory):
        """
        Gets the adapter of the supplied adapter factory
        :param adapter_factory: the adapter factory to find the adapter in.
        :return:
        """
        param_tree_name = u'Classification' if adapter_factory == self.classification_adapter_factory else u'Segmentation'

        default_adapter_class = ManualDetectorAdapter
        if adapter_factory == self.classification_adapter_factory:
            default_adapter_class = ManualClassifierAdapter

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

    def get_measurer_list(self):
        """
        :return: The list of selected parameters to measure
        """
        return self.parameter_manager.parameter_list()

    # endregion

    def load_workspace(self, workspace):
        """
        Method that loads the workspace to update visual options from main window.
        :param workspace:
        """
        self.widget.load_workspace(workspace)

    def detect(self):
        """
        Perform the detection on the small signal to visualize an
        approximation of the detection algorithm
        :return:
        """
        # get the detector to perform segmentation
        detector = self.detector.get_instance(self.widget.signal)

        self.widget.elements = detector.detect()

        # update the visual items of the segmentation process
        self.widget.add_segmentation_items(self.detector.get_visual_items())

        self.widget.graph()