# Voice-Activated AI Assistant (Gemini 2.5 Flash)

A fully localized, voice-controlled Python AI assistant powered by the Gemini 2.5 Flash model. This project features natural conversational memory, OS-level file management, web automation, and is architected to be easily extensible for IoT and embedded systems integration (such as triggering Raspberry Pi GPIO pins via voice).

## Features
* **Conversational Memory:** Utilizes Gemini's Chat Sessions to retain context over long interactions.
* **Local OS Integration:** Maps and opens secure local files and directories via voice command.
* **Automated Note-Taking:** Generates timestamped `.txt` files automatically in a dedicated directory.
* **Media & Web Automation:** Connects to standard browsers to parse and execute automated searches.
* **Hardware Ready:** Structured to easily incorporate hardware control functions for physical relays and sensors.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone 
[https://github.com/chiragvanve/gemini-voice-assistant.git]
(https://github.com/chiragvanve/gemini-voice-assistant.git)
   cd gemini-voice-assistant

2. Install the required dependencies:

pip install -r requirements.txt

(Note: Windows users may need to use pipwin install pyaudio if standard PyAudio wheel building fails).

3.Configure the API Key:

Open gemini-voice-assistant.py and replace "YOUR_API_KEY_HERE" with your actual Google Gemini API Key.

4.Run the Application

