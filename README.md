# Abstract

The purpose of this work is to investigate the development of voice-activated personal assistants like Beartha and Link with an emphasis on achieving natural interaction, low latency, and utility for the end-user. This documentation serves as a reflective account of the experiments and findings thus far, focusing on three key research questions:

1. How can low latency be achieved with different technologies?
2. How do users experience such a system?
3. What technologies are essential for achieving an optimal outcome?

---

## Diary Entry: The Iterative Journey Toward Voice-Activated Assistants - September 6, 2023

### Embracing Minimalism & Hotkeys over Hotwords for Quick Iterations

#### Today's Milestones

- Produced hotwords for voice activation
- Devised a script for generating datasets for hotwords and non-hotwords
- Reassessed and leaned towards a hotkey-based approach for quick prototype iteration

#### Insights & Observations

I spent the day diving into the development of a voice-activated assistant. Initially, the focus was on using hotwords for activation, backed by training a machine-learning model + onnx. While fully doable, I started leaning towards using hotkeys as a more immediate and reliable solution.

The idea of a minimalist assistant that resides in the system tray came up, which seems more pragmatic. Upon pressing an unused hotkey, a pop-up would appear to indicate it's "listening," ready for a command that would be processed through OpenAI's API and TTS.

#### Technology Choices

- **TTS Model:** Piper, a decent Text-to-Speech engine. Investigating voice cloning and multi-language support. [Piper](https://github.com/rhasspy/piper)
- **STT Model:** WhisperX, which seems superior to the basic Whisper. Need to confirm license details. [WhisperX](https://github.com/m-bain/whisperX)

#### Security & Accessibility

Security remains a concern, especially for the hotword-based approach that requires the software to be always listening. Accessibility won't be dismissed; both hotkeys and hotwords are good ideas.

#### Future Considerations

- The ability to interrupt ongoing TTS speech for a more interactive experience.
- Need for sentence splitting and queueing for natural speech synthesis, JSON -> key value pair.
- Considering the tech stack and potential platforms (Ubuntu for development, but considering Windows and mobile).

#### Conclusion

Today's work indicates that a minimalist, yet robust, voice-activated assistant is entirely plausible. By utilizing hotkeys for quicker iterations, I can develop a functional prototype in a shorter time frame. The end goal remains the same: a low-latency, highly responsive, and user-friendly voice assistant.

**Time Investment**: 8-9 hours

---

## Diary Notation: Bachelor's Thesis on Voice-Activated Personal Assistants - September 5, 2023

### Experimental Setup and Findings

#### Raspberry Pi

- **Model**: Raspberry Pi 4 with 2GB RAM and added swap space
- **TTS and STT Models Tested**: Whisper and WhisperX
- **Performance Metrics**: Latency and Text Accuracy
- **Challenges**: Unreliable performance, Torch compatibility issues
- **Troubleshooting**: Investigated solutions through online searches

#### Digital Ocean Droplet

- **Configuration**: 2 vCPUs, 2GB RAM, 60GB Disk running Ubuntu 22.04 (LTS) x64
- **Performance Metrics**: Latency ranged from 5 to 16 seconds for TTS return
- **Optimization Attempts**: No further attempts due to unsatisfactory base performance and additional cost implications

#### DietPi

- **TTS and STT Models Tested**: Various Torch implementations
- **Performance Metrics**: Unsatisfactory latency and text accuracy

#### Local Setup (Dell G3 with GTX 1060 Ti and 32GB RAM running Ubuntu 23.x)

- **Rationale**: For better control over resources and performance
- **Setup**: Clone of public GitHub repository, Called API to Digital Ocean Flask for server-based execution + Nginx
### Conclusion

- **Time Investment**: 6-7 hours

After considerable experimentation and evaluation, it has been determined that a local setup offers the most promising avenue for further development. While it is possible to deploy voice-activated personal assistants on Raspberry Pi and cloud-based servers, the trade-offs in terms of performance and time investment do not align with the objectives of this work. Future research will focus on optimizing TTS and STT performance on the local setup.