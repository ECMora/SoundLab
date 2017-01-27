from PyQt4.QtGui import *
import sys
from duetto.audio_signals import openSignal
from duetto.widgets.OscillogramWidget import OscillogramWidget


app = QApplication([])

signal = openSignal("example.wav")

osc_widget = OscillogramWidget()

# set the signal to the widget
osc_widget.signal = signal

# graph the signal
osc_widget.graph()

# could be visualized just a section of the signal
# osc_widget.graph(indexFrom=0,indexTo=signal.length/2)

sys.exit(app.exec_())




