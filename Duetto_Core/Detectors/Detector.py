from numpy import *
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor

class Detector:

    def __init__(self):
        self.pointers=[]
        self.intervals=[]
        self.rectangles=[]

    def detect(self,signal):
        pass

    def cursors(self):
        for c in self.intervals:
            yield c
        for c in self.pointers:
            yield c
        for c in self.rectangles:
            yield c

