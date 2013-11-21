from matplotlib.colors import ListedColormap
import matplotlib.mlab as mlab
import numpy

"Clase que implementa los metodos" \
" para el trabajo con distintas ventanas en el spectrograma"
class FFTWindows:
    def rectangular(self,M):
        "La doc de kaiser indica que con beta=0 es similar a una ventana rectangular"
        return numpy.kaiser(len(M),0)
    def kaiser(self,M):
        return numpy.kaiser(len(M),14)
    def blackman(self,M):
        return numpy.blackman(len(M))
    def bartlett(self,M):
        return numpy.bartlett(len(M))
    def hamming(self,M):
        return numpy.hamming(len(M))

class SpecgramSettings:
    """Struct for the representation of usefull FFT params"""
    fwin=FFTWindows()
    windows=[fwin.hamming,
             fwin.rectangular,
             mlab.window_hanning,
             fwin.blackman,
             fwin.bartlett,
             fwin.kaiser,
             mlab.window_none]

    def __init__(self,NFFT=512,overlap=32,window=windows[0]):
        self.NFFT=NFFT
        self.overlap=overlap
        self.window=window
        self.colors=[]
        regularlcolor=[[.0,.0,.0]]
        #make alist with the colors ordered
        gray=[]
        for i in range(1,100):
            gray.append([1-0.01*i,1-0.01*i,1-0.01*i])
        self.colors.append(gray)
        self.colors.append(gray)


        self.colorPalette=ListedColormap(self.colors[0],name="DuettoColorMap")
        self._colorPaleteIndex=0#the color palette with the specgram is displayed its a matplotlib.cm.Colormap object
        self.threshold=5#the % of the specgram that is visible
        self.grid=False

    def _getColorPaleteIndex(self):
        return self._colorPaleteIndex
    def _setColorPaleteIndex(self, value):
        self._colorPaleteIndex=0 if value > len(self.colors) else value
        self.colorPalette=ListedColormap(self.colors[self._colorPaleteIndex],name="DuettoColorMap")

    colorPaleteIndex= property(_getColorPaleteIndex, _setColorPaleteIndex)

