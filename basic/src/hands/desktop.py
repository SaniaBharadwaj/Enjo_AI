import os
import ctypes
import subprocess

# Audio libraries
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class DesktopController:
    def __init__(self):
        print(">> Hands: Desktop Controller Online.")
        self.os_type = os.name # 'nt' is Windows

    def execute(self, command, target=None):
        """
        The main switch for all desktop actions.
        command: "open", "system", "volume"
        target: "spotify", "lock", "50", "mute"
        """
        command = command.lower()
        if target:
            target = target.lower()

        if command == "open":
            return self._open_app(target)
        elif command == "system":
            return self._system_cmd(target)
        elif command == "volume":
            return self._volume_control(target)

        return ">> Error: Unknown Hand Command."

    def _open_app(self, app_name):
        """
        Opens applications based on common names.
        """
        # Common Windows App Map
        app_map = {
            "chrome": "chrome.exe",
            "spotify": "spotify.exe",
            "discord": "update.exe --processStart Discord.exe", # Discord is weird
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "vscode": "code",
            "cmd": "start cmd",
            "explorer": "explorer"
        }

        # Use mapped name if exists, else try raw name
        target_exe = app_map.get(app_name, app_name)

        try:
            # shell=True allows running commands like they are typed in cmd
            subprocess.Popen(target_exe, shell=True)
            return f"Opened {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}. ({e})"

    def _system_cmd(self, action):
        if action == "lock":
            ctypes.windll.user32.LockWorkStation()
            return "System Locked."
        elif action == "shutdown":
            os.system("shutdown /s /t 10")
            return "Shutting down in 10s. (Type 'shutdown /a' to cancel)"
        elif action == "sleep":
            os.system("rundll32.dll powrprof.dll,SetSuspendState 0,1,0")
            return "Going to sleep."
        return "Unknown system command."

    def _volume_control(self, level):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, clsctx=ctypes.CLSCTX_ALL, activation_params=None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

            if level == "mute":
                current = volume.GetMute()
                volume.SetMute(not current, None) # Toggle
                return "Volume Muted/Unmuted."

            if level == "max":
                volume.SetMasterVolumeLevelScalar(1.0, None)
                return "Volume set to 100%."

            # Set specific percentage (0.0 to 1.0)
            try:
                vol_float = float(level) / 100
                volume.SetMasterVolumeLevelScalar(vol_float, None)
                return f"Volume set to {level}%."
            except ValueError:
                return "Invalid volume level."

        except Exception as e:
            return f"Volume Error: {e}"