import speech_recognition as sr
import sys
import os
from faster_whisper import WhisperModel

class Ears:
    def __init__(self):
        print(">> Ears: Initializing Neural Hearing (Faster-Whisper)...")

        # 1. SETUP WHISPER (The Brain)
        # Downloads 'base.en' (~80MB) automatically on first run.
        try:
            # device="cpu" is compatible with everything.
            # If you have an NVIDIA GPU, you can change to device="cuda".
            self.model = WhisperModel("base.en", device="cpu", compute_type="int8")
            print(">> Ears: Whisper Model Loaded.")
        except Exception as e:
            print(f"!! CRITICAL: Whisper Load Failed. ({e})")
            self.model = None

        # 2. SETUP MIC (The Hardware) - Instant Load Optimization
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 400  # Adjust this if your room is noisy

        try:
            self.mic = sr.Microphone()
            with self.mic as source:
                print(">> Ears: Calibrating ambient noise... (Silence please)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                print(">> Ears: Calibration complete. (Mic is HOT)")
        except Exception as e:
            print(f"!! CRITICAL: No Microphone found. ({e})")
            self.mic = None

        # Cache path for temporary audio
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.cache_dir = os.path.join(self.base_dir, "data")
        self.temp_wav = os.path.join(self.cache_dir, "input_cache.wav")

    def listen(self):
        """
        Listens via Mic, saves to temp wav, and runs Whisper locally.
        """
        try:
            # A. Visual Prompt
            print("\n👤 You (Type or Enter to Speak): ", end="", flush=True)

            # B. Check for Text Input first
            user_input = sys.stdin.readline().strip()
            if user_input:
                return user_input # Text Mode

            # C. Voice Mode
            if not self.mic:
                print("   >> ❌ No Mic connected.")
                return None

            if not self.model:
                print("   >> ❌ Whisper model not loaded.")
                return None

            print("   >>Listening...")

            with self.mic as source:
                try:
                    # Listen for audio (Timeouts prevent hanging forever)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    print("   >> ❌ Silence.")
                    return None

            print("   >> 🧠 Dreaming (Transcribing)...")

            # D. Save Raw Audio to Disk
            with open(self.temp_wav, "wb") as f:
                f.write(audio.get_wav_data())

            # E. Run Whisper (The Magic)
            # beam_size=5 is smarter/slower. 1 is fastest.
            segments, info = self.model.transcribe(self.temp_wav, beam_size=5)

            # Combine segments
            full_text = " ".join([segment.text for segment in segments]).strip()

            if not full_text:
                print("   >> ❌ Heard nothing.")
                return None

            print(f"   >> 🗣️ Heard: {full_text}")

            # Cleanup
            if os.path.exists(self.temp_wav):
                os.remove(self.temp_wav)

            return full_text

        except KeyboardInterrupt:
            return "exit"
        except Exception as e:
            print(f">> Ears Error: {e}")
            return None