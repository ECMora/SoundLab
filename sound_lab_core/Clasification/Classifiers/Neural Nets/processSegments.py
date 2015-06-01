import pickle
import os

from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager
import numpy as np

from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement
from sound_lab_core.ParametersMeasurement.TimeParameters.DurationTimeParameter import DurationTimeParameter
from sound_lab_core.ParametersMeasurement.TimeParameters.RmsTimeParameter import RmsTimeParameter
from sound_lab_core.ParametersMeasurement.TimeParameters.StartToMaxTimeParameter import StartToMaxTimeParameter
from sound_lab_core.ParametersMeasurement.TimeParameters.ZeroCrossRateParameter import ZeroCrossRateParameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.BandWidthParameter import BandWidthParameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.MaxFreqParameter import MaxFreqParameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.MinFreqParameter import MinFreqParameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeakFreqParameter import PeakFreqParameter
from sound_lab_core.ParametersMeasurement.SpectralParameters.PeaksAboveParameter import PeaksAboveParameter
from sound_lab_core.ParametersMeasurement.WaveParameters import PeakToPeakParameter, LocalMaxMeanParameter


class SegmentsReader:

    param_measurers = [DurationTimeParameter(), LocalMaxMeanParameter(), #EntropyTimeParameter(),
                       PeakToPeakParameter(), RmsTimeParameter(), StartToMaxTimeParameter(),
                       ZeroCrossRateParameter(), BandWidthParameter(), MaxFreqParameter(), MinFreqParameter(),
                       PeakFreqParameter(), PeaksAboveParameter()]

    measures = None

    def import_segments_to_duetto_db(self):
        pass

    def load_signals_from_class(self,classPath, className):
        wavMng = WavStreamManager()
        self.measures = None

        for dirPath, _ , files in os.walk(classPath):

            for file in files:

                with open(dirPath+'/'+file, 'rb') as f:
                    signal = wavMng.read(f)

                other = self.measure_signal_segments(signal)
                if self.measures is None:
                    self.measures = other
                else: self.measures = np.concatenate((self.measures, other),axis=0)

        with open(classPath + '/' + className, 'wb') as f:
            pickle.dump(self.measures, f)

    def measure_signal_segments(self,signal):

        elements = []
        elements_measure = None

        for init, end in signal.extraData:
            elements.append(OneDimensionalElement(signal,int(init*signal.samplingRate), int(end*signal.samplingRate)))

        for element in elements:
            measure = np.array([],dtype=np.float64)

            for measurer in self.param_measurers:
                result = measurer.measure(element)
                measure = np.concatenate((measure, np.array([result])), axis=0)

            if elements_measure is None:
                elements_measure = np.array([measure])
            else: elements_measure = np.concatenate((elements_measure, np.array([measure])), axis=0)

        return elements_measure

classPath = 'D:/Duetto/Clasificacion(Redes Neuronales)/NeuralNetClassifier/Segments/'
classNames = ['FMC', 'FMCa', 'FL', 'FML']

for className in classNames:

    sr = SegmentsReader()
    sr.load_signals_from_class(classPath + className, className)
    print('segments class ' + className + ' finished.')