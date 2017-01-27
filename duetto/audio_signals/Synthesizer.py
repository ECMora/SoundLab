import numpy as np

from duetto.audio_signals import AudioSignal


class Synthesizer:
    """
    Class that provides several methods for the
    signal creation process.
    """

    @staticmethod
    def insertWhiteNoise(audio_signal=None, duration=1000,indexFrom=0):
        """
        Insertion of a white noise of duration "duration" into the signal audio_signal at position indexFrom.
        :return:
        """
        if audio_signal is None:
            audio_signal = AudioSignal()

        # generate the noise array
        data = np.array([int(np.random.uniform(audio_signal.minimumValue, audio_signal.maximumValue))
                            for _ in np.arange(duration * audio_signal.samplingRate/1000.0)], dtype=audio_signal.data.dtype)

        # create the noisy signal
        signal = AudioSignal(samplingRate=audio_signal.samplingRate,
                    bitDepth=audio_signal.bitDepth,
                    channelCount=audio_signal.channelCount,
                    data=data)

        audio_signal.insert(signal, indexFrom)
        audio_signal.insert(signal, indexFrom)
        signal.name = "unnamed"
        return audio_signal

    @staticmethod
    def generateSilence(samplingRate=44100, bitDepth=16, duration=1000):
        signal_data = np.zeros(duration * samplingRate/1000.0, dtype=np.int16)
        signal = AudioSignal(samplingRate=samplingRate,bitDepth=bitDepth,data=signal_data)
        signal.name = "unnamed"
        return signal

    @staticmethod
    def generateWhiteNoise(samplingRate=44100, bitDepth=16, duration=1000):
        signal = AudioSignal(samplingRate=samplingRate, bitDepth=bitDepth)
        signal.name = "unnamed"
        return Synthesizer.insertWhiteNoise(signal, duration=duration)



