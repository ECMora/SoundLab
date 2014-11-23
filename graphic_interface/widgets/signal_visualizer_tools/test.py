from PyQt4.QtCore import QTimer
from PyQt4.QtGui import *
from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager
from graphic_interface.widgets.SoundLabSpectrogramWidget import SoundLabSpectrogramWidget
from graphic_interface.widgets.SoundLabOscilogramWidget import SoundLabOscilogramWidget
from graphic_interface.widgets.QSignalVisualizerWidget import QSignalVisualizerWidget


app = QApplication([])
# w = SoundLabOscilogramWidget()
# w = SoundLabSpectrogramWidget()
w = QSignalVisualizerWidget()

s = WavStreamManager().read(open("1.wav"))
# t = QTimer()
# t.timeout.connect(w.c)
# t.start(4000)
w.signal = s
w.graph()
w.show()
app.exec_()


