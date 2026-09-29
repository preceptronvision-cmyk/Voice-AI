from faster_whisper import WhisperModel
from app.logger import logger
from app.config import config
import numpy as np
import time


class FasterWhisperSTT:
    """Speech-to-Text using faster-whisper."""

    def __init__(self, model_size=None, device=None, compute_type=None):
        self.model_size = model_size or config.WHISPER_MODEL
        self.device = device or config.WHISPER_DEVICE
        self.compute_type = compute_type or config.WHISPER_COMPUTE_TYPE

        logger.info(
            f"Loading Faster-Whisper model "
            f"({self.model_size}) on {self.device}..."
        )

        try:
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )

            logger.info("Faster-Whisper model loaded successfully.")

        except Exception as e:
            logger.error(f"Failed to load Faster-Whisper: {e}")
            raise

    def transcribe(self, audio_array: np.ndarray) -> str:

        # Ensure 1D array
        audio_array = audio_array.flatten().astype(np.float32)

        # Audio duration
        audio_duration = len(audio_array) / config.AUDIO_SAMPLE_RATE

        # Start timing
        start_time = time.perf_counter()

        # Transcribe
        segments, info = self.model.transcribe(
            audio_array,
            beam_size=5,
            language=config.TRANSCRIPTION_LANGUAGE,
            task=config.TRANSCRIPTION_TASK,
            vad_filter=False,
            without_timestamps=True,
            condition_on_previous_text=False
        )

        transcript = ""

        for segment in segments:
            transcript += segment.text

        # End timing
        processing_time = time.perf_counter() - start_time

        # Real-time factor
        if audio_duration > 0:
            realtime_factor = processing_time / audio_duration
        else:
            realtime_factor = 0

        logger.info(
            f"Whisper: audio={audio_duration:.2f}s | "
            f"processing={processing_time:.2f}s | "
            f"RTF={realtime_factor:.2f}x"
        )

        return transcript.strip()