from speechcorrection.tts.tts_base import TTSBase
import torch
import os
from TTS.api import TTS

class VoiceGenerator(TTSBase):
    def __init__(self, corrected_script = None, basic_voice_path = None, output_wav_path = None):
        self.__basic_voice_path = basic_voice_path
        self.__corrected_script = corrected_script
        self.__output_wav_path = output_wav_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device = self.device)

    def execute(self):
        if (self.__basic_voice_path is None or not isinstance(self.__basic_voice_path, str) or 
            not self.__basic_voice_path.endswith('.wav')):
            raise ValueError("basic_voice_path의 경로가 지정되어 있지 않거나 올바른 파일 형식이 아닙니다.")
        
        if not os.path.exists(self.__basic_voice_path):
            raise ValueError(f"파일 {self.__basic_voice_path}이 존재하지 않습니다.")
        
        if (self.__corrected_script is None or not isinstance(self.__corrected_script, str) or 
            self.__corrected_script == ""):
            raise ValueError("corrected_script가 설정되어 있지 않거나, 올바르지 않은 형식, 혹은 비어 있습니다.")
        
        if (self.__output_wav_path is None or not isinstance(self.__output_wav_path, str) or 
            not self.__output_wav_path.endswith('.wav')):
            raise ValueError("output_wav_path의 경로가 지정되어 있지 않거나 올바른 파일 형식이 아닙니다.")
        
        try:
            self.tts.tts_to_file(
            text=self.__corrected_script,
            speaker_wav= self.__basic_voice_path,
            file_path=self.__output_wav_path,
            language="ko")
        except Exception as err:
            raise RuntimeError(f"TTS생성이 정상적으로 이루어지지 않았습니다. 원인 : {err}")
        

    @property
    def basic_voice_path(self):
        return self.__basic_voice_path

    @basic_voice_path.setter
    def basic_voice_path(self, basic_voice_path):
        self.__basic_voice_path = basic_voice_path

    @property
    def corrected_script(self):
        return self.__corrected_script

    @corrected_script.setter
    def corrected_script(self, corrected_script):
        self.__corrected_script = corrected_script

    @property
    def output_wav_path(self):
        return self.__output_wav_path

    @output_wav_path.setter
    def output_wav_path(self, output_wav_path):
        self.__output_wav_path = output_wav_path
