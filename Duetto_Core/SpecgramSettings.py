import matplotlib.mlab as mlab

import numpy

"Clase que implementa los metodos" \
" para el trabajo con distintas ventanas en el spectrograma"
class FFTWindows:
    def Hanning(self,M):
        return numpy.hanning(len(M))*M

    def Rectangular(self,M):
        "La doc de kaiser indica que con beta=0 es similar a una ventana rectangular"
        return numpy.kaiser(len(M),0)
    def Kaiser(self,M):
        return numpy.kaiser(len(M),14)
    def Blackman(self,M):
        return numpy.blackman(len(M))
    def Bartlett(self,M):
        return numpy.bartlett(len(M))
    def Hamming(self,M):
        return numpy.hamming(len(M))



    def WindowNone(self,M):
        return mlab.window_none(len(M))

class SpecgramSettings:
    """Struct for the representation of usefull FFT params"""
    fwin=FFTWindows()
    windows=[fwin.Hamming,
             fwin.Rectangular,
            fwin.Hanning,
             fwin.Blackman,
             fwin.Bartlett,
             fwin.Kaiser,
            fwin.WindowNone ]

    def __init__(self,NFFT=512,overlap=32,window=windows[0]):
        self.NFFT=NFFT
        self.overlap=overlap
        self.visualOverlap = overlap
        self.window=window
        #self.colorPalette=ListedColormap(self.colors[0],name="DuettoColorMap")

        self._colorPaletteIndex=0#the color palette with the specgram is displayed its a matplotlib.cm.Colormap object
        self.threshold=30#the % of the specgram that is not visible
        self.grid=False



