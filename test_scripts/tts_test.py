def enable_xtts_safe_load():
    import torch
    from TTS.config.shared_configs import BaseDatasetConfig
    from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig
    from TTS.tts.models.xtts import XttsArgs

    torch.serialization.add_safe_globals([
        BaseDatasetConfig,
        XttsConfig,
        XttsAudioConfig,
        XttsArgs
    ])
enable_xtts_safe_load()
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
print("XTTS LOADED")