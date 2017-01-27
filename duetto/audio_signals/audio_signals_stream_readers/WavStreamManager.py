from io import SEEK_CUR
import struct
import numpy as np
from scipy.io import wavfile
from numpy.compat import asbytes
import pickle
from duetto.audio_signals.AudioSignal import AudioSignal
from duetto.audio_signals.audio_signals_stream_readers.AudioStreamManager import AudioStreamManager


def _as_signed(data):
    """
    Returns an array with the values of data as signed integers. If the values of data are signed integers, data
    itself is returned. If the original values are unsigned integers the returned array is such that for the lowest
    original values, negative integers are returned, maintaining the original differences between all values.
    :param data: A numpy ndarray of signed or unsigned integers.
    """
    if data.dtype.str[1] == 'u':
        return (data - (1 << (data.dtype.itemsize * 8 - 1))).astype(data.dtype.str.replace('u', 'i'))
    return data


def _as_unsigned(data):
    """
    Returns an array with the values of data as unsigned integers. If the values of data are unsigned integers, data
    itself is returned. If the original values are signed integers the returned array is such that for negative
    original values, the lowest (closest to 0) integers are returned, maintaining the original differences between
    all values.
    :param data: A numpy ndarray of signed or unsigned integers.
    """
    if data.dtype.str[1] == 'i':
        return (data + (1 << (data.dtype.itemsize * 8 - 1))).astype(data.dtype.str.replace('i', 'u'))
    return data


class WavStreamManager(AudioStreamManager):
    """
    Class that can read and write audio signals from and to streams in WAV format.
    """

    def __init__(self):
        AudioStreamManager.__init__(self)

    def read(self, stream):
        """
        Reads an audio signal from a given readable and seekable stream in WAV format. Returns the read signal. The
        stream is closed after it is read.
        :param stream: An instance of a class derived from io.IOBase.
            The stream from which to read. A call to its readable() and seekable() methods must return True. Its
            contents must be in WAV format, otherwise an exception is raised.
        """
        # assert stream.readable(), 'Stream to read from is not readable.'
        # assert stream.seekable(), 'Stream to read from is not seekable.'

        # noinspection PyPep8Naming
        rate, bits, noc, userData, data = self._open(stream)

        # samples in 8-bit wav files are stored as unsigned integers
        # we convert them because AudioSignal works only with signed integer samples, no matter the bit depth
        data = _as_signed(data)
        if noc > 1:
            # noinspection PyPep8Naming
            channelData = [data[:, i] for i in range(noc)]
        else:
            # noinspection PyPep8Naming
            channelData = [data]

        signal = AudioSignal(rate, bits, noc, channelData[0], False)

        # dumps the byte array
        try:
            signal.extraData = pickle.loads(userData)
        except KeyError as ex:
            pass
        except EOFError as ex:
            pass

        for i in range(1, noc):
            signal.update_channel(channelData[i], i)

        return signal

    def _open(self, stream):
        """
        Reads a stream that contains an wav signal. Returns a tuple containing sampling rate, bit depth, number of
        channels, user data, and data in that order. Before returning it closes the stream.
        :param stream: An instance of a class derived from io.IOBase.
            The stream from which to read. A call to its readable() and seekable() methods must return True. Its
            contents must be in WAV format, otherwise an exception is raised.
        """
        # read the first chunk (the riff chunk), contains the size and a way to know this is a WAV stream
        fsize = wavfile._read_riff_chunk(stream)

        noc = 1
        bits = 16
        rate = 44100
        # pickle.dumps('')
        # noinspection PyPep8Naming
        userData = ''
        data = None

        # read each chunk
        while stream.tell() < fsize:
            chunk_id = stream.read(4)

            if chunk_id == asbytes('fmt '):
                # read fmt chunk, contains all metadata
                size, comp, noc, rate, sbytes, ba, bits = wavfile._read_fmt_chunk(stream)
            elif chunk_id == asbytes('data'):
                # read data chunk
                data = wavfile._read_data_chunk(stream, noc, bits)
            elif chunk_id == asbytes('duet'):
                # chunk of extra data stored in the file
                # noinspection PyPep8Naming
                userData = self._readUserChunk(stream)
            else:
                # ignore unknown chunk
                dt = stream.read(4)
                if wavfile._big_endian:
                    fmt = '>i'
                else:
                    fmt = '<i'
                size = struct.unpack(fmt, dt)[0]
                stream.seek(size, SEEK_CUR)

        stream.close()
        return rate, bits, noc, userData, data

    def write(self, audioSignal, stream):
        """
        Writes an audio signal to a given writable and seekable stream in WAV format. Returns nothing. The stream is
        closed after writing to it.
        :param audioSignal: An instance of AudioSignal.
            The signal to be written to the stream.
        :param stream: An instance of a class derived from io.IOBase.
            The stream in which to write. A call to its writable() and seekable() methods must return True.
        :param userData: A bytearray.
            Extra data to be written to the stream.
        """
        # assert stream.writable(), 'Stream to write to is not writable.'
        # assert stream.seekable(), 'Stream to write to is not seekable.'

        # write riff chunk (the size is set to 0 and changed at the end)
        stream.write(asbytes('RIFF'))
        stream.write(asbytes('\x00\x00\x00\x00'))
        stream.write(asbytes('WAVE'))

        # write fmt chunk
        stream.write(asbytes('fmt '))
        noc = audioSignal.channelCount
        rate = audioSignal.samplingRate
        bits = audioSignal.bitDepth
        sbytes = audioSignal.samplingRate * (bits // 8) * noc
        ba = noc * (bits // 8)
        stream.write(struct.pack('<ihHIIHH', 16, 1, noc, rate, sbytes, ba, bits))

        # write user chunk
        # noinspection PyPep8Naming
        extraData = pickle.dumps(audioSignal.extraData)
        stream.write(asbytes('duet'))
        stream.write(struct.pack('<i', len(extraData)))
        stream.write(extraData)

        # data chunk
        stream.write(asbytes('data'))
        # get the data from all the channels in the correct format to be written using the tofile method
        data = np.array(audioSignal.channelData).transpose()

        # samples in 8-bit wav files must be stored as unsigned integers
        # we must convert them because AudioSignal works only with signed integer samples, no matter the bit depth
        if audioSignal.bitDepth == 8:
            data = _as_unsigned(data)

        stream.write(struct.pack('<i', data.nbytes))
        import sys
        # if big endian, swap bytes of data before writing
        if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and sys.byteorder == 'big'):
            data = data.byteswap()
        data.tofile(stream)

        # determine file size and place it in correct position at start of the file.
        size = stream.tell()
        stream.seek(4)
        stream.write(struct.pack('<i', size - 8))

        stream.close()

    def _readUserChunk(self, stream):
        """
        Read the extra chunk of data stored in the file
        :param stream:
        """
        if wavfile._big_endian:
            fmt = '>i'
        else:
            fmt = '<i'

        size = struct.unpack(fmt, stream.read(4))[0]
        data = stream.read(size)
        return str(data)
