from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation
import numpy as np


class FrequencyMeasurementLocation(MeasurementLocation):
    """
    A frequency location of measurement is an interval of the segment
    in which would be measured parameters. It defines an interval of frequency in
    which the measurement will be executed
    """

    def __init__(self, min_kHz=0, max_kHz=250, NFFT=512, overlap=50):
        # name of the measurement location
        MeasurementLocation.__init__(self, NFFT, overlap)

        # the freq interval in which would be measured
        # the parameters
        self.min_kHz = min_kHz
        self.max_kHz = max_kHz

        self.name = unicode(min_kHz) + u"-" + unicode(max_kHz) + u" kHz"

    def get_freq_limits(self, freqs):
        """
        computes and return the indexes of the current frecuency slice
        :param freqs: The array of frequencies
        :return:
        """
        min_freq = self.min_kHz * 1000
        max_freq = self.max_kHz * 1000

        return np.searchsorted(freqs, min_freq), np.searchsorted(freqs, max_freq)