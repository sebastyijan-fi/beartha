import sounddevice as sd
import time
from transformers import VitsModel, AutoTokenizer
import torch
from queue import Queue
import threading
import concurrent.futures

# Initialize model and tokenizer
model = VitsModel.from_pretrained("facebook/mms-tts-eng")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

# Initialize global queue for texts and audios
text_queue = Queue()
audio_queue = Queue()

# Function to generate audio
def generate_audio(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    waveform = output.squeeze().numpy()
    return waveform

# Thread to populate audio queue
def populate_audio_queue():
    while True:
        next_text = text_queue.get()
        if next_text == "EXIT":
            audio_queue.put("EXIT")
            break

        audio = generate_audio(next_text)
        audio_queue.put(audio)

# Thread to play audio
def play_audio():
    while True:
        next_audio = audio_queue.get()
        if next_audio == "EXIT":
            break
        sd.play(next_audio, model.config.sampling_rate)
        sd.wait()
        time.sleep(0.5)  # 0.5-second delay between sentences

# Function to populate text queue
def populate_text_queue(long_text):
    sentences = long_text.split('. ')
    for sentence in sentences:
        text_queue.put(sentence.strip())
    text_queue.put("EXIT")

# Your long text here
long_text = "I was born in Tel Aviv, in what is now Israel, in 1934, while my mother was visiting her extended family there; our regular domicile was in Paris. My parents were Lithuanian Jews, who had immigrated to France in the early 1920s and had done quite well. My father was the chief of research in a large chemical factory. But although my parents loved most things French and had some French friends, their roots in France were shallow, and they never felt completely secure. Of course, whatever vestiges of security they’d had were lost when the Germans swept into France in 1940. What was probably the first graph I ever drew, in 1941, showed my family’s fortunes as a function of time – and around 1940 the curve crossed into the negative domain. I will never know if my vocation as a psychologist was a result of my early exposure to interesting gossip, or whether my interest in gossip was an indication of a budding vocation. Like many other Jews, I suppose, I grew up in a world that consisted exclusively of people and words, and most of the words were about people."

# Populate the text queue
populate_text_queue(long_text)

# Create and start threads
populate_audio_thread = threading.Thread(target=populate_audio_queue)
play_audio_thread = threading.Thread(target=play_audio)

populate_audio_thread.start()
play_audio_thread.start()

