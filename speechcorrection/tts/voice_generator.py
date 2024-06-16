from speechcorrection.tts.tts_base import TTSBase
import os
from google.cloud import texttospeech


class VoiceGenerator(TTSBase):
    def __init__(self, voice_type=False, corrected_script=None, basic_voice_path=None):
        self.__voice_type = voice_type
        self.__corrected_script = corrected_script
        self.__basic_voice_path = basic_voice_path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'auth_key.json'
        self.tts_client = texttospeech.TextToSpeechClient()

    def execute(self):
        if (self.__corrected_script is None or not isinstance(self.__corrected_script, str) or
                self.__corrected_script == ""):
            raise ValueError("corrected_script가 설정되어 있지 않거나, 올바르지 않은 형식, 혹은 비어 있습니다.")

        if (self.__basic_voice_path is None or not isinstance(self.__basic_voice_path, str) or
                not self.__basic_voice_path.endswith('.wav')):
            raise ValueError("basic_voice_path의 경로가 지정되어 있지 않거나 올바른 파일 형식이 아닙니다.")

        try:
            synthesis_input = texttospeech.SynthesisInput(text=self.__corrected_script)
            voice_type = texttospeech.VoiceSelectionParams(
                language_code="ko-KR",
                name=('ko-KR-Wavenet-B' if self.__voice_type else 'ko-KR-Wavenet-D')
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16
            )
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice_type,
                audio_config=audio_config
            )

            with open(self.__basic_voice_path, "wb") as out:
                out.write(response.audio_content)

        except Exception as err:
            raise RuntimeError(f"TTS생성이 정상적으로 이루어지지 않았습니다. 원인 : {err}")

    @property
    def voice_type(self):
        return self.__voice_type

    @voice_type.setter
    def voice_type(self, voice_type):
        self.__voice_type = voice_type

    @property
    def corrected_script(self):
        return self.__corrected_script

    @corrected_script.setter
    def corrected_script(self, corrected_script):
        self.__corrected_script = corrected_script

    @property
    def basic_voice_path(self):
        return self.__basic_voice_path

    @basic_voice_path.setter
    def basic_voice_path(self, basic_voice_path):
        self.__basic_voice_path = basic_voice_path
