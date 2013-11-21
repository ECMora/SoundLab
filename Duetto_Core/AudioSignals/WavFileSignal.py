from PyQt4.QtCore import QBuffer, QByteArray, QIODevice
from PyQt4.QtGui import QMessageBox
from PyQt4.phonon import *
import pyglet
from scipy.io import wavfile
from numpy.compat import asbytes
import struct
from Duetto_Core.AudioSignals.FileAudioSignal import FileAudioSignal

class WavFileSignal(FileAudioSignal):
    """
    class that represents a signal from a file in the local file system
    """
    def __init__(self):
        FileAudioSignal.__init__(self)
        self.channels=1
        self.userData=[]
        #self.sum=0
        #self.times=0.0



    def open(self,path):
        """open a wav file for its processing"""
        try:
            FileAudioSignal.open(self,path)
            self.read(path)
            self.path=path
            #source=Phonon.MediaSource(self.path)
            #so2=Phonon.MediaSource(QBuffer(QByteArray(bytes(self.data))))
            #self.AudioPlayer=Phonon.createPlayer(Phonon.MusicCategory,source)
            #self.AudioPlayer.prefinishMarkReached.connect(self.restartPlayer)
            #self.AudioPlayer.finished.connect(self.restartPlayer)
            self.AudioPlayer=pyglet.media.Player()
            source = pyglet.media.load(self.path)
            self.AudioPlayer.queue(source)

        except Exception, e:
            QMessageBox.warning(QMessageBox(),"Error","Could not load the file. "+e.message)

    def play(self, startIndex=0, endIndex=-1, speed=1):
        """
        plays the sound of the signal in the interval [startIndex:endIndex]
        with the specified speed %"""
        startIndex=startIndex*1000.0/self.samplingRate
        endIndex= endIndex if endIndex!=-1 else len(self.data)
        endIndex=endIndex*1000/self.samplingRate
        self.AudioPlayer.source.seek(startIndex*1000)

        #self.end=endIndex
        self.AudioPlayer.play()


    MS_DELAY=24 #delay in ms betwen the prefinish mark and the efective silence of the player
    TEMP_FILE_NAME="temp.wav"

    def stop(self):
         if(self.AudioPlayer != None):
            self.AudioPlayer._audio.stop()
    def pause(self):
        if(self.AudioPlayer != None):
            self.AudioPlayer.pause()

    def restartPlayer(self):
        #self.sum+=self.AudioPlayer.currentTime()-self.end
        #self.times=self.times+1
        #print("sum "+str(self.sum)+" times "+str(self.times)+" mean "+str(self.sum/self.times))
        if(self.AudioPlayer != None):
            self.AudioPlayer.source.stop()

    def read(self,file):
        if hasattr(file,'read'):
            fid = file
        else:
            fid = open(file, 'rb')
        fsize = wavfile._read_riff_chunk(fid)
        noc = 1
        bits = 8
        while (fid.tell() < fsize):
            # read the next chunk
            chunk_id = fid.read(4)
            if chunk_id == asbytes('fmt '):
                size, comp, noc, self.samplingRate, sbytes, ba, bits = wavfile._read_fmt_chunk(fid)
            elif chunk_id == asbytes('data'):
                data = wavfile._read_data_chunk(fid, noc, bits)
                self.data=data
            elif chunk_id == asbytes('uh++'):
                self.userData = self.readUserChunk(fid)
            else:
                data = fid.read(4)
                if wavfile._big_endian:
                    fmt = '>i'
                else:
                    fmt = '<i'
                size = struct.unpack(fmt, data)[0]
                fid.seek(size, 1)
        fid.close()


    def save(self, path="",chunk=bytearray([])):
        """saves to a file the signal on self.data with the correspondient chunk"""

        fid = open(path, 'wb')
        fid.write(asbytes('RIFF'))
        fid.write(asbytes('\x00\x00\x00\x00'))
        fid.write(asbytes('WAVE'))
        # fmt chunk
        fid.write(asbytes('fmt '))
        if self.data.ndim == 1:
            noc = 1
        else:
            noc = self.data.shape[1]
        bits = self.data.dtype.itemsize * 8
        sbytes = self.samplingRate*(bits // 8)*noc
        ba = noc * (bits // 8)
        fid.write(struct.pack('<ihHIIHH', 16, 1, noc, self.samplingRate, sbytes, ba, bits))

        #user chunk
        fid.write(asbytes('uh++'))
        fid.write(struct.pack('<i', len(chunk)))
        fid.write(chunk)

        # data chunk
        fid.write(asbytes('data'))
        fid.write(struct.pack('<i', self.data.nbytes))
        import sys
        data=self.data
        if self.data.dtype.byteorder == '>' or (self.data.dtype.byteorder == '=' and sys.byteorder == 'big'):
            data = self.data.byteswap()
        data.tofile(fid)
        # Determine file size and place it in correct
        #  position at start of the file.
        size = fid.tell()
        fid.seek(4)
        fid.write(struct.pack('<i', size-8))
        fid.close()

    def toWav(self):
        return self

    def readUserChunk(self, fid):
        if wavfile._big_endian:
            fmt = '>i'
        else:
            fmt = '<i'
        size = struct.unpack(fmt,fid.read(4))[0]
        data=fid.read(size)
        return data

    #def loadSource(self):
    #    self.AudioPlayer.setCurrentSource(Phonon.MediaSource(self.TEMP_FILE_NAME))
    #    self.save(self.TEMP_FILE_NAME)
    #    self.AudioPlayer.setCurrentSource(Phonon.MediaSource(self.TEMP_FILE_NAME))
