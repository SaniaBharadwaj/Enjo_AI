# src/brain/local_engine.py
from ollama import chat, ResponseError

class LocalEngine:
    def __init__(self, preferred_model="llama3"):
        # We store the model name the Brain asks for
        self.model_name = preferred_model

        # Future-proof: Ensure we default to something safe if config is empty
        if not self.model_name:
            self.model_name = "llama3"

    def think(self, messages):
        """
        Receives the FULL context from core.py (System Prompt + History + User Input)
        and feeds it directly to the local model.
        """
        print(f"⚡ [Local] Thinking with {self.model_name}...")

        try:
            # We pass the 'messages' list directly.
            # This list ALREADY contains the System Prompt from bot_personality.py
            response = chat(
                model=self.model_name,
                messages=messages
            )

            return response['message']['content']

        except ResponseError as e:
            return f"Local Model Error: {e.error}"
        except Exception as e:
            return f"CRITICAL: Local Ollama unreachable. Is 'ollama serve' running? ({e})"