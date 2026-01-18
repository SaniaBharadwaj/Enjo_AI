# v0.2/src/brain/memory.py
import json
import os

class MemorySystem:
    def __init__(self):
        # 1. Calculate Path
        # Logic: brain -> src -> v0.2 -> data
        current_dir = os.path.dirname(os.path.abspath(__file__)) # .../src/brain
        src_dir = os.path.dirname(current_dir)                   # .../src
        v02_dir = os.path.dirname(src_dir)                       # .../v0.2

        self.data_dir = os.path.join(v02_dir, "data")
        self.profile_path = os.path.join(self.data_dir, "profile.json")
        self.history_path = os.path.join(self.data_dir, "history.json")

        # 2. DEBUG: Tell us where you are looking
        print(f">> DEBUG: Memory initializing at: {self.data_dir}")

        # 3. Ensure folder & files exist NOW
        self._initialize_storage()



    def _initialize_storage(self):
        """Forces creation of the folder and empty JSON files if missing."""
        try:
            # Create Folder
            if not os.path.exists(self.data_dir):
                print(">> Memory: Creating 'data' directory...")
                os.makedirs(self.data_dir, exist_ok=True)

            # Create Profile JSON if missing
            if not os.path.exists(self.profile_path):
                print(">> Memory: Creating empty profile.json...")
                with open(self.profile_path, 'w', encoding='utf-8') as f:
                    json.dump({"name": None, "stocks": [], "projects": []}, f, indent=4)

            # Create History JSON if missing
            if not os.path.exists(self.history_path):
                print(">> Memory: Creating empty history.json...")
                with open(self.history_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=4)

        except Exception as e:
            print(f">> MEMORY CRASH: Could not create files. {e}")

    # --- PERMANENT MEMORY (Profile) ---
    def load_profile(self):
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def update_profile(self, new_data_dict):

        """
        Merges a dictionary of new facts into the permanent profile.
        Example input: {'location': 'Tokyo', 'hobby': 'Coding'}
        """
        current_data = self.load_profile()

        # Loop through new facts and update/overwrite
        for key, value in new_data_dict.items():
            # If it's a list (like stocks), append to it instead of overwriting
            if isinstance(value, list) and isinstance(current_data.get(key), list):
                # Merge unique items
                current_list = current_data.get(key, [])
                combined = list(set(current_list + value))
                current_data[key] = combined
            else:
                # Standard overwrite (e.g. Location changed from London to Tokyo)
                current_data[key] = value

        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=4, sort_keys=True)

        print(f">> Memory: Profile merged updates -> {list(new_data_dict.keys())}")

    # --- TEMPORARY MEMORY (Chat History) ---
    def load_history(self):
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def save_history(self, history):
        # Save last 20 messages
        trimmed = history[-10:]
        try:
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(trimmed, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f">> Memory Save Error: {e}")

    def wipe_temporary(self):
        if os.path.exists(self.history_path):
            os.remove(self.history_path)
            # Re-create empty file immediately
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
        print(">> Memory: Short-term cache cleared.")