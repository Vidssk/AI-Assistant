from pathlib import Path
from pathlib import Path
from dotenv import load_dotenv
import GPUtil
import psutil
import os

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT.parent / ".env")

# Base directory of the project
# ROOT = Path(__file__).resolve().parent.parent
# print(f"ROOT: {ROOT.parent}")

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

SEARCH_DIRS = [
        Path.home() / "Documents",
        Path.home() / "Downloads",
        Path.home() / "Desktop",
]


def get_system_info():
    # CPU
    cpu = {
        "usage": psutil.cpu_percent(interval=None),
        "temperature": None,  # We'll fill this in if available
    }

    # Memory
    memory = psutil.virtual_memory()
    memory_info = {
        "used": round(memory.used / (1024**3), 2),   # GB
        "total": round(memory.total / (1024**3), 2), # GB
    }

    # GPU
    gpu_info = {
        "usage": 0.0,
        "temperature": 0.0,
        "vram_used": 0.0,
        "vram_total": 0.0,
    }

    gpus = GPUtil.getGPUs()

    if gpus:
        gpu = gpus[0]
        gpu_info = {
            "name": gpu.name,
            "usage": gpu.load * 100,
            "temperature": gpu.temperature,
            "vram_used": gpu.memoryUsed,
            "vram_total": gpu.memoryTotal,
        }

    return {
        "cpu": cpu,
        "gpu": gpu_info,
        "memory": memory_info,
    }