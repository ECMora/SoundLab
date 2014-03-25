import pyqtgraph.examples
import pyqtgraph as pg
#pyqtgraph.examples.run()
import numpy as np
app = pg.QtGui.QApplication([])
x2 = np.linspace(-100, 100, 1000)
data2 = np.sin(x2) / x2
p8 = pg.PlotWidget(title="Region Selection")
p8.plot(data2, pen=(255,255,255,200))
lr = pg.LinearRegionItem([400,700])
p8.addItem(lr)
p8.show()
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.instance().exec_()
