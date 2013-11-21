from numpy import concatenate
from Duetto_Core.Cursors.Cursor import Cursor
from numpy.compat import asbytes
class IntervalCursor(Cursor):

    def __init__(self,minValue=0,maxValue=0):
        Cursor.__init__(self)
        self.min=int(minValue)
        self.max=int(maxValue)

    def shift(self,value):
        self.max+=value
        self.min+=value

    def toByteArray(self):
        return concatenate((self.visualOptions.toByteArray(),
                            bytearray(self.intToByteArray(self.min)),
                            bytearray(self.intToByteArray(self.max))))

    def fromByteArray(self,array):
        self.visualOptions.fromByteArray(array[0:-8])
        self.min=self.byteArrayToInt(array[-8:-4])
        self.max=self.byteArrayToInt(array[-4:len(array)])

    def sizeInBytes(self):
        return 8




