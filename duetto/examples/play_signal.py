from duetto.audio_signals import openSignal
from duetto.audio_signals.AudioSignalPlayer import AudioSignalPlayer

# open a signal
signal = openSignal("example.wav")

player = AudioSignalPlayer(signal)
player.playLoop = True
# play the sound
player.play()

# you can play the signal at different play speeds in % of the normal recording speed
# player.play(speed=200)

# you can play the signal at different play speeds in % of the normal recording speed
# player.play(speed=50)

# stop the thread to listen
x = raw_input()



