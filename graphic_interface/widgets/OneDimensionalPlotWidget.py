# -*- coding: utf-8 -*-
from duetto.audio_signals import AudioSignal
from graphic_interface.one_dimensional_transforms.OneDimensionalTransform import *
from graphic_interface.widgets.SoundLabOscillogramWidget import SoundLabOscillogramWidget


class OneDimPlotWidget(SoundLabOscillogramWidget):
    """
    Plots a one dimensional transformation of a signal
    """

    def __init__(self, parent=None,**kargs):
        # set the one dimensional one_dim_transform currently applied to the signal
        self.__one_dim_transform = None

        self.plot_color = "CC3"

        SoundLabOscillogramWidget.__init__(self, **kargs)

    def load_workspace(self, workspace, forceUpdate=False):
        SoundLabOscillogramWidget.load_workspace(self,workspace,forceUpdate)
        self.plot_color = workspace.theme.plot_color

    # region Property Transform
    # the signal and the one_dim_transform update is made on the window
    # that controls this widget to avoid redefine the signal property of the widget

    @property
    def one_dim_transform(self):
        return self.__one_dim_transform

    @one_dim_transform.setter
    def one_dim_transform(self, transform):
        """
        Change the current one dim transformation
        visualized by the widget
        :return:
        """
        if not isinstance(transform, OneDimensionalTransform):
            raise Exception("Invalid type. one_dim_transform must be of type OneDimensionalTransform")

        self.__one_dim_transform = transform

        self.__one_dim_transform.signal = self.signal

        self.__one_dim_transform.dataChanged.connect(self.graph)

    # endregion

    def graph(self, indexFrom=0, indexTo=-1):
        """
        Graphs the one dimensional one_dim_transform of a signal interval on the widget
        :param indexFrom: start value of the signal interval in array data indexes
        :param indexTo: end value of the signal interval in array data indexes
        :return:
        """
        if self.one_dim_transform is not None:
            self.clear()
            self.plot(self.one_dim_transform.getData(indexFrom, indexTo), pen=self.plot_color)