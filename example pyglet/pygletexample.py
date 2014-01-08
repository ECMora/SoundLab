from Duetto_Core.SignalProcessors.SignalProcessor import envelope
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from matplotlib.pylab import *
import math
wav = WavFileSignal()
wav.open("..\\..\\ficheros de audio\\Clasif\c1.wav")


#for i in wav.data:
#    print(i)
#print("************************")

print(min(wav.data))

#
#plot(envelope(wav))
#
#show()



