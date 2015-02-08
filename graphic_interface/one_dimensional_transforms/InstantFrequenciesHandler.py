from duetto.dimensional_transformations.one_dimensional_transforms.InstantFrequenciesTransform import InstantFrequencies
from graphic_interface.one_dimensional_transforms.OneDimensionalHandler import OneDimensionalHandler


class InstantFrequenciesHandler(OneDimensionalHandler):

    def __init__(self, parent):
        OneDimensionalHandler.__init__(self, parent)
        self._transform_class = InstantFrequencies

    def get_transform_class(self):
        return self._transform_class

    def get_transform_instance(self):
        return self._transform_class()

    def get_settings(self, transform):
        """

        :type transform: InstantFrequencies
        """
        # return [{u'name': unicode(self.tr(u'Instantaneous Frequency')), u'type': u'group',
        #          u'children': []}]
        return []

    def get_axis_labels(self):
        return {u'X': u'Time (s)', u'Y': u'Frequency (kHz)' }

    def apply_settings_change(self, transform, change):
        """

        :type transform: InstantFrequencies
        """
        childName, _change, data = change
