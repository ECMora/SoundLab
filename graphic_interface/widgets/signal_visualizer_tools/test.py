from PyQt4.QtCore import QTimer
from PyQt4.QtGui import *
from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager
from graphic_interface.widgets.SoundLabSpectrogramWidget import SoundLabSpectrogramWidget
from graphic_interface.widgets.SoundLabOscilogramWidget import SoundLabOscilogramWidget
from graphic_interface.widgets.QSignalVisualizerWidget import QSignalVisualizerWidget

def x():
    w.copy()
    print(len(w.signal))
    w.paste()
    print("copiando")
    w.graph()

app = QApplication([])

# w = SoundLabOscilogramWidget()
# w = SoundLabSpectrogramWidget()
w = QSignalVisualizerWidget()

s = WavStreamManager().read(open("1.wav"))
t = QTimer()
t.timeout.connect(x)
t.start(2000)
w.signal = s
w.graph()
w.show()
app.exec_()


