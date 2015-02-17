#  -*- coding: utf-8 -*-


class Element:
    """
    Represents the minimal piece of information to classify
    An element in an N dimensional transform of the signal. Is an N dimensional region
    that contains a superior energy that the fragment of signal near to it.
    Ej of 1 dimensional Transform : scale, normalize, oscilogram
    Ej of 2 dimensional Transform : spectrogram
    """

    def __init__(self, signal):
        # the signal in which this elements is defined
        self.signal = signal