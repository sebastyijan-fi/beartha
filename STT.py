import sounddevice as sd
import numpy as np
import librosa
from scipy.io.wavfile import write
import onnxruntime
import whisperx

# Initialize ONNX runtime and Whisper
sess = onnxruntime.InferenceSession("hotword.onnx", providers=['CPUExecutionProvider'])
device = "cuda"
compute_type = "float16"
whisper_model = whisperx.load_model("small", device, compute_type=compute_type)

# Function to extract features
def extract_features(audio_data):
    audio_mono = np.mean(audio_data, axis=1)
    mel_spec = librosa.feature.melspectrogram(y=audio_mono, sr=44100)
    return mel_spec.mean(axis=1).reshape(1, -1)

# Transcribe using Whisper
def record_and_transcribe():
    print("Start speaking...")
    temp_audio_path = "temp_audio.wav"
    silent_chunk_counter = 0
    silence_threshold = 200

    all_audio_data = []
    while True:
        audio_chunk = sd.rec(int(44100 * 0.5), samplerate=44100, channels=2, dtype='int16')
        sd.wait()
        silent_chunk_counter += 1 if np.mean(np.abs(audio_chunk)) < silence_threshold else 0

        if silent_chunk_counter > 3:
            break

        all_audio_data.append(audio_chunk)

    audio = np.vstack(all_audio_data)

    # Save to a temporary file
    write(temp_audio_path, 44100, audio)

    # Transcription
    transcribe_audio = whisperx.load_audio(temp_audio_path)
    result = whisper_model.transcribe(transcribe_audio, batch_size=16)
    print("Transcription result:", result["segments"])

    # Optional: remove temp file
    # os.remove(temp_audio_path)

# Listen for hotword and activate recording and transcription
while True:
    print("Listening for hotword...")
    audio_chunk = sd.rec(int(44100 * 2), samplerate=44100, channels=2, dtype='int16')
    sd.wait()

    features = extract_features(audio_chunk)
    pred_onx = sess.run(None, {'float_input': features.astype(np.float32)})[0]

    if pred_onx == 1:
        print("Hotword detected. Starting transcription.")
        record_and_transcribe()
