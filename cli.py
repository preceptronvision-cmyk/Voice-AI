import sys
import argparse
import numpy as np
import sounddevice as sd
from app.stt.whisper import FasterWhisperSTT
from app.audio.microphone import MicrophoneStream
from app.config import config

def list_devices():
    print("🎙️ Available Audio Devices:")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"[{i}] {dev['name']}")
    print("\nDefault Input Device:", sd.default.device[0])

def strip_overlap(new_text, last_text):
    if not new_text or not last_text:
        return new_text
    new_words = new_text.split()
    last_words = last_text.split()
    for i in range(len(last_words)):
        suffix = " ".join(last_words[i:])
        if new_text.startswith(suffix):
            remaining = new_text[len(suffix):].strip()
            if remaining and remaining[0] in ".,!?":
                remaining = remaining[1:].strip()
            return remaining
    return new_text

def run_cli(device_idx=None):
    print("🎙️ Voice AI - Terminal Mode")
    print("===========================\n")
    
    stt = FasterWhisperSTT()
    
    sample_rate = config.AUDIO_SAMPLE_RATE
    window_samples = sample_rate * config.AUDIO_WINDOW_SECONDS
    overlap_samples = sample_rate * config.AUDIO_OVERLAP_SECONDS
    step_samples = window_samples - overlap_samples
    
    audio_buffer = np.array([], dtype=np.float32)
    last_transcript = ""
    
    print(f"\nListening on device {device_idx if device_idx is not None else 'default'}... (Press Ctrl+C to stop)")
    print("-" * 50)
    
    try:
        with MicrophoneStream(sample_rate=sample_rate, channels=1, device=device_idx) as mic:
            while True:
                chunk = mic.read_chunk()
                if chunk is not None:
                    # chunk is shape (frames, channels)
                    chunk = chunk.flatten()
                    audio_buffer = np.concatenate((audio_buffer, chunk))
                    
                    if len(audio_buffer) >= window_samples:
                        window_audio = audio_buffer[:window_samples]
                        
                        max_vol = np.max(np.abs(window_audio))
                        if max_vol > 0.001:
                            transcript = stt.transcribe(window_audio)
                            if transcript:
                                display_text = strip_overlap(transcript, last_transcript)
                                if display_text:
                                    print(display_text, end=" ", flush=True)
                                    last_transcript = transcript
                        
                        audio_buffer = audio_buffer[step_samples:]
                        
    except KeyboardInterrupt:
        print("\n\nStopped listening.")
    except Exception as e:
        print(f"\nError during transcription: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice AI Terminal Mode")
    parser.add_argument("--list-devices", action="store_true", help="List available audio input devices")
    parser.add_argument("--device", type=int, default=None, help="Device index to use for microphone")
    
    args = parser.parse_args()
    
    if args.list_devices:
        list_devices()
    else:
        run_cli(args.device)
