import os
import random
import numpy as np
import subprocess
from pydub import AudioSegment

# Configurable Variables
pitch_factor_min = 0.8
pitch_factor_max = 1.2
noise_level = 0.005  # Increasing the noise level
n_samples = 10  # You can change this or keep using input

# Create dataset folders
os.makedirs('hotword', exist_ok=True)
os.makedirs('not_hotword', exist_ok=True)

# Function to generate audio using Piper
def generate_audio_with_piper(text, filename):
    cmd = f"echo '{text}' | piper --model en_US-lessac-medium --output_file {filename}"
    subprocess.run(cmd, shell=True)

# Function to add random noise
def add_noise(audio, noise_level=0.2):
    audio_samples = np.array(audio.get_array_of_samples())
    max_amplitude = np.max(np.abs(audio_samples))
    noise = np.random.normal(0, max_amplitude * noise_level, audio_samples.shape[0])
    audio_with_noise = audio_samples + noise
    audio_with_noise = np.clip(audio_with_noise, -32768, 32767)  # Clip values to int16 range
    audio_with_noise = np.int16(audio_with_noise)
    return AudioSegment(
        audio_with_noise.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )


# Function to randomly change pitch
def random_change_pitch(audio):
    pitch_factor = random.uniform(pitch_factor_min, pitch_factor_max)
    return audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * pitch_factor)
    }).set_frame_rate(audio.frame_rate)

# Generate hotword samples
text = "Link!"
for i in range(n_samples):
    output_filename = f'hotword/hotword_{i}.wav'
    generate_audio_with_piper(text, output_filename)
    audio = AudioSegment.from_file(output_filename)
    audio = random_change_pitch(audio)
    audio.export(f"hotword/hotword_{i}.wav", format="wav")

# Generate not-hotword samples
random_words = ["apple", "banana", "cherry", "date", "elderberry"]
for i in range(n_samples):
    random_word = np.random.choice(random_words)
    output_filename = f'not_hotword/not_hotword_{i}.wav'
    generate_audio_with_piper(random_word, output_filename)
    audio = AudioSegment.from_file(output_filename)
    audio = add_noise(audio, noise_level)
    audio.export(f"not_hotword/not_hotword_{i}.wav", format="wav")

print(f"Generated {n_samples} hotword and {n_samples} not-hotword samples.")
