from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.TimeParameters.EndTimeParameterAdapter import EndTimeParameterAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.StartTimeParameterAdapter import StartTimeParameterAdapter


class ParametersAdapterFactory(QObject):
    """
    The general one dimensional handler. The one that delegates on each of the corresponding one dimensional handlers
    to do the job.
    This class inherits from QObject to be able to use translations. A valid parent must be supplied on __init__
    """

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._handlers_by_name = {
            'Start Time': StartTimeParameterAdapter(parent),
            'End Time': EndTimeParameterAdapter(parent)
        }
        self._handlers_by_class = {handler.get_parameter_class(): handler for _, handler in
                                   self._handlers_by_name.items()}

    def get_parameters_names(self):
        """
        Gets the name of all registered one dimensional transforms.
        :return: a list of str, each the name of one transform
        """
        return self._handlers_by_name.keys()

    def get_parameter(self, name):
        """
        Gets an instance of the corresponding one dimensional transform given its name.
        :param name: a str, the name of the transform. Must be one of the values returned by the get_all_transforms_names method.
        :return: an instance of the corresponding one dimensional transform
        """
        return self._handlers_by_name[name].get_parameter_instance()

    def get_settings(self, parameter):
        """
        Gets the settings of the corresponding one dimensional transform with the values of the supplied instance
        :param parameter: the one dimensional transform instance from which to take the values
        :return: a list of dicts in the way needed to create the param tree
        """
        return self._handlers_by_class[parameter.__class__].get_settings(parameter)
