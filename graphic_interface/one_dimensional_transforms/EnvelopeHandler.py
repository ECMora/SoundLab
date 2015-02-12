from duetto.dimensional_transformations.one_dimensional_transforms.EnvelopeTransform import Envelope
from graphic_interface.one_dimensional_transforms.OneDimensionalHandler import OneDimensionalHandler


class EnvelopeHandler(OneDimensionalHandler):

    def __init__(self, parent):
        OneDimensionalHandler.__init__(self, parent)
        self._transform_class = Envelope

    def get_transform_class(self):
        return self._transform_class

    def get_transform_instance(self):
        return self._transform_class()

    def get_settings(self, transform):
        """

        :type transform: Envelope
        """
        return [     {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': transform.decay, u'step': 0.5},
                     {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'int', u'value': transform.softFactor, u'step': 1},
                     {u'name': unicode(self.tr(u'Function Type')), u'type': u'list', u'value': transform.functionType,
                      u'default': "sin",
                      u'values': [(u"Sin", "sin"),
                                  (u'Lineal', "lineal"),
                                  (u"Cuadratic", "cuadratic")]}]
    def get_axis_labels(self):
        return {u'X': u'Time (s)', u'Y': u'Amplitude' }

    def get_y_default(self, transform):
        """

        :type transform: Envelope
        """
        return (0, 100)

    def get_y_limits(self, transform):
        """

        :type transform: Envelope
        """
        return (0,100)

    def apply_settings_change(self, transform, change):
        """

        :type transform: Envelope
        """
        childName, _change, data = change

        # in all this methods I'm relaying on the transform to check if data is different from previous data and any
        # other desired optimization
        if childName == unicode(self.tr(u'Decay (ms)')):
            transform.decay = data

        elif childName == unicode(self.tr(u'Soft Factor')):
            transform.softFactor = data

        elif childName == unicode(self.tr(u'Function Type')):
            transform.functionType = data
