from PyQt4.QtCore import QObject
from graphic_interface.one_dimensional_transforms import *


class OneDimensionalGeneralHandler(QObject):
    """
    The general one dimensional handler. The one that delegates on each of the corresponding one dimensional handlers
    to do the job.
    This class inherits from QObject to be able to use translations. A valid parent must be supplied on __init__
    """

    def __init__(self, parent):
        QObject.__init__(self, parent)

        self._handlers_by_name = {
            'Envelope': EnvelopeHandler(parent),
            'Averaged Power Spectrum': AveragePowSpecHandler(parent),
            'Logarithmic Power Spectrum': LogarithmicPowSpecHandler(parent),
            'Instant Frequencies': InstantFrequenciesHandler(parent)
        }
        self._handlers_by_class = {handler.get_transform_class(): handler for _, handler in
                                   self._handlers_by_name.items()}

    def get_all_transforms_names(self):
        """
        Gets the name of all registered one dimensional transforms.
        :return: a list of str, each the name of one transform
        """
        return self._handlers_by_name.keys()

    def get_transform(self, name):
        """
        Gets an instance of the corresponding one dimensional transform given its name.
        :param name: a str, the name of the transform. Must be one of the values returned by the get_all_transforms_names method.
        :return: an instance of the corresponding one dimensional transform
        """
        return self._handlers_by_name[name].get_transform_instance()

    def get_y_default(self, transform):
        """
        Gets the default Y range values according to the transform param
        :param transform: the one dimensional transform instance from which to take the values
        :return: a tuple with the min and max default values
        """
        return self._handlers_by_class[transform.__class__].get_y_default(transform)

    def get_default_lines(self, transform):
        return self._handlers_by_class[transform.__class__].get_default_lines()

    def get_y_limits(self, transform):
        """
        Gets the Y axis limits values of the corresponding transform
        :param transform: the one dimensional transform instance from which to take the values
        :return: a tuple with the min and max limits values
        """
        return self._handlers_by_class[transform.__class__].get_y_limits(transform)

    def get_axis_labels(self, transform):
        """
        Gets the axis labels information of the corresponding transform to show it when graphing
        :param transform: the one dimensional transform instance from which to take the values
        :return: a dict with the axis information of the corresponding one dimensional transform
        """
        return self._handlers_by_class[transform.__class__].get_axis_labels()

    def get_settings(self, transform):
        """
        Gets the settings of the corresponding one dimensional transform with the values of the supplied instance
        :param transform: the one dimensional transform instance from which to take the values
        :return: a list of dicts in the way needed to create the param tree
        """
        return self._handlers_by_class[transform.__class__].get_settings(transform)

    def apply_settings_change(self, transform, changes):
        """
        Applies the given changes to the given transform
        :param transform: the one dimensional transform instance which settings are to be changed
        :param changes: the changes to apply in the way provided by the param tree
        """
        self._handlers_by_class[transform.__class__].apply_settings_change(transform, changes)
