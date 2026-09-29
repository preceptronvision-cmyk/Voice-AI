import sounddevice as sd
import numpy as np
from app.logger import logger
from app.config import config
from app.audio.buffer import AudioBuffer

class MicrophoneStream:
    """
    Context manager that reads audio from the microphone and places it into an AudioBuffer.
    """
    def __init__(self, sample_rate=None, channels=None, blocksize=None, device=None):
        self.sample_rate = sample_rate or config.AUDIO_SAMPLE_RATE
        self.channels = channels or config.AUDIO_CHANNELS
        self.blocksize = blocksize or config.AUDIO_CHUNK_SIZE
        self.device = device
        self.buffer = AudioBuffer()
        self.stream = None
        
    def _audio_callback(self, indata, frames, time, status):
        """This is called for each audio block by sounddevice."""
        if status:
            logger.warning(f"Audio stream status: {status}")
        
        # indata is a numpy array (frames x channels)
        # We make a copy because the underlying buffer can be reused
        self.buffer.put(indata.copy())
        
    def __enter__(self):
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32',
            blocksize=self.blocksize,
            device=self.device,
            callback=self._audio_callback
        )
        self.stream.start()
        logger.info(f"Microphone stream started ({self.sample_rate}Hz, {self.channels} channels).")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            logger.info("Microphone stream stopped.")
            
    def read_chunk(self, block=True, timeout=None):
        """Reads the next chunk from the internal buffer."""
        try:
            return self.buffer.get(block=block, timeout=timeout)
        except Exception:
            return None
