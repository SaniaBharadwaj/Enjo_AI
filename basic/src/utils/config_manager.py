import json
import os

class ConfigManager:
    _instance = None
    _config_cache = None

    @staticmethod
    def load_config():
        """
        Singleton pattern to load config once and keep it in memory.
        """
        if ConfigManager._config_cache:
            return ConfigManager._config_cache

        # Locate the data/config.json file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = os.path.join(base_dir, "data", "config.json")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"CRITICAL: Config file missing at {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            ConfigManager._config_cache = json.load(f)

        return ConfigManager._config_cache