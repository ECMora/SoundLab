from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal

def on_newDataRecorded(frame_count):
    print(frame_count)


a = WavFileSignal()
a.recordNotifier = on_newDataRecorded

a.record()

b = raw_input()