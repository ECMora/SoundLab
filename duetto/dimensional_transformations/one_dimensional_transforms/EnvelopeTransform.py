# -*- coding: utf-8 -*-
from duetto.dimensional_transformations.one_dimensional_transforms.OneDimensionalTransform import OneDimensionalTransform
import numpy as np


class Envelope(OneDimensionalTransform):
    """
    This is a class inherited from OneDimensionalTransform that specifies a
    signal envelope computation and properties
    """
    def __init__(self, signal=None, decay=1., softFactor=6, functionType="sin"):
        # the processing options for the envelope transform
        self._decay = decay
        self._softFactor = softFactor
        self._functionType = functionType

        OneDimensionalTransform.__init__(self, signal=signal)

    #region Properties decay, softFactor, functionType

    @property
    def decay(self):
        return self._decay

    @decay.setter
    def decay(self, value):
        self._decay = value

    @property
    def softFactor(self):
        return self._softFactor

    @softFactor.setter
    def softFactor(self, value):
        self._softFactor = value


    @property
    def functionType(self):
        return self._functionType

    @functionType.setter
    def functionType(self, value):
        self._functionType = value

    #endregion

    def getData(self, indexFrom, indexTo):
            envelope = self.abs_decay_averaged_envelope(self.signal.data[indexFrom:indexTo], self.decay, self.softFactor,
                                                        self.functionType)
            bins = [self.signal.getTime(x) for x in np.arange(0, indexTo - indexFrom)]

            percent = []
            for index in np.arange(len(envelope)):
                val = envelope[index]
                if val == 0:
                    percent.append(0)
                else:
                    percent.append((val * 100)/self.signal.maximumValue)

            return (bins, percent)

    def abs_decay_averaged_envelope(self, data, decay=1., softfactor=6, type="sin"):
            """
            decay is the minThresholdLabel number of samples in data that separates two elements
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
