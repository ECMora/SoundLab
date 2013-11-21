from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from numpy import zeros
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
from Duetto_Core.Detectors.Detector import Detector

class SpectrogramHillDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.boolCopy=zeros((10,10),bool)

    def detect(self,signal,umbral,Pxx, freqs, bins):
        #gets the  relevant regions in spectrogram
        #in this version just insert a rectangular cursor

        self.boolCopy=zeros((len(Pxx),len(Pxx[0])),bool)
        regionsOverUmbral=[]

        for i  in range(len(Pxx)):
            for j in range(len(Pxx[i])):
                if(Pxx[i][j]>umbral):
                    self.boolCopy[i][j]=True
        for i  in range(len(Pxx)):
            for j in range(len(Pxx[i])):
                if(self.boolCopy[i][j]==True):
                    regionBounds=self.__islandDelete(i,j)
                    rc=IntervalCursor()
                    rc.visualOptions.oscilogramCursor=False
                    rc.min,rc.max=regionBounds[0],regionBounds[1]
                    self.intervals.append(rc)

    def __islandDelete(self,i,j):
        #delete a bolean (True and False) island in map with earth in the
        #i,j position
        #returns a tuple with the min row ,max row, min column, max column coordinates of the bool island
        df=[-1,-1,-1,0,1,1,1,0]
        dc=[-1, 0, 1,1,1,0,-1,-1]
        result=(i,i,j,j)
        self.boolCopy[i][j]=False
        for dir in range(len(df)):
            if(i+df[dir]>=0 and i+df[dir]<len(self.boolCopy) and
               j+dc[dir]>=0 and j+dc[dir]<len(self.boolCopy[i]) and self.boolCopy[i+df[dir]][j+dc[dir]]):
                best=self.__islandDelete(i+df[dir],j+dc[dir])
                result=(min(result[0],best[0]),max(result[1],best[1]),min(result[2],best[2]),max(result[3],best[3]))
        return result





#from collections import deque
#from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
#from numpy import zeros
#from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
#from Duetto_Core.Detectors.Detector import Detector
#
#class SpectrogramHillDetector(Detector):
#    def __init__(self):
#        Detector.__init__(self)
#        self.boolCopy=zeros((10,10),bool)
#        self.dic={}
#        self.a=0
#
#
#    def detect(self,signal,umbral,Pxx, freqs, bins, im):
#        #gets the  relevant regions in spectrogram
#        #in this version just insert a rectangular cursor
#
#        self.boolCopy=zeros((len(Pxx),len(Pxx[0])),bool)
#        self.df=[-1,-1,-1,0,1,1,1,0]
#        self.dc=[-1, 0, 1,1,1,0,-1,-1]
#
#        for i  in range(len(Pxx)):
#            for j in range(len(Pxx[i])):
#                if(Pxx[i][j]>umbral):
#                    self.boolCopy[i][j]=True
#                else:
#
#        print("comienzo a buscar")
#        for i  in range(len(Pxx)):
#            for j in range(len(Pxx[i])):
#                if(self.boolCopy[i][j]):
#                    print("buscando")
#                    regionBounds=self.__islandDelete(i,j)
#                    rc=IntervalCursor()
#                    rc.visualOptions.oscilogramCursor=False
#                    #rc.min,rc.max=bins[regionBounds[0]],bins[regionBounds[1]]
#                    rc.min,rc.max=regionBounds[0],regionBounds[1]
#                    self.intervals.append(rc)
#
#
#
#
#    def __islandDelete(self,i,j):
#        #delete a bolean (True and False) island in map with earth in the
#        #i,j position
#        #returns a tuple with the min row ,max row, min column, max column coordinates of the bool island
#        result=(i,i,j,j)
#        self.boolCopy[i][j]=False
#
#        queue=deque()
#        queue.append((i,j))
#
#        while(len(queue)>0):
#            print(len(queue))
#            elem=queue.popleft()
#            for dir in range(len(self.df)):
#                if(elem[0]+self.df[dir]>=0 and elem[0]+self.df[dir]<len(self.boolCopy) and
#                   elem[1]+self.dc[dir]>=0 and elem[1]+self.dc[dir]<len(self.boolCopy[elem[1]]) and self.boolCopy[elem[0]+self.df[dir]][elem[1]+self.dc[dir]]):
#                    queue.append((elem[0]+self.df[dir],elem[1]+self.dc[dir]))
#                    best=(elem[0]+self.df[dir],elem[0]+self.df[dir],elem[1]+self.dc[dir],elem[1]+self.dc[dir])
#                    result=(min(result[0],best[0]),max(result[1],best[1]),min(result[2],best[2]),max(result[3],best[3]))
#        return result
#
#
#







