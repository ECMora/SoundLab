
from Power_Spectrum import Ui_PowSpecWindow
from PyQt4 import QtGui


class PowerSpectrumWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.show()

    def plot(self, data, rate, NFFT, window):
        self.ui.pow_spec.Plot_Power_Spectrum(data, rate, NFFT, window)
        self.ui.pow_spec.draw()

