from speechcorrection.stt.stt_base import STTBase
import whisper


class ScriptGenerator(STTBase):
    # 처음 초기화할 때 사용할 모델명, 음성 파일의 경로를 매개변수로 받음
    def __init__(self, model_name="small", voice_path=None):
        self.__model = whisper.load_model(model_name)
        self.__origin_voice_path = voice_path
        self.__origin_script = None

    # 음성파일을 변환된 스크립트로 변환 후 반환하는 메소드
    def execute(self):
        if self.__origin_voice_path is None:
            raise ValueError("음성 파일이 설정되지 않았습니다. 음성 파일을 다시 설정해주세요.")

        result = self.__model.transcribe(self.__origin_voice_path)
        self.__origin_script = result["text"]

        return self.__origin_script

    # 음성파일 경로를 반환하는 메소드
    @property
    def origin_voice_path(self):
        return self.__origin_voice_path

    # 원본 음성파일 경로를 내부 변수에 저장 메소드
    @origin_voice_path.setter
    def origin_voice_path(self, voice_path):
        self.__origin_voice_path = voice_path

    # 변환한 스크립트 반환 메소드
    @property
    def origin_script(self):
        return self.__origin_script
