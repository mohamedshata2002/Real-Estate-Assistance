import pyaudio
import numpy as np
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os
import torch
# from melo.api import TTS
from playsound import playsound
from time import sleep
# Configuration
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
SILENCE_THRESHOLD = 500  # Threshold for detecting silence
SILENCE_DURATION = 3 # Duration of silence to stop recording (in seconds)

def is_silent(data):
   
    """Check if the given audio data is silent."""
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.max(audio_data) < SILENCE_THRESHOLD

def record_audio():
    """Record audio until silence is detected."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
    
    print("Recording started...")
    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if is_silent(data):
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > (RATE / CHUNK * SILENCE_DURATION):
            break

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(frames)

import wave
import os

def save_audio(filename, audio_data):
    """Save the recorded audio to a file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)

    print(f"Audio saved as {filename}")

# if __name__ == "__main__":
#     audio_data = record_audio()
#     save_audio("output.wav", audio_data)
#     print("Audio saved as output.wav")




device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-small"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)
def encoder(path):

    result = pipe(path,generate_kwargs={"language": "arabic"})
    return result["text"]








