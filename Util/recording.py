__author__ = 'Andres'

from array import array
from struct import pack
import wave

import pyaudio
from scipy.signal import medfilt
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
        y1 = medfilt(r, 3)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return sample_width, y1


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


rec = recording()
rec.record_to_file("pip.wav")