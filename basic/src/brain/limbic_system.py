import re
import sys
import os

# Add path to find utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_manager import ConfigManager

class LimbicSystem:
    def __init__(self):
        # 1. Load from Config (Single Source of Truth)
        self.config = ConfigManager.load_config()
        self.emotions = self.config.get("emotions", {})

        # 2. Pre-sort categories for priority (The Aurora Protocol Logic)
        # We manually define priority checks here since JSON order isn't guaranteed
        self.priority_order = ["fear", "angry", "tsundere", "whisper", "happy", "critical", "sad"]

        # 'Relaxed' is the catch-all for mild frustration, checked separately

    def detect_emotion(self, text):
        text = text.lower()

        # --- CHECK 1: PRIORITY TIERS ---
        for emotion in self.priority_order:
            keywords = self.emotions.get(emotion, {}).get("keywords", [])
            for word in keywords:
                # Regex match whole words
                if re.search(r'\b' + re.escape(word) + r'\b', text):
                    return emotion

        # --- CHECK 2: MILD FRUSTRATION (Relaxed) ---
        # If no priority emotion found, check if it's just mild venting
        relaxed_keywords = self.emotions.get("relaxed", {}).get("keywords", [])
        for word in relaxed_keywords:
             if re.search(r'\b' + re.escape(word) + r'\b', text):
                 return "relaxed"

        # --- CHECK 3: CONTEXT CLUES ---
        if "!" in text and "?" not in text:
            return "happy"
        if "..." in text:
            return "relaxed"

        return "normal"