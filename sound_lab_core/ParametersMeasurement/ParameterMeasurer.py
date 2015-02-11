# -*- coding: utf-8 -*-


class ParameterMeasurer:
    """
    Class that represent an object that measure parameters
    in segments.
    """

    def __init__(self):
        """
        Create a parameter measurer
        :return:
        """

        # the name of the parameter
        self._name = ""

    # region Parameter Name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, (str,unicode)):
            raise Exception("Invalid type for name. Must be str or unicode.")

        self._name = new_name

    # endregion

    def measure(self, segment):
        """
        Abstract method that performs the measure of the
        parameter over the supplied segment.
        :param segment:
        :return:
        """
        pass