# ENJO: Anthropomorphic AI Assistant
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI Engine](https://img.shields.io/badge/Core-Gemini%20%7C%20Llama3-purple)](https://ollama.com/)
[![Status](https://img.shields.io/badge/Status-Prototype%20(v0.2)-green)]()
[![License](https://img.shields.io/badge/license-GNU-green)]()

## 🙏 Acknowledgments
* **Google Gemini API** for cloud intelligence.
* **Groq** for high-speed inference.
* **Ollama** for local offline capabilities.
* **KOKORO TTS** for the voice synthesis.

**ENJO** (Evolving Neural Justified Operator) is a self-evolving AI companion designed to transition from a terminal-based logic engine ("The Brain") into a fully autonomous desktop agent ("The Body").

Unlike standard chatbots, ENJO features a **Unified Brain Architecture** that seamlessly switches between High-IQ Cloud Models (Gemini/Groq) and Privacy-Focused Local Models (Llama 3 via Ollama) depending on network availability.

--Windows Only--
---

## 🧠 Core Architecture (Basic)

### 1. The Unified Brain
ENJO utilizes a single neural core that manages cognitive load efficiently:
* **Dynamic Switching:** Automatically detects internet loss and switches to local Llama 3 models without user intervention.
* **Subconscious Layer:** A background process that analyzes user conversation for permanent facts (e.g., "I own Tesla stock") and silently updates the user profile.
* **Resource Efficiency:** Optimized to run on consumer hardware by sharing API connections between conscious (chat) and subconscious (memory) threads.

### 2. Infinite Memory
* **Profile.json:** A JSON-based long-term storage that remembers user details, stocks, and projects indefinitely.
* **Dynamic Profiling:** No hardcoded categories. If you say "I am allergic to peanuts," ENJO dynamically creates an `allergy` category in its memory structure.

### 3. The Senses
* **Ears:** Real-time Speech-to-Text using Google Speech Recognition (Low latency).
* **Mouth:** High-fidelity Neural TTS (Text-to-Speech) using `kokoro tts` with distinct voice personalities (e.g., Japanese-accented English).

### 4. The Hands
* **Desktop Hands:** Can open apps, control volume, lock the system, and manage media playback.
*  **Map Your Apps**
    * Open `data/config.json`.
    * Update the `app_paths` section with the real paths to your `.exe` files (Chrome, Spotify, VS Code, etc.).

## 🎨 Customization

ENJO is designed to be a mirror of its user. You are encouraged to strip out the demo personality and replace it with your own.

### 1. Define the Identity (The Soul)
Navigate to `src/brain/bot_personality.py`. This file contains the AI's core instructions.
* **Change the Name:** Replace "ENJO" with your preferred assistant name.
* **Edit `CORE`:** Define who the AI is (e.g., "You are a witty, sarcasm-loving assistant" or "You are a stoic, data-driven butler").

### 2. Train the Subconscious (The Memory)
Navigate to `src/brain/subconscious.py`. This controls what the AI considers "Important."
* The default setup listens for **names, stocks, and projects**.
* **Customize the Prompt:** You can edit the `get_analysis_prompt` function to track different things.
    * *Example:* If you are a medical student, tell it to "Extract any mentions of medical definitions or drug names."
    * *Example:* If you are a writer, tell it to "Extract plot ideas and character names."

### 3. Voice & Accent
Navigate to `src/senses/mouth.py`.
* Change `self.voice` to any Kokoro TTS voice ID (e.g., 'af_bella', 'af_sarah', 'am_michael').
---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) (for offline capabilities)
* Google/Groq API Keys (optional, for cloud intelligence)

  **Configure API Keys**
    * Create a `.env` file in the root directory.
    * Add your keys:
        ```ini
        GEMINI_API_KEY=your_gemini_key_here
        GROQ_API_KEY=your_groq_key_here
        ```

*(Note: `kokoro-onnx` and `soundfile` are required for voice).*

*  **Setup Kokoro (Crucial Step)**
    * This project uses `kokoro-onnx` for speech.
    * **Action:** Download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from the official Kokoro repository.
    * Place them inside the `data/` folder of this project.

### Setup
1. Clone the repository:
   ```bash
   git clone (https://github.com/SaniaBharadwaj/Enjo_AI.git)cd ENJO

pip install -r requirements.txt
(Required libs: google-genai, groq, ollama, kokoro-tts, pygame, SpeechRecognition)

Run the latest version (Basic):
python Basic/src/main.py

Talk: "Enjo, open Spotify and play some music."

System: "Enjo, lock the computer."

Chat: "Who are you?"

🎭 Customization
Want to change how Enjo acts? You don't need to code. Open src/brain/bot_personality.py and edit the system_prompt text string.

Example:

Python

# Make her a Pirate
system_prompt = """
You are Captain Enjo. You speak like a pirate.
You control the user's ship (computer).
"""
⚠️ Disclaimer
This is a Public Basic release.

It does not include the advanced "Voicevox" engine or the "Emotional Affection System" found in the private build.

Always check code before running it, especially code that can execute system commands.

Created by Sania | 2026
