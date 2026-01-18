from src.brain.core import Brain
from src.senses.mouth import Mouth
from src.senses.ears import Ears
from src.utils.config_manager import ConfigManager
from src.hands.desktop import DesktopController

class ENJO:
    def __init__(self):
        self.config = ConfigManager.load_config()
        version = self.config.get("system", {}).get("version", "1.0-Public")
        name = self.config.get("system", {}).get("name", "Enjo")

        print(f"\n>> SYSTEM: Booting {name} v{version}...")

        # Initialize Organs
        self.brain = Brain()
        self.mouth = Mouth()
        self.ears = Ears()
        self.hands = DesktopController() # Grants control over OS

        print(">> SYSTEM: All organs online.")

    def run(self):
        self.mouth.speak("System online.")

        while True:
            try:
                # --- PHASE 1: SENSORY INPUT ---
                user_input = self.ears.listen()
                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    self.mouth.speak("Shutting down.")
                    break

                # --- PHASE 2: COGNITION (Brain) ---
                # No emotion override needed for Basic Mode
                response = self.brain.think(user_input)

                # Clean Response for logs
                clean_response = response
                if "]: " in response:
                    clean_response = response.split("]: ")[-1]

                # --- PHASE 3: ACTION PARSER ---
                final_text_to_speak = clean_response

                if "[ACTION:" in response:
                    try:
                        # Extract Tag
                        start = response.find("[ACTION:")
                        end = response.find("]", start)
                        action_tag = response[start:end+1]

                        # Parse Command
                        content = action_tag.replace("[ACTION:", "").replace("]", "").strip()
                        cmd, target = content.split("|")

                        print(f"   (🦾 Action: {cmd.strip().upper()} -> {target.strip()})")

                        # Execute (No Affection Check in Basic Mode)
                        result = self.hands.execute(cmd.strip(), target.strip())
                        print(f"   >> System: {result}")

                        # Remove tag from speech
                        final_text_to_speak = response.replace(action_tag, "").strip()

                    except Exception as e:
                        print(f"   >> Action Error: {e}")

                # --- PHASE 4: SPEAK ---
                if final_text_to_speak:
                    print(f"🤖 ENJO: {final_text_to_speak}", flush=True)
                    self.mouth.speak(final_text_to_speak)

            except KeyboardInterrupt:
                print("\n>> SYSTEM: Manual Interrupt.")
                break
            except Exception as e:
                print(f">> CRITICAL RUNTIME ERROR: {e}")

if __name__ == "__main__":
    bot = ENJO()
    bot.run()