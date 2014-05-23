# -*- coding: utf-8 -*-
import os
from scipy.io import wavfile
from numpy.compat import asbytes
from numpy import argmax,sum,abs
import struct
import random
from Duetto_Core.AudioSignals.FileAudioSignal import FileAudioSignal


class WavFileSignal(FileAudioSignal):
    """
    class that represents a signal from a file in the local file system
    """

    # if path is supplied the rest of the arguments are ignored
    # otherwise a new signal is created with the value of the other arguments
    def __init__(self, path=None, samplingRate=44100, duration=5, bitDepth=16, whiteNoise=False):
        FileAudioSignal.__init__(self)
        self.small = None
        if path:
            self.open(path)
            self.name = os.path.basename(unicode(self.path))
        else:
            self.openNew(samplingRate, duration, bitDepth, whiteNoise)
        self.userData = []


    def open(self, path):
        """open a wav file for its processing"""
        FileAudioSignal.open(self, path)
        self.read(path)

        self.removeDCOffset()
        self.channelData = [self.data[:, i] for i in range(self.channels)] if self.channels > 1 else [self.data]
        self.data = self.channelData[0]
        #self.pad()
        self.path=path

    def smallSignal(self):
        if  len(self.data) < 0.1 * self.samplingRate: #<100 ms
            return self
        if self.small is not None:
            return self.small
        s = WavFileSignal(samplingRate=self.samplingRate, duration=0.04, bitDepth=self.bitDepth, whiteNoise=False)

        #10 intervals of 3 ms sep by 1 ms of  silence
        i_max,media = argmax(self.data),sum(abs(self.data))/len(self.data)

        ms = int(self.samplingRate/1000)

        aux =  self.data[max(i_max-1.5*ms , 0): min(i_max+1.5*ms,len(self.data))]
        s.data[16*ms : 16*ms+aux.size] = aux

        for i in range(0,10):
            if i == 4:
                continue
            try:
                x = random.randint(0,10)
                index =i*len(self.data)/10+x*len(self.data)/100
                s.data[i * 4 * ms: (i * 4 + 3) * ms] = self.data[index:index + 3 * ms]
            except:
                pass
        self.small = s
        return s

    def read(self, file):
        if hasattr(file, 'read'):
            fid = file
        else:
            fid = open(file, 'rb')
        fsize = wavfile._read_riff_chunk(fid)
        noc = 1
        bits = 8
        while fid.tell() < fsize:
            # read the next chunk
            chunk_id = fid.read(4)
            if chunk_id == asbytes('fmt '):
                size, comp, noc, self.samplingRate, sbytes, ba, bits = wavfile._read_fmt_chunk(fid)
                self.bitDepth = bits
                self.channels = noc
            elif chunk_id == asbytes('data'):
                data = wavfile._read_data_chunk(fid, noc, bits)
                self.data = data
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

    def save(self, path="", chunk=bytearray([])):
        """saves to a file the signal on self.data with the corresponding chunk"""
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
        data = self.data
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
        size = struct.unpack(fmt, fid.read(4))[0]
        data = fid.read(size)
        return data

    #def loadSource(self):
    #    self.AudioPlayer.setCurrentSource(Phonon.MediaSource(self.TEMP_FILE_NAME))
    #    self.save(self.TEMP_FILE_NAME)
    #    self.AudioPlayer.setCurrentSource(Phonon.MediaSource(self.TEMP_FILE_NAME))


