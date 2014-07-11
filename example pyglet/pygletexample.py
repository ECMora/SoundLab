import numpy as np
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal

def envelope(data):
    i = j = 0
    diference = 3.0
    maximum = minimum = data[i]
    data = np.array(data, float)
    envelopedata = np.zeros(len(data), dtype=float)
    while i < len(data):
        if data[i] > minimum + diference or data[i] < maximum - diference:
            #maxi = np.max(data[j:(i-1)])
            envelopedata[j:i] = [maximum]*(i-j)
            j = i
            maximum = minimum = data[i]
        maximum = max(maximum, data[i])
        minimum = min(minimum, data[i])
        i = i + 1
    envelopedata[j:i] = [maximum]*(i-j)
    return envelopedata.tolist()


def gate(data, threshold):
    data = envelope(data)
    print data
    data = np.array(data, float)
    data = np.where(data > threshold, 1, 0)
    return data.tolist()


from pylab import plot,show
plot(envelope(abs((WavFileSignal("c1.wav").data))))
show()

#data = [x*random.randint(-6, 6)*0.3 for x in range(1, 6)]
#print data
#threshold = random.randint(4, 7)*0.6
#print threshold
#print gate(data, threshold)