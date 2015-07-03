__author__ = 'y.febles'


class VisualItemsVisibility:
    """
    Class that encapsulate the visibility of the different
    visual items.  Behavior as an structure.
    """

    def __init__(self, osc_text=True, osc_figures=True, osc_parameters=True, osc_items=True,
                spec_text=True, spec_figures=True, spec_parameters=True, spec_items=True):

        # the visibility of oscilogram elements
        self.osc_items = osc_items
        self.osc_text = osc_text
        self.osc_figures = osc_figures
        self.osc_parameters = osc_parameters

        # the visibility of spectrogram elements
        self.spec_items = spec_items
        self.spec_text = spec_text
        self.spec_figures = spec_figures
        self.spec_parameters = spec_parameters

    # region Properties

    @property
    def oscilogram_items_visible(self):
        return self.osc_items

    @oscilogram_items_visible.setter
    def oscilogram_items_visible(self, value):
        self.osc_items = value

    @property
    def spectrogram_items_visible(self):
        return self.spec_items

    @spectrogram_items_visible.setter
    def spectrogram_items_visible(self, value):
        self.spec_items = value

    @property
    def oscilogram_text_visible(self):
        return self.osc_text

    @oscilogram_text_visible.setter
    def oscilogram_text_visible(self, value):
        self.osc_text = value

    @property
    def oscilogram_figures_visible(self):
        return self.osc_figures

    @oscilogram_figures_visible.setter
    def oscilogram_figures_visible(self, value):
        self.osc_figures = value

    @property
    def oscilogram_parameters_visible(self):
        return self.osc_parameters

    @oscilogram_parameters_visible.setter
    def oscilogram_parameters_visible(self, value):
        self.osc_parameters = value

    @property
    def spectrogram_text_visible(self):
        return self.spec_text

    @spectrogram_text_visible.setter
    def spectrogram_text_visible(self, value):
        self.spec_text = value

    @property
    def spectrogram_figures_visible(self):
        return self.spec_figures

    @spectrogram_figures_visible.setter
    def spectrogram_figures_visible(self, value):
        self.spec_figures = value

    @property
    def spectrogram_parameters_visible(self):
        return self.spec_parameters

    @spectrogram_parameters_visible.setter
    def spectrogram_parameters_visible(self, value):
        self.spec_parameters = value

    # endregion

    def __eq__(self, other):
        return other is not None and isinstance(other, VisualItemsVisibility) and \
               self.oscilogram_figures_visible == other.oscilogram_figures_visible and \
               self.oscilogram_items_visible == other.oscilogram_items_visible and \
               self.oscilogram_text_visible == other.oscilogram_text_visible and \
               self.oscilogram_parameters_visible == other.oscilogram_parameters_visible and \
               self.spectrogram_figures_visible == other.spectrogram_figures_visible and \
               self.spectrogram_text_visible == other.spectrogram_text_visible and \
               self.spectrogram_items_visible == other.spectrogram_items_visible and \
               self.spectrogram_parameters_visible == other.spectrogram_parameters_visible