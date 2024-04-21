from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

path = r"C:\Users\rlatk\AppData\Local\Programs\Python\Python311\Lib\site-packages"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/multilingual/multi-dataset/xtts_v2")

syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path
)

text = "Hello world"

outputs = syn.tts(text)
syn.save_wav(outputs, "audio.wav")
