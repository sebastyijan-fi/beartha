import os
import numpy as np
import sounddevice as sd
import librosa
from scipy.io import wavfile
from sklearn.neural_network import MLPClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# Directory Management
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Audio Operations
def save_audio(audio, filename, path='hotword'):
    filepath = os.path.join(path, filename)
    wavfile.write(filepath, 44100, audio)

def record_audio(duration, samplerate=44100):
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()
    return audio

def augment_audio(audio, n_augment=10):
    return [audio + np.random.normal(0, 1, audio.shape) for _ in range(n_augment)]

# Feature Extraction
def extract_features(audio_data):
    audio_mono = np.mean(audio_data, axis=1)
    mel_spec = librosa.feature.melspectrogram(y=audio_mono, sr=44100)
    return mel_spec.mean(axis=1)

# Main Execution
if __name__ == '__main__':
    create_directory('hotword')

    # Record and augment hotword
    print("Recording hotword. Speak into the mic.")
    hotword = record_audio(2)
    print("Hotword recorded.")
    save_audio(hotword, 'original_hotword.wav')
    augmented_hotwords = augment_audio(hotword)

    # Feature Extraction
    X_train = [extract_features(aug) for aug in augmented_hotwords]
    y_train = [1] * len(X_train)

    # Train and save the model
    clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500)
    clf.fit(X_train, y_train)

    # Export to ONNX
    initial_type = [('float_input', FloatTensorType([None, X_train[0].shape[0]]))]
    onnx_model = convert_sklearn(clf, initial_types=initial_type)
    with open("hotword_model.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())

    # Test the original hotword
    original_feature = extract_features(hotword).reshape(1, -1)
    original_result = clf.predict(original_feature)
    print("Original hotword detected successfully.") if original_result == 1 else print("Original hotword not detected. Retrain the model.")
