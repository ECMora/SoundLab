from WaveletMeanParameter import WaveletMeanParameter
from WaveletCentroidParameter import WaveletCentroidParameter
from WaveletDeltaParameter import WaveletDeltaParameter
from WaveletVarParameter import WaveletVarParameter

EPS = 1e-9
DEC_LEVEL = 6


#def fix(data, level):
#    min_pot2 = 1 << level
#    pot2 = 1
#    while pot2 < len(data) or pot2 < min_pot2:
#        pot2 <<= 1
#    new_data = np.zeros(pot2)
#    for i in range(len(data)):
#        new_data[i] = data[i]
#    return new_data
