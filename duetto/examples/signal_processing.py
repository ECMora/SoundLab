from PyQt4.QtGui import *
import sys
from duetto.audio_signals import openSignal
from duetto.widgets.OscillogramWidget import OscillogramWidget
from duetto.signal_processing.CommonSignalProcessor import CommonSignalProcessor


app = QApplication([])

signal = openSignal("example.wav")

signal_processor = CommonSignalProcessor(signal)

osc_widget = OscillogramWidget()

# set the signal to the widget
osc_widget.signal = signal

# graph the signal
osc_widget.graph()

# silence the signal
signal_processor.setSilence(0, signal.length / 2)

# reverse the signal
# signal_processor.reverse(0, signal.length / 2)

# positives values of  the signal data
# signal_processor.positivesValues(0, signal.length / 2)

# negatives values of  the signal data
# signal_processor.negativesValues(0, signal.length / 2)

sys.exit(app.exec_())


