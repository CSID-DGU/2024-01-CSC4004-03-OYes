## Voice Changer
1. install requirements by using pip
cmd에서 VoiceChanger 경로로 이동한 후 requrements.txt를 이용해 라이브러리를 설치합니다.
- install python
- enter 'pip install -r requirements.txt' /currently works in windows

2. install pytorch in https://pytorch.org/get-started/locally/
위의 홈페이지로 접속하여 상황에 알맞은 pip 명령어를 받아 실행합니다.

3. install FFmpeg
운영체제에 따라서 아래의 파일을 다운로드하여 VoiceChanger 폴더에 넣거나 cmd에서 하단의 명령어를 입력합니다.
- https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffmpeg.exe
- https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffprobe.exe
- download two files and put it in the VoiceChanger folder
- if Ubuntu or Debian, use 'sudo apt install ffmpeg'

4. download pretrained models
아래의 홈페이지로 접속하여 필요한 파일을 다운로드 받아, assets 폴더에 같은 이름을 가진 폴더를 생성하고 그 내부에 넣습니다.
- https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main
- hubert\hubert_base.pt
- pretrained_V2\f0D40k.pth and f0G40k.pth
- rmvpe.pt
- create hubert, pretrained_V2, rmvpe and log folder in assets folder
- each file should be placed in folder created

5. run the main.py
main.py에는 추론과 학습을 진행하는 예시 코드가 들어 있습니다. 모듈의 경로가 바뀌는 경우 import 경로 수정이 필요합니다.
- main.py should be placed in the same directory with VoiceChanger folder