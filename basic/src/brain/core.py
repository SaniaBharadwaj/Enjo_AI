# src/brain/core.py
import time
from google import genai
from google.genai import types
from groq import Groq

from src.brain.local_engine import LocalEngine
from src.brain.model_loader import ModelConfig
import src.brain.bot_personality as Personality
from src.brain.memory import MemorySystem
from src.brain.subconscious import Subconscious

from src.utils.config_manager import ConfigManager

class Brain:
    def __init__(self):
        print(">> Brain: Initializing Unified Neural Core...")

        # 1. LOAD RESOURCES
        self.config = ModelConfig()
        self.memory = MemorySystem()
        self.subconscious = Subconscious()
        self.profile = self.memory.load_profile()
        self.history = self.memory.load_history()

        # 2. INIT CLOUD CLIENTS
        self.gemini_client = None
        if self.config.gemini_key:
            try:
                self.gemini_client = genai.Client(api_key=self.config.gemini_key)
            except Exception:
                pass

        self.groq_client = None
        if self.config.groq_key:
            try:
                self.groq_client = Groq(api_key=self.config.groq_key)
            except Exception:
                pass

        # 3. INIT LOCAL ENGINE
        self.local_engine = None

        # 4. STARTUP CONNECTION
        self.active_provider = "none"
        self.active_model_name = "Unknown"
        self.last_cloud_check = time.time() # Start the timer now

        # Initial Check (Run once at startup)
        self._refresh_connection_status()
        self._update_system_prompt()

    def _update_system_prompt(self):
            """Re-injects profile data into the personality."""

            # 1. Format User Data (Stocks, Projects, Name)
            profile_text = (
                f"\n\n[USER PERMANENT DATA]\n"
                f"Name: {self.profile.get('name', 'Shin')}\n"
                f"Stocks: {self.profile.get('stocks', [])}\n"
                f"Projects: {self.profile.get('projects', [])}"
            )

            # Add any extra fields found in memory
            if self.profile:
                for k, v in self.profile.items():
                    if k not in ["name", "stocks", "projects"]:
                        profile_text += f"\n{k.capitalize()}: {v}"

            # 2. Load Base Personality (Rules are now hidden inside here!)
            base_system = Personality.Personality.get_system_prompt("default")

            # 3. Combine
            self.system_prompt = base_system + profile_text

    def _engage_local_mode(self):
        print(" Switching to Local Core.")
        if self.local_engine is None:
            try:
                self.local_engine = LocalEngine(preferred_model=self.config.local_model_name)
            except Exception as e:
                print(f"!! CRITICAL: Local Engine failed ({e})")
                self.active_provider = "none"
                return

        self.active_provider = "local"
        self.active_model_name = self.local_engine.model_name

    def _refresh_connection_status(self):
        # This function prints, so we only call it when necessary
        print(">> Brain: Checking connectivity matrix...", end="", flush=True)

        # A. Try Gemini
        if self.gemini_client:
            try:
                self.gemini_client.models.get(model=f"models/{self.config.gemini_models[0]}")
                self.active_provider = "gemini"
                self.active_model_name = self.config.gemini_models[0]
                print(" Connected (Gemini).")
                return
            except Exception:
                pass

        # B. Try Groq
        if self.groq_client:
            try:
                self.groq_client.models.list()
                self.active_provider = "groq"
                self.active_model_name = self.config.groq_models[0]
                print(" Connected (Groq).")
                return
            except Exception:
                pass

        # C. Fallback to Local
        print(" Offline.", end="")
        self._engage_local_mode()

    def _switch_provider(self):
        """Silent Failover: Gemini -> Groq -> Local"""
        # We print a warning, but we DO NOT re-run the full connection check
        print(f"\n>> WARNING: {self.active_provider} failed. Switching...", end="")

        if self.active_provider == "gemini":
            if self.groq_client:
                self.active_provider = "groq"
                self.active_model_name = self.config.groq_models[0]
                print(" Switched to Groq.")
            else:
                self._engage_local_mode()

        elif self.active_provider == "groq":
            self._engage_local_mode()

        elif self.active_provider == "local":
            print(" All brains exhausted.")
            self.active_provider = "none"

    def _generate_text(self, payload, is_chat=True):
        try:
            if self.active_provider == "gemini":
                if is_chat:
                    return self.gemini_client.models.generate_content(model=self.active_model_name, contents=payload).text
                else:
                    return self.gemini_client.models.generate_content(model=self.active_model_name, contents=payload).text

            elif self.active_provider == "groq":
                if not is_chat:
                    payload = [{"role": "user", "content": payload}]
                chat = self.groq_client.chat.completions.create(messages=payload, model=self.active_model_name)
                return chat.choices[0].message.content

            elif self.active_provider == "local":
                if not is_chat:
                    payload = [{"role": "user", "content": payload}]
                return self.local_engine.think(payload)

        except Exception:
            return None # Return None to trigger failover

    def think(self, user_input, emotion_override=None):
        # 1. SMART RECONNECT (Cloud check logic)
        if self.active_provider == "local":
            if (time.time() - self.last_cloud_check > 1800):
                print(">> Brain: Scheduled network check...")
                self._refresh_connection_status()
                self.last_cloud_check = time.time()

        # 2. LOAD DEFENSE PROTOCOLS (From Config)
        config = ConfigManager.load_config()
        defense_map = config.get("defense_protocols", {})

        # If the Limbic System detected a threat (angry/fear), inject the protocol
        system_directive = defense_map.get(emotion_override, "")

        # 3. PREPARE PROMPT
        # We append the directive to the user's input so the LLM sees it immediately.
        final_prompt = user_input + system_directive

        # --- SUBCONSCIOUS (Facts) ---
        if self.active_provider != "none":
            # ... (Subconscious logic remains the same) ...
            try:
                analysis_prompt = self.subconscious.get_analysis_prompt(user_input)
                raw_analysis = self._generate_text(analysis_prompt, is_chat=False)
                if raw_analysis:
                    new_facts = self.subconscious.parse_result(raw_analysis)
                    if new_facts:
                        self.memory.update_profile(new_facts)
                        self.profile = self.memory.load_profile()
                        self._update_system_prompt()
            except Exception:
                pass

        # --- CONSCIOUS (Generation) ---
        # ... (Failover loop remains the same) ...
        # Just ensure you are using 'final_prompt' in the payload construction!

        # (Copy the existing failover loop here, ensuring 'final_prompt' is used)
        attempts = 0
        while attempts < 3:
            if self.active_provider == "none":
                return ">> System Error: No AI models available."

            if self.active_provider == "gemini":
                payload = [types.Content(role="user", parts=[types.Part.from_text(text=self.system_prompt)])]
                for msg in self.history:
                    payload.append(types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["text"])]))
                payload.append(types.Content(role="user", parts=[types.Part.from_text(text=final_prompt)]))
            else:
                payload = [{"role": "system", "content": self.system_prompt}]
                for msg in self.history:
                    role = "assistant" if msg["role"] == "model" else "user"
                    payload.append({"role": role, "content": msg["text"]})
                payload.append({"role": "user", "content": final_prompt})

            response_text = self._generate_text(payload, is_chat=True)

            if response_text:
                self._update_memory(user_input, response_text)
                return f"\n[{self.active_provider}]: {response_text}"
            else:
                self._switch_provider()
                attempts += 1

        return ">> Error: Network Unstable."

    def _update_memory(self, user, ai):
        self.history.append({"role": "user", "text": user})
        self.history.append({"role": "model", "text": ai})
        self.memory.save_history(self.history)