from numpy import concatenate
from Duetto_Core.Cursors.Cursor import Cursor



class PointerCursor(Cursor):

    def __init__(self,index=0):
        Cursor.__init__(self)
        self.index=index
    def toByteArray(self):
        return concatenate((self.visualOptions.toByteArray(),
                            bytearray(self.intToByteArray(self.index))))
    def fromByteArray(self,array):
        self.visualOptions.fromByteArray(array[0:-4])
        self.index=self.byteArrayToInt(array[-4:len(array)])
    def sizeInBytes(self):
        return 4




