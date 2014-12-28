# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, pyqtSignal
import numpy as np
from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from duetto.audio_signals import AudioSignal
from graphic_interface.windows.ParameterList import DuettoListParameterItem


class OneDimensionalTransform(QObject):
    """

    """

    # SIGNALS
    # signal raised when the parameters of the one_dim_transform change
    # and the one_dim_transform data must be recomputed
    dataChanged = pyqtSignal()

    def __init__(self, signal=None):
        QObject.__init__(self)
        # the parameter object with the set of parameters for the tree widget
        self.parameter = None

        # the parameter tree widget with the options
        self._parameterTree = self._getParameterTree()



        self._signal = signal

    def _getParameterTree(self):
        """
        Abstract method to implement in descendants.
        :return: returns the parameter tree with the visual options
        for the user interaction of the one dimensional function
        """
        return self._createParameterTree(self._createParameter([]))

    def _createParameter(self, params):
        """
        create and returns a parameter tree with the params supplied
        :param params:
        :return:
        """
        ListParameter.itemClass = DuettoListParameterItem
        ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        return ParamTree

    def _createParameterTree(self,parameter):
        """
        Create the parameter tree widget with the parameter supplied
        :param parameter: The pyqtgraph Parameter to insert in the tree widget
        :return:
        """
        parameterTree = ParameterTree()
        parameterTree.setAutoScroll(True)
        parameterTree.setHeaderHidden(True)
        parameterTree.setParameters(parameter, showTop=False)

        return parameterTree

    # region Properties signal, settings
    @property
    def settings(self):
        """
        Parameter tree widget with the visual settings
        of the function. Used for add it in a widget layout
        and interact with the user.
        :return:
        """
        return self._parameterTree

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

    # endregion

    def getData(self, indexFrom, indexTo):
        """
        Computes and returns the one dimensional one_dim_transform
        over the signal data in the supplied interval.
        :param indexFrom: the start of the signal interval to process in signal array data indexes.
        :param indexTo: the end of the signal interval to process in signal array data indexes..
        """
        return np.zeros(indexTo-indexFrom)





