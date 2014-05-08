
from Power_Spectrum import Ui_PowSpecWindow
from PyQt4 import QtGui,QtCore


class PowerSpectrumWindow(QtGui.QMainWindow):
    def __init__(self,parent=None,plotColor="FFF",backColor="FFF",gridx=True,gridy=True,minY=-50,maxY=5,lines=True):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.show()
        self.plotColor = plotColor
        self.backColor = backColor
        self.gridx = gridx
        self.gridy = gridy
        self.maxY = maxY
        self.minY = minY
        self.lines =lines
        self.ui.pow_spec.pow_spectrum.PointerChanged.connect(self.updateStatusBar)

    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def plot(self, data, rate, NFFT, window,overlap):

        self.NFFT = NFFT
        self.window = window
        self.rate = rate
        self.overlap = overlap
        self.ui.pow_spec.Plot_Power_Spectrum(data, self.rate, self.NFFT, self.window,self.overlap,self.plotColor, self.backColor, self.gridx, self.gridy,self.minY,self.maxY,self.lines)


    def updatePowSpectrumInterval(self,data):
        self.ui.pow_spec.Plot_Power_Spectrum(data,self.rate,self.NFFT,self.window,self.overlap,self.plotColor, self.backColor, self.gridx, self.gridy)

