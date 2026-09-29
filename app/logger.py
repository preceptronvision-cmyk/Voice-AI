import logging
import os


def setup_logger():
    logger = logging.getLogger("VoiceAI")
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if not logger.handlers:

        # Create logs directory
        os.makedirs("logs", exist_ok=True)

        # Log file
        file_handler = logging.FileHandler(
            "logs/voice_ai.log",
            encoding="utf-8"
        )

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)

        # Only write logs to file
        logger.addHandler(file_handler)

        # Suppress chatty external libraries
        logging.getLogger("faster_whisper").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("multipart").setLevel(logging.WARNING)

    return logger


logger = setup_logger()