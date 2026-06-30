import sounddevice as sd
import json
import time
from pathlib import Path

# #region agent log
def _dbg_io(hypothesis_id, location, message, data=None):
    try:
        log_path = Path(__file__).resolve().parents[2] / "debug-8c9fdb.log"
        payload = {"sessionId": "8c9fdb", "hypothesisId": hypothesis_id, "location": location, "message": message, "data": data or {}, "timestamp": int(time.time() * 1000)}
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass
# #endregion

def resolve_input_device_index(mic_index=None):
    if mic_index is not None:
        return mic_index

    default = sd.default.device
    if isinstance(default, (list, tuple)) and default[0] is not None:
        return default[0]
    if isinstance(default, int):
        return default

    for i, device in enumerate(sd.query_devices()):
        if device["max_input_channels"] > 0:
            return i

    return None

def setupInputDevice():
    preferred_devices = [
        "Microphone (2- JOUNIVO MICROPHO",
        # "Microphone (Logi C270 HD WebCam",
        "Favorite Device two"
    ]

    input_device = {
        "index": None,
        "name": ""
    }

    devices = sd.query_devices()

    for i, device in enumerate(devices):
        device_name = device["name"]

        # Skip devices that can't record
        if device["max_input_channels"] <= 0:
            continue

        for preferred in preferred_devices:
            if preferred in device_name:
                input_device["index"] = i
                input_device["name"] = device_name
                # #region agent log
                _dbg_io("A", "setup_io_devices.py:setupInputDevice", "matched preferred input device", input_device)
                # #endregion
                return input_device

    fallback_index = resolve_input_device_index()
    if fallback_index is not None:
        input_device["index"] = fallback_index
        input_device["name"] = sd.query_devices(fallback_index)["name"]
        # #region agent log
        _dbg_io("A", "setup_io_devices.py:setupInputDevice", "using fallback input device", input_device)
        # #endregion

    # #region agent log
    _dbg_io("A", "setup_io_devices.py:setupInputDevice", "no input device resolved", input_device)
    # #endregion
    return input_device

def setupOutputDevice():
    preferred_devices = [
        "Speakers (2- Echo-6SR)",
        "Speakers",
        "Favorite Output Device"
    ]

    output_device = {
        "index": None,
        "name": ""
    }

    devices = sd.query_devices()

    for i, device in enumerate(devices):
        device_name = device["name"]

        # Skip devices that can't play audio
        if device["max_output_channels"] <= 0:
            continue

        for preferred in preferred_devices:
            if preferred in device_name:
                output_device["index"] = i
                output_device["name"] = device_name
                return output_device

    return output_device

def printInputDeviceList():
    devices = sd.query_devices()

    for i, device in enumerate(devices):
        device_name = device["name"]
        print(f"IDX: {i}, device: {device_name}")

if __name__ == "__main__":
    printInputDeviceList()
    # input_device = setupInputDevice()
    # print(f"Input Device: {input_device['name']} at idx: {input_device['index']}")
    # output_device = setupOutputDevice()
    # print(f"Input Device: {output_device['name']} at idx: {output_device['index']}")