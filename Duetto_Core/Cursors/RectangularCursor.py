from numpy import concatenate
from Duetto_Core.Cursors.Cursor import Cursor
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor

class RectangularCursor(Cursor):

    def __init__(self):
        Cursor.__init__(self)
        self.intervalX=IntervalCursor()
        self.intervalY=IntervalCursor()

    def shift(self,valueX,valueY):
        self.intervalX.shift(valueX)
        self.intervalY.shift(valueY)
    def toByteArray(self):
        return concatenate((self.visualOptions.toByteArray(),
                     bytearray(self.intervalX.toByteArray()),
                     bytearray(self.intervalY.toByteArray())))

    def fromByteArray(self,array):
        self.visualOptions.fromByteArray(array[0:-2*self.intervalX.sizeInBytes()])
        self.intervalX.fromByteArray(array[-2*self.intervalX.sizeInBytes():-self.intervalX.sizeInBytes()])
        self.intervalY.fromByteArray(array[-self.intervalX.sizeInBytes():len(array)])

