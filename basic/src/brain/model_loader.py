# src/brain/loader.py
import os
from dotenv import load_dotenv

load_dotenv()

class ModelConfig:
    def __init__(self):
        # 1. Cloud Configuration
        self.gemini_key = os.getenv("GOOGLE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")


        self.gemini_models = [
            "gemini-2.5-flash",       # Fastest, Newest
            "gemini-2.5-flash-lite",       # Reliable fallback
            "gemini-3-flash-preview",
            "gemini-3-pro-preview",
            "gemini-2.5-pro"   # High intelligence fallback
        ]

        self.groq_models = [
            "openai/gpt-oss-120b",    # Smartest free Groq model (2026)
            "openai/gpt-oss-20b",        # Strong reasoning
            "llama-3.1-8b-instant",
            # "groq/compound",
            "llama-3.3-70b-versatile"      # Fast fallback
        ]

        # 2. Local Configuration
        # We only define the PREFERENCE here. The Engine handles the rest.
        self.local_model_name = "llama3"