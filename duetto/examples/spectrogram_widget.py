from PyQt4.QtGui import *
import sys
from duetto.audio_signals import openSignal
from duetto.widgets.SpectrogramWidget import SpectrogramWidget


app = QApplication([])

signal = openSignal("example.wav")

spec_widget = SpectrogramWidget()

# is possible to select the histogram position and visibility
spec_widget = SpectrogramWidget(visible_histogram=True)
#
# spec_widget = SpectrogramWidget(visible_histogram=True,horizontal_histogram=False)

# set the signal to the widget
spec_widget.signal = signal

# graph the signal
spec_widget.graph()

# could be visualized just a section of the signal
spec_widget.graph(indexFrom=0,indexTo=signal.length/2)

sys.exit(app.exec_())


