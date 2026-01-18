import os
import re
import pygame
import soundfile as sf
from kokoro_onnx import Kokoro
from src.utils.config_manager import ConfigManager

class Mouth:
    def __init__(self):
        print(">> Mouth: Initializing Kokoro Neural Engine...")
        self.config = ConfigManager.load_config()

        try:
            pygame.mixer.init()
        except Exception:
            pass

        # Load Kokoro Model
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, "data")
            k_conf = self.config.get("mouth_kokoro", {})

            model_path = os.path.join(data_dir, k_conf.get("model", "kokoro-v1.0.onnx"))
            voices_path = os.path.join(data_dir, k_conf.get("voices", "voices-v1.0.bin"))

            if not os.path.exists(model_path):
                print(f"!! CRITICAL: Kokoro model not found at {model_path}")
                self.active = False
                return

            self.kokoro = Kokoro(model_path, voices_path)
            self.default_voice = k_conf.get("default_voice", "af_bella")
            self.active = True
            print(">> Mouth: Online.")
        except Exception as e:
            print(f"!! Mouth Init Error: {e}")
            self.active = False

    def _clean_text_for_speech(self, text):
        """
        Removes Markdown, Emojis, and special symbols that ruin TTS.
        """
        # 1. Remove Markdown symbols (*, #, _, `)
        # Replaces "**Bold**" with "Bold", "*sigh*" with "sigh"
        text = re.sub(r'[*#_`~]', '', text)

        # 2. Remove Emojis and non-standard symbols
        # This regex keeps only:
        # - Alphanumeric (\w)
        # - Spaces (\s)
        # - Standard Punctuation (.,!?;:'")
        # Everything else (😀, ⚡, 🛑) is deleted.
        text = re.sub(r'[^\w\s,!.?;:\'\"-]', '', text)

        # 3. Collapse multiple spaces into one
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def _apply_phonetic_filters(self, text):
        """
        Helper to fix pronunciation of common terms.
        """
        replacements = {
            "Enjo": "En-joe",
            "Sania": "Sah-nee-ah",
            "baka": "bah-kah",
            "kawaii": "kah-wah-ee",
            "oyasumi": "oh-yah-su-me",
            "arigato": "ah-ree-gah-toe"
        }
        for word, phone in replacements.items():
            # Use regex to replace whole words only to avoid replacing parts of other words
            text = re.sub(r'\b' + re.escape(word) + r'\b', phone, text, flags=re.IGNORECASE)
        return text

    def speak(self, text):
        """Speaks the text using Kokoro TTS."""
        if not self.active or not text:
            return

        # 1. Clean the text (Remove Emojis/Markdown)
        clean_text = self._clean_text_for_speech(text)

        # 2. Apply Phonetic Fixes
        final_text = self._apply_phonetic_filters(clean_text)

        # If cleaning removed everything (e.g. input was just "😊"), don't speak
        if not final_text.strip():
            return

        try:
            # 3. Generate Audio
            samples, sample_rate = self.kokoro.create(
                final_text,
                voice=self.default_voice,
                speed=1.0,
                lang="en-us"
            )

            # 4. Save & Play
            temp_path = "temp_speech.wav"
            sf.write(temp_path, samples, sample_rate)

            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()

            if os.path.exists(temp_path):
                os.remove(temp_path)

        except Exception as e:
            print(f">> TTS Error: {e}")