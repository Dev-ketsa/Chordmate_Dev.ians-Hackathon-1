import pyaudio
import numpy as np
import os, sys, contextlib

CHUNK = 4096
RATE = 44100

@contextlib.contextmanager
def ignore_stderr():
    """Hides the ALSA/PortAudio system warnings."""
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(sys.stderr.fileno())
    try:
        os.dup2(devnull, sys.stderr.fileno())
        yield
    finally:
        os.dup2(old_stderr, sys.stderr.fileno())
        os.close(devnull)
        os.close(old_stderr)

class AudioStream:
    def __init__(self):
        with ignore_stderr():
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                                    input=True, frames_per_buffer=CHUNK)

    def read(self):
        raw_data = self.stream.read(CHUNK, exception_on_overflow=False)
        return np.frombuffer(raw_data, dtype=np.int16)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

def get_loudness(audio_data):
    return np.abs(audio_data).mean()