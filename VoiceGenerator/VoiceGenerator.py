import torch
import os
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"

class VoiceGenerator:
    def __init__(self) -> None:
        # loading xtts_v2 tts model
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device = device)
        self.input_str = ""
    def set_correction_script(self, input_str) -> None:
        self.input_str = input_str
    def get_basic_voice(self) -> str:
        output_path = "output.wav"
        if self.input_str == "":
            # do something
            print("Error : empty input string")
            os.abort() # SIGABRT
        # generate speech by cloning a voice using default settings
        self.tts.tts_to_file(
            text=self.input_str,
            speaker_wav= "speaker_voice.wav",
            file_path=output_path,
            language="ko")
        
        return os.path.abspath(output_path)

if __name__ == "__main__":
    vg = VoiceGenerator()
    vg.set_correction_script("안녕하세요. 반갑습니다.")
    print(vg.get_basic_voice())

