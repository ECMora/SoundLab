from duetto.audio_signals.Synthesizer import Synthesizer

# create a silence signal
signal = Synthesizer.generateSilence(samplingRate=44100,bitDepth=16,duration=1000)

print(signal.data)

print(signal.duration)

# create a white noise signal

signal = Synthesizer.generateWhiteNoise(samplingRate=44100, bitDepth=16, duration=1000)

print(signal.data)

print(signal.duration)


