# -*- coding: utf-8 -*-
from graphic_interface.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
import numpy as np


class Envelope(OneDimensionalTransform):
    def __init__(self, signal=None):
        # the processing options for the envelope one_dim_transform
        self.decay = 1.00
        self.softfactor = 6
        self.function_type = "sin"

        OneDimensionalTransform.__init__(self, signal=signal)

    def _getParameterTree(self):
        # create the tree with the params of the envelope one dim one_dim_transform
        params = [{u'name': unicode(self.tr(u'Envelope')), u'type': u'group',
                   u'children': [
                       {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': 1.00, u'step': 0.5},
                       {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'int', u'value': 6, u'step': 1},
                       {u'name': unicode(self.tr(u'Function Type')), u'type': u'list', u'value': "sin",
                        u'default': "sin",
                        u'values': [(u"Sin", "sin"),
                                    (u'Lineal', "lineal"),
                                    (u"Cuadratic", "cuadratic")]}
                   ]}]

        self.parameter = self._createParameter(params)

        # connect to register the changes on the param tree
        self.parameter.sigTreeStateChanged.connect(self.parameterChanged)

        return self._createParameterTree(self.parameter)

    def parameterChanged(self, param, changes):
        """
        Method that listen to the changes on the parameter tree and change the
        internal variables.
        :param param: The parameter tree
        :param changes: the changes made
        :return:
        """
        if self.parameter is None:
            return

        data_changed = False

        for param, change, data in changes:
            path = self.parameter.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Envelope')) + \
                    u'.' + unicode(self.tr(u'Decay (ms)'))and self.decay != data:

                self.decay = data
                data_changed = True

            elif childName == unicode(self.tr(u'Envelope')) + \
                    u'.' + unicode(self.tr(u'Soft Factor')) and self.softfactor != data:

                self.softfactor = data
                data_changed = True

            elif childName == unicode(self.tr(u'Envelope')) + \
                    u'.' + unicode(self.tr(u'Function Type')) and self.function_type != data:
                self.function_type = data
                data_changed = True

        if data_changed:
            self.dataChanged.emit()

    def getData(self, indexFrom, indexTo):
            envelope = self.abs_decay_averaged_envelope(self.signal.data[indexFrom:indexTo], self.decay, self.softfactor,
                                                        self.function_type)
            return envelope

    def abs_decay_averaged_envelope(self, data, decay=1, softfactor=6, type="sin"):
            """
            decay is the min number of samples in data that separates two elements
            """

            rectified = np.array(abs(data))

            i = 1
            arr = np.zeros(len(rectified), dtype=np.int32)
            current = rectified[0]
            fall_init = None

            while i < len(arr):
                if fall_init is not None:
                    value = rectified[fall_init]
                    if type == "lineal":
                        value -= rectified[fall_init] * (i - fall_init) / decay  # lineal
                    elif type == "sin":
                        value = rectified[fall_init] * np.sin(((i - fall_init) * 1.0 * np.pi) / (decay * 2) + np.pi / 2)
                    elif type == "cuadratic":
                        value = rectified[fall_init] * (1 - ((i - fall_init) * 1.0) / decay) ** 2

                    arr[i - 1] = max(value, rectified[i])
                    fall_init = None if (value <= rectified[i] or i - fall_init >= decay) else fall_init
                else:
                    fall_init = i - 1 if rectified[i] < current else None
                    arr[i - 1] = current
                current = rectified[i]
                i += 1

            arr[-1] = current

            if softfactor > 1:
                return np.array([np.mean(arr[i - softfactor:i]) for i, _ in enumerate(arr, start=softfactor)])
            return arr
