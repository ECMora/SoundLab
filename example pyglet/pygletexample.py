
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from pyqtgraph.ptime import time
#app = QtGui.QApplication([])
#
#p = pg.plot()
#p.setWindowTitle('pyqtgraph example: PlotSpeedTest')
#
#signal = WavFileSignal()
#
#signal.open("..\\..\\ficheros de audio\\Playback_1.wav")
#p.setRange(QtCore.QRectF(0, -(2**(signal.bitDepth-1)), len(signal.data), 2**signal.bitDepth))
#curve = p.plot(signal.data[::10])
#
#
#
#
#
#
#
### Start Qt event loop unless running in interactive mode.
#if __name__ == '__main__':
#    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()
pg.