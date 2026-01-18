import sys
import os
import time

# --- SETUP PATHS ---
# Ensure Python can find the 'src' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.append(src_path)

# --- IMPORTS ---
try:
    from src.utils.config_manager import ConfigManager
    from src.senses.mouth import Mouth
    from src.brain.core import Brain
    from src.hands.desktop import DesktopController
    print(">> [0/4] Imports Successful.")
except ImportError as e:
    print(f"!! CRITICAL IMPORT ERROR: {e}")
    print("!! Make sure you are running this from the root folder (Enjo/).")
    print("!! Also ensure you installed requirements: pip install -r requirements.txt")
    sys.exit()

def run_diagnostics():
    print("\n===========================================")
    print("   🛠️  ENJO SYSTEM DIAGNOSTICS (Basic)   ")
    print("===========================================")

    # 1. TEST CONFIG
    print("\n>> [1/4] Testing Configuration...")
    try:
        config = ConfigManager.load_config()
        name = config.get("system", {}).get("name", "Unknown")
        print(f"   - System Name: {name}")
        print("   - Config Load: ✅ OK")
    except Exception as e:
        print(f"   !! Config Failed: {e}")
        return

    # 2. TEST BRAIN (Connectivity)
    print("\n>> [2/4] Testing Brain (AI Connectivity)...")
    try:
        # Initialize Brain (this checks API keys)
        bot_brain = Brain()
        provider = bot_brain.active_provider.upper()
        print(f"   - Active Provider: {provider}")

        if provider == "NONE":
            print("   !! WARNING: No AI provider connected. Check your .env file or API keys.")
            print("   !! Enjo will technically run, but she will be brain dead.")
        else:
            print("   - Sending Test Signal ('Say hello')...")
            # We send a simple "Say Hello" without memory to test the connection
            response = bot_brain.think("This is a diagnostic test. Say 'Connection Verified' briefly.")
            print(f"   - AI Response: \"{response}\"")

            if response and "Error" not in response:
                print("   - Brain Status: ✅ OK")
            else:
                print("   - Brain Status: ❌ ERROR (See log above)")

    except Exception as e:
        print(f"   !! Brain Failed: {e}")

    # 3. TEST MOUTH (TTS)
    print("\n>> [3/4] Testing Mouth (Kokoro TTS)...")
    try:
        bot_mouth = Mouth()

        if bot_mouth.active:
            print("   - Engine: Kokoro ONNX")
            print("   - Speaking: 'Diagnostics in progress...'")
            # We speak a simple line to verify audio driver and model
            bot_mouth.speak("Diagnostics in progress. Audio system nominal.")
            print("   - Audio Output: ✅ OK (Did you hear it?)")
        else:
            print("   !! Mouth Error: Engine not active. Check 'data/' folder for model files.")

    except Exception as e:
        print(f"   !! Mouth Failed: {e}")

    # 4. TEST HANDS (Desktop Control)
    print("\n>> [4/4] Testing Hands (OS Integration)...")
    try:
        hands = DesktopController()

        # Action A: Volume Check (Safe visual/auditory test)
        print("   - Test A: Muting System Volume (1 sec)...")
        hands.execute("volume", "mute")
        time.sleep(1)
        print("   - Test A: Unmuting...")
        hands.execute("volume", "mute")
        print("   - Volume Control: ✅ OK")

        # Action B: Safe App Launch
        # We try to launch Calculator because almost every Windows PC has it
        print("   - Test B: Launching Calculator...")
        result = hands.execute("open", "calculator")
        print(f"   - Execution Result: {result}")

        if "Failed" in result:
             print("   !! Note: Calculator failed. Check 'config.json' paths.")
        else:
             print("   - App Launch: ✅ OK")

    except Exception as e:
        print(f"   !! Hands Failed: {e}")

    print("\n===========================================")
    print("   🏁  DIAGNOSTIC COMPLETE")
    print("===========================================")

if __name__ == "__main__":
    run_diagnostics()