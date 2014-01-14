from string import join
from numpy import *
from numpy.ma import left_shift
from Duetto_Core.Storable import Storable

class LineType:
#    Enum for the visual options of the line
    DOT,FULL=range(2)
ARRAYLENGTH=5


class CursorOptions(Storable):

    def __init__(self):
        self.lineWidth=1
        self.lineType=LineType.DOT
        self.oscilogramCursor=True
        self.vertical=True
        self.visible=True
        self.comment=""

    def clone(self):
        copy=CursorOptions()
        copy.lineWidth=self.lineWidth
        copy.lineType=self.lineType
        copy.oscilogramCursor=self.oscilogramCursor
        copy.vertical=self.vertical
        copy.visible=self.visible
        copy.comment=self.comment
        return copy

    def toByteArray(self):
        return bytearray([self.lineWidth,self.lineType,self.oscilogramCursor,
                              self.vertical,self.visible])



    def fromByteArray(self,array):
        if(len(array)<ARRAYLENGTH):
            raise "Array to short"
        self.lineWidth=int(array[0])
        self.lineType=int(array[1])
        self.oscilogramCursor=bool(array[2])
        self.vertical=bool(array[3])
        self.visible=bool(array[4])



class Cursor(Storable):

    def __init__(self,lineWidth=1,lineType=LineType.DOT,comment="",oscilogramCursor=True,spectrogramCursor=False,vertical=True):
        self.visualOptions=CursorOptions()
        self.visualOptions.lineWidth=lineWidth
        self.visualOptions.lineType=lineType
        self.visualOptions.comment=comment
        self.visualOptions.oscilogramCursor=oscilogramCursor
        self.visualOptions.vertical=vertical

    def toByteArray(self):
        return self.visualOptions.toByteArray()
    def fromByteArray(self,array):
        self.visualOptions.fromByteArray(array)

    def intToByteArray(self,n,places=4):
        arr=[]
        while(n>0):
            arr.insert(0,n%256)
            n=n/256
        if(len(arr)<places):
            while(len(arr)<places):
                arr.insert(0,0)
            return arr
        return arr[-places:len(arr)]

    def byteArrayToInt(self,array):
        n=array[0]
        for i in range(1,len(array)):
            n*=256
            n+=array[i]
        return n

    def sizeInBytes(self):
        return -1
