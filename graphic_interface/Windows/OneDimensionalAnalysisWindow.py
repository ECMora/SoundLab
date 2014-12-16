# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from graphic_interface.windows.one_dim_transforms_window import Ui_OneDimensionalWindow
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.one_dimensional_transforms.OneDimensionalTransforms import *


class OneDimensionalAnalysisWindow(QtGui.QMainWindow, Ui_OneDimensionalWindow):
    """
    Window that allow to create and visualize one dimensional transforms on signals
    """
    DOCK_OPTIONS_WIDTH = 250

    def __init__(self,parent=None):
        super(OneDimensionalAnalysisWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()

        # connect the tool detected data to show the status bar message
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        # Parameter Tree Settings
        self.__createParameterTree()

    def load_Theme(self, theme):
        """
        Load the supplied theme into the widget inside.
        :param theme: The theme with the visual options
        :return:
        """
        self.widget.load_Theme(theme)

    # region Graph

    def graph(self):
        self.widget.graph()

    def updateGraph(self, indexFrom, indexTo):
        """
        Update the graph of the one dimensional
        selected transformation in the signal interval supplied.
        Apply the transformation to the signal interval and plot it.
        :param indexFrom: start of the interval in signal data indexes
        :param indexTo: end of the interval in signal data indexes
        :return:
        """
        pass

    # endregion

    # region Parameter Tree Options

    def __createParameterTree(self):
        """
        Create the ParameterTree with the options of the window.
        The ParameterTree contains the combo box of
        the active one dimensional transforms to select.
        :return:
        """
        params = [
            {u'name': unicode(self.tr(u'One_Dim_Transform')), u'type': u'list',
             u'value': u"Envelope",
             u'default': Envelope,
             # classes of the one dim transforms. to add a new one
             # just add it to the list and implement it
             u'values': [(u'Envelope', Envelope),
                         (u'AveragePowSpec', AveragePowSpec),
                         (u'LogarithmicPowSpec', LogarithmicPowSpec),
                         (u'InstantaneousFrequencies', InstantaneousFrequencies)
             ]}
        ]

        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)

        # create and set initial properties
        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(self.DOCK_OPTIONS_WIDTH)
        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        # connect the signals to react when a change of transform is made
        self.ParamTree.param(unicode(self.tr(u'One_Dim_Transform'))).sigValueChanged.connect(self.changeTransform)

        # set a default one dim transform to the widget
        self.widget.transform = Envelope()

        # reload the new widgets transform options
        self.reloadOptionsWidget(self.widget.transform)

    def reloadOptionsWidget(self, one_dim_transform):
        """
        Refresh the parameter tree and the layout
        of the options windows when a change of  transformation is made.
        removes the old transformation options and set the parameter tree
        of the new one.
        :param one_dim_transform: the new transform.
        :return:
        """

        options_window_layout = QtGui.QVBoxLayout()
        options_window_layout.setMargin(0)
        options_window_layout.addWidget(self.parameterTree)
        options_window_layout.setStretchFactor(self.parameterTree,0)

        # add the parameter tree of the transform if exists
        if one_dim_transform is not None:
            options_window_layout.addWidget(one_dim_transform.settings)

        # removing the old layout from the dock widget
        self.dock_settings_contents = QtGui.QWidget()
        self.dock_settings_contents.setLayout(options_window_layout)
        self.dockSettings.setWidget(self.dock_settings_contents)

        self.dockSettings.setVisible(True)
        self.dockSettings.setFixedWidth(self.DOCK_OPTIONS_WIDTH)

    def changeTransform(self, parameter):
        """
        Method invoked when a new transform is selected.
        Change the transform in the widget and update the options window
        :param parameter: the parameter tree node that change
        :return:
        """

        transform_class = parameter.value()

        self.widget.transform = transform_class()

        self.reloadOptionsWidget(self.widget.transform)

    # endregion

    def updateStatusBar(self, line):
        """
        Update the status bar window message.
        :param line: The (string) to show as message
        :return: None
        """
        self.statusbar.showMessage(line)