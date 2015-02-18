# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from duetto.audio_signals import AudioSignal
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree.parameterTypes import ListParameter
from duetto.dimensional_transformations.one_dimensional_transforms.InstantFrequenciesTransform import InstantFrequencies
from graphic_interface.one_dimensional_transforms.OneDimensionalGeneralHandler import OneDimensionalGeneralHandler
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.windows.ui_python_files.one_dim_transforms_window import Ui_OneDimensionalWindow


class OneDimensionalAnalysisWindow(QtGui.QMainWindow, Ui_OneDimensionalWindow):
    """
    Window that allow to create and visualize one dimensional transforms on signals
    """

    # region CONSTANTS
    DOCK_OPTIONS_WIDTH = 350
    WIDGET_MINIMUM_HEIGHT = 350
    WIDGET_MINIMUM_WIDTH = 1.5 * DOCK_OPTIONS_WIDTH

    # endregion
    def __init__(self, parent=None, signal=None):
        super(OneDimensionalAnalysisWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.widget.setMinimumWidth(self.WIDGET_MINIMUM_WIDTH)
        self.widget.setMinimumHeight(self.WIDGET_MINIMUM_HEIGHT)

        self._transforms_handler = OneDimensionalGeneralHandler(self)

        # connect the tool detected data to show the status bar message
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        self._indexTo = -1
        self._indexFrom = 0

        if signal is None:
            raise Exception("Signal can't be None.")

        # set a default one dim one_dim_transform to the widget
        self.widget.signal = signal

        # self.signal = signal
        self.widget.one_dim_transform = InstantFrequencies(signal)

        # Parameter Tree Settings
        self.__createParameterTree()

        # self._transforms_handler.dataChanged.connect(self.widget.graph)

    def load_workspace(self, workspace):
        """
        Load the supplied theme into the widget inside.
        :param theme: The theme with the visual options
        :return:
        """
        self.widget.load_workspace(workspace)

    # region Properties IndexTo IndexFrom

    @property
    def indexTo(self):
        return self._indexTo

    @indexTo.setter
    def indexTo(self, value):
        self._indexTo = value

    @property
    def indexFrom(self):
        return self._indexFrom

    @indexFrom.setter
    def indexFrom(self, value):
        self._indexFrom = value

    # endregion

    # region Graph

    def graph(self, indexFrom=0, indexTo=-1):
        """
        Update the graph of the one dimensional
        selected transformation in the signal interval supplied.
        Apply the transformation to the signal interval and plot it.
        :param indexFrom: start of the interval in signal data indexes
        :param indexTo: end of the interval in signal data indexes
        :return:
        """
        indexTo = indexTo if indexTo >=0 else self.widget.signal.length

        if indexTo != self.indexTo:
            self.indexTo = indexTo

        if indexFrom != self.indexFrom:
            self.indexFrom = indexFrom

        labels = self._transforms_handler.get_axis_labels(self.widget.one_dim_transform)
        self.widget.graph(indexFrom, indexTo, labels)

    # endregion

    # region Parameter Tree Options

    def __createParameterTree(self):
        """
        Create the ParameterTree with the options of the window.
        The ParameterTree contains the combo box of
        the active one dimensional transforms to select.
        :return:
        """
        transforms = self._transforms_handler.get_all_transforms_names()
        transforms = [(unicode(self.tr(unicode(t))), t) for t in transforms]
        params = [
            {u'name': unicode(self.tr(u'Select')),
             u'type': u'list',
             u'value': transforms[0][1],
             u'default': transforms[0][1],
             u'values': transforms},
            {u'name':  unicode(self.tr(u'Settings')), u'type': u'group'}
        ]

        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name=u'One Dimensional Transform', type=u'group', children=params)

        # create and set initial properties
        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree)


        # connect the signals to react when a change of one_dim_transform is made
        self.ParamTree.param(unicode(self.tr(u'Select'))).sigValueChanged.connect(self.changeTransform)

        # reload the new widgets one_dim_transform options
        self._transform_paramTree = None
        self.reloadOptionsWidget(self.widget.one_dim_transform)

    def reloadOptionsWidget(self, one_dim_transform):
        """
        Refresh the parameter tree and the layout
        of the options windows when a change of  transformation is made.
        removes the old transformation options and set the parameter tree
        of the new one.
        :param one_dim_transform: the new one_dim_transform.
        :return:
        """
        options_window_layout = QtGui.QVBoxLayout()
        options_window_layout.setMargin(0)
        options_window_layout.addWidget(self.parameterTree)

        # add the parameter tree of the one_dim_transform if exists
        if one_dim_transform is not None:

            # clear the settings options of the parameter tree
            if self._transform_paramTree is not None:
               self.ParamTree.param(u'Settings').clearChildren()
            params = self._transforms_handler.get_settings(one_dim_transform)
            self._transform_paramTree = Parameter.create(name=u'Parameters', type=u'group', children=params)

            if params:
                self.ParamTree.param(u'Settings').addChild(self._transform_paramTree)

            # getting transform graph information by the general handler
            labels = self._transforms_handler.get_axis_labels(one_dim_transform)
            limits = self._transforms_handler.get_y_limits(one_dim_transform)
            default_limits =  self._transforms_handler.get_y_default(one_dim_transform)

            # setting the default Y range values
            self.widget.minY = default_limits[0]
            self.widget.maxY = default_limits[1]

            # adding the range params to the settings
            rangeParams = [  { u'name': unicode(self.tr(u'Min')), u'type': u'int', u'limits': limits, u'value': self.widget.minY },
                             { u'name': unicode(self.tr(u'Max')), u'type': u'int', u'limits': limits, u'value': self.widget.maxY }
                          ]

            self._yRange_paramTree = Parameter.create(name=labels[u'Y'], type=u'group', children=rangeParams)
            self.ParamTree.param(u'Settings').addChild(self._yRange_paramTree)

            # setting the connecting lines option on settings with default transform value
            self.widget.lines = self._transforms_handler.get_default_lines(one_dim_transform)

            lines = {u'name': unicode(self.tr(u'Connect points')),
                      u'type':u'bool',
                      u'value': self.widget.lines,
                      u'default': self.widget.lines}

            self.ParamTree.param(u'Settings').addChild(lines)

            # connecting the signals to the change handler function
            self.ParamTree.param(u'Settings').param(u'Connect points').sigTreeStateChanged.connect(self.connectLinesChanged)
            self._transform_paramTree.sigTreeStateChanged.connect(self.changeTransformSettings)
            self._yRange_paramTree.sigTreeStateChanged.connect(self.changeYRangeSettings)

        # removing the old layout from the dock widget
        self.dock_settings_contents = QtGui.QWidget()
        self.dock_settings_contents.setLayout(options_window_layout)
        self.dockSettings.setWidget(self.dock_settings_contents)
        self.dockSettings.setVisible(True)
        self.dockSettings.setMinimumWidth(self.DOCK_OPTIONS_WIDTH)

    def changeTransform(self, parameter):
        """
        Method invoked when a new one_dim_transform is selected.
        Change the one_dim_transform in the widget and update the options window
        :param parameter: the parameter tree node that change
        :return:
        """

        transform_name = parameter.value()

        self.widget.one_dim_transform = self._transforms_handler.get_transform(transform_name)

        self.reloadOptionsWidget(self.widget.one_dim_transform)

        self.update()

        self.graph(indexFrom=self.indexFrom, indexTo=self.indexTo)

    def connectLinesChanged(self, param, changes):

        param, change, data = changes[0]
        self.widget.lines = data

        self.graph(indexFrom=self.indexFrom, indexTo=self.indexTo)

    def changeTransformSettings(self, param, changes):

        for param, change, data in changes:
            path = self._transform_paramTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            self._transforms_handler.apply_settings_change(self.widget.one_dim_transform, (childName, change, data))

        self.graph(indexFrom=self.indexFrom, indexTo=self.indexTo)

    def changeYRangeSettings(self, param, changes):

        labels = self._transforms_handler.get_axis_labels(self.widget.one_dim_transform)
        for param, change, data in changes:
            path = self._transform_paramTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == u'Min':
                self.widget.minY = data

            if childName ==u'Max':
                self.widget.maxY = data


        self.graph(indexFrom=self.indexFrom, indexTo=self.indexTo)

    # endregion

    def updateStatusBar(self, line):
        """
        Update the status bar window message.
        :param line: The (string) to show as message
        :return: None
        """
        self.statusbar.showMessage(line)