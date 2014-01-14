from Duetto_Core.SignalProcessors.SignalProcessor import envelope
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from matplotlib.pylab import *
import math
#wav = WavFileSignal()
#wav.open("..\\..\\ficheros de audio\\Clasif\\c5.wav")


#for i in wav.data:
#    print(i)
#print("************************")

#x= envelope(wav.data, decay=500)
#plot(x)
#show()

a= [1, 2,3,6,12, 24  , 56 ,148 , 473 ,2034,14798 ,  372049, 39054730,74767615,49046,49046,  748, 748,66, 66,11]

print(sum(a)/128)