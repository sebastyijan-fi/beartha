# Abstract

The purpose of this work is to investigate the development of voice-activated personal assistants like Beartha and Link with an emphasis on achieving natural interaction, low latency, and utility for the end-user. This documentation serves as a reflective account of the experiments and findings thus far, focusing on three key research questions:

1. How can low latency be achieved with different technologies?
2. How do users experience such a system?
3. What technologies are essential for achieving an optimal outcome?

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
- **Setup**: Clone of public GitHub repository, Flask for server-based execution, and Uvicorn + Nginx for local deployment
### Conclusion

- **Time Investment**: 6-7 hours

After considerable experimentation and evaluation, it has been determined that a local setup offers the most promising avenue for further development. While it is possible to deploy voice-activated personal assistants on Raspberry Pi and cloud-based servers, the trade-offs in terms of performance and time investment do not align with the objectives of this work. Future research will focus on optimizing TTS and STT performance on the local setup.