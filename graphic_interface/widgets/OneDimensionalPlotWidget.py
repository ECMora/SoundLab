# -*- coding: utf-8 -*-
from duetto.audio_signals import AudioSignal
from graphic_interface.one_dimensional_transforms.OneDimensionalTransforms import *
from graphic_interface.widgets.SoundLabOscillogramWidget import SoundLabOscillogramWidget


class OneDimPlotWidget(SoundLabOscillogramWidget):
    """
    Plots a one dimensional transformation of a signal
    """

    def __init__(self, parent=None,**kargs):
        # set the one dimensional transform currently applied to the signal
        self.one_dim_transform = None

        self.plot_color = "CC3"

        SoundLabOscillogramWidget.__init__(self, **kargs)

    def load_Theme(self, theme):
        SoundLabOscillogramWidget.load_Theme(self,theme)
        self.plot_color = theme.plot_color

    # region Property Transform

    @property
    def transform(self):
        return self.one_dim_transform

    @transform.setter
    def transform(self, transform):
        """
        Change the current one dim transformation
        visualized by the widget
        :return:
        """
        if not isinstance(transform, OneDimensionalFunction):
            raise Exception("Invalid type. transform must be of type OneDimensionalFunction")

        self.one_dim_transform = transform

        self.transform.signal = self.signal

        self.transform.dataChanged.connect(self.graph)

    # endregion

    def graph(self, indexFrom=0, indexTo=-1):
        # SoundLabOscillogramWidget.graph(self)
        if self.one_dim_transform is not None:
            self.clear()
            self.plot(self.transform.getData(indexFrom, indexTo),pen=self.plot_color)