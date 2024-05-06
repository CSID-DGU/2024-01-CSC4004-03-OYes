import whisper

class ScriptGenerator:
    def __init__(self, model_name):
        self.model = whisper.load_model(model_name)
        self.audio = None # 멤버 변수로 음성파일 경로 저장
        self.transcribed_text = None #멤버 변수로 텍스트파일 경로 저장

    # 원본 음성 파일 멤버 변수에 저장
    def set_origin_voice(self, audio_file_loc):
        self.audio = audio_file_loc

    # 원본 음성 파일을 Script로 변환한 text 파일의 경로를 반환
    def get_origin_script(self):
        if self.transcribed_text is None:
            raise ValueError("변환된 텍스트 파일이 존재하지 않습니다.")
        
        return self.transcribed_text
        
    # 음성을 텍스트로 변환해 파일에 작성하는 함수 (매개변수로 파일의 경로들을 받음)
    def transcribe_to_text(self, audio_file_loc, output_file_loc):
        if self.audio is None:
            raise ValueError("음성 파일이 설정되지 않았습니다. 음성파일을 다시 설정해주세요.")
        
        with open(output_file_loc, "w") as output_file: # w 모드를 사용했으므로 output_file에 정보가 있더라도 덮어쓰기
            result = self.model.transcribe(audio_file_loc)
            transcribed_text = result["text"]
            
            # '.'을 기준으로 줄바꿈하여 텍스트를 파일에 작성 
            transcribed_lines = transcribed_text.split('.')
            for line in transcribed_lines:
                output_file.write(line.strip() + '\n')
        
        # 변환된 텍스트 파일의 경로를 멤버 변수에 저장
        self.transcribed_text = output_file_loc
        # 변환된 텍스트가 쓰여진 파일의 경로를 반환
        return output_file_loc

if __name__ == "__main__":
    # ScriptGenerator 인스턴스 생성
    transcriber = ScriptGenerator("base")
    
    #음성 파일 및 텍스트 파일 경로 설정
    audio_file = "testnews.wav" 
    output_file = "speech_to_text.txt" 
    
    transcriber.set_origin_voice(audio_file)
    # transcribe 메소드를 사용해 텍스트를 파일에 작성
    transcribed_file = transcriber.transcribe_to_text(audio_file, output_file)
    print("변환된 파일 경로:", transcribed_file)