import os
import urllib.request

# Define paths
base_dir = "v0.2/data"
os.makedirs(base_dir, exist_ok=True)

urls = {
    "kokoro-v1.0.onnx": "https://huggingface.co/suno/kokoro/resolve/main/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://huggingface.co/suno/kokoro/resolve/main/voices-v1.0.bin",
}

print(">> Downloading Kokoro AI Model (This may take a moment)...")
for filename, url in urls.items():
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, path)
        print(f"✔ {filename} saved.")
    else:
        print(f"✔ {filename} already exists.")

print(">> Kokoro Setup Complete.")