import numpy as np
from numpy import fft
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal

signal = WavFileSignal()
signal.generateWhiteNoise(1000)
signal.save("signal.wav")

def record():
    pass

def play():
    pass

def compare(signal,signal2):
    pass