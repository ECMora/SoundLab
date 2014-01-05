from Duetto_Core.SignalProcessors.SignalProcessor import envelope
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from matplotlib.pylab import *
import math
wav = WavFileSignal()
wav.open("..\\..\\ficheros de audio\Clasif\\c1.wav")
print("YA")

plot(envelope(wav,decay=5))

show()



