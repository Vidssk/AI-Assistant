from pathlib import Path
from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT.parent / ".env")

# Base directory of the project
# ROOT = Path(__file__).resolve().parent.parent
print(f"ROOT: {ROOT.parent}")

JARVIS_VOICE_SAMPLE = ROOT / "voice_samples/Jarvis/jarvis.wav"

AGENTS_DIR = ROOT / "agents"

APP_MAP = {
    "notepad": os.getenv("NOTEPAD_PATH"),
    "calculator": os.getenv("CALCULATOR_PATH"),
    "dlss swapper": os.getenv("DLSS_SWAPPER_PATH"),
    "chrome": os.getenv("CHROME_PATH"),
    "spotify": os.getenv("SPOTIFY_PATH"),
    "uvr": os.getenv("UVR_PATH"),
    "ultimate vocal remover": os.getenv("UVR_PATH"),
    "obsidian": os.getenv("OBSIDIAN_PATH"),
    "blender": os.getenv("BLENDER_PATH"),
    "fl studio": os.getenv("FL_STUDIO_PATH"),
    "fruity loops": os.getenv("FL_STUDIO_PATH"),
    "fruity loop": os.getenv("FL_STUDIO_PATH"),
    "007 first light": os.getenv("FIRST_LIGHT_URI"),
    "forza horizon 6": os.getenv("FORZA_HORIZON_6_URI"),
    "gris": os.getenv("GRIS_URI"),
}

spotify_credentials = {
    "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    "SPOTIFY_DEVICE_ID": os.getenv("SPOTIFY_DEVICE_ID")
}
print(f"client id: {spotify_credentials['client_id']}\n client_secret: {spotify_credentials['client_secret']}\n redirect_uri {spotify_credentials['redirect_uri']}")
SEARCH_DIRS = [
        Path.home() / "Documents",
        Path.home() / "Downloads",
        Path.home() / "Desktop",
]

