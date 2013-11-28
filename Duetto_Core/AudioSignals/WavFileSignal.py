from PyQt4.QtGui import QMessageBox
import pyaudio
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




    def open(self,path):
        """open a wav file for its processing"""
        try:
            FileAudioSignal.open(self,path)
            self.read(path)
            self.path=path
            self.timer.stop()
            formatt=(pyaudio.paInt8 if self.bitDepth==8 else pyaudio.paInt16 if self.bitDepth==16 else pyaudio.paFloat32)
            self.stream =self.playAudio.open(format=formatt,
                            channels=self.channels,
                            rate=self.samplingRate,
                            output=True,
                            start=False,
                            stream_callback=self.callback())
        except Exception, e:
            QMessageBox.warning(QMessageBox(),"Error","Could not load the file. "+e.message)

    def play(self, startIndex=0, endIndex=-1, speed=100):
        """
        plays the sound of the signal in the interval [startIndex:endIndex]
        with the specified speed %"""
        if(self.playStatus==self.PLAYING):
            return
        if(self.playStatus==self.PAUSED):
            self.stream.start_stream()
            self.playStatus=self.PLAYING
            self.timer.start(self.tick)
            return

        self.playStatus=True
        formatt=(pyaudio.paInt8 if self.bitDepth==8 else pyaudio.paInt16 if self.bitDepth==16 else pyaudio.paFloat32)
        self.stream =self.playAudio.open(format=formatt,
                            channels=self.channels,
                            rate=self.samplingRate,
                            output=True,
                            start=False,
                            stream_callback=self.callback())

        endIndex=endIndex if endIndex!=-1 else len(self.data)
        self.stream._rate=int(self.samplingRate*speed/100.0)
        self.playSection=(startIndex,endIndex,startIndex)
        self.stream.start_stream()
        self.timer.start(self.tick)

    def stop(self):
        self.timer.stop()
        if(self.stream!=None and self.stream.is_active()):
            self.stream.stop_stream()
            self.stream.close()
        self.playStatus=self.STOPPED


    def pause(self):
        self.timer.stop()
        if(self.stream!=None and self.stream.is_active()):
            self.stream.stop_stream()
        self.playStatus=self.PAUSED


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
                self.bitDepth=bits
                self.channels=noc
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
