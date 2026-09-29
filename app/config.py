import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    APP_NAME = os.getenv("APP_NAME", "Voice AI")
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    WS_HOST = os.getenv("WS_HOST", "localhost")
    WS_PORT = int(os.getenv("WS_PORT", "8000"))
    
    AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", "1"))
    AUDIO_CHUNK_SIZE = int(os.getenv("AUDIO_CHUNK_SIZE", "512"))
    AUDIO_WINDOW_SECONDS = int(os.getenv("AUDIO_WINDOW_SECONDS", "3"))
    AUDIO_OVERLAP_SECONDS = int(os.getenv("AUDIO_OVERLAP_SECONDS", "1"))

    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
    WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
    WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

    TRANSCRIPTION_LANGUAGE = os.getenv("TRANSCRIPTION_LANGUAGE", "en")
    TRANSCRIPTION_TASK = os.getenv("TRANSCRIPTION_TASK", "transcribe")

config = Config()
