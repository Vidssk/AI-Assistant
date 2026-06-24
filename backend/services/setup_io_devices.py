import sounddevice as sd

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
                return input_device

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