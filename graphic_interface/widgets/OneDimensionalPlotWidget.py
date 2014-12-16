# -*- coding: utf-8 -*-
from graphic_interface.one_dimensional_transforms.OneDimensionalTransforms import *
from graphic_interface.widgets.SoundLabOscillogramWidget import SoundLabOscillogramWidget


class OneDimPlotWidget(SoundLabOscillogramWidget):
    """
    Plots a one dimensional transformation of a signal
    """

    def __init__(self, parent=None,**kargs):
        SoundLabOscillogramWidget.__init__(self, **kargs)

        # set the one dimensional transform currently applied to the signal
        self.one_dim_transform = None

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

    # endregion

    def graph(self,indexFrom=0,indexTo=-1):
        # SoundLabOscillogramWidget.graph(self)
        if self.one_dim_transform is not None:
            pass