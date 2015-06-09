__author__ = 'Andres'
from sys import byteorder
from array import array
from struct import pack
import wave


try:
    import pyaudio

    CHECK_PYLIB = True
except ImportError:
    CHECK_PYLIB = False
from PySide import QtCore


class recording(QtCore.QThread):
    updateProgressS = QtCore.Signal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.THRESHOLD = 1000
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100
        self.RECORD_SECONDS = 2


    def is_silent(self, snd_data):
        print(max(snd_data))
        return max(snd_data) < self.THRESHOLD


    def normalize(self, snd_data):
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r


    def trim(self, snd_data):
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.THRESHOLD:
                    snd_started = True
                    r.append(i)
                elif snd_started:
                    r.append(i)
            return r

        snd_data = _trim(snd_data)

        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data


    def add_silence(self, snd_data, seconds):
        r = array('h', [0 for i in range(int(seconds * self.RATE))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self.RATE))])
        return r

    def record(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=1, rate=self.RATE,
                                  input=True, output=True,
                                  frames_per_buffer=self.CHUNK_SIZE)
        r = array('h')
        print("start recording", int(self.RATE / self.CHUNK_SIZE * self.RECORD_SECONDS))

        for i in range(0, int(self.RATE / self.CHUNK_SIZE * self.RECORD_SECONDS)):
            snd_data = array('h', self.stream.read(self.CHUNK_SIZE))
            r.extend(snd_data)
            self.updateProgressS.emit(i + 1)
        print("stop recording")
        sample_width = self.p.get_sample_size(self.FORMAT)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return sample_width, r


    def record_one(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=1, rate=self.RATE,
                                  input=True, output=True,
                                  frames_per_buffer=self.CHUNK_SIZE)
        num_silent = 0
        snd_started = False

        r = array('h')
        print("start recording")
        while 1:

            snd_data = array('h', self.stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.is_silent(snd_data)
            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 30:
                break
        print("stop recording")
        sample_width = self.p.get_sample_size(self.FORMAT)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        # r = normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.5)
        return sample_width, r


    def record_to_file(self, path):
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()


    """
    def play_wav(path):
        # open a wav format music
        f = wave.open(path, "rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        #open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        #read data
        data = f.readframes(CHUNK_SIZE)

        #paly stream
        while data != '':
            stream.write(data)
            data = f.readframes(CHUNK_SIZE)

        #stop stream
        stream.stop_stream()
        stream.close()

        #close PyAudio
        p.terminate()

    """