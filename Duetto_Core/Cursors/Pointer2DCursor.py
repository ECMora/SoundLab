from numpy import concatenate
from Duetto_Core.Cursors.Cursor import Cursor


class Pointer2DCursor(Cursor):
    def __init__(self, indexes=(0, 0)):
        Cursor.__init__(self)
        self.indexes = indexes

    def toByteArray(self):
        return concatenate((self.visualOptions.toByteArray(),
                            bytearray(self.intToByteArray(self.indexes[0])),
                            bytearray(self.intToByteArray(self.indexes[1]))))

    def fromByteArray(self, array):
        self.visualOptions.fromByteArray(array[0: -8])
        self.indexes = (self.byteArrayToInt(array[-8: -4]), self.byteArrayToInt(array[-4:]))

    def sizeInBytes(self):
        return 8
