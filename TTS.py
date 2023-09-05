import whisperx
import whisper
import time
import torch
import psutil
import json

def resource_usage():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    return cpu, memory

def run_experiment(model_name, device, audio_file, compute_type):
    torch.cuda.empty_cache()
    start_time = time.time()
    start_cpu, start_memory = resource_usage()

    if model_name == "WhisperX":
        model = whisperx.load_model("small", device, compute_type=compute_type)
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio)
    else:
        model = whisper.load_model("small")
        result = model.transcribe(audio_file)

    end_cpu, end_memory = resource_usage()
    time_taken = time.time() - start_time

    return {
        "model": model_name,
        "time_taken": time_taken,
        "start_cpu": start_cpu,
        "end_cpu": end_cpu,
        "start_memory": start_memory,
        "end_memory": end_memory
    }

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    audio_file = "output_audio.mp3"
    compute_type = "float32"

    experiments = []
    for model_name in ["WhisperX", "Whisper"]:
        result = run_experiment(model_name, device, audio_file, compute_type)
        experiments.append(result)

    with open("experiments.json", "w") as f:
        json.dump(experiments, f, indent=4)

    print("Experiment results saved in 'SST_experiments.json'")
