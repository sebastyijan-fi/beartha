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

# Initialize logging
logging.basicConfig(filename='voice_assistant.log', level=logging.DEBUG)

# Load variables from .env file
load_dotenv()

# Initialize WhisperX
device = "cuda"
try:
    model = whisperx.load_model("small", device)
except Exception as e:
    logging.error(f"Failed to load WhisperX model: {e}")

# Initialize GPT model
openai.api_key = os.getenv("OPEN_AI_KEY")

rec_status = False
myrecording = []

def start_recording():
    global rec_status
    rec_status = True
    t = threading.Thread(target=record_audio)
    t.start()
    logging.info("Recording started")

def record_audio():
    global myrecording
    myrecording = []
    start_time = time.time()
    while rec_status:
        try:
            audio_chunk = sd.rec(int(44100 * 2), dtype='int16', channels=1, samplerate=44100, blocking=True)
            myrecording.append(audio_chunk)
        except Exception as e:
            logging.error(f"Error during recording: {e}")
    logging.info(f"Recording stopped. Time taken: {time.time() - start_time} seconds")

def stop_recording():
    global rec_status
    rec_status = False
    audio_data = np.vstack(myrecording)
    with wave.open('temp_audio.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio_data.tostring())
    process_audio_and_send('temp_audio.wav')

def process_audio_and_send(audio_file):
    start_time = time.time()
    try:
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio)
        segments = result["segments"]
    except Exception as e:
        logging.error(f"WhisperX transcription failed: {e}")
        return

    # Send to GPT-3 API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": segments[0]['text']}
            ]
        )
    except Exception as e:
        logging.error(f"OpenAI API request failed: {e}")
        return

    logging.info(f"Processing and API request time taken: {time.time() - start_time} seconds")

    reply_content = response['choices'][0]['message']['content']
    generate_and_play(reply_content)

def generate_and_play(text):
    start_time = time.time()
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            cmd = f"echo '{text}' | piper --model en_US-lessac-medium --output_file {tmp_wav.name}"
            subprocess.run(cmd, shell=True)

            # Check if the file exists and is non-empty
            if os.path.exists(tmp_wav.name) and os.path.getsize(tmp_wav.name) > 0:
                audio = AudioSegment.from_wav(tmp_wav.name)
                audio.export(tmp_wav.name, format="wav")
                subprocess.run(["aplay", tmp_wav.name], stderr=subprocess.PIPE)
            else:
                logging.error(f"Temporary WAV file is missing or empty: {tmp_wav.name}")
    except Exception as e:
        logging.error(f"Error during audio generation and playback: {e}")
    logging.info(f"Audio generation and playback time: {time.time() - start_time} seconds")

def on_closing():
    global rec_status
    rec_status = False
    root.quit()
    root.destroy()


root = tk.Tk()
root.title("Voice Assistant")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

btn_start = ttk.Button(frame, text="Start Recording", command=start_recording)
btn_start.grid(row=0, column=0, sticky=tk.W)

btn_stop = ttk.Button(frame, text="Stop Recording", command=stop_recording)
btn_stop.grid(row=0, column=1, sticky=tk.W)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
