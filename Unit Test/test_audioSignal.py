from unittest import TestCase
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal


class TestAudioSignal(TestCase):
    def test_play(self):
        for i in range(1000,20000,1000):
            sound = AudioSignal()
            sound.openNew(i,1,16,False)
            self.assertIsNone(sound.stream,"Stream is not none before play")
            sound.play()
            self.assertIsNotNone(sound.stream,"Stream is none after play")
            self.checkMetadata(sound,i,16,i,1)
            self.assertEqual(sound.playStatus,AudioSignal.PLAYING,"Fail the play")

    def checkMetadata(self,sound=None,samplingRate=0,bitDepth=0,duration=0,channels=0):
        if sound is None:
            return
        self.assertEqual(sound.samplingRate,samplingRate,"Wrong samplingRate")
        self.assertEqual(sound.bitDepth,bitDepth,"Wrong bitDepth")
        self.assertEqual(len(sound.data),duration,"Wrong duration")
        self.assertEqual(sound.channels,channels,"Wrong amount of channels")


    def test_stop(self):
        for i in range(1000,20000,1000):
            sound = AudioSignal()
            sound.openNew(i,1,16,False)
            # self.assertIsNone(sound.stream,"Stream is not none before play")
            # sound.play()
            # self.assertIsNotNone(sound.stream,"Stream is none after play")
            sound.stop()
            self.assertIsNone(sound.stream,"Stream is not none before play")
            self.checkMetadata(sound,i,16,i,1)
            self.assertEqual(sound.playStatus,AudioSignal.STOPPED,"Fail the play")

    def test_pause(self):
        self.fail()

    def test_record(self):
        self.fail()