import threading
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import openai
import wave
import whisperx
import subprocess
import tempfile
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import logging
import time
import re


def init_logging():
    logging.basicConfig(filename="voice_assistant.log", level=logging.DEBUG)


def init_env():
    load_dotenv()
    openai.api_key = os.getenv("OPEN_AI_KEY")


def init_models(device="cuda"):
    try:
        return whisperx.load_model("small", device)
    except Exception as e:
        logging.error(f"Failed to load WhisperX model: {e}")
        return None


rec_status = False
myrecording = []

def clean_special_chars(text):
    return re.sub(r'[^a-zA-Z0-9 .!?]', '', text)

def clean_response_text(text):
    return re.sub(r'[^a-zA-Z0-9 .!?]', '', text)

def record_audio():
    global myrecording
    myrecording.clear()
    start_time = time.time()
    while rec_status:
        audio_chunk = sd.rec(
            int(44100 * 2), dtype="int16", channels=1, samplerate=44100, blocking=True
        )
        myrecording.append(audio_chunk)
    logging.info(f"Recording time: {time.time() - start_time}s")


def start_recording():
    global rec_status
    rec_status = True
    t = threading.Thread(target=record_audio)
    t.start()
    logging.info("Recording started")


def stop_recording():
    global rec_status
    rec_status = False
    audio_data = np.vstack(myrecording)
    save_audio_to_wav(audio_data)
    process_audio_and_send("temp_audio.wav")


def save_audio_to_wav(audio_data, filename="temp_audio.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio_data.tostring())


def generate_and_play(text):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        cmd = f"echo '{text}' | piper --model en_US-lessac-medium --output_file {tmp_wav.name}"
        subprocess.run(cmd, shell=True)
        audio = AudioSegment.from_wav(tmp_wav.name)
        audio.export(tmp_wav.name, format="wav")
        subprocess.run(["aplay", tmp_wav.name], stderr=subprocess.PIPE)


def create_transcript(segments):
    texts = [seg["text"] for seg in segments]
    full_transcript = " ".join(texts)
    return clean_special_chars(full_transcript)

def process_audio_and_send(audio_file):
    start_time = time.time()

    try:
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio)
        segments = result["segments"]
    except Exception as e:
        logging.error(f"WhisperX transcription failed: {e}")
        return

    full_transcript = create_transcript(segments)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_transcript},
            ],
        )
    except Exception as e:
        logging.error(f"OpenAI API request failed: {e}")
        return

    reply_content = response["choices"][0]["message"]["content"]
    clean_reply = clean_response_text(reply_content)
    generate_and_play(clean_reply)

    logging.info(f"Processing and API request time taken: {time.time() - start_time} seconds")

def on_closing():
    global rec_status
    rec_status = False
    root.quit()
    root.destroy()


if __name__ == "__main__":
    init_logging()
    init_env()
    model = init_models()

    root = tk.Tk()
    root.title("Voice Assistant")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    btn_start = ttk.Button(
        frame, text="Start Recording", command=lambda: start_recording()
    )
    btn_start.grid(row=0, column=0, sticky=tk.W)

    btn_stop = ttk.Button(
        frame, text="Stop Recording", command=lambda: stop_recording()
    )
    btn_stop.grid(row=0, column=1, sticky=tk.W)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
